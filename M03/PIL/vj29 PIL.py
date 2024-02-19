from PIL import Image
import sys

subfolder = 'Fotografije'

image_name = "Python_logo_and_wordmark.png"
sourcepath = sys.path[0] + '\\' + subfolder + '\\' + image_name
source = Image.open(sourcepath)

image_name = "Algebra_campus.jpg"
destpath = sys.path[0] + '\\' + subfolder + '\\' + image_name
dest = Image.open(destpath)

print(source.size)
print(dest.size)

dest.paste(source,(500,300),source)
image_name = "Algebra_campus_watermark.jpg"
filepath = sys.path[0] + '\\' + subfolder + '\\' + image_name
dest.save(filepath,'JPEG')