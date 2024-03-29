***Custom Node Testing Tools*** - Table of Contents

- [Overview](#overview)
- [Purposes](#purposes)
- [Test Types](#test-types)
    - [Image Size Permutations](#image-size-permutations)
    - [Tensor Format/Type Permutations](#tensor-formattype-permutations)

&nbsp;

# Overview

- Loads and executes a custom node using the same methods as comfy, just specify the path and the node's name
- Lots of default tests which generate branches based on the input fields of the custom node
  - [Image Size Permutations](#image-size-permutations)
  - [Tensor Format/Type Permutations](#tensor-formattype-permutations)
- Each test class generates branches for its target input fields (e.g., the *image size test* generates permutations of image size comparisons for each IMAGE or MASK field)
  - For the other fields/inputs not being tested, they are chosen randomly from the available options or ranges, so a large number of input permutations gets tested naturally while running the main test classes
- Creates a visual webview of the test results from each test class and opens it automatically
  - After opening, all the generated data, images, html, etc. are deleted, but the results will still visible in the browser. This way there is no cleanup required
- Has checks to ensure tests won't be too demanding or take too long to run
- Uses test data that is fast to work with to enable a large number of branches (e.g., 64x64  random noise image tensors)
- Auto-generate Edge cases to fill out coverage until a threshold is hit
- In some cases, uses a database of real images to test with, but still descales them to a smaller size to keep the tests fast
  - When visual consistency from input to output is relevant to the test
  - To test differnet file formats, channel numbers, exif, etc.
  - The database includes a wide diversity of images/videos
  - Test images can be added by moving files to the `test_images` folder

# Purposes 

- Allow for fast testing/debugging of custom nodes without requiring you to constantly relaunch comfy process or suffer from inconsistencies with the comfy webview's grid's state not updating the way you expect between tests
- Compare speed/efficiency of different methods
- Auto-generate permutations for full branch coverage of a custom node's processes
- Help identify issues with mismatched tensor shapes/sizes/formats more easily
- Visualize how a node performs (its output) across all possible input permutations for a custom node
- Test inference algorithms
- Help improve speed

&nbsp;

# Test Types

### Image Size Permutations

![test-results-webview-picture-img_sizes_types](wiki/wiki-media/test-results-webview-picture-img_sizes_types.png)

<!-- ![test-results-webview-picture-img_sizes_types-max](wiki/wiki-media/test-results-webview-picture-img_sizes_types-max.png)

700+ branches in <2 seconds -->

### Tensor Format/Type Permutations

![test-results-webview-picture-tensor_types.png](wiki/wiki-media/test-results-webview-picture-tensor_types.png)


<!-- # Demo

![test suite webview demo gif](wiki/wiki-media/test-results-webview-gif2.gif)

![test suite webview screenshot](wiki/wiki-media/test-results-webview-picture.png) -->
