# User Inputs:
TARGET_CUSTOM_NODES_DIR = (
    "/home/c_byrne/tools/sd/sd-interfaces/ComfyUI/custom_nodes/elimination-nodes"
)
TARGET_NODE_CLASS_NAME = "Composite Alpha Layer | Elimination Nodes"
# Set the max branches for each test class to prevent situations where there could technically be hundreds of branches to test. Will try to select the most relevant branches to test when truncating.
MAX_BRANCHES = 30
# If the node being tested accepts a MODEL input field, set the model name how it appears in the LoadCheckpoint selection dropdown, most likely without a path
USE_MODEL = "Stable-diffusion/vibrant/dreamshaper_8.safetensors"


# --------------------
TENSOR_FIELDS = [
    "IMAGE",
    "MASK",
    "LATENT",
    "IMAGES",
]
EDGE_CASE_PIXELS = 1
VERBOSE = True
ALLOW_REPEAT_BRANCHES = True
COLOR_ORDERS = [
    "light_red",
    "light_yellow",
    "light_green",
    "light_blue",
    "light_magenta",
    "light_cyan",
    "red",
    "yellow",
]
ORDER_STRINGS = [
    "1st Largest",
    "2nd Largest",
    "3rd Largest",
    "4th Largest",
    "5th Largest",
    "6th Largest",
    "7th Largest",
    "8th Largest",
]
VIDEO_EXTENSION_LIST = [
    ".mp4",
    ".mov",
    ".avi",
    ".mkv",
    ".webm",
    ".flv",
    ".wmv",
    ".vob",
    ".ogv",
    ".ogg",
    ".m4v",
    ".m2ts",
    ".mts",
    ".m2t",
    ".ts",
    ".m2v",
    ".m2ts",
    ".m2p",
    ".m2t",
    ".m2v",
    ".m4v",
    ".m4p",
    ".m4b",
    ".m4a",
    ".m4r",
    ".m4a",
    ".m4b",
    ".m4r",
    ".m4p",
    ".3gp",
    ".3g2",
    ".3gpp",
]

PICTURE_EXTENSION_LIST = [
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".tiff",
    ".bmp",
    ".webp",
    ".svg",
    ".eps",
    ".raw",
    ".cr2",
    ".nef",
    ".orf",
    ".sr2",
    ".raf",
    ".pef",
    ".dng",
    ".ico",
    ".psd",
    ".ai",
    ".xcf",
    ".indd",
    ".cdr",
    ".xpm",
    ".dds",
    ".tga",
    ".thm",
    ".yuv",
]
