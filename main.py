import sys
import os
import importlib.util
import logging
import traceback
import time
import utils.folder_paths as folder_paths
import argparse


class NodeTest:
    def __init__(self, target_node_dir: str, target_node_classname: str):
        self.node_path = target_node_dir
        self.node_name = target_node_classname

        self.NODE_CLASS_MAPPINGS = {}
        self.NODE_DISPLAY_NAME_MAPPINGS = {}
        self.EXTENSION_WEB_DIRS = {}
        print(f"Testing {self.node_name} node")
        success = self.load_custom_node()
        print(f"Loading Success: {success}")

        self.target_node = {
            "class": self.NODE_CLASS_MAPPINGS[self.node_name],
            "instance": self.NODE_CLASS_MAPPINGS[self.node_name](),
            "input_types": self.NODE_CLASS_MAPPINGS[self.node_name].INPUT_TYPES(),
        }
        print(f"Target Node Input Types:\n{self.target_node['input_types']}")

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
    TARGET_CUSTOM_NODES_DIR = (
        "/home/c_byrne/tools/sd/sd-interfaces/ComfyUI/custom_nodes/elimination-nodes"
    )
    TARGET_NODE_CLASS_NAME = "Composite Alpha Layer | Elimination Nodes"
    NodeTest(TARGET_CUSTOM_NODES_DIR, TARGET_NODE_CLASS_NAME)
    # NodeTest("composite_alpha_to_base_node", PATH_TO_CUSTOM_NODE)
