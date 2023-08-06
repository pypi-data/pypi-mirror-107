import json
from dotmap import DotMap
import base64
import hashlib
import string


def rand_string(seed, length, used=[]):
	matches = True
	while matches:
		output = str(
			base64.urlsafe_b64encode(
				hashlib.md5(str(seed).encode('utf-8')).digest()),
			'utf-8'
		).rstrip(string.punctuation)[0:length-1]
		seed = seed + "1"
		matches = output in used

	return output


def credentials_loader(file):
	with open(file, "r") as fp:
		creds = DotMap(json.load(fp))

	return creds


class Stack:
	"""absolute pile of shite, do not use,
	use python lists instead

	please..."""
	top = 0
	stack = []
	isEmpty = True
	isFull = False

	def __init__(self):
		self.top = 0
		self.stack = []
		self.isEmpty = True
		self.isFull = False

	def add(self, data):
		self.isEmpty = False
		self.top += 1
		self.stack.append(data)

	def pop(self):
		data = self.stack.pop(self.top)
		self.top -= 1
		return data


def write(filepath, list1):
	"""small writing to file algorithm, works well"""
	filepath = str(filepath)
	file = open(filepath, "w")
	for count in range(len(list1)):
		file.write(str(list1[count]))
		if (len(list1) - 1) > count > 0:
			file.write("\n")
	file.close()


def quicksort(data):  # quicksort algorithm. takes list
	if data:
		less, equal, greater = partition(data)
		return quicksort(less) + equal + quicksort(greater)
	return data


def partition(data):
	"""ignore me, subset of quicksort"""
	pivot = data[0]
	less, equal, greater = [], [], []
	for temp in data:
		if temp < pivot:
			less.append(temp)
		elif temp > pivot:
			greater.append(temp)
		else:
			equal.append(temp)
	return less, equal, greater


def import_list(filepath):
	"""imports list from a file,
	takes a filepath, returns a list"""
	txt = open(filepath, "r")
	shuffled = txt.read().splitlines()
	txt.close()
	return shuffled


def sort_from_to_file(infile, outfile, debug=False):  # takes in file, writes sorted list to another file
	"""imports a file to a list,
	sorts it,
	writes to another files"""
	sorted_list = sort_from_file(infile, debug)
	write(outfile, sorted_list)
	if debug:
		print("Written:", len(sorted_list), "words.")


def sort_from_file(infile, debug=False):  # takes in file, returns sorted list
	"""imports a file to list,
	sorts it,
	returns a sorted list"""
	shuffled = import_list(infile)
	sorted_list = quicksort(shuffled)
	if debug:
		print("Sorted:", len(sorted_list), "words.")
	return sorted_list


def binary_search(string, data):
	"""binary search.
	takes search string and list,
	returns location and data from location"""
	sort = quicksort(data)
	lower_value = 0
	upper_value = len(sort)
	found = False
	location = 0
	if string not in data:
		raise ValueError("query item is not in data")
	while not found:
		halfway = ((upper_value - lower_value) // 2) + lower_value
		if string >= sort[halfway]:
			lower_value = halfway
		else:
			upper_value = halfway
		if upper_value == lower_value or upper_value == lower_value + 1:
			location = int(lower_value)
			print(location)
			found = True
	return location, data[location]


def find_mid(list1):
	"""integer division to find "mid" value of list or string"""
	length = len(list1)
	mid = length // 2
	return mid
