import numpy as np
from typing import Literal, Any
import cv2

class ArucoDetectionError(Exception):
    pass

class ArucoMarker():
    corners: np.ndarray
    id: int
    top_left: list[int]
    top_right: list[int]
    bottom_right: list[int]
    bottom_left: list[int]
    
    # this method checks whether reshaping to (4,2) is possible
    def check_corners(self, corners: np.ndarray) -> np.ndarray:
        try: 
            corners_checked = corners.reshape((4, 2))
            corners_checked_int = np.int32(corners_checked)
            return corners_checked_int
        except:
            raise ArucoDetectionError(f"The corners supplied ({corners}) cannot be used.")
    
    # assign corner coordinates as lists [x, y] to variables top_left, top_right, etc.   
    def name_corners(self, corners) -> None:
        (top_left, top_right, bottom_right, bottom_left) = corners
        self.top_left = top_left.tolist()
        self.top_right = top_right.tolist()
        self.bottom_right = bottom_right.tolist()
        self.bottom_left = bottom_left.tolist()
    
    # a convenient getter for the named corners;
    # returns the coordinates [x, y] of the chosen corner    
    def x(self, code: Literal['tl', 'tr', 'br', 'bl']) -> list[int]:
        choice = self.top_left
        if code == 'tr':
            choice = self.top_right
        if code == 'br':
            choice = self.bottom_right
        if code == 'bl':
            choice = self.bottom_left
        return choice
    
    # the constructor 
    def __init__(self, id, corners):
        self.corners = self.check_corners(corners)
        self.id = int(id)
        self.name_corners(self.corners)
    
    # if an object is printed
    def __repr__(self):
        return f'ArucoMarker(id: {self.id}, top_left: {self.top_left}, top_right: {self.top_right}, bottom_right: {self.bottom_right}, bottom_left: {self.bottom_left})'

# Aruco Dict id - this is an int, which is looked up
# with this method
def get_aruco_dict_id(code: str) -> int:
    # prepend DICT_
    key = f"DICT_{code.strip().upper()}"
    # check if the key is exposed by cv2.aruco
    try:
        dict_id = getattr(cv2.aruco, key)
    # raise an error if not successful
    except AttributeError:
        raise ArucoDetectionError(f"Unknown ArUCo dictionary: key")
    return dict_id

# method 'arucos' extracts ArucoMarkers from an image
def arucos(img_path: str, *, 
           aruco_dict_code: str,
           aruco_parameter_tweak: dict[str, Any] | None,
           aruco_ids: list[int] | None = None,
           output_path: str | None = None) -> list[ArucoMarker]:
    # Load image
    img = cv2.imread(img_path)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {img_path}")
    
    # get aruco dictionary id
    aruco_dict_id = get_aruco_dict_id(aruco_dict_code)

    # Convert to grayscale (recommended for detection)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Choose 4x4 ArUco dictionary (e.g. 50 possible IDs)
    aruco_dict = cv2.aruco.getPredefinedDictionary(aruco_dict_id)
    parameters = cv2.aruco.DetectorParameters()
    
    # Try to adjust detector parameters
    # see options at https://docs.opencv.org/4.x/d1/dcd/structcv_1_1aruco_1_1DetectorParameters.html
    if (aruco_parameter_tweak):
        try:
            for param_name, new_setting in aruco_parameter_tweak.items():
                setattr(parameters, param_name, new_setting)
        except AttributeError:
            raise ArucoDetectionError(f"Parameter {param_name} either does not exist or cannot be set to {new_setting}!")

    # Create detector (OpenCV 4.7+ API)
    detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

    # Detect markers
    corners, ids, _ = detector.detectMarkers(gray)

    # Report how many were found
    num_detected = 0 if ids is None else len(ids)
    
    arucomarkers: list[ArucoMarker] = []

    if ids is not None:
        # Flatten IDs for easier iteration
        ids = ids.flatten()
        
        # Check if all the necessary ids were found
        if aruco_ids:
            if not set(aruco_ids).issubset(set(ids)):
                raise ArucoDetectionError(f"ArUco ids {aruco_ids} were not all found in image {str(img_path)}!")
                
        for marker_corners, marker_id in zip(corners, ids):
            # save as ArucoMarker
            am = ArucoMarker(marker_id, marker_corners)
            arucomarkers.append(am)

        # Save to output if output_path is specified
        if output_path:
            # Draw all detected markers on a copy of the image
            img_drawn = img.copy()
            cv2.aruco.drawDetectedMarkers(img_drawn, corners, ids)
            cv2.imwrite(output_path, img_drawn)
            print(f"Output image with drawn markers saved to: {output_path}")

        # return
        return arucomarkers
    else:
        raise ArucoDetectionError(f"No ArUco markers were found in image {str(img_path)}!")
        
if __name__ == "__main__":
    code = "7X7_1000"
    id = get_aruco_dict_id(code)
    print(f"The id of aruco dict {code} is: {id}")