from pathlib import Path
from arucutter.pipeline import pipeline
from arucutter.config import Config
from arucutter import __version__
from typing import Annotated
import typer
from rich.progress import track

app = typer.Typer()

help_text = f"arucutter version {__version__}, visit https://github.com/joheli/arucutter for help"

@app.callback(invoke_without_command = True, help = help_text)
def main(config_file: Annotated[Path, typer.Option("-c", "--config", exists=True, readable=True, dir_okay=False)] = Path("arucutter.toml")):
    
    config = Config.from_toml(str(config_file))
    
    input_dir = config.directories.img_directory
    file_extensions = {".png", ".jpg", ".jpeg"}
    
    img_files = [f for f in input_dir.iterdir() if f.suffix.lower() in file_extensions and f.is_file()]
    
    for img_path in track(img_files, description="Processing files"):
        pipeline(img_path, config=config)
    
def cli():
    app()