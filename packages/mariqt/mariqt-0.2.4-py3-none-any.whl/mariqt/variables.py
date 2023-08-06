""" A dictionary holding various header field names to store 4.5D navigation information in the form of: t (utc time), x (longitude), y (latitude), z (depth: below sea level), a (altitude: above seafloor)"""

version = '0.9.0'

pos_header = {
		# Field/column name definition for internally handling this kind of t,y,x,z,h position data
		"mariqt":{
			'utc':'utc',	# YYYY-MM-DD HH:ii:ss.sssss+0000 (UTC!!!) -> t-axis
			'lat':'lat',	# Decimal degrees, WGS84 / EPSG4362 -> y-axis
			'lon':'lon',	# Decimal degrees, WGS84 / EPSG4326 -> x-axis
			'dep':'dep',	# Depth of the signal, sample, platform, ... *in the water* -> z-axis, positive when submerged, negative when in air
			'hgt':'hgt'		# Height above the seafloor -> relative measure!
		},

		# Definition of field/column names according to the iFDO specification:
		# https://gitlab.hzdr.de/datahub/marehub/ag-videosimages/metadata-profiles-fdos/-/blob/master/MareHub_AGVI_iFDO.md
		"ifdo":{'utc':'image-datetime','lat':'image-latitude','lon':'image-longitude','dep':'image-depth','hgt':'image-meters-above-ground'},

		# Definition of field/column names according to the "Acquisition, Curation and Management Workflow"
		# for marine image data https://www.nature.com/articles/sdata2018181
		"acmw":{'utc':'SUB_datetime','lat':'SUB_latitude','lon':'SUB_longitude','dep':'SUB_depth','hgt':'SUB_distance'},

		# Definition of field/colum names as they occur in a DSHIP export file

		# for RV Sonne posidonia beacons
		"SO_NAV-2_USBL_Posidonia":{1:{'utc':'date time','lat':'USBL.PTSAG.1.Latitude','lon':'USBL.PTSAG.1.Longitude','dep':'USBL.PTSAG.1.Depth'},
									2:{'utc':'date time','lat':'USBL.PTSAG.2.Latitude','lon':'USBL.PTSAG.2.Longitude','dep':'USBL.PTSAG.2.Depth'},
									4:{'utc':'date time','lat':'USBL.PTSAG.4.Latitude','lon':'USBL.PTSAG.4.Longitude','dep':'USBL.PTSAG.4.Depth'},
									5:{'utc':'date time','lat':'USBL.PTSAG.5.Latitude','lon':'USBL.PTSAG.5.Longitude','dep':'USBL.PTSAG.5.Depth'}},

		# for RV Sonne itself (GPS)
		"SO_NAV-1_GPS_Saab":{'utc':'date time','lat':'SYS.STR.PosLat','lon':'SYS.STR.PosLon'},


		# for RV Maria S Merian sonardyne beacons
		"MSM_NAV-2_USBL_Sonardyne":{2104:{'utc':'date time','lat':'Ranger2.PSONLLD.2104.position_latitude','lon':'Ranger2.PSONLLD.2104.position_longitude','dep':'Ranger2.PSONLLD.2104.depth'},
									2105:{'utc':'date time','lat':'Ranger2.PSONLLD.2105.position_latitude','lon':'Ranger2.PSONLLD.2105.position_longitude','dep':'Ranger2.PSONLLD.2105.depth'}},

		# for RV Maria S Metian itself (GPS)
		"MSM_NAV-1_GPS_Debeg4100":{'utc':'date time','lat':'SYS.STR.PosLat','lon':'SYS.STR.PosLon'},

		# Definition of field/column names according to the DSM Workbench
		"workbench": {},

		# Definition of field/column names required for assigning EXIF infos to a JPG file
		"exif":{'utc':'CreateDate','lat':'GPSLatitude','lon':'GPSLongitude','dep':'GPSAltitude','hgt':'GPSDestDistance'},

		# Definition of field/column names according to the AWI O2A GeoCSV standard
		# https://confluence.digitalearth-hgf.de/display/DM/O2A+GeoCSV+Format
		# Warning: GeoCSVs need an additional WKT column: geometry [point] with values like: POINT(latitude longitude)
		# Warning: depth and altitude are guessed as i could not find it in the documentation
		"o2a":{'utc':'datetime','lat':'latitude [deg]','lon':'longitude [deg]','dep':'depth [m]','hgt':'altitude [m]'},

		# Definition of field/column names according to the OFOP software
		# Warning: OFOP requires two separate columns for date and time
		# Warning: Depth can also be in column SUB1_USBL_Depth
		# ---- USBL depth kommt vom USBL System, nur depth von einem (online/logging) Drucksensor, manchmal gibt es nur USBL.
		# Warning: It does not have to be SUB1 it can also be SUB2, SUB3, ...
		"ofop":{'utc':'Date\tTime','lat':'SUB1_Lat','lon':'SUB1_Lon','dep':'SUB1_Depth','hgt':'SUB1_Altitude'},

		# Definition of field/column names according to the world data center PANGAEA
		"pangaea":{
				'utc':'DATE/TIME',								# (1599)
				'lat':'LATITUDE',								# (1600)
				'lon':'LONGITUDE',								# (1601)
				'dep':'DEPTH, water [m]',						# (1619)
				'hgt':'Height above sea floor/altitude [m]'		# (27313)
				},

		# Definition of field/column names according to the annotation software BIIGLE
		"biigle":{'utc':'taken_at','lat':'lat','lon':'lng','dep':'gps_altitude','hgt':'distance_to_ground'}

}

