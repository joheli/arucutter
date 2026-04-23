# arucutter

`arucutter` extracts rectangular regions (boxes and optional labels) from images using ArUco markers as reference points.

It is designed for scenarios where you photograph objects with marker frames and want consistent, automatic cropping—even if the camera angle or position varies.

---

## What it does

Given an image with ArUco markers around objects, `arucutter` will:

- detect ArUco markers
- compute perspective transforms
- crop defined regions ("boxes")
- optionally crop associated labels

---

## Quickstart (1 minute)

```bash
git clone https://github.com/joheli/arucutter.git
cd arucutter

uv venv --python 3.13
uv pip install .

arucutter -c arucutter.toml
```

This processes the sample images in `demo/input` and writes results to `demo/output`. 

---

## Requirements

- Python 3.13+
- Images in .png, .jpg, or .jpeg
- ArUco markers visible in the images

---

## Install

Type `uv pip install https://github.com/joheli/arucutter.git` to install, preferably into a fresh environment. This makes application `arucutter` available from the command line.

## How it works

You configure everything in a `.toml` file:

- where input images live
- where outputs should go
- which markers define each box
- (optional) which markers define labels

Run:

```bash
arucutter -c your_config.toml
```

---

## Minimal config example

```toml
[directories]
img_directory = "demo/input"
output_directory = "demo/output"

[minimal]
width = 1800
height = 1000
aruco_ids = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
area_increase = "prevent"

[[box]]
aruco_ids = [6, 7, 2, 1]
corners = ['tr', 'tl', 'bl', 'br']
output_width = 360
output_height = 500

[aruco]
dict_code = "4X4_50" 
```

Check out the supplied configuration file ([arucutter.toml](arucutter.toml)) for a more applied example.

---

## Marker ordering (important!)

Each box or label is defined by:

- 4 marker IDs
- 4 corresponding corners (to specify the exact points in the image that serve as rectangle corners)

Order must be:

top-left → top-right → bottom-right → bottom-left

Corner values:

- tl = top-left
- tr = top-right
- br = bottom-right
- bl = bottom-left

---

## Output

- cropped box images
- cropped label images (if configured)
- optional debug image with detected markers

---


## Complete configuration options 

The program is entirely controlled by the configuration file (see [arucutter.toml](arucutter.toml)), which you supply via command line option `-c`. 
Within it, you can specify the parameters below.

### Directories
Section `[directories]` allows you to input the directory where the source images sit and the directory where you want the output to be saved. Optionally, you
can specify if you wish to output an image with the found ArUCo markers highlighted (for debugging, e.g. to see which markers were detected).

### Minimal
Section `[minimal]` specifies minimal quality criteria that your images have to meet to be processed. By default, enlargement of boxes and labels is prevented (`area_increase` is set to "prevent"); if you want to just warn about or allow enlargement, set to "warn" or "allow", respectively.

### Boxes and Labels
You *must* specify one or more boxes by entering the ArUco ids, corners, the segment output width, and segment output height to section `[[box]]`. You *can* also add labels to sections using headings `[[label]]`. If you do, you have to add **one label per box**, i.e. if the number of boxes and labels do not match, an error is thrown.

### Aruco
Section `[aruco]` exposes some of the innards of [OpenCV's aruco module](https://docs.opencv.org/3.4/d9/d6d/tutorial_table_of_content_aruco.html). Here, you can specify the ArUCo dictionary to be used and additional parameters used for the detection of markers in an image.

---

## Common pitfalls

- Wrong corner order → distorted output
- Output directory missing → error
- Labels count ≠ boxes count → error

---

## License

MIT

## Acknowledgements

I would like to profusely thank the creators of [OpenCV](https://opencv.org/), [Pydantic](https://pydantic.dev/), [Rich](https://rich.readthedocs.io), and [Typer](https://typer.tiangolo.com/). They make this world a better place. 