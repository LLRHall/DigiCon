from __future__ import division
import cv2
import numpy as np
import json
import math
import os
from fpdf import FPDF
from aws import medical_report , txt2img , name_find

def show_img(img):
	cv2.imshow("img",img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def read_json(path):
	data = json.load(open(path))
	text_detected = data["TextDetections"]
	return text_detected

def render_text(txt):

	# img[y_min:y_max,x_min:x_max,:] = 255
	# putText(img,text_cur,(x_min,y_max),cv2.FONT_HERSHEY_COMPLEX_SMALL,scale,(0,0,0),2)

	font = cv2.FONT_HERSHEY_COMPLEX_SMALL
	fontScale = 1
	thickness = 2
	textSize = cv2.getTextSize(txt,font,fontScale,thickness)
	# print(textSize)
	textColor = (0,0,0)

	frame  = np.ones((300,300,1),np.uint8)*255
	frame  = np.ones((textSize[0][1]+5,textSize[0][0]+5,3), np.uint8)*255
	# show_img(frame)

	# height = textSize[0][0]
	# width = textSize[0][1]

	location = (0,textSize[0][1])

	cv2.putText(frame, txt, location, font, fontScale, color = textColor,thickness=thickness)

	# show_img(frame)
	return frame


def replace(text,img):
	# print(len(text))
	# print(text)
	rows, cols = img.shape[:2]
	boxes = {}
	box_id = 0

	img_new = np.ones((rows,cols),np.uint8)*0

	for i in range(len(text)):
		box = text[i]["Geometry"]["BoundingBox"]
		poly = text[i]["Geometry"]["Polygon"]
		x = []
		y = []
		for j in range(len(poly)):
			x.append(poly[j]["X"])
			y.append(poly[j]["Y"])

		x_min = int(min(x) * cols)
		x_max = int(max(x) * cols)
		y_min = int(min(y) * rows)
		y_max = int(max(y) * rows)
		# print(x_min,x_max,y_min,y_max)
		# cv2.rectangle(img,(x_min,y_min),(x_max,y_max),(0,255,0),3)

		#replacing with the text
		text_cur = text[i]["DetectedText"]
		# print(text_cur)

		cur_img = render_text(text_cur)
		# img[y_min:y_max,x_min:x_max] = cv2.resize(cur_img,(x_max-x_min,y_max-y_min))
		boxes[box_id] = (x_min,x_max,y_min,y_max,cv2.resize(cur_img,(x_max-x_min,y_max-y_min)),text_cur)
		img_new[y_min:y_max,x_min:x_max] = box_id
		# print(img_new)
		# show_img(img_new)
		box_id += 1

	# show_img(img_new)

	for key in boxes:
		cur_region = boxes[key][4]
		cur_x_min = boxes[key][0]
		cur_x_max = boxes[key][1]
		cur_y_min = boxes[key][2]
		cur_y_max = boxes[key][3]
		cur_text = boxes[key][5]
		# print(cur_text)
		# print(cur_x_min,cur_x_max,cur_y_min,cur_y_max)
		img_cur_regn = img_new[cur_y_min:cur_y_max,cur_x_min:cur_x_max]
		# show_img(img_cur_regn)
		flag = True
		counter1 =0
		counter2 =0
		for id_ in np.nditer(img_cur_regn):
			# print(id_)
			counter1+=1
			if id_ != key:
				counter2+=1
				flag= False
				# break

		ratio = counter2/counter1
		# print(counter2, counter1)
		# print(ratio)
		if flag or ratio <= 0.2:
			img[cur_y_min:cur_y_max,cur_x_min:cur_x_max] = cv2.resize(cur_region,(cur_x_max-cur_x_min,cur_y_max-cur_y_min))
			# show_img(img)
		# else :
		# 	print("********************** not printing this *************************")
	return img

def main(aws_result_json, filename, UPLOAD_FOLDER):
	abs_path_upload = os.path.join(UPLOAD_FOLDER, filename)
	# text = read_json("./out.txt")
	img= cv2.imread(abs_path_upload)
	replace(aws_result_json["TextDetections"],img)
	RESULT_FOLDER = UPLOAD_FOLDER.rstrip('uploads') + 'results'
	cv2.imwrite(os.path.join(RESULT_FOLDER, filename), img)
	pdf = FPDF()
	pdf.add_page()
	x,y,w,h = 0,0,200,250
	pdf.image(os.path.join(UPLOAD_FOLDER, filename), x,y,w,h)

	pdf.add_page()
	x,y,w,h = 0,0,200,250
	pdf.image(os.path.join(RESULT_FOLDER, filename), x,y,w,h)

	#adding name address to the pdf
	name , address = name_find.get_details(aws_result_json)
	personal_details = []
	personal_details.append("******** Patient Details ******* ") 
	personal_details.append("Name : "+ name) 
	personal_details.append("Address : " + address)

	txt2img.list_to_png(personal_details,RESULT_FOLDER,'/personal_details.png')
	pdf.add_page()
	x,y,w,h = 0,0,200,250
	pdf.image(os.path.join(RESULT_FOLDER, 'personal_details.png'), x,y,w,h)

	#adding the reports to the pdf
	report = ["***** Prescription Details ******* "]
	report = report+medical_report.medical_report(aws_result_json, abs_path_upload)
	# print(report)
	txt2img.list_to_png(report,RESULT_FOLDER, '/report.png')
	pdf.add_page()
	x,y,w,h = 0,0,200,250
	pdf.image(os.path.join(RESULT_FOLDER, 'report.png'), x,y,w,h)
	

	pdf.output(os.path.join(RESULT_FOLDER, filename)+".pdf","F")