navigation_equipment = {
	'SO':{'satellite':'SO_NAV-1_GPS_Saab','underwater':'SO_NAV-2_USBL_Posidonia'},
	'MSM':{'satellite':'','underwater':''}
}

date_formats = {"pangaea":"%Y-%m-%dT%H:%M:%S",
				"mariqt":"%Y-%m-%d %H:%M:%S.%f",
				"mariqt_files":"%Y%m%d_%H%M%S",
				"mariqt_short":"%Y-%m-%d %H:%M:%S",
				"gx_track":"%Y-%m-%dT%H:%M:%SZ",
				"dship":"%Y/%m/%d %H:%M:%S"}

col_header = {'pangaea':{'annotation_label':'Annotation label'},
			'mariqt':{'uuid':'image-uuid',
						'img':'image-filename',
						'utc':'image-datetime',
						'lat':'image-latitude',
						'lon':'image-longitude',
						'dep':'image-depth',
						'hgt':'image-meters-above-ground',
						'hash':'image-hash'},
			'exif':{'img':'SourceFile',
					'uuid':'imageuniqueid'}}

photo_types = ['jpg','png','bmp','raw','jpeg']
video_types = ['mp4','mov','avi']
image_types = photo_types + video_types

equipment_types = ['CAM','HYA','ENV','NAV','SAM','PFM']

colors = ['#94B242','#24589B','#DCB734','#E7753B','#A0BAAC','#CAD9A0','#82C9EB','#E9DCA6','#ED9A72','#D0DDD6','#EFF5E4','#E6F5FB','#F7F1DC','#F9DED2','#E8EEEB']
color_names = {'entity':'#94B242','process':'#24589B','infrastructure':'#DCB734','missing':'#ED9A72','error':'#E7753B','green':'#94B242','light_green':'#EFF5E4','blue':'#24589B','light_blue':'#E6F5FB','yellow':'#DCB734','light_yellow':'#F7F1DC','red':'#E7753B','light_red':'#F9DED2','grey':'#A0BAAC','light_grey':'#E8EEEB','mid_green':'#CAD9A0','mid_blue':'#82C9EB','mid_yellow':'#E9DCA6','mid_red':'#ED9A72','mid_grey':'#D0DDD6','dark_grey':'#6D7F77',}

