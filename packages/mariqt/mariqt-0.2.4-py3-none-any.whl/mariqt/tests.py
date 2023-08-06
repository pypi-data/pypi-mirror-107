""" This file contains various validation functions to check whether given parameters adhere to the MareHub AG V/I conventions"""
import mariqt.variables as miqtv
import mariqt.directories as miqtd
import datetime

def isValidPerson(o:dict):
	""" Checks whether the dict contains the four fields needed to identify a person"""
	req = ['affiliation', 'email', 'name', 'orcid']
	for r in req:
		if not r in o or o[r] == "":
			return False
	return True


def isValidDatapath(path:str):
	""" Check whether a path leads to a proper leaf data folder (raw, processed, etc.)"""
	try:
		d = miqtd.Dir(path)
		return d.validDataDir()
	except:
		return False


def isValidEventName(event:str):
	""" Check whether an event name follows the conventions: <project>[-<project part>]_<event-id>[-<event-id-index>][_<device acronym>]"""
	tmp = event.split("_")
	if len(tmp) < 2 or len(tmp) > 3:
		return False
	tmp2 = tmp[0].split("-")
	if len(tmp2) == 2:
		try:
			int(tmp2[1])
		except:
			return False

	tmp2 = tmp[1].split("-")
	if len(tmp2) == 1:
		try:
			int(tmp2[0])
		except:
			return False
	elif len(tmp2) == 2:
		try:
			int(tmp2[0])
			int(tmp2[1])
		except:
			return False
	else:
		return False
	return True


def isValidEquipmentID(eqid:str):
	""" Check whether an equipment id follows the convention: <owner>_<type>-<type index[_<subtype>[_<name>]]>"""
	eq = eqid.split("_")
	if len(eq) < 2:
		print("too short")
		return False
	eq2 = eq[1].split("-")
	if len(eq2) != 2:
		print("second too short")
		return False
	try:
		int(eq2[1])
	except:
		print("second second no int")
		return False
	if eq2[0] not in miqtv.equipment_types:
		print(eq2[0],"not in eq types")
		return False
	return True

def isValidImageName(name:str):
	""" Check whether an image filename adheres to the convention: <event>_<sensor>_<date>_<time>.<ext>"""
	tmp = name.split("_")

	# Find the sensor part of the name
	eq_type_idx = -1
	for i in range(0,len(tmp)):
		tmp2 = tmp[i].split("-")
		if tmp2[0] in miqtv.equipment_types:
			eq_type_idx = i
			break
	if eq_type_idx < 0:
		return False

	event = tmp[0]
	for i in range(1,eq_type_idx-1):
		event += "_" + tmp[i]
	if not isValidEventName(event):
		print(event,"is not a valid event name")
		return False

	eqid = tmp[eq_type_idx-1]
	for i in range(eq_type_idx,len(tmp)-2):
		eqid += "_" + tmp[i]

	if not isValidEquipmentID(eqid):
		print(eqid,"is not a valid equipment id")
		return False

	pos = tmp[-1].find(".")
	dt_str = tmp[-2]+tmp[-1][0:pos]
	ext = tmp[-1][pos+1:].lower()
	if not ext in miqtv.image_types:
		return False

	try:
		dt = datetime.datetime.strptime(dt_str,"%Y%m%d%H%M%S")
	except:
		try:
			dt = datetime.datetime.strptime(dt_str,"%Y%m%d%H%M%S.%f")
		except:
			print(dt_str,"cannot be parsed as date time")
			return False
	return True


