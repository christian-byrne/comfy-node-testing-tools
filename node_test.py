import sys
import os
import importlib.util
import logging
import traceback
import time
import argparse
import random

import unittest
import torch
import os
import sys
from torchvision import transforms

from src.utils import folder_paths
from src.view_results.results_webview import ComparisonGrid
from src.utils.tensor_utils import TensorImgUtils

from src.utils.logger import smart_print
from src.tests.test_tensor_types import TensorTypesTest
from src.constants import MAX_BRANCHES, TARGET_CUSTOM_NODES_DIR, TARGET_NODE_CLASS_NAME


class NodeTest:
    def __init__(
        self, target_node_dir: str, target_node_classname: str, max_branches=40
    ):
        self.node_path = target_node_dir
        self.node_name = target_node_classname
        self.max_branches = max_branches

        self.NODE_CLASS_MAPPINGS = {}
        self.NODE_DISPLAY_NAME_MAPPINGS = {}
        self.EXTENSION_WEB_DIRS = {}
        smart_print(f"Testing {self.node_name} node")
        success = self.load_custom_node()
        smart_print(f"Loading Success: {success}")

        self.target_node = {
            "class": self.NODE_CLASS_MAPPINGS[self.node_name],
            "instance": self.NODE_CLASS_MAPPINGS[self.node_name](),
            "input_types": self.NODE_CLASS_MAPPINGS[self.node_name].INPUT_TYPES(),
        }
        smart_print(f"Target Node Input Types: {self.target_node['input_types']}")
        self.target_node["tensor_input_fields"] = self.parse_tensor_input_fields(
            self.target_node["input_types"]
        )
        smart_print(
            f"Target Node Tensor Input Fields: {self.target_node['tensor_input_fields']}"
        )

        tensor_test = TensorTypesTest(
            self.target_node["instance"],
            self.target_node["tensor_input_fields"],
            self.target_node["input_types"],
        )
        tensor_test.run(max_branches=self.max_branches)

    def parse_tensor_input_fields(self, INPUT_TYPES):
        """Parse the input types for the node

        Example shape of INPUT_TYPES:
        Inputs: {'required': {'base_image': ('IMAGE',), 'cutout': ('IMAGE',), 'cutout_alpha': ('MASK',), 'size_matching_method': (['cover_crop_center', 'cover_crop', 'center_dont_resize', 'fill', 'fit_center', 'crop_larger_center', 'crop_larger_topleft'],), 'invert_cutout': ('BOOLEAN', {'default': False, 'label_on': 'enabled', 'label_off': 'disabled'})}}
        """
        match_keys = ["IMAGE", "MASK", "LATENT", "IMAGES"]
        input_fields = []

        for category in INPUT_TYPES.values():
            for field_ui_name, field_config in category.items():
                if field_config[0] in match_keys:
                    input_fields.append((field_ui_name, field_config[0]))

        print(f"Input Fields: {input_fields}")
        return input_fields

    def load_custom_node(self, ignore=set()):
        """From: https://github.com/comfyanonymous/ComfyUI/blob/f2fe635c9f56a8e78866f59b3f110585e75b42f4/nodes.py#L1873C1-L1874C1"""
        module_name = os.path.basename(self.node_path)
        if os.path.isfile(self.node_path):
            sp = os.path.splitext(self.node_path)
            module_name = sp[0]
        try:
            if os.path.isfile(self.node_path):
                module_spec = importlib.util.spec_from_file_location(
                    module_name, self.node_path
                )
                module_dir = os.path.split(self.node_path)[0]
            else:
                module_spec = importlib.util.spec_from_file_location(
                    module_name, os.path.join(self.node_path, "__init__.py")
                )
                module_dir = self.node_path

            module = importlib.util.module_from_spec(module_spec)
            sys.modules[module_name] = module
            module_spec.loader.exec_module(module)

            if (
                hasattr(module, "WEB_DIRECTORY")
                and getattr(module, "WEB_DIRECTORY") is not None
            ):
                web_dir = os.path.abspath(
                    os.path.join(module_dir, getattr(module, "WEB_DIRECTORY"))
                )
                if os.path.isdir(web_dir):
                    self.EXTENSION_WEB_DIRS[module_name] = web_dir

            if (
                hasattr(module, "NODE_CLASS_MAPPINGS")
                and getattr(module, "NODE_CLASS_MAPPINGS") is not None
            ):
                for name in module.NODE_CLASS_MAPPINGS:
                    if name not in ignore:
                        self.NODE_CLASS_MAPPINGS[name] = module.NODE_CLASS_MAPPINGS[
                            name
                        ]
                if (
                    hasattr(module, "NODE_DISPLAY_NAME_MAPPINGS")
                    and getattr(module, "NODE_DISPLAY_NAME_MAPPINGS") is not None
                ):
                    self.NODE_DISPLAY_NAME_MAPPINGS.update(
                        module.NODE_DISPLAY_NAME_MAPPINGS
                    )
                return True
            else:
                logging.warning(
                    f"Skip {self.node_path} module for custom nodes due to the lack of NODE_CLASS_MAPPINGS."
                )
                return False
        except Exception as e:
            logging.warning(traceback.format_exc())
            logging.warning(
                f"Cannot import {self.node_path} module for custom nodes: {e}"
            )
            return False


if __name__ == "__main__":
    NodeTest(TARGET_CUSTOM_NODES_DIR, TARGET_NODE_CLASS_NAME, MAX_BRANCHES)
    # NodeTest("composite_alpha_to_base_node", PATH_TO_CUSTOM_NODE)