ifdo_header_fields = {
	'image-set-name':{'comment':'A unique name for the image set','alt-fields':[]},
	'image-set-project':{'comment':'Project','alt-fields':['image-project']},
	'image-set-context':{'comment':'Expedition or cruise or experiment or ...','alt-fields':['image-context']},
	'image-set-abstract':{'comment':'500 - 2000 characters describing what, when, where, why and how the data was collected.','alt-fields':['']},
	'image-set-event':{'comment':'One event of a project or expedition or cruise or experiment or ...','alt-fields':['image-event']},
	'image-set-platform':{'comment':'Sensors URN or Equipment Git ID (Handle)','alt-fields':['image-platform']},
	'image-set-sensor':{'comment':'Sensors URN or Equipment Git ID (Handle)','alt-fields':['image-sensor']},
	'image-set-uuid':{'comment':'A UUID (version 4 - random) for the entire image set','alt-fields':['']},
	'image-set-handle':{'comment':'A Handle (using the UUID?) to point to the landing page of the data set','alt-fields':['']},
	'image-set-data-handle':{'comment':'A Handle (using the UUID?) to point from the metadata to the data','alt-fields':['']},
	'image-set-metadata-handle':{'comment':'A Handle (using the UUID?) to point to this metadata record','alt-fields':['']},
	'image-set-creators':{'comment':'Orcids (or Name, E-Mail)','alt-fields':['image-creators']},
	'image-set-pi':{'comment':'Orcid (or Name & E-Mail) of principal investigator','alt-fields':['image-pi']},
	'image-set-license':{'comment':'License to use the data (should be FAIR!)','alt-fields':['image-license']},
	'image-set-copyright':{'comment':'Copyright sentence / contact person or office','alt-fields':['image-copyright']},
	'image-set-crs':{'comment':'The coordinate reference system','alt-fields':['image-crs']},
	'image-set-coordinate-uncertainty':{'comment':'Average/static uncertainty of coordinates in this dataset, given in meters','alt-fields':['image-coordinate-uncertainty']},
	'image-set-longitude':{'comment':'Decimal degrees: D.DDDDDDD','alt-fields':['image-longitude']},
	'image-set-latitude':{'comment':'Decimal degrees: D.DDDDDDD','alt-fields':['image-latitude']},
	'image-set-depth':{'comment':'Use when camera below water, then it has positive values','alt-fields':['image-set-altitude','image-depth','image-altitude']},
	'image-set-altitude':{'comment':'Use wenn camera above water, then it has positive values','alt-fields':['image-set-depth','image-altitude','image-depth']}
}

ifdo_item_fields = {
	'image-uuid':{'comment':'UUID (version 4 - random) for the image file (still or moving)','alt-fields':[]},
	'image-filename':{'comment':'A filename string to identify the image data on disk (no absolute path!)','alt-fields':[]},
	'image-hash':{'comment':'A hash to represent the whole file (including UUID in metadata!) to verify integrity on disk','alt-fields':[]},
	'image-datetime':{'comment':'UTC: YYYY-MM-DD HH:MM:SS.SSSSS','alt-fields':[]},
	'image-longitude':{'comment':'Decimal degrees: D.DDDDDDD','alt-fields':['image-set-longitude']},
	'image-latitude':{'comment':'Decimal degrees: D.DDDDDDD','alt-fields':['image-set-latitude']},
	'image-depth':{'comment':'Use when camera below water, then it has positive values','alt-fields':['image-altitude','image-set-depth','image-set-altitude']},
	'image-altitude':{'comment':'Use wenn camera above water, then it has positive values','alt-fields':['image-depth','image-set-altitude','image-set-depth']},
	'image-coordinate-uncertainty':{'comment':'Optional, only needed when no static value is given for the image-set','alt-fields':['image-set-coordinate-uncertainty']}
}

ifdo_content_fields = {
	'image-set-sequence-image':{'comment':'2D image with the pixel dimension of <number of images / frames> x <height of one image / frame> containing one column of each image /frame in the image set, stacked along the horizontal of the sequence image according to the acquisition time. Handle URL to an image'},
	'image-entropy':{'comment':'1D time series constructed of single entropy values for each image / frame <image filename 1>: <entropy 1>\n<image filename 2>: <entropy 2\n...>'},
	'image-particle-count':{'comment':'1D time series constructed of single particle/object count values for each image / frame <image filename 1>: <particle count 1>\n<image filename 2>: <particle count 2\n...>'},
	'image-average-color':{'comment':'Set of n 1D time series constructed of the average colour for each image / frame and the n channels of an image (e.g. 3 for RGB) <image filename 1>:\n\t<channel 0>: <value>\n\t<channel 1>: <value>\n<image filename 2>:\n\t<channel 0>: <value>\n...>'},
	'image-mpeg7-colorlayout':{'comment':'An nD feature vector per image / frame of varying dimensionality according to the chosen descriptor settings.'},
	'image-mpeg7-colorstatistic':{'comment':'An nD feature vector per image / frame of varying dimensionality according to the chosen descriptor settings.'},
	'image-mpeg7-colorstructure':{'comment':'An nD feature vector per image / frame of varying dimensionality according to the chosen descriptor settings.'},
	'image-mpeg7-dominantcolor':{'comment':'An nD feature vector per image / frame of varying dimensionality according to the chosen descriptor settings.'},
	'image-mpeg7-edgehistogram':{'comment':'An nD feature vector per image / frame of varying dimensionality according to the chosen descriptor settings.'},
	'image-mpeg7-homogeneoustexture':{'comment':'An nD feature vector per image / frame of varying dimensionality according to the chosen descriptor settings.'},
	'image-mpeg7-scalablecolor':{'comment':'An nD feature vector per image / frame of varying dimensionality according to the chosen descriptor settings.'}
}

