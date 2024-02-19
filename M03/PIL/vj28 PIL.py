from PIL import Image
import sys

subfolder = 'Fotografije'

def photo_load():
	image_name = 'Algebra_campus.jpg'
	filepath = sys.path[0] + '\\' + subfolder + '\\' + image_name

	photo = Image.open(filepath)

	# print(photo)
	# print(f"Format: {photo.format}")
	# print(f"Mode: {photo.mode}")
	# print(f"Size: {photo.size}")

	return photo

def photo_crop(photo):
	offset = 500
	L = 0+offset
	U = 0+offset
	R = photo.size[0]-offset
	D = photo.size[1]-offset

	crop = photo.crop((L,U,R,D))

	# photo.show()
	# crop.show()

	image_name = 'Algebra_campus_crop.jpg'
	filepath = sys.path[0] + '\\' + subfolder + '\\' + image_name
	crop.save(filepath,'JPEG')
	image_name = 'Algebra_campus_crop.png'
	filepath = sys.path[0] + '\\' + subfolder + '\\' + image_name
	crop.save(filepath,'PNG')

def photo_mode_bw(photo):
	photo_bw = photo.convert(mode='L')
	image_name = 'Algebra_campus_bw.png'
	filepath = sys.path[0] + '\\' + subfolder + '\\' + image_name
	photo_bw.save(filepath,'JPEG')

# photo_crop(photo_load())
# photo_mode_bw(photo_load())