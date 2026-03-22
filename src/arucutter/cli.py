from arucutter.utils import deskew_and_crop, describe_image
from arucutter.aruco import arucos
from arucutter.config import Config, Directories, Minimal, Box
from pathlib import Path

def pipeline():
    config = Config.from_toml("arucutter.toml")
    input_dir = config.directories.img_directory
    file_extensions = {".png", ".jpg", ".jpeg"}
    img_files = [f for f in input_dir.iterdir() if f.suffix.lower() in file_extensions and f.is_file()]
    
    for img_path in img_files:
        img_det = describe_image(str(img_path))
        print(f"Here are some image details: {img_det}")
        arucomarkers = arucos(img_path=img_path, 
                              output_path=config.directories.output_directory / f"{img_path.stem}_found_arucos.png")
        # print(arucomarkers)
        arucomarkers_dict = {a.id:a for a in arucomarkers}
        # print(arucomarkers_dict)
        
        output_count = 1
        
        for box in config.box:
            src_points = [arucomarkers_dict[i].x(c) for i, c in zip(box.aruco_ids, box.corners)]
            deskew_and_crop(image_path=img_path, src_points=src_points, dst_width=box.output_width, 
                            dst_height=box.output_height, 
                            output_path=config.directories.output_directory / f"{img_path.stem}_box_{output_count}.png")
            output_count += 1
    
def cli():
    pipeline()
    
if __name__ == "__main__":
    cli()