ifdo_capture_fields = {
	'image-set-acquisition':{'comment':'photo: still images, video: moving images, scan: microscopy / slide scans','valid':['photo','video','scan','slide']},
	'image-set-quality':{'comment':'raw: straight from the sensor, processed: QA/QCd, product: image data ready for interpretation','valid':['raw', 'processed', 'product']},
	'image-set-deployment':{'comment':'mapping: planned path execution along 2-3 spatial axes, stationary: fixed spatial position, survey: planned path execution along free path, exploration: unplanned path execution, experiment: observation of manipulated environment, sampling: ex-situ imaging of samples taken by other method','valid':['mapping', 'stationary', 'survey', 'exploration', 'experiment', 'sampling']},
	'image-set-navigation':{'comment':'satellite: GPS/Galileo etc., beacon: USBL etc., transponder: LBL etc., reconstructed: position estimated from other measures like cable length and course over ground','valid':['satellite', 'beacon', 'transponder', 'reconstructed']},
	'image-set-scale-reference':{'comment':'3D camera: the imaging system provides scale directly, calibrated camera: image data and additional external data like object distance provide scale together, laser marker: scale information is embedded in the visual data, optical flow: scale is computed from the relative movement of the images and the camera navigation data','valid':['3D camera', 'calibrated camera', 'laser marker', 'optical flow']},
	'image-set-illumination':{'comment':'sun: the scene is only illuminated by the sun, artificial: the scene is only illuminated by artificial light, mixed light: both sunlight and artificial light illuminate the scene','valid':['sun', 'artificial', 'mixed']},
	'image-set-resolution':{'comment':'average size of one pixel of an image','valid':['km', 'hm', 'dam', 'm', 'cm', 'mm', 'µm']},
	'image-set-marine-zone':{'comment':'seafloor: images taken in/on/right above the seafloor, watercolumn: images taken in the free water without the seafloor or the sea surface in sight, seasurface: images taken right below the sea surface, atmosphere: images taken outside of the water, laboratory: images taken ex-situ','valid':['seafloor', 'watercolumn', 'seasurface', 'atmosphere', 'laboratory']},
	'image-set-spectral-resolution':{'comment':'grayscale: single channel imagery, rgb: three channel imagery, multi-spectral: 4-10 channel imagery, hyper-spectral: 10+ channel imagery','valid':['grayscale', 'rgb', 'multi-spectral', 'hyper-spectral']},
	'image-set-capture-mode':{'comment':'whether the time points of image capture were systematic, human-triggered or both','valid':['timer','manual','mixed']},
	'image-area':{'comment':'The footprint of the entire image in square meters'},
	'image-pixel-per-millimeter':{'comment':'Resolution of the imagery in pixels / millimeter which is identical to megapixel / square meter'},
	'image-meters-above-ground':{'comment':'Distance of the camera to the seafloor'},
	'image-set-camera-intrinsics':{'comment':'4x3 K matrix encoding the six intrinsic parameters (f, m_x,m_y,u_o,v_o, gamma): focal length [px], inverse pixel width & height, principal point x/y, skew coefficient.'},
	'image-set-camera-extrinsics':{'comment':'4x4 pose matrix (R,T). See: http://dx.doi.org/10.1201/9781315368597'},
	'image-acquisition-settings':{'comment':'All the information that is recorded by the camera in the EXIF, IPTC etc. As a dict. Includes ISO, aperture, etc.'},
	'image-set-spatial-contraints':{'comment':'A description / definition of the spatial extent of the study area (inside which the photographs were captured), including boundaries and reasons for constraints (e.g. scientific, practical)'},
	'image-set-temporal-constraints':{'comment':'A description / definition of the temporal extent, including boundaries and reasons for constraints (e.g. scientific, practical)'},
	'image-set-target-environment':{'comment':'A description, delineation, and definition of the habitat or environment of study, including boundaries of such'},
	'image-set-objective':{'comment':'A general translation of the aims and objectives of the study, as they pertain to biology and method scope. This should define the primary and secondary data to be measured and to what precision.'},
	'image-set-reference-calibration':{'comment':'Calibration data and information on calibration process'},
	'image-set-time-synchronisation':{'comment':'Synchronisation procedure and determined time offsets between camera recording values and UTC'},
	'image-set-item-identification-scheme':{'comment':'How the images file names are constructed. Should be like this `<project>_<event>_<sensor>_<date>_<time>.<ext>`'},
	'image-set-curation-protocol':{'comment':'A description of the image and metadata curation steps and results'}
}
