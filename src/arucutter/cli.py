from arucutter.utils import deskew_and_crop, arucos

def pipeline():
    img_path = "experiments/input/aruco04.jpg"
    arucomarkers = arucos(img_path=img_path, output_path="experiments/output/output_aruco.png")
    # print(arucomarkers)
    arucomarkers_dict = {a.id:a for a in arucomarkers}
    # print(arucomarkers_dict)
    src_points1 = [arucomarkers_dict[2].top_left,
                  arucomarkers_dict[3].top_left,
                  arucomarkers_dict[8].bottom_left,
                  arucomarkers_dict[7].bottom_left]
    src_points2 = [arucomarkers_dict[7].bottom_left,
                  arucomarkers_dict[6].bottom_left,
                  arucomarkers_dict[1].top_left,
                  arucomarkers_dict[2].top_left]
    src_points3 = [arucomarkers_dict[13].bottom_left,
                  arucomarkers_dict[12].bottom_left,
                  arucomarkers_dict[7].bottom_left,
                  arucomarkers_dict[8].bottom_left]
    src_points4 = [arucomarkers_dict[7].bottom_left,
                  arucomarkers_dict[8].bottom_left,
                  arucomarkers_dict[13].bottom_left,
                  arucomarkers_dict[12].bottom_left]
    src_points5 = [arucomarkers_dict[13].bottom_left,
                  arucomarkers_dict[8].bottom_left,
                  arucomarkers_dict[7].bottom_left,
                  arucomarkers_dict[12].bottom_left]
    #print(src_points)
    deskew_and_crop(image_path=img_path, src_points=src_points1, dst_width=600, dst_height=600)
    deskew_and_crop(image_path=img_path, src_points=src_points2, dst_width=600, dst_height=600, output_path="experiments/output/deskewed2.png")
    deskew_and_crop(image_path=img_path, src_points=src_points3, dst_width=600, dst_height=600, output_path="experiments/output/deskewed3.png")
    deskew_and_crop(image_path=img_path, src_points=src_points4, dst_width=600, dst_height=600, output_path="experiments/output/deskewed4.png")
    deskew_and_crop(image_path=img_path, src_points=src_points5, dst_width=600, dst_height=600, output_path="experiments/output/deskewed5.png")
    print("fut")
    
def cli():
    pipeline()
    
if __name__ == "__main__":
    cli()