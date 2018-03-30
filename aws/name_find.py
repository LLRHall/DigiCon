import json
from pprint import pprint
import re

def get_details(json_file):
	# dic = json.load(json_file)
	dic = json_file
	#pprint(data)

	name = ''
	address = ''
	for entry in dic["TextDetections"]:
		text = entry['DetectedText']

		if 'name' in text.lower():
			#print text
			br = text.split('name')
			if len(br) < 2:
				br = text.split('Name')
			if len(br) < 2:
				br = text.split('NAME')
			#print br	
			if len(br) > 1:
				#print br
				temp_name = re.sub('[^a-zA-z0-9 ]*','', br[1])#br[1].strip('[^a-zA-z0-9 ]*')	
				temp_name = temp_name.strip()	
				if len(temp_name) > 0:
					name = temp_name

		if 'address' in text.lower():
			#print text
			br = text.split('address')
			if len(br) < 2:
				br = text.split('ADDRESS')
			if len(br) < 2:
				br = text.split('Address')

			if len(br) > 1:
				temp_address =  re.sub('[^a-zA-z0-9 ]*','', br[1])#br[1].strip('[^a-zA-z0-9]*')
				#if len(address) > 0:
				temp_address = temp_address.strip()
				if len(temp_address) > 0:
					address = temp_address


	return name, address

# print get_details(open('temp.json'))






