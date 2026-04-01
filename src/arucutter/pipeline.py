from pathlib import Path
from arucutter.config import Config
from arucutter.aruco import arucos
from arucutter.utils import describe_image, deskew_and_crop

class ArucutterError(Exception):
    pass

def pipeline(config: Config):
    input_dir = config.directories.img_directory
    file_extensions = {".png", ".jpg", ".jpeg"}
    img_files = [f for f in input_dir.iterdir() if f.suffix.lower() in file_extensions and f.is_file()]
    
    for img_path in img_files:
        img_det = describe_image(img_path)
        
        # skip image if minimal parameters not met
        if img_det["width"] < config.minimal.width or img_det["height"] < config.minimal.height:
            print(f"""
                  Image {img_path} does not meet minimal requirements.
                  Minimal height has to be {config.minimal.height}.
                  Minimal width has to be {config.minimal.width}.
                  Image {img_path} has the following details: {img_det}
                  """)
            # skip
            continue
        
        # output found markers as well?
        output_found_markers_path = None
        if config.directories.output_found_markers:
            output_found_markers_path = config.directories.output_directory / f"{img_path.stem}_found_arucos.png"
        # get ArUco markers
        arucomarkers = arucos(img_path=img_path,
                              aruco_dict_code=config.aruco.dict_code,
                              aruco_parameter_tweak=config.aruco.detector_parameters,
                              aruco_ids=config.minimal.aruco_ids,
                              output_path=output_found_markers_path)
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