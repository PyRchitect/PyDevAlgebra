import sys
import cv2
import numpy as np

subfolder = "Fotografije"
filename = "Algebra_greyp.jpg"
file_photo = sys.path[0] + '\\' + subfolder + '\\' + filename

subfolder = "Resources"
filename = "deploy.prototxt"
file_deploy = sys.path[0] + '\\' + subfolder + '\\' + filename

subfolder = "Resources"
filename = "weights.caffemodel"
file_weights = sys.path[0] + '\\' + subfolder + '\\' + filename

model = cv2.dnn.readNetFromCaffe(file_deploy,file_weights)

file_photo_cv2 = cv2.imread(file_photo)

(height,width) = file_photo_cv2.shape[:2]

blob_image = cv2.dnn.blobFromImage(
	cv2.resize(file_photo_cv2,(300,300)),
	1.0,
	(300,300),
	(104.0,177.0,123.0)
)

model.setInput(blob_image)

detektirana_lica = model.forward()

broj_lica=0

for i in range(0,detektirana_lica.shape[2]):
	okvir = detektirana_lica[0,0,i,3:7]*np.array([width,height,width,height])
	(startX,startY,endX,endY) = okvir.astype('int')
	vjerojatnost = detektirana_lica[0,0,i,2]
	if vjerojatnost > 0.140:
		cv2.rectangle(file_photo_cv2,(startX,startY),(endX,endY),(0,255,0),2)
		broj_lica += 1

# subfolder = "Rezultat"
# file_folder = sys.path[0] + '\\' + subfolder 

# if not os.path.exists(file_folder):
# 	os.makedirs(file_folder)

# file_path = file_folder + '\\' + file_photo
# file_photo_cv2.imwrite(file_path,file_photo_cv2)

cv2.imshow('Pronadjena lica',file_photo_cv2)
cv2.waitKey()
print(f"Pronađeno je {broj_lica} lica!")