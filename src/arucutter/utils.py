import cv2
import numpy as np
from arucutter.aruco import ArucoMarker

def deskew_and_crop(
    image_path: str,
    src_points: np.ndarray,
    dst_width: int,
    dst_height: int,
    output_path: str = "arucos/output/deskewed.png"
):
    """
    image_path : path to input image
    src_points : 4x2 array-like of (x, y) in source image
                 order: top-left, top-right, bottom-right, bottom-left
    dst_width  : width of output rectangle in pixels
    dst_height : height of output rectangle in pixels
    output_path: where to save result
    """
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")

    # Ensure float32 and correct shape
    src = np.array(src_points, dtype=np.float32).reshape(4, 2)

    # Destination rectangle
    dst = np.array(
        [
            [0, 0],
            [dst_width - 1, 0],
            [dst_width - 1, dst_height - 1],
            [0, dst_height - 1],
        ],
        dtype=np.float32,
    )

    # Perspective transform matrix
    M = cv2.getPerspectiveTransform(src, dst)

    # Warp (deskew) to desired size
    warped = cv2.warpPerspective(img, M, (dst_width, dst_height))

    # Save and also return the result
    cv2.imwrite(output_path, warped)
    return warped

def rescale(frame, scales = (0.8, 0.3)):
    width = int(frame.shape[1] * scales[0])
    height = int(frame.shape[0] * scales[1])
    dimensions = (width, height)
    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)

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