def isValidiFDOField(field,value):
	if field in ['image-filename']:
		if not isValidImageName(value):
			raise Exception('Invalid item name',value)
	elif field in ['image-datetime']:
		try:
			datetime.datetime.strptime(value,'%Y-%m-%d %H:%M:%S.%f')
		except:
			raise Exception('Invalid datetime value',value)
	elif field in ['image-longitude','image-set-longitude']:
		try:
			value = float(value)
		except:
			raise Exception(field,'value is not a float',value)
		if value < -180 or value > 180:
			raise Exception(field,'value is out of bounds',value)
	elif field in ['image-latitude','image-set-latitude']:
		try:
			value = float(value)
		except:
			raise Exception(field,'value is not a float',value)
		if value < -90 or value > 90:
			raise Exception(field,'value is out of bounds',value)
	elif field in ['image-depth','image-set-depth']:
		try:
			value = float(value)
		except:
			raise Exception(field,'value is not a float',value)
		if value < 0:
			raise Exception(field,'value is out of bounds',value)
	elif field in ['image-altitude','image-set-altitude']:
		try:
			value = float(value)
		except:
			raise Exception(field,'value is not a float',value)
		if value < 0:
			raise Exception(field,'value is out of bounds',value)
	elif field in ['image-set-abstract']:
		if len(value) < 100 or len(value) > 1000:
			raise Exception("Length of the abstract is too long or too short")
	elif field in ['image-pi','image-set-pi']:
		if not isValidPerson(value):
			raise Exception("Not a valid person description for the pi")
	elif field in ['image-set-creators']:
		for p in value:
			if not isValidPerson(p):
				raise Exception("Not a valid person description for one of the creators")
	elif field in ['image-set-coordinate-uncertainty','image-coordinate-uncertainty']:
		try:
			value = float(value)
		except:
			raise Exception(field,'value is not a float',value)
		if value < 0:
			raise Exception(field,'value is out of bounds',value)

	return value

def isValidiFDOItem(item:dict,header:dict,all_items_have:dict):
	for req in miqtv.ifdo_item_fields:

		field_found = False
		alt_field_found = False

		if req in item and item[req] != "":
			field_found = True
		elif len(miqtv.ifdo_item_fields[req]['alt-fields']) > 0:
			for alt in miqtv.ifdo_item_fields[req]['alt-fields']:
				if alt[0:len('image-set-')] == "image-set-":
					if alt in header and header[alt] != "":
						alt_field_found = True
				elif alt[0:len('image-')] == "image-":
					if alt in item and item[alt] != "":
						alt_field_found = True

		# A required field was not found
		if not field_found:
			if req in all_items_have:
				del all_items_have[req]
			if not alt_field_found:
				raise Exception('Missing',req,'in item',item,"and alternative fields.")

		# A required field was found, now check its value
		else:
			item[req] = isValidiFDOField(req,item[req])


def isValidiFDOCoreHeader(header:dict,all_items_have:dict):
	for req in miqtv.ifdo_header_fields:

		field_found = False
		alt_field_found = False

		if req in header and header[req] != "":
			field_found = True
		elif len(miqtv.ifdo_header_fields[req]['alt-fields']) > 0:
			for alt in miqtv.ifdo_header_fields[req]['alt-fields']:
				if alt[0:len('image-set-')] == "image-set-":
					if alt in header and header[alt] != "":
						alt_field_found = True
				elif alt[0:len('image-')] == "image-":
					if alt in all_items_have and all_items_have[alt]:
						alt_field_found = True

		# A required field was not found
		if not field_found:
			if not alt_field_found:
				raise Exception('Missing',req,'in header',header,'and alternative fields')
		else:
			# Validata values
			header[req] = isValidiFDOField(req,header[req])


def isValidiFDOCapture(iFDO:dict):
	return isValidiFDO(iFDO,miqtv.ifdo_capture_fields)
def isValidiFDOContent(iFDO:dict):
	return isValidiFDO(iFDO,miqtv.ifdo_content_fields)

def isValidiFDO(iFDO,ref):
	vals_missing = []
	for req in ref:
		if req[:9] == 'image-set':
			# It is a header field
			if req not in iFDO['image-set-header']:
				vals_missing.append(req)
		else:
			# It is an item field:
			num = 0
			for item in iFDO['image-set-items']:
				if req not in iFDO['image-set-items'][item]:
					num += 1
				elif 'valid' in ref[req] and iFDO['image-set-items'][item][req] not in ref[req]['valid']:
					num += 1
			if num == len(iFDO['image-set-items']):
				vals_missing.append(req+": no image item has correct value")
			elif num > 0:
				vals_missing.append(req+": "+str(num)+" of "+str(len(iFDO['image-set-items']))+" lack correct value")
	return vals_missing
