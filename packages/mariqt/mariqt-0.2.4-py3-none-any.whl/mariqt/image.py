import os
import yaml
import json
import datetime
import subprocess

import PIL.Image
import PIL.ExifTags

import mariqt.core as miqtc
import mariqt.directories as miqtd
import mariqt.tests as miqtt
import mariqt.variables as miqtv
import mariqt.files as miqtf
import mariqt.navigation as miqtn
import mariqt.settings as miqts


def getVideoRuntime(path):
	""" Uses FFMPEG to determine the runtime of a video in seconds. Returns 0 in case their was any issue"""
	command = "ffprobe -v fatal -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "+path
	result = subprocess.run(command.split(" "),stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	try:
		return float(result.stdout)
	except:
		return 0


def getVideoStartTime(path):
	""" Uses FFMPEG to determine the start time of a video from the metadata of the video file. Returns an empty string in case there was any issue"""
	command = "ffprobe -v fatal -show_entries format_tags=creation_time -of default=noprint_wrappers=1:nokey=1 "+path
	result = subprocess.run(command.split(" "),stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	return result.stdout.decode("utf-8").strip()


def getVideoUUID(path):
	""" Uses FFMPEG to query a video file for a UUID in its metadata. Returns an empty string if there is no UUID encoded in the file"""
	command = "ffprobe -v fatal -show_entries format_tags=UUID -of default=noprint_wrappers=1:nokey=1 "+path
	result = subprocess.run(command.split(" "),stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	return result.stdout.decode("utf-8").strip()


def getImageUUID(path):
	""" Uses exiftool to query an image file for a UUID in its metadata. Returns an empty string if there is no UUID encoded in the file."""
	command = "exiftool -imageuniqueid "+path
	result = subprocess.run(command.split(" "),stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	txt = result.stdout.decode("utf-8").strip()
	if txt != "":
		txt = txt.split("\n")[-1]# Omit Perl warnings
		txt = txt.split(":")[1].strip()
	return txt


def getImageUUIDsForFolder(path):
	""" Uses exiftool to query all images in folder path for the UUID in their metadata. Returns a dict with filename -> UUID keys/values. Or an empty dict if none of the images has a UUID in the metadata. Images without a UUID do not make it into the returned dict!"""
	command = "exiftool -T -filename -imageuniqueid " + path
	result = subprocess.run(command.split(" "),stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	txt = result.stdout.decode("utf-8").strip()
	ret = {}
	if txt != "":
		lines = txt.split("\n")
		for line in lines:
			tmp = line.split("\t")
			if len(tmp) < 2:
				continue
			ret[tmp[0]] = tmp[1].split()
	return ret


def createiFDOForEvent(dir:miqtd.Dir,ifdo_params,handle_prefix = '20.500.12085'):
	""" Use this function to create an iFDO in case you are following all the other MareHUB AG V/I and mariqt conventions."""

	if dir.sensor() == "":
		print("Path given does not contain sensor information",dir.str())
		return {}

	ifdo_params['image-set-sensor'] = dir.sensor()
	ifdo_params['image-set-event'] = dir.event()

	if not 'image-set-uuid' in ifdo_params:
		ifdo_params['image-set-uuid'] = str(miqtc.uuid4())
	if not 'image-set-handle' in ifdo_params:
		ifdo_params['image-set-handle'] = handle_prefix + "/" + ifdo_params['image-set-uuid']
	if not 'image-set-data-handle' in ifdo_params:
		ifdo_params['image-set-data-handle'] = handle_prefix + "/" + ifdo_params['image-set-uuid'] + "@data"
	if not 'image-set-metadata-handle' in ifdo_params:
		ifdo_params['image-set-metadata-handle'] = handle_prefix + "/" + ifdo_params['image-set-uuid'] + "@metadata"
	if not 'image-set-name' in ifdo_params:
		ifdo_params['image-set-name'] = ifdo_params["image-set-project"] + " " + dir.event() + " " + dir.sensor()

	# Parse image-set-abstract and fill its placeholders with information!
	ifdo_params['image-set-abstract'] = miqts.parseReplaceVal(ifdo_params,'image-set-abstract')

	# Which files contain the information needed to create the iFDO items and which columns shall be used
	req = {'hashes':{'suffix':'_image-hashes.txt','cols':['image-hash'],'optional':[]},
			'navigation':{'suffix':'_image-navigation.txt','cols':['image-longitude','image-latitude'],'optional':['image-depth','image-altitude','image-second']},
			'scaling':{'suffix':'_image-scaling.txt','cols':['image-pixel-per-millimeter'],'optional':[]},
			'uuids':{'suffix':'_image-uuids.txt','cols':['image-uuid'],'optional':[]},
			'datetime':{'suffix':'_image-start-times.txt','cols':['image-datetime'],'optional':[]},
			'area':{'suffix':'_image-areas.txt','cols':['image-area'],'optional':[]},
			'features':{'suffix':'_image-features.txt','cols':['image-entropy','image-average-color','image-mpeg7-colorlayout','image-mpeg7-colorstatistic','image-mpeg7-colorstructure','image-mpeg7-dominantcolor','image-mpeg7-edgehistogram','image-mpeg7-homogeneoustexture','image-mpeg7-scalablecolor'],'optional':[]},
			'settings':{'suffix':'_image-acquisition-settings.txt','cols':['image-acquisition-settings'],'optional':[]}}

	int_folder = dir.replace(dir.dp.TYPE,"intermediate")

	item_data = {}
	for r in req:
		if not os.path.exists(int_folder + dir.event() + "_" + dir.sensor() + req[r]['suffix']):
			raise Exception("Image item file is missing:",int_folder + dir.event() + "_" + dir.sensor() + req[r]['suffix'])
		tmp_data = miqtf.tabFileData(int_folder + dir.event() + "_" + dir.sensor() + req[r]['suffix'],req[r]['cols']+['image-filename']+req[r]['optional'],key_col='image-filename',optional=req[r]['optional'])
		for img in tmp_data:
			if img not in item_data:
				item_data[img] = {}
			for v in tmp_data[img]:
				item_data[img][v] = tmp_data[img][v]
			item_data[img]['image-filename'] = img

	prev_len = -1
	for item in item_data:
		if prev_len > 0 and len(item) != prev_len:
			raise Exception("Not all items have the same amount of metadata",len(item),prev_len)

	if len(item_data) == 0:
		raise Exception("No iFDO items")

	return createiFDO(ifdo_params,item_data.values())


def createiFDO(header:dict,items:dict):
	""" Creates FAIR digital object for the image data itself. This consists of header information and item information."""

	yml = {'image-set-items':{},'image-set-header':{}}

	if len(items) == 0:
		raise Exception('No item information given')

	# Find header fields that allow items to specify overloads. In case all items have that overload specified, the header is not required.
	all_items_have = {}
	for req in miqtv.ifdo_header_fields:
		if len(miqtv.ifdo_header_fields[req]['alt-fields']) > 0:
			for alt in miqtv.ifdo_header_fields[req]['alt-fields']:
				if alt in all_items_have:
					continue
				elif alt[0:len('image-')] == "image-" and alt[0:len('image-set-')] != "image-set-":
					all_items_have[alt] = True


	# Validate item information
	for item in items:

		miqtt.isValidiFDOItem(item,header,all_items_have)

		# Put all item information into the yaml struct to write to disk
		yml['image-set-items'][item['image-filename']] = {}
		for it in item:
			if it != 'image-filename':
				yml['image-set-items'][item['image-filename']][it] = item[it]

	# Validate header information
	miqtt.isValidiFDOCoreHeader(header,all_items_have)

	# Add all header fields to the yaml struct for writing
	for key in header:
		yml['image-set-header'][key] = header[key]

	return yml


def writeiFDO(iFDO:dict,path:miqtd.Dir):
	""" Writes an iFDO to disk"""

	dst_path = path.tosensor()+'products/'+path.event()+'_'+path.sensor()+'_iFDO.yaml'

	o = open(dst_path,"w")
	yaml.dump(iFDO,o)
	o.close()


def browseFolderForImages(path:str,types = miqtv.image_types):
	""" Recursively scans a folder for media folders (specified by the given file types you are looking for).

	The result variable contains a dictionary with the found file paths as keys and
	a triple for each of those files with the file size, runtime and file extension:
	<name>:[<size>,<runtime>,<ext>]
	"""

	ret = {}
	files = os.listdir(path)
	for file in files:

		# Skip config files
		if file[0] == ".":
			continue

		# Recurse into subfolders
		if os.path.isdir(path+file):
			ret += browseFolderForImages(path+file+"/",types)

		elif os.path.isfile(path+file):
			file_ext = os.path.splitext(file)[1].replace(".","").lower()
			if file_ext in types:
				ret[path+file] = [os.stat(path+file).st_size,-1,file_ext]
				if file_ext in miqtv.video_types:
					# This is a video file, check its runtime with ffmpeg
					ret[path+file][1] = getVideoRuntime(path+file)
	return ret


def createImageList(path:miqtd.Dir,overwrite=False,write_path:bool=False,img_types = miqtv.image_types):
	""" Creates a text file that contains one line per image file found in path

	Can overwrite an existing file list file if told so.
	Can add the full absolute path to the text file if told so (by providing the absolute path you want as the write_path variable)
	Can filter which images (or actually all file types) to put into the file. Default is all image types.
	"""

	if not path.exists():
		return False,"Path not found"

	# Potentially create output folder
	path.createTypeFolder(["intermediate"])

	# Check whether the full path shall be written
	if write_path == True:
		write_path = path
	else:
		write_path = ""

	# Scan the directory and write all files to the output file
	dst_path = path.tosensor()+"intermediate/"+path.event()+"_"+path.sensor()+"_images.lst"
	if not os.path.exists(dst_path) or overwrite:
		try:
			lst = open(dst_path,"w")
			files = os.listdir(path.tosensor()+"raw/")
			for file in files:
				if file[0] == ".":
					continue
				fn, fe = os.path.splitext(file)
				if fe[1:].lower() in img_types:
					lst.write(write_path+file+"\n")
			lst.close()
			return True,"Created output file."
		except:
			return False,"Could not create output file."
	else:
		return True,"Output file exists."


def createUUIDFile(path:miqtd.Dir):
	""" Creates a text file with two columns: image-filename and image-uuid.

	The UUID is only *taken* from the metadata of the images. It does not write UUIDs to the metadata in case some files are missing it.
	But, it creates a CSV file in that case that you can use together with exiftool to add the UUID to your data. Beware! this can destroy your images
	if not done properly! No guarantee is given it will work. Be careful!
	"""

	uuid_path = path.tosensor()+"/intermediate/"+path.event()+"_"+path.sensor()+"_image-uuids.txt"

	# Check whether a file with UUIDs exists, then read it
	uuids = {}
	if os.path.exists(uuid_path):
		uuids = miqtf.tabFileData(uuid_path,[miqtv.col_header['mariqt']['img'],miqtv.col_header['mariqt']['uuid']],key_col=miqtv.col_header['mariqt']['img'])

	if os.path.exists(path.tosensor()+"/raw/"):

		missing_uuids = {}
		added_uuids = 0

		img_paths = browseFolderForImages(path.tosensor()+"/raw/")
		for file in img_paths:
			file_name = file.replace(path.tosensor()+"/raw/","")
			if file_name not in uuids:

				# Check whether this file contains a UUID that is not known in the UUID file yet
				if os.path.splitext(file)[1][1:].lower() in miqtv.photo_types:
					uuid = getImageUUID(file)
				elif os.path.splitext(file)[1][1:].lower() in miqtv.video_types:
					uuid = getVideoUUID(file)
				else:
					raise Exception("Unsupported file type to determine UUID from metadata: "+os.path.splitext(file)[1][1:])

				if uuid == "":
					uuid = miqtc.uuid4()
					missing_uuids[file] = uuid
				else:
					uuids[file_name] = uuid
					added_uuids += 1
			else:
				uuids[file_name] = uuids[file_name][miqtv.col_header['mariqt']['uuid']]

		# If previously unknown UUIDs were found in the file headers, add them to the UUID file
		if added_uuids > 0:
			res = open(uuid_path,"w")
			res.write(miqtv.col_header['mariqt']['img']+"\t"+miqtv.col_header['mariqt']['uuid']+"\n")
			for file in uuids:
				res.write(file+"\t"+str(uuids[file])+"\n")
			res.close()

		if len(missing_uuids) > 0:
			ecsv_path = path.tosensor()+"/intermediate/"+path.event()+"_"+path.sensor()+"_exif-add-uuid.csv"
			csv = open(ecsv_path,"w")
			csv.write(miqtv.col_header['exif']['img']+","+miqtv.col_header['exif']['uuid']+"\n")
			for img in missing_uuids:
				csv.write(img+","+str(missing_uuids[img])+"\n")
			return False,"exiftool -csv="+ecsv_path+" "+path.tosensor()+"raw/"

		return True,"All images have a UUID"
	return False,"Path "+path.tosensor()+"/raw/ not found."



def createImageNavigationFile(path:miqtd.Dir,nav_path:str,nav_header = miqtv.pos_header['pangaea'],date_format = miqtv.date_formats['pangaea'],overwrite=False):
	""" Creates a text file with 4.5D navigation data for each image"""

	dst_path = path.tosensor()+'intermediate/'+path.event()+'_'+path.sensor()+'_image-navigation.txt'

	if os.path.exists(dst_path) and not overwrite:
		return True,"Output file exists: "+dst_path

	if not os.path.exists(nav_path):
		return False,"Navigation file not found: "+nav_path

	if not os.path.exists(path.tosensor()+"raw"):
		return False,"Image folder not found: "+path.tosensor()+"raw"

	# Load navigation data
	nav_data = miqtn.readAllPositionsFromFilePath(nav_path,nav_header,date_format)

	image_dts = {}
	img_paths = browseFolderForImages(path.tosensor()+"/raw/")
	for file in img_paths:
		file_name = file.replace(path.tosensor()+"/raw/","")

		tmp = file_name.split("_")
		dt_image = datetime.datetime.strptime(tmp[-2]+tmp[-1][0:tmp[-1].find(".")]+"+0000","%Y%m%d%H%M%S%z")
		dt_image_ts = int(dt_image.timestamp())

		if dt_image_ts not in nav_data.positions:
			return False,"Could not find "+str(dt_image_ts)+" in "+str(len(nav_data.positions))+" positions"
		else:
			pos = nav_data.positions[dt_image_ts]
			image_dts[file_name] = [dt_image.strftime(miqtv.date_formats['mariqt']),pos.lat,pos.lon,pos.dep,pos.hgt]

	if len(image_dts) > 0:

		# Check whether depth and height are set
		lat_identical,lon_identical,dep_identical,hgt_identical,dep_not_zero,hgt_not_zero = miqtn.checkPositionContent(nav_data)

		# Write to navigation txt file
		res = open(dst_path,"w")
		res.write(miqtv.col_header['mariqt']['img']+"\t"+miqtv.col_header['mariqt']['utc']+"\t"+miqtv.col_header['mariqt']['lat']+"\t"+miqtv.col_header['mariqt']['lon'])
		if dep_not_zero:
			res.write("\t"+miqtv.col_header['mariqt']['dep'])
		if hgt_not_zero:
			res.write("\t"+miqtv.col_header['mariqt']['dep'])
		res.write("\n")

		for file in image_dts:
			res.write(file+"\t"+image_dts[file][0]+"\t"+str(image_dts[file][1])+"\t"+str(image_dts[file][2]))
			if dep_not_zero:
				res.write("\t"+str(image_dts[file][3]))
			if hgt_not_zero:
				res.write("\t"+str(image_dts[file][4]))
			res.write("\n")
		res.close()

		# Write to geojson file
		geojson = {'type':'FeatureCollection','name':path.event()+"_"+path.sensor()+"_image-navigation",'features':[]}
		for file in image_dts:
			if dep_not_zero:
				geojson['features'].append({'type':'Feature','properties':{'id':file},'geometry':{'type':"Point",'coordinates':[float(image_dts[file][1]),float(image_dts[file][2]),float(image_dts[file][3])]}})
			else:
				geojson['features'].append({'type':'Feature','properties':{'id':file},'geometry':{'type':"Point",'coordinates':[float(image_dts[file][1]),float(image_dts[file][2])]}})
		o = open(dst_path.replace(".txt",".geojson"),"w",errors="ignore",encoding='utf-8')
		json.dump(geojson, o, ensure_ascii=False, indent=4)

		return True,"Navigation data created"
	else:
		return False,"No image coordinates found"


def createImageSHA256File(path:miqtd.Dir):
	""" Creates a text file with two columns: image-filename and image-hash (a SHA256 hash)"""

	dst_path = path.tosensor()+"intermediate/"+path.event()+"_"+path.sensor()+"_image-hashes.txt"

	hashes = {}
	if os.path.exists(dst_path):
		hashes = miqtf.tabFileData(dst_path,[miqtv.col_header['mariqt']['img'],miqtv.col_header['mariqt']['hash']],key_col=miqtv.col_header['mariqt']['img'])

	img_paths = browseFolderForImages(path.tosensor()+"/raw/")

	if len(img_paths) > 0:

		added_hashes = 0
		for file in img_paths:
			file_name = file.replace(path.tosensor()+"/raw/","")
			if file_name in hashes:
				hashes[file_name] = hashes[file_name][miqtv.col_header['mariqt']['hash']]
			else:
				hashes[file_name] = miqtc.sha256HashFile(file)
				added_hashes += 1

		if added_hashes > 0:
			hash_file = open(dst_path,"w")
			hash_file.write(miqtv.col_header['mariqt']['img']+"\t"+miqtv.col_header['mariqt']['hash']+"\n")
			for file_name in hashes:
				hash_file.write(file_name+"\t"+hashes[file_name]+"\n")
			hash_file.close()
			return True,"Added "+str(added_hashes)+" to hash file"
		else:
			return True,"All hashes exist"

	else:
		return False,"No images found to hash"


def createStartTimeFile(path:miqtd.Dir):
	""" Creates a text file with two columns: image-filename and image-datetime"""

	dst_path = path.tosensor()+"intermediate/"+path.event()+"_"+path.sensor()+"_image-start-times.txt"

	img_paths = browseFolderForImages(path.tosensor()+"/raw/")

	if len(img_paths) > 0:

		o = open(dst_path,"w")
		o.write("image-filename\timage-datetime\n")

		for file in img_paths:
			file_name = file.replace(path.tosensor()+"/raw/","")

			tmp = file_name.split("_")
			dt = datetime.datetime.strptime(tmp[5]+"_"+tmp[6].replace(".JPG","")+"+0000",miqtv.date_formats['mariqt_files']+"%z")
			o.write(file_name+"\t"+dt.strftime(miqtv.date_formats['mariqt'])+"\n")

		o.close()
		return True,"Created start time file"
	else:
		return False,"No images found to hash"


def createAcquisitionSettingsEXIFFile(path:miqtd.Dir):

	dst_path = path.tosensor()+"intermediate/"+path.event()+"_"+path.sensor()+"_image-acquisition-settings.txt"

	if os.path.exists(dst_path):
		return True, "Result file exists"

	if not os.path.exists(path.tosensor()+"raw/"):
		return False, print("No source files exists")

	img_paths = browseFolderForImages(path.tosensor()+"/raw/")
	if len(img_paths) > 0:

		o = open(dst_path,"w")
		o.write("image-filename\timage-acquisition-settings\n")
		for file in img_paths:
			file_name = file.replace(path.tosensor()+"/raw/","")
			image = PIL.Image.open(file)

			exif = {}
			for k, v in image._getexif().items():
				if k in PIL.ExifTags.TAGS:
					if not isinstance(v,bytes):
						exif[PIL.ExifTags.TAGS.get(k)] = v
			o.write(file_name+"\t"+str(exif)+"\n")
		return True,"Created acquisition settings file"
	else:
		return False, "No images found"

def allImageNamesValidIn(path:miqtd.Dir,sub:str = "raw"):
	""" Validates that all image file names are valid in the given folder."""

	img_paths = browseFolderForImages(path.tosensor()+"/"+sub+"/")
	for file in img_paths:
		file_name = file.replace(path.tosensor()+"/"+sub+"/","")
		if not miqtt.isValidImageName(file_name):
			return False,"Invalid file name: "+file_name
	return True,"All filenames valid"


def computeImageScaling(area_file:str, data_path:str, dst_file:str, img_col:str = "Image number/name", area_col:str = "Image area", area_factor_to_one_square_meter:float = 1.0):
	""" Turns an ASCII file with image->area information into an ASCII file with image->scaling information

	Path to the source file is given, path to the result file can be given or is constructed from the convention
	"""

	import math
	from PIL import Image
	import mariqt.files as miqtf


	miqtc.assertExists(area_file)

	area_data = miqtf.tabFileData(area_file,[img_col,area_col],key_col = img_col,graceful=True)

	o = open(dst_file,"w")
	o.write("image-filename\timage-pixel-per-millimeter\n")

	for img in area_data:

		with Image.open(data_path + img) as im:
			w,h = im.size

			scaling = math.sqrt(w*h / (float(area_data[img][area_col]) * area_factor_to_one_square_meter * 1000000))
			o.write(img + "\t" + str(scaling) + "\n")
