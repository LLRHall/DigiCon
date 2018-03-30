import json
import cv2
import numpy as np
from skimage.transform import (hough_line, hough_line_peaks,
                               probabilistic_hough_line)
from skimage.feature import canny
from skimage import data
import matplotlib.pyplot as plt
from matplotlib import cm
from PIL import Image
from skimage import filters
from skimage.color import rgb2gray
import operator

def show_img(img):
	cv2.imshow("img",img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def y_coordinate_extractor(img_arr):
    middle_y_coor = 0.5 * img_arr.shape[0]
    image = rgb2gray(img_arr)
    image = np.asarray(image>0.5, dtype = np.float32)
    edges = filters.sobel_h(image)

    h,theta,d = hough_line(edges)
    upper_y = img_arr.shape[0]
    lower_y = 0
    thres_upp = img_arr.shape[0]
    thres_low = img_arr.shape[0]


    for _, angle, dist in zip(*hough_line_peaks(h, theta, d)):
        y0 = (dist - 0 * np.cos(angle)) / np.sin(angle)
        y1 = (dist - image.shape[1] * np.cos(angle)) / np.sin(angle)

        avg = (y0 + y1)/2
        if avg - middle_y_coor < thres_low and avg - middle_y_coor > 0:
            lower_y = avg
            thres_low = avg - middle_y_coor
        if middle_y_coor - avg < thres_upp and middle_y_coor - avg > 0:
            upper_y = avg
            thres_upp = middle_y_coor - avg

    return upper_y, lower_y

def render_text(txt):

	# img[y_min:y_max,x_min:x_max,:] = 255
	# putText(img,text_cur,(x_min,y_max),cv2.FONT_HERSHEY_COMPLEX_SMALL,scale,(0,0,0),2)

	font = cv2.FONT_HERSHEY_COMPLEX_SMALL
	fontScale = 1
	thickness = 2
	textSize = cv2.getTextSize(txt,font,fontScale,thickness)
	# #print(textSize)
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
		text_cur = text[i]["DetectedText"]
		
		cur_img = render_text(text_cur)
		boxes[box_id] = (x_min,x_max,y_min,y_max,cv2.resize(cur_img,(x_max-x_min,y_max-y_min)),text_cur)
		img_new[y_min:y_max,x_min:x_max] = box_id
		box_id += 1

	j=0
	Newboxes={}
	for key in boxes:
		cur_region = boxes[key][4]
		cur_x_min = boxes[key][0]
		cur_x_max = boxes[key][1]
		cur_y_min = boxes[key][2]
		cur_y_max = boxes[key][3]
		cur_text = boxes[key][5]

		# #print cur_text
		# #print(cur_x_min,cur_x_max,cur_y_min,cur_y_max)
		img_cur_regn = img_new[cur_y_min:cur_y_max,cur_x_min:cur_x_max]
		# show_img(img_cur_regn)
		flag = True
		counter1 =0
		counter2 =0
		for id_ in np.nditer(img_cur_regn):
			# #print(id_)
			counter1+=1
			if id_ != key:
				counter2+=1
				flag= False
				# break

		ratio = counter2/counter1
		# #print(counter2, counter1)
		# #print(ratio)
		if flag or ratio <= 0.5:
			img[cur_y_min:cur_y_max,cur_x_min:cur_x_max] = cv2.resize(cur_region,(cur_x_max-cur_x_min,cur_y_max-cur_y_min))
			Newboxes[j]=boxes[key]
			#print Newboxes[j][5]
			j=j+1

	# #print Newboxes
	#sorted_boxes = sorted(Newboxes.items(), key=lambda (k,v):(v[3],k))
	temp_dict = {}
	for key in Newboxes:
		temp_dict[key] = Newboxes[key][3]


	# sorted_boxes = sorted(temp_dict.items(), key=lambda (k,v):(v,k))
	sorted_boxes = [(k, temp_dict[k]) for k in sorted(temp_dict, key=temp_dict.get, reverse=False)]
	##print "------------baa"


	arr = []
	for key in sorted_boxes:
		# #print key
		arr.append(Newboxes[key[0]][5])

		
	index = []
	for j in range(len(arr)):
		parent_string = ''
		key_string = j
		for k in range(len(arr)):
			temp1 = arr[j].split()
			temp2 = arr[k].split()

			if all(x in temp2 for x in temp1) and len(arr[k]) > len(parent_string):
				key_string = k
				parent_string = arr[k]
		index.append(key_string)		
	
	#print index
	#index = set(index)
	used = set()
	unique = [x for x in index if x not in used and (used.add(x) or True)]	

	#print unique
	#print index
	arr = [arr[i] for i in unique]

	return arr


def medical_report(json_data, image_name):

	#with open(json_file) as json_data:
	#    d = json.load(json_data)
	d = json_data

	length = len(d['TextDetections'])

	img_rgb = image_name
	img_arr = np.array(Image.open(img_rgb), dtype=np.uint8)

	y1,y2 = y_coordinate_extractor(img_arr)
	y1=y1/img_arr.shape[0]
	y2=y2/img_arr.shape[0]
	min_Y = min(y1,y2)
	max_Y = max(y1,y2)

	r= {}
	j=0
	for i in range(0,length):
		count = 0
		x0 = d['TextDetections'][i]['Geometry']['Polygon'][0]['Y']
		x1 = d['TextDetections'][i]['Geometry']['Polygon'][1]['Y']
		x2 = d['TextDetections'][i]['Geometry']['Polygon'][2]['Y']
		x3 = d['TextDetections'][i]['Geometry']['Polygon'][3]['Y']

		# #print x0, x1, x2, x3
		if x0 >= min_Y and x0 <= max_Y:
			count= count + 1

		if x1 >= min_Y and x1 <= max_Y:
			count= count + 1

		if x2 >= min_Y and x2 <= max_Y:
			count= count + 1

		if x3 >= min_Y and x3 <= max_Y:
			count= count + 1

		if count >=2:
			r[j]=d['TextDetections'][i]
			j=j+1

	return replace(r, img_arr)


#with open('temp.json') as json_data:
#	d = json.load(json_data)

#print medical_report(d, "test_1.jpg")
