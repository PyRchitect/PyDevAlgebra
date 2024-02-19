from PIL import Image, ImageFilter
import sys

subfolder = 'Fotografije'

def photo_load():
	image_name = 'Algebra_campus.jpg'
	filepath = sys.path[0] + '\\' + subfolder + '\\' + image_name
	photo = Image.open(filepath)
	return photo

def photo_edit(photo:'Image'):
	photo_edit = photo.transpose(Image.TRANSVERSE).show()
	photo_edit.show()

	# FLIP_TOP_BOTTOM
	# FLIP_LEFT_RIGHT
	# ROTATE_90
	# ROTATE_180
	# ROTATE_270
	# TRANSPOSE
	# TRANSVERSE

def photo_filter(img:'Image'):
	img00 = img.filter(ImageFilter.BLUR).show()

	# img01 = img.filter(ImageFilter.CONTOUR).show()
	# img02 = img.filter(ImageFilter.EDGE_ENHANCE).show()
	# img03 = img.filter(ImageFilter.EDGE_ENHANCE_MORE).show()
	# img04 = img.filter(ImageFilter.EMBOSS).show()
	# img05 = img.filter(ImageFilter.FIND_EDGES).show()
	# img06 = img.filter(ImageFilter.SHARPEN).show() 
	# img07 = img.filter(ImageFilter.SMOOTH).show()
	# img08 = img.filter(ImageFilter.SMOOTH_MORE).show() 
	# img09 = img.filter(ImageFilter.BoxBlur(radius=3)).show()
	# img09 = img.filter(ImageFilter.BoxBlur(radius=10)).show()
	# img10 = img.filter(ImageFilter.GaussianBlur(radius=8)).show()
	# img11 = img.filter(ImageFilter.UnsharpMask(radius=7, percent=250, threshold=3)).show()
	# img12 = img.filter(ImageFilter.MaxFilter(size=7)).show()
	# img13 = img.filter(ImageFilter.MedianFilter(size=7)).show()
	# img14 = img.filter(ImageFilter.MinFilter(size=7)).show() 

# photo_edit(photo_load())
photo_filter(photo_load())