import torch
import unittest
from torchvision import transforms

from src.tests.test_class import GenericTest
from src.utils.tensor_utils import TensorImgUtils
from src.generate_branches.branch_generator import BranchGenerator
from src.view_results.results_webview import ComparisonGrid
from src.utils.logger import smart_print
from src.utils.comfy_utils import call_node, random_inputs
from src.manage_test_media.test_images import TestImages


class ImageSizesTest(GenericTest):
    def __init__(self, node, tensor_fields: list[(str, str)], INPUT_TYPES: dict):
        super().__init__(node, tensor_fields, INPUT_TYPES)
        self.title = "Image Size Permutations"
        self.test_images = TestImages(max_height=224, max_width=224)

    def __call__(self, max_branches=40):
        test_images = [None] * len(self.tensor_fields)

        # If image/mask pairs in inputs, use single rgba image split into rgb/a, for more realistic testing
        remaining = self.tensor_fields_types[:]
        while "MASK" in remaining and "IMAGE" in remaining:
            rgba_img = self.test_images.get_media(1, tags=["rgba"], as_pil=True)[0]
            rgba_img = TensorImgUtils.convert_to_type(
                transforms.ToTensor()(rgba_img), "BHWC"
            )
            alpha = rgba_img[:, :, :, 3]
            img = rgba_img[:, :, :, :3]

            mask_index = remaining.index("MASK")
            # Find the closest image index to the mask index
            image_indices = [i for i, x in enumerate(remaining) if x == "IMAGE"]
            index_diffs = [abs(mask_index - i) for i in image_indices]
            image_index = image_indices[index_diffs.index(min(index_diffs))]

            test_images[image_index] = transforms.ToPILImage()(
                TensorImgUtils.convert_to_type(img, "CHW")
            )
            test_images[mask_index] = transforms.ToPILImage()(
                TensorImgUtils.convert_to_type(alpha, "CHW")
            )
            remaining[image_index] = None
            remaining[mask_index] = None

        for index, tensor_field in enumerate(remaining):
            if not tensor_field:
                continue
            if tensor_field[1] == "MASK":
                test_images[index] = self.test_images.get_media(
                    1, tags=["alpha-layers"], as_pil=True
                )[0]
            else:
                test_images[index] = self.test_images.get_media(
                    1, tags=["people", "real"], as_pil=True
                )[0]

        super().set_branches(
            BranchGenerator().gen_branches_img_size(
                test_images,
                max_branches=max_branches,
            )
        )
        super().set_results(ComparisonGrid(self.title))
        super().run(self.test_branch)

    def test_branch(self, branch_name: str, branch: dict):
        inputs = super().get_branch_inputs(branch_name, branch)
        error_msg = super().get_branch_error_msg(branch_name, branch, inputs)

        try:
            output = call_node(self.node, inputs)
            assert (
                TensorImgUtils.identify_type(output)[1] == "BHWRGB"
            ), "Wrong Tensor Type Returned"
        except Exception as e:
            print(error_msg)
            print(f"\nError: {e}")
            return

        output = TensorImgUtils.convert_to_type(output, "CHW")
        super().add_output_to_results(branch_name, output)
