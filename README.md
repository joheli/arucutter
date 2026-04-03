# arucutter

`arucutter` is a tool for cutting out boxes out of a picture containing [ArUco markers](https://www.uco.es/investiga/grupos/ava/portfolio/aruco/). In other words, `arucutter` segments a given image using ArUco markers as visual cues that inform the segmentation process.

## Install

Type `pip install https://github.com/joheli/arucutter.git` to install. Prepend `uv` to the previous command if you use [uv](https://docs.astral.sh/uv/).

> [!IMPORTANT]
> When creating a virtual environment with `uv`, make sure the selected python version is at least 3.13 - this may not be the default on your machine! If necessary, explicitly type `uv venv --python 3.13` (see [uv docs](https://docs.astral.sh/uv/concepts/python-versions/)).

## Usage

Supply a configuration file as option `-c` to the commandline application `arucutter`. Check out the supplied configuration file ([arucutter.toml](arucutter.toml)) to get an overview of the contents. The presented toml file is prefilled and corresponds to the images supplied in folder [demo/input](demo/input). Please go ahead and alter it to your needs.

### Configuration 

The program is entirely controlled by the configuration file (see [arucutter.toml](arucutter.toml)), which you supply via command line option `-c`. 
Within it, you can specify the parameters below.

#### Directories
Section `[directories]` allows you to input the directory where the source images sit and the directory where you want the output to be saved. Optionally, you
can specify if you wish to output an image with the found ArUCo markers highlighted (for debugging, e.g. to see which markers were detected).

#### Minimal
Section `[minimal]` specifies minimal quality criteria that your images have to meet to be processed.

#### Boxes and Labels
You *must* specify one or more boxes by entering the ArUco ids, corners, the segment output width, and segment output height to section `[[box]]`. You *can* (i.e. as an option) add labels to sections with headings `[[label]]`. If you do, you have to add **one label per box**, i.e. if the number of boxes and labels do not match, an error is thrown.

#### Aruco
Section `[aruco]` exposes some of the innards of [OpenCV's aruco module](https://docs.opencv.org/3.4/d9/d6d/tutorial_table_of_content_aruco.html). Here, you can specify the ArUCo dictionary to be used and additional parameters used for the detection of markers in an image.

## Demo

Git clone the whole repo to a temporary directory by typing `git clone https://github.com/joheli/arucutter.git`. Install as above.
Type `arucutter` or `arucutter -c arucutter.toml` to witness the processing of files in directory `demo`.

## Acknowledgements

I would like to profusely thank the creators of [OpenCV](https://opencv.org/), [Pydantic](https://pydantic.dev/), [Rich](https://rich.readthedocs.io), and [Typer](https://typer.tiangolo.com/). They make this world a better place. 