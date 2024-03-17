import torch
import unittest

from src.tests.test_class import GenericTest
from src.utils.tensor_utils import TensorImgUtils
from src.generate_branches.branch_generator import BranchGenerator
from src.view_results.results_webview import ComparisonGrid
from src.utils.logger import smart_print
from src.utils.comfy_utils import call_node, random_inputs


class TensorTypesTest(GenericTest):
    def __init__(self, node, tensor_fields: list[(str, str)], INPUT_TYPES: dict):
        super().__init__(node, tensor_fields, INPUT_TYPES)
        self.title = "Tensor Types Permutations"

    def __call__(self, max_branches=40):
        super().set_branches(
            BranchGenerator().gen_branches_tensor_types(
                self.tensor_fields_types, max_branches=max_branches
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

    def __mask_from(self, img: torch.Tensor) -> torch.Tensor:
        """Try to extract the alpha layer from the image. If it doesn't exist,
        return a white mask.

        Do not alter the shape/format/type of the tensor in any way, otherwise
        the purpose of the test is defeated."""
        img_type = TensorImgUtils.identify_type(img)[0]
        channel_dim = img_type.index("C")
        if channel_dim == 0:
            if img.shape[channel_dim] == 4:
                img_alpha = img[3, :, :]
            else:
                img_alpha = torch.ones_like(img[0, :, :])
        elif channel_dim == 2:
            if img.shape[channel_dim] == 4:
                img_alpha = img[:, :, 3]
            else:
                img_alpha = torch.ones_like(img[:, :, 0])
        elif channel_dim == 3:
            if img.shape[channel_dim] == 4:
                print("img.shape[channel_dim] == 4")
                print(f"img.shape: {img.shape}")
                print(f"channel_dim: {channel_dim}")
                img_alpha = img[:, :, :, 3]
            else:
                img_alpha = torch.ones_like(img[:, :, :, 0])
        elif channel_dim == 1:
            if img.shape[channel_dim] == 4:
                img_alpha = img[:, 0, :, :]
            else:
                img_alpha = torch.ones_like(img[:, 0, :, :])
