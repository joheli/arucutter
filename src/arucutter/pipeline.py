from pathlib import Path
from arucutter.config import Config
from arucutter.aruco import arucos
from arucutter.utils import describe_image, deskew_and_crop, hexit, retrieve_boxnr, persist_boxnr

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
                  Skipping image {img_path}, as it does not meet minimal requirements.
                  Minimal height has to be {config.minimal.height}.
                  Minimal width has to be {config.minimal.width}.
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
        
        # retrieve the latest box number from file .boxnr
        box_nr = retrieve_boxnr()
        
        # copy list of labels from config; it might be None
        labels = config.label
        
        # if None, create a list of None
        if not config.label:
            labels = [None] * len(config.box)
            
        for b, l in zip(config.box, labels):
            src_points = [arucomarkers_dict[i].x(c) for i, c in zip(b.aruco_ids, b.corners)]
            deskew_and_crop(image_path=img_path, src_points=src_points, dst_width=b.output_width, dst_height=b.output_height, 
                            output_path=config.directories.output_directory / f"{img_path.stem}_box_{hexit(box_nr)}.png")
            if l:
                src_points = [arucomarkers_dict[i].x(c) for i, c in zip(l.aruco_ids, l.corners)]
                deskew_and_crop(image_path=img_path, src_points=src_points, dst_width=l.output_width, dst_height=l.output_height, 
                                output_path=config.directories.output_directory / f"{img_path.stem}_label_{hexit(box_nr)}.png")
            box_nr += 1
        
        # finally save the last box_nr to .boxnr
        persist_boxnr(box_nr)