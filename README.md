# arucutter

`arucutter` is a tool to cut out boxes out of a picture containing several [ArUco markers](https://www.uco.es/investiga/grupos/ava/portfolio/aruco/), which
are robust visual cues that are easily detected and tracked in images. 

In other words, `arucutter` segments the picture using ArUco markers as "anchor points".

## Install

Type `pip install https://github.com/joheli/arucutter.git` to install. Prepend `uv` to previous command if you use uv.

## Usage

Supply a configuration toml file as option `-c` to the commandline application `arucutter`. Check out the supplied configuration file ([arucutter.toml](arucutter.toml)) to get an overview of the contents. The presented toml file prefilled to accomodate images supplied in [demo](demo), so please go ahead and alter it to your needs.

## Demo

Git clone the whole repo to a temporary directory by typing `git clone https://github.com/joheli/arucutter.git`. Install as above.
Type `arucutter` or `arucutter -c arucutter.toml` to witness the processing of files in directory `demo`.