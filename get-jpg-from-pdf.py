from pdf2image import convert_from_path
from scipy.ndimage import interpolation
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


# check which - old or new jpegs - height is smaller, if any for the resizing to happen
print (f"old hei: {list_of_resolutions[0][0]}")
print (f"new hei: {list_of_resolutions[1][0]}")
old_height = list_of_resolutions[0][0]
new_height = list_of_resolutions[1][0]

resized_CV2_images = []

if old_height > new_height:
    # resize the old pictures
    print ("resizing old images")
    for currentImage in list_of_CV2_image_lists[0]:
        # note, that the above extracted shape tuple is in a different order as the resize function wants. Therefore reversed for usage...
        resizedImage = cv2.resize(currentImage, (list_of_resolutions[1][1],list_of_resolutions[1][0]), interpolation = cv2.INTER_AREA)
        cv2.imwrite(r"C:\Users\50000700\Python\Python_repos\pdf-drawing-differences\pdf\temp\resized.jpg", resizedImage)
        resized_CV2_images.append(resizedImage)
    list_of_CV2_image_lists[0] = resized_CV2_images
elif new_height > old_height:
    # resize the new pictures
    print ("resizing new images")
    for currentImage in list_of_CV2_image_lists[1]:
        # note, that the above extracted shape tuple is in a different order as the resize function wants. Therefore reversed for usage...
        resizedImage = cv2.resize(currentImage, (list_of_resolutions[0][1],list_of_resolutions[0][0]), interpolation = cv2.INTER_AREA)
        cv2.imwrite(r"C:\Users\50000700\Python\Python_repos\pdf-drawing-differences\pdf\temp\resized.jpg", resizedImage)
        resized_CV2_images.append(resizedImage)
    list_of_CV2_image_lists[1] = resized_CV2_images
else :
    # if the hei are the same for old and new
    pass


# print transparent overlays

for idx, current_old_image in enumerate(list_of_CV2_image_lists[0]):
    current_new_image = list_of_CV2_image_lists[1][idx]

    # convert images to grayscale
    gray_old = cv2.cvtColor(current_old_image, cv2.COLOR_BGR2GRAY)
    gray_new = cv2.cvtColor(current_new_image, cv2.COLOR_BGR2GRAY)

    # compute structural similarity index (SSIM)
    (score, diff) = compare_ssim(gray_old, gray_new, full=True)
    diff = (diff * 255).astype("uint8")
    # value can fall between -1 to 1, where 1 is the perfect match
    print("SSIM: {}".format(score))

    # treshold the difference image, followed by finding contours to
    # obtain the regions of the two images that differ
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # copy input picture, as overlay has to be on different picture
    new_overlay = current_new_image.copy()
    # define output picture
    output = current_new_image.copy()
    alpha = 0.2

    for c in cnts:
        # compute the bounding box of the contour and then draw the
        # bounding box on both input images to represent where the two
        # images differ
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(new_overlay, (x, y), (x + w, y + h), (0, 0, 255), -1)

    cv2.addWeighted(new_overlay, alpha, current_new_image, 1 - alpha, 0, output)

    cv2.imwrite(r"C:\Users\50000700\Python\Python_repos\pdf-drawing-differences\pdf\temp\output.jpg", output)
