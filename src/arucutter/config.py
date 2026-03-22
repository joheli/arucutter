from pathlib import Path
from pydantic import BaseModel, Field, DirectoryPath, AfterValidator
from typing import Annotated, Literal
# from typing_extensions import Self
import tomllib

def length_four(l: list[int|Literal["tl", "tr", "bl", "br"]]) -> list[int|Literal["tl", "tr", "bl", "br"]]:
    if len(l) != 4:
        raise ValueError(f"The length of {l} is not 4!")
    return l

class Directories(BaseModel):
    img_directory: DirectoryPath
    output_directory: DirectoryPath

class Minimal(BaseModel):
    width: Annotated[int, Field(gt = 1799)]
    height: Annotated[int, Field(gt = 999)]
    aruco_ids: list[int]

class Box(BaseModel):
    aruco_ids: Annotated[list[int], AfterValidator(length_four)]
    corners: Annotated[list[Literal["tl", "tr", "bl", "br"]], AfterValidator(length_four)]  
    output_width: int
    output_height: int

class Config(BaseModel):
    directories: Directories
    minimal: Minimal
    box: list[Box]
    
    # @model_validator(mode = "after")
    # def check_box_dimensions(self) -> Self:
    #     for bx in self.box:
    #         if bx.output_height > 777
    
    @classmethod
    def from_toml(cls, path: str | Path) -> "Config":
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(str(p))
        data = tomllib.loads(p.read_text(encoding="utf-8"))
        return cls.model_validate(data)
    
if __name__ == "__main__":
    cfg = Config.from_toml("arucutter.toml")
    print(cfg)