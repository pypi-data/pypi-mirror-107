import os
import sys
import uuid
import hashlib
import zipfile

def assertExists(path):
	""" Asserts that a file/folder exists and otherwise terminates the program"""
	if not os.path.exists(path):
		raise NameError("Could not find: " + path)


def assertSlash(path):
	""" Asserts that a path string to a directory ends with a slash"""
	if not os.path.isdir(path):
		return path
	elif not path[-1] == "/":
		return path + "/"
	else:
		return path


def humanReadable(val):
	""" Turns a number > 0 (int/float) into a shorter, human-readable string with a size character (k,M,G,...)"""

	sign = 1
	if val < 0:
		sign = -1
		val *= -1

	if val < 1:
		suffixes = ['m','µ','n','p','a','f']
		idx = -1
		while val < 0.001:
			val *= 1000
			idx += 1
		if idx >= 0:
			return str(sign*round(val))+suffixes[idx]
		else:
			return str(sign*val)
	else:
		suffixes=['k','M','G','T','P','E']
		idx = -1
		while val > 1000:
			val /= 1000
			idx += 1
		if idx >= 0:
			return str(sign*round(val))+suffixes[idx]
		else:
			return str(sign*val)

def uuid4():
	""" Returns a random UUID (i.e. a UUID version 4)"""
	return uuid.uuid4()


def sha256HashFile(path):
	""" Returns the SHA256 hash of the file at path"""
	sha256_hash = hashlib.sha256()
	with open(path,"rb") as f:
		for byte_block in iter(lambda: f.read(4096),b""):
			sha256_hash.update(byte_block)
		return sha256_hash.hexdigest()

def md5HashFile(path):
	""" Returns the MD5 hash of the file at path"""
	md5_hash = hashlib.md5()
	with open(path, "rb") as f:
		for byte_block in iter(lambda: f.read(4096), b""):
			md5_hash.update(byte_block)
	return md5_hash.hexdigest()


def rgb2hex(r,g,b):
	return '#{:02x}{:02x}{:02x}'.format(r, g, b)
