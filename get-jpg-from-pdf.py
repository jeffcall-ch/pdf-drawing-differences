from pdf2image import convert_from_path
from skimage.measure import compare_ssim
import imutils
import cv2
import numpy as np
import pathlib

# input variables
pdf_folder_old = r"C:\Users\50000700\Python\Python_repos\pdf-drawing-differences\pdf\old"
pdf_folder_new = r"C:\Users\50000700\Python\Python_repos\pdf-drawing-differences\pdf\new"
temp_folder = r"C:\Users\50000700\Python\Python_repos\pdf-drawing-differences\pdf\temp"
folder_difference_on_new = r"C:\Users\50000700\Python\Python_repos\pdf-drawing-differences\pdf\difference_on_new"
input_pdf_file_old = r"\AD00039347.pdf"
input_pdf_file_new = r"\AD00039347-01.pdf"

# define a list to hold the old and new pdf files - will make easier to process without code duplication
input_output_pdf_list = []
input_output_pdf_list.append(pathlib.Path(pdf_folder_old + input_pdf_file_old))
input_output_pdf_list.append(pathlib.Path(pdf_folder_new + input_pdf_file_new))

# define list to hold a old and new CV2 image lists (list of lists)
list_of_CV2_image_lists = []
# define list of resolutions
list_of_resolutions = []

for pdf_file in input_output_pdf_list:
    pages = convert_from_path(pdf_file, 200)

    # extract jpeg files page by page and save them
    page_counter = 1
    list_of_extracted_jpegs = []
    for page in pages:
        newFileName = temp_folder + r"\\" + pdf_file.stem + "_" + str(page_counter) + '.jpeg'
        page_counter += 1
        page.save(newFileName, 'JPEG')
        list_of_extracted_jpegs.append(newFileName)

    # create CV2 images from the files
    list_of_CV2_images_from_extracted_jpegs = []
    for currentJpeg in list_of_extracted_jpegs:
        list_of_CV2_images_from_extracted_jpegs.append(cv2.imread(currentJpeg))
        print (currentJpeg)

    list_of_CV2_image_lists.append(list_of_CV2_images_from_extracted_jpegs)
    height, width = list_of_CV2_images_from_extracted_jpegs[0].shape[:2]
    list_of_resolutions.append(list_of_CV2_images_from_extracted_jpegs[0].shape[:2])
    print (f"jpeg resolution - height x width: {height} x {width}")


def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized



# check which - old or new jpegs - height is smaller, if any for the resizing to happen
print (f"old hei: {list_of_resolutions[0][0]}")
print (f"new hei: {list_of_resolutions[1][0]}")
old_height = list_of_resolutions[0][0]
new_height = list_of_resolutions[1][0]

if old_height > new_height:
    # resize the old pictures
    print ("resizing old images")
    for currentImage in list_of_CV2_image_lists[0]:
        image_resize(currentImage, height = new_height)
        cv2.imwrite(r"C:\Users\50000700\Python\Python_repos\pdf-drawing-differences\pdf\temp\resized.jpg", currentImage)
elif new_height > old_height:
    # resize the new pictures
    print ("resizing new images")
    for currentImage in list_of_CV2_image_lists[1]:
        image_resize(currentImage, height = old_height)
        cv2.imwrite(r"C:\Users\50000700\Python\Python_repos\pdf-drawing-differences\pdf\temp\resized.jpg", currentImage)
else :
    # if the hei are the same for old and new
    pass





