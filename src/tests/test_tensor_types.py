import torch
import unittest

from src.utils.tensor_utils import TensorImgUtils
from src.generate_branches.branch_generator import BranchGenerator
from src.view_results.results_webview import ComparisonGrid
from src.utils.logger import smart_print
from src.utils.comfy_utils import call_node, random_inputs


class TensorTypesTest:
    def __init__(self, node, tensor_fields: list[(str, str)], INPUT_TYPES, max_branches):
        self.tensor_fields = tensor_fields
        self.INPUT_TYPES = INPUT_TYPES
        self.tensor_fields_types = [field[1] for field in tensor_fields]
        self.tensor_fields_names = [field[0] for field in tensor_fields]
        self.max_branches = max_branches
        self.title = "Tensor Types Permutations"

        self.branches = BranchGenerator().gen_branches_tensor_types(
            self.tensor_fields_types, max_branches=self.max_branches
        )
        results_webview = ComparisonGrid(self.title)

        smart_print(f"Testing: {self.title}")

        for branch_descrip, branch in self.branches.items():

            kwargs = {}
            failure_msg = [f"{branch_descrip}\n"]
            for field_config, branch_field in zip(self.tensor_fields, branch):
                field_ui_name = field_config[0]
                smart_print(f"field_ui_name: {field_ui_name}")
                field_type = field_config[1]
                smart_print(f"field_type: {field_type}")
                field_input_tensor = branch_field["tensor_image"]

                results_webview.add(
                    branch_descrip,
                    field_ui_name,
                    TensorImgUtils.convert_to_type(field_input_tensor, "CHW"),
                )

                kwargs[field_ui_name] = field_input_tensor
                failure_msg.append(
                    f"({field_type}) {field_ui_name}: {field_input_tensor.shape}"
                )
            failure_msg = ", ".join(failure_msg)

            random_kwargs = random_inputs(self.INPUT_TYPES, self.tensor_fields_names)
            kwargs.update(random_kwargs)
            results_webview.append_to_section_descripttion(
                branch_descrip, f"Random Inputs: {random_kwargs}"
            )

            try:
                output = call_node(node, kwargs)
            except Exception as e:
                print(failure_msg)
                print(f"\nError: {e}")
                continue

            assert (
                TensorImgUtils.identify_type(output)[1] == "BHWRGB"
            ), f"Wrong Tensor Type Returned — {failure_msg}"

            output = TensorImgUtils.convert_to_type(output, "CHW")
            print(f"output shape: {output.shape}")

            if isinstance(output, tuple) or isinstance(output, list):
                i = 0
                while i < len(output):
                    return_item = output[i]
                    print(f"return item type: {type(return_item)}")
                    if not isinstance(return_item, torch.Tensor):
                        print(f"return item shape: {return_item.shape}")
                        i += 1
                        continue

                    results_webview.add(
                        branch_descrip,
                        "Output",
                        TensorImgUtils.convert_to_type(return_item, "CHW"),
                    )
                    i += 1
            else:
                results_webview.add(
                    branch_descrip,
                    "Output",
                    TensorImgUtils.convert_to_type(output, "CHW"),
                )

        results_webview.show_webview()

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
