import math
import mariqt.core as miqtc

class Position:
	""" A class defining a 4.5D position, encoded by a utc time, latitude, longitude, depth and height. Depth and heigt are optional."""
	def __init__(self,utc:int,lat:float,lon:float,dep:float=0,hgt:float=-1):
		self.lat = lat
		self.lon = lon
		self.utc = utc
		self.dep = dep
		self.hgt = hgt


class Positions:
	""" A class that holds several 4.5D Positions in the form of a dictionary with UNIX timestamps as keys and containing (x,y,z,d,h) tuples. Decorator pattern of a dictionary"""

	def __init__(self,positions={}):
		self.positions = positions
	def setPos(self,p:Position):
		self.positions[p.utc] = p
	def setVals(self,utc:int,lat:float,lon:float,dep:float=0,hgt:float=-1):
		self.positions[utc] = Position(utc,lat,lon,dep,hgt)
	def remUTC(self,utc:int):
		del self.positions[utc]
	def remPos(self,p:Position):
		del self.positions[p.utc]
	def len(self):
		return len(self.positions)
	def __getitem__(self,utc:int):
		return self.positions[utc]
	def __setitem__(self,utc:int,p:Position):
		self.positions[utc] = p
	def keys(self):
		return self.positions.keys()


def distanceLatLon(lat_1,lon_1,lat_2,lon_2):
	""" Computes a distance in meters from two given decimal lat/lon values."""

	lat_1_r = math.radians(lat_1)
	lon_1_r = math.radians(lon_1)
	lat_2_r = math.radians(lat_2)
	lon_2_r = math.radians(lon_2)

	lat_offset = lat_1_r - lat_2_r
	lon_offset = lon_1_r - lon_2_r

	alpha = 2 * math.asin(math.sqrt(math.pow(math.sin(lat_offset / 2), 2) + math.cos(lat_1_r) * math.cos(lat_2_r) * math.pow(math.sin(lon_offset / 2), 2)))
	return alpha * 6371000 # Earth's radius


def distancePositions(p1:Position,p2:Position):
	""" Computes a distance in meters from two given positions"""
	return distanceLatLon(p1.lat,p1.lon,p2.lat,p2.lon)


def getDecDegCoordinate(val):
	""" Asserts that the given value is a decimal degree float value"""
	if isinstance(val, float):
		return val
	else:
		return decmin2decdeg(val)


def decdeg2decmin(val,xy = ""):
	""" Turns a float representation of a coordinate (lat/lon) into a string representation using decimal minutes"""
	if val < 0:
		dec = math.ceil(val)
		if xy == "lat":
			xy = "S"
			dec *= -1
			val *= -1
		elif xy == "lon":
			xy = "W"
			dec *= -1
			val *= -1
	else:
		dec = math.floor(val)
		if xy == "lat":
			xy = "N"
		elif xy == "lon":
			xy = "E"
	min = str(round(60*(val - dec),3))
	add = ""
	for i in range(len(min[min.find(".")+1:]),3):
		add += "0"
	return str(dec)+"°"+min+add+xy


def decmin2decdeg(str):
	""" Converts a decimal degree string ("117° 02.716' W") to a decimal degree float"""
	str = str.strip()
	try:
		return float(str)
	except:
		p1 = str.find(chr(176))# This is an ISO 8859-1 degree symbol: °
		p2 = str.find(chr(39))# This is a single tick: '
		deg = int(str[0:p1].strip())
		min = float(str[p1+1:p2].strip())
		reg = str[p2+1:].strip()

		if reg.lower() == "s" or reg.lower() == "w":
			deg *= -1
			return deg - min/60
		else:
			return deg + min/60
