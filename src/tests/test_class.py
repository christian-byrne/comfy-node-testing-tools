import torch
import unittest

from src.utils.tensor_utils import TensorImgUtils
from src.generate_branches.branch_generator import BranchGenerator
from src.view_results.results_webview import ComparisonGrid
from src.utils.logger import smart_print
from src.utils.comfy_utils import call_node, random_inputs


class GenericTest:
    def __init__(self, node, tensor_fields: list[(str, str)], INPUT_TYPES: dict):
        self.node = node
        self.tensor_fields = tensor_fields
        self.INPUT_TYPES = INPUT_TYPES
        self.tensor_fields_types = [field[1] for field in tensor_fields]
        self.tensor_fields_names = [field[0] for field in tensor_fields]

    def __str__(self) -> str:
        return str(
            {
                "test_title": self.title,
                "results": self.results.sections,
                "results_dir": self.results.results_dir,
                "branches": self.branches,
            }
        )

    def set_branches(self, branches: dict):
        self.branches = branches

    def get_branches(self):
        return self.branches

    def set_results(self, results: ComparisonGrid):
        self.results = results

    def get_results(self):
        return self.results

    def run(self, branch_tester):
        smart_print(f"Testing: {self.title}")

        for branch_description, branch in self.branches.items():
            branch_tester(branch_description, branch)

        self.results.show_webview()

    def add_output_to_results(self, branch_name: str, output: any):
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

    def get_branch_error_msg(self, branch_name: str, branch: dict, inputs: dict) -> str:
        failure_msg = [f"{branch_name}\n"]
        for field_config, branch_field in zip(self.tensor_fields, branch):
            failure_msg.append(
                f"({field_config[1]}) {field_config[0]}: "
                + f"{branch_field['tensor_image'].shape}"
            )

        failure_msg = ", ".join(failure_msg) + "\n" + f"Random Inputs Used:\n{inputs}"
        return failure_msg

    def get_branch_inputs(self, branch_name: str, branch: dict) -> dict:
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
