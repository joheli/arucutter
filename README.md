# arucutter

`arucutter` is a tool to cut out boxes out of a picture containing several aruco markers.

In other words, it segments the picture using aruco markers as anchor points.

## Install

Type `pip install https://github.com/joheli/arucutter.git` to install. Prepend `uv` to previous command if you use uv.

## Usage

Supply a configuration toml file as option `-c` to the commandline application `arucutter`. Check out the supplied config file ([arucutter.toml](arucutter.toml)) to get an overview of the contents.

## Demo

Git clone the whole repo to a temporary directory by typing `git clone https://github.com/joheli/arucutter.git`. Install as above.
Type `arucutter` or `arucutter -c arucutter.toml` to witness the processing of files in directory `demo`.