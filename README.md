# Custom Node Testing Tools

## Purposes 

- Allow for fast testing/debugging of custom nodes without requiring you to constantly relaunch comfy process or suffer from inconsistencies with the comfy webview's grid's state not updating the way you expect between tests
- Work with `unittest`
- Compare speed/efficiency of different methods
- Auto-generate permutations for full branch coverage of a custom node's processes
  - For IMAGE inputs, generate all permutations of image size comparisons (e.g., case 1: img1 width > img2 width and img1 height > img2 height, case 2: img1 width < img2 width and img1 height < img2 height,...)
  - For IMAGE inputs, generate all permutations of tensor formats (e.g., test with CHW, HWC, BCHW, HW, etc.)
  - For Number inputs, generate all permutations of number comparisons (e.g., case 1: num1 > num2, case 2: num1 < num2,...)
  - For Selection inputs, generate all permutations of selection choices
  - etc...
- Optionally, auto-generate Edge cases to fill out coverage until a threshold is hit
  - Prime numbers
  - Bounds (0 or 1)
  - Uncommon file formats
- Help identify issues with mismatched tensor shapes/sizes/formats more easily
- Organize and display test results, particularly results that involve generated/modified images
  - In a nice bootstrap webview that highlights all the important information about each test case
  - Or with a generated image grid that composites together all results

## Demo

![test suite webview demo gif](wiki/wiki-media/test-results-webview-gif2.gif)

![test suite webview screenshot](wiki/wiki-media/test-results-webview-picture.png)

![test-results-webview-picture-tensor_types.png](wiki/wiki-media/test-results-webview-picture-tensor_types.png)