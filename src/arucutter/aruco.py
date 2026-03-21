import numpy as np

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
        
    def __init__(self, id, corners):
        self.corners = self.check_corners(corners)
        self.id = int(id)
        self.name_corners(self.corners)
        
    def __repr__(self):
        return f'ArucoMarker(id: {self.id}, top_left: {self.top_left}, top_right: {self.top_right}, bottom_right: {self.bottom_right}, bottom_left: {self.bottom_left})'