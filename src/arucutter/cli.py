from pathlib import Path
from arucutter.pipeline import pipeline
from arucutter.config import Config
from typing import Annotated
import typer
    
def main(config_file: Annotated[Path, typer.Option("-c", "--config", exists=True, readable=True, dir_okay=False)] = Path("arucutter.toml")):
    config = Config.from_toml(str(config_file))
    pipeline(config=config)
    
def cli():
    typer.run(main)