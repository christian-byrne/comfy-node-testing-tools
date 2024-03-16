import torch
import unittest

from src.utils.tensor_utils import TensorImgUtils
from src.generate_branches.branch_generator import BranchGenerator
from src.view_results.results_webview import ComparisonGrid
from src.utils.logger import smart_print
from src.utils.comfy_utils import call_node, random_inputs


class TensorTypesTest:
    def __init__(self, node, tensor_fields: list[(str, str)], INPUT_TYPES):
        self.node = node
        self.tensor_fields = tensor_fields
        self.INPUT_TYPES = INPUT_TYPES
        self.tensor_fields_types = [field[1] for field in tensor_fields]
        self.tensor_fields_names = [field[0] for field in tensor_fields]
        self.title = "Tensor Types Permutations"

    def run(self, max_branches=40):
        self.branches = BranchGenerator().gen_branches_tensor_types(
            self.tensor_fields_types, max_branches=max_branches
        )
        self.results = ComparisonGrid(self.title)
        smart_print(f"Testing: {self.title}")

        for branch_description, branch in self.branches.items():
            self.__test_branch(branch_description, branch)

        self.results.show_webview()

    def __test_branch(self, branch_name: str, branch: dict):
        inputs = self.__get_branch_inputs(branch_name, branch)
        error_msg = self.__get_branch_error_msg(branch_name, branch, inputs)

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
        self.__add_output_to_results(branch_name, output)

    def __add_output_to_results(self, branch_name: str, output: any):
        if isinstance(output, tuple) or isinstance(output, list):
            i = 0
            while i < len(output):
                return_item = output[i]
                if not isinstance(return_item, torch.Tensor):
                    i += 1
                    continue

                self.results.add(
                    branch_name,
                    "Output",
                    TensorImgUtils.convert_to_type(return_item, "CHW"),
                )
                i += 1
        else:
            self.results.add(
                branch_name,
                "Output",
                TensorImgUtils.convert_to_type(output, "CHW"),
            )

    def __get_branch_error_msg(
        self, branch_name: str, branch: dict, inputs: dict
    ) -> str:
        failure_msg = [f"{branch_name}\n"]
        for field_config, branch_field in zip(self.tensor_fields, branch):
            failure_msg.append(
                f"({field_config[1]}) {field_config[0]}: "
                + f"{branch_field['tensor_image'].shape}"
            )

        failure_msg = ", ".join(failure_msg) + "\n" + f"Random Inputs Used:\n{inputs}"
        return failure_msg

    def __get_branch_inputs(self, branch_name: str, branch: dict) -> dict:
        kwargs = {}
        for field_config, branch_field in zip(self.tensor_fields, branch):
            field_ui_name = field_config[0]
            field_input_tensor = branch_field["tensor_image"]
            kwargs[field_ui_name] = field_input_tensor
            self.results.add(
                branch_name,
                field_ui_name,
                TensorImgUtils.convert_to_type(field_input_tensor, "CHW"),
            )

        random_kwargs = random_inputs(self.INPUT_TYPES, self.tensor_fields_names)
        kwargs.update(random_kwargs)
        self.results.append_to_section_description(
            branch_name, f"Random Inputs: {random_kwargs}"
        )

        return kwargs

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
