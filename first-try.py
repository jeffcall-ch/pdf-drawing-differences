from skimage.measure import compare_ssim
import imutils
import cv2

# load the 2 images
imageA = cv2.imread(r"C:\Users\50000700\Python\Python_repos\pdf-drawing-differences\sample_images\masterA.jpg")
imageB = cv2.imread(r"C:\Users\50000700\Python\Python_repos\pdf-drawing-differences\sample_images\masterB_with_extras.jpg")

# convert images to grayscale
grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

# compute structural similarity index (SSIM)
(score, diff) = compare_ssim(grayA, grayB, full=True)
diff = (diff * 255).astype("uint8")
# value can fall between -1 to 1, where 1 is the perfect match
print("SSIM: {}".format(score))

# treshold the difference image, followed by finding contours to
# obtain the regions of the two images that differ
thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)


# cv2.imwrite(r"C:\Users\50000700\Python\Python_repos\pdf-drawing-differences\sample_images\diff.jpg", diff)

# loop over cntours
# for c in cnts:
#     # compute the bounding box of the contour and then draw the
# 	# bounding box on both input images to represent where the two
# 	# images differ
# 	(x, y, w, h) = cv2.boundingRect(c)
# 	cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
# 	cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)

# cv2.imwrite(r"C:\Users\50000700\Python\Python_repos\pdf-drawing-differences\sample_images\image_B_highlighted.jpg", imageB)

# copy input picture, as overlay has to be on different picture
imageBOverlay = imageB.copy()
# define output picture
output = imageB.copy()
alpha = 0.2


for c in cnts:
    # compute the bounding box of the contour and then draw the
	# bounding box on both input images to represent where the two
	# images differ
	(x, y, w, h) = cv2.boundingRect(c)
	cv2.rectangle(imageBOverlay, (x, y), (x + w, y + h), (0, 0, 255), -1)

cv2.addWeighted(imageBOverlay, alpha, imageB, 1 - alpha, 0, output)

cv2.imwrite(r"C:\Users\50000700\Python\Python_repos\pdf-drawing-differences\sample_images\image_B_highlighted.jpg", output)
