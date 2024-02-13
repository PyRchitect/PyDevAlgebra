from PIL import Image, ImageEnhance
import sys

subfolder = 'Fotografije'

def photo_load():
	image_name = 'Algebra_campus.jpg'
	filepath = sys.path[0] + '\\' + subfolder + '\\' + image_name
	photo = Image.open(filepath)
	return photo

def photo_brightness(img:'Image'):
	image_enhancer_1 = ImageEnhance.Brightness(img)
	image_enhancer_1.enhance(4).show()
	# img_enhancer_2 = ImageEnhance.Contrast(img)
	# img_enhancer_2.enhance(4).show()
	# img_enhancer_3 = ImageEnhance.Sharpness(img)
	# img_enhancer_3.enhance(6).show()
	# img_enhancer_4 = ImageEnhance.Color(img)
	# img_enhancer_4.enhance(6).show() 

photo_brightness(photo_load())