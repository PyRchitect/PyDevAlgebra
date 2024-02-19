from PIL import Image, ImageDraw
import sys

subfolder = 'Fotografije'

def photo_load():
	image_name = 'Algebra_campus.jpg'
	filepath = sys.path[0] + '\\' + subfolder + '\\' + image_name
	photo = Image.open(filepath)
	return photo

def offset_coords(offset,img:'Image'):
	L = offset
	U = offset
	R = img.size[0]-offset
	D = img.size[1]-offset
	return (L,U,R,D)

def photo_draw_line(img:'Image'):
	draw = ImageDraw.Draw(img)
	draw.line(offset_coords(500,img),fill='blue')
	img.show()

def photo_draw_rectangle(img:'Image'):
	draw = ImageDraw.Draw(img)
	draw.rectangle(offset_coords(500,img),fill=None,outline="red",width=5)
	img.show()

def photo_draw_ellipse(img:'Image'):
	draw = ImageDraw.Draw(img)
	draw.ellipse(offset_coords(500,img),fill=None,outline="red",width=5)
	img.show()

photo_draw_line(photo_load())
# photo_draw_rectangle(photo_load())
# photo_draw_ellipse(photo_load())