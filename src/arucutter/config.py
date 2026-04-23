from pathlib import Path
from pydantic import BaseModel, Field, DirectoryPath, AfterValidator, model_validator
from typing import Annotated, Literal, Any
from typing_extensions import Self
import tomllib

class ArucutterConfigError(Exception):
    pass

def length_four(l: list[int|Literal["tl", "tr", "bl", "br"]]) -> list[int|Literal["tl", "tr", "bl", "br"]]:
    if len(l) != 4:
        raise ValueError(f"The length of {l} is not 4!")
    return l

class Aruco(BaseModel):
    dict_code: str
    detector_parameters: dict[str, Any] | None = None

class Directories(BaseModel):
    img_directory: DirectoryPath
    output_directory: DirectoryPath
    output_found_markers: bool = False

class Minimal(BaseModel):
    width: Annotated[int, Field(gt = 1799)]
    height: Annotated[int, Field(gt = 999)]
    aruco_ids: list[int]
    area_increase: Literal["warn", "allow", "prevent"] = "prevent"

class Box(BaseModel):
    aruco_ids: Annotated[list[int], AfterValidator(length_four)]
    corners: Annotated[list[Literal["tl", "tr", "bl", "br"]], AfterValidator(length_four)]  
    output_width: int
    output_height: int

class Config(BaseModel):
    aruco: Aruco
    directories: Directories
    minimal: Minimal
    box: list[Box]
    label: list[Box] | None = None
    
    @model_validator(mode = "after")
    def check_labels(self) -> Self:
        # are labels present at all?
        if (self.label):
            # length of label has to be the same as that of box
            if len(self.box) != len(self.label):
                raise ArucutterConfigError(f"The number of boxes (provided: {len(self.box)}) and labels (provided: {len(self.label)}) are not equal!")
        return self
            
    @classmethod
    def from_toml(cls, path: str | Path) -> "Config":
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"The supplied config file {p} was not found!")
        data = tomllib.loads(p.read_text(encoding="utf-8"))
        return cls.model_validate(data)
    
if __name__ == "__main__":
    cfg = Config.from_toml("arucutter.toml")
    print(cfg)