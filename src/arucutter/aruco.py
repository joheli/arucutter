import numpy as np
from typing import Literal
import cv2

class ArucoMarker():
    corners: np.ndarray
    id: int
    top_left: list[int]
    top_right: list[int]
    bottom_right: list[int]
    bottom_left: list[int]
    
    def check_corners(self, corners: np.ndarray) -> np.ndarray:
        try: 
            corners_checked = corners.reshape((4, 2))
            corners_checked_int = np.int32(corners_checked)
            return corners_checked_int
        except:
            raise ValueError(f"The corners supplied ({corners}) cannot be used.")
        
    def name_corners(self, corners) -> None:
        (top_left, top_right, bottom_right, bottom_left) = corners
        self.top_left = top_left.tolist()
        self.top_right = top_right.tolist()
        self.bottom_right = bottom_right.tolist()
        self.bottom_left = bottom_left.tolist()
        
    def x(self, code: Literal['tl', 'tr', 'br', 'bl']) -> list[int]:
        choice = self.top_left
        if code == 'tr':
            choice = self.top_right
        if code == 'br':
            choice = self.bottom_right
        if code == 'bl':
            choice = self.bottom_left
        return choice
        
    def __init__(self, id, corners):
        self.corners = self.check_corners(corners)
        self.id = int(id)
        self.name_corners(self.corners)
        
    def __repr__(self):
        return f'ArucoMarker(id: {self.id}, top_left: {self.top_left}, top_right: {self.top_right}, bottom_right: {self.bottom_right}, bottom_left: {self.bottom_left})'
    
def arucos(img_path: str, output_path: str) -> list[ArucoMarker]:
    # Load image
    img = cv2.imread(img_path)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {img_path}")
    
    #img_rs = img

    # Convert to grayscale (recommended for detection)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Choose 4x4 ArUco dictionary (e.g. 50 possible IDs)
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    parameters = cv2.aruco.DetectorParameters()
    
    # Try relaxing or adjusting these
    parameters.minMarkerPerimeterRate = 0.03   # default ~0.03
    parameters.maxMarkerPerimeterRate = 0.1    # default ~4.0, sometimes increase
    parameters.useAruco3Detection = False      # default =  False

    parameters.minDistanceToBorder = 3         # if markers are near image edges
    parameters.adaptiveThreshWinSizeMin = 3
    parameters.adaptiveThreshWinSizeMax = 33 # or higher
    parameters.adaptiveThreshWinSizeStep = 10
    parameters.adaptiveThreshConstant = 7     # tweak if illumination is tricky

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

        for marker_corners, marker_id in zip(corners, ids):
            # save as ArucoMarker
            am = ArucoMarker(marker_id, marker_corners)
            arucomarkers.append(am)

            # print(f"Marker ID: {am.id}")
            # print(f"  top_left:      {am.top_left}") # converts it to [x,y]
            # print(f"  top_right:     {am.top_right}")
            # print(f"  bottom_right:  {am.bottom_right}")
            # print(f"  bottom_left:   {am.bottom_left}")

        # Draw all detected markers on a copy of the image
        img_drawn = img.copy()
        cv2.aruco.drawDetectedMarkers(img_drawn, corners, ids)

        # Save or show
        cv2.imwrite(output_path, img_drawn)
        print(f"Output image with drawn markers saved to: {output_path}")

        # Optional: display (comment out if running headless)
        # cv2.imshow("Detected ArUco markers", img_drawn)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        print(f"Detected {num_detected} ArUco markers")
        return arucomarkers
    else:
        print("No markers detected.")