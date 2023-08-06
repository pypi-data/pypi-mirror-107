###############################################################################
# Coscine Python3 Client
# Version 0.3.2
# Copyright (c) 2018-2021 RWTH Aachen University
# Contact: coscine@itc.rwth-aachen.de
# Git: https://git.rwth-aachen.de/coscine/docs/public/wiki/-/tree/master/
# Please direct bug reports, feature requests or questions at the URL above
# by opening an issue.
###############################################################################
# This python wrapper implements a client for the Coscine API.
# Coscine is an open source project at RWTH Aachen University for
# the management of research data.
# Visit https://coscine.rwth-aachen.de for more information.
###############################################################################

import os
from collections.abc import MutableMapping
from collections import OrderedDict
from .exceptions import *

###############################################################################

class MetadataForm(MutableMapping):

	"""
	Coscine Metadata Input Form

	Can be used to generate and manipulate json-ld formatted metadata
	"""

###############################################################################

	def __init__(self, handle, project, resource):
		self.store = {}
		self._keys = {}
		self.vocabulary = {}
		self.handle = handle
		self.profile = handle.get_application_profile(resource, parse=True)
		for entry in self.profile["graph"]:
			if "class" in entry:
				uri = entry["class"]
				name = entry["name"][self.handle.lang]
				data = handle.get_instance(project, uri)
				lang = self.handle.lang
				vocabulary = {}
				if lang not in data:
					lang = "en"
				for entry in data[lang]:
					vocabulary[entry["name"]] = entry["value"]
				self.vocabulary[name] = vocabulary
		self.reset()

###############################################################################

	def __getitem__(self, key):
		return self.store[key]

###############################################################################

	def __setitem__(self, key, value):
		if key not in self._keys:
			raise KeyError(key)
		elif self.is_controlled(key):
			vocabulary = self.get_vocabulary(key)
			if type(value) is list:
				self.store[key] = []
				for val in value:
					if val in vocabulary:
						self.store[key].append(vocabulary[val])
					else:
						raise VocabularyError(val)
			else:
				if value in vocabulary:
					self.store[key] = vocabulary[value]
				else:
					raise VocabularyError(value)
		else:
			self.store[key] = value

###############################################################################

	def __delitem__(self, key):
		del self.store[key]

###############################################################################

	def __iter__(self):
		return iter(self.store)

###############################################################################

	def __len__(self):
		return len(self.store)

###############################################################################

	def __repr__(self):
		entries = []
		for key in self._keys:
			R = " "
			C = " "
			value = ""
			if self.is_required(key):
				R = "R"
			if self.is_controlled(key):
				C = "C"
			if key in self.store:
				value = " = %s" % self.store[key]
			text = " [%s%s] %s%s" % (R, C, key, value)
			entries.append(text)

		format = \
			"_______________________________\n\n" \
			"   Coscine Metadata Form\n" \
			"_______________________________\n\n" \
			" [R: Required] [C: Controlled]\n" \
			"-------------------------------\n" \
			+ "\n".join(entries) + \
			"\n_______________________________\n"
		return format

###############################################################################

	def is_required(self, key):

		"""
		Determines wether a key is required

		Parameters
		-----------
		key : str

		Returns
		--------
		bool
		"""

		info = self._keys[key]
		if "minCount" in info and info["minCount"] > 0:
			return True
		else:
			return False

###############################################################################

	def is_controlled(self, key):

		"""
		Determines wether a key is controlled by a vocabulary

		Parameters
		-----------
		key : str

		Returns
		--------
		bool
		"""

		if key in self.vocabulary:
			return True
		else:
			return False

###############################################################################

	def get_vocabulary(self, key):

		"""
		Returns the vocabulary associated with a controlled key

		Parameters
		-----------
		key : str

		Returns
		--------
		dict
		"""

		if self.is_controlled(key):
			return self._keys[key]["vocabulary"]
		else:
			msg = "Key [%s] is not controlled by a vocabulary!" % key
			raise CoscineException(msg)

###############################################################################

	def keys(self):

		"""
		Enumerates the keys of the input form
		"""

		keys = []
		for key in self._keys:
			keys.append(key)
		return keys

###############################################################################

	def reset(self):

		"""
		Resets the input form to default
		"""

		self.store.clear()
		for entry in self.profile["graph"]:
			name = entry["name"][self.handle.lang]
			self._keys[name] = entry

			if self.is_controlled(name):
				self._keys[name]["vocabulary"] = self.vocabulary[name]

		# Sort the keys according to their application profile order
		tuples = sorted(self._keys.items(), key = lambda x: x[1]["order"])
		self._keys = OrderedDict(tuples)

###############################################################################

	def generate(self):

		"""
		Generates JSON-LD formatted metadata representation
		
		Raises
		------
		RequirementError
			When one or more required have not been set

		Returns
		--------
		JSON-LD formatted metadata
		"""

		metadata = {}
		RDFTYPE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"

		# Set application profile type used for the metadata
		metadata[RDFTYPE] = [{
			"type": "uri",
			"value": self.profile["id"]
		}]

		# Collect missing required fields
		missing = []

		# Set metadata fields
		for key in self._keys:
			if key not in self.store:
				if self.is_required(key):
					missing.append(key)
			else:
				field = self._keys[key]
				path = field["path"]
				metadata[path] = [{
					"value": self.store[key],
					"datatype": field["datatype"],
					"type": field["type"]
				}]

		# Check missing field list
		if len(missing) > 0:
			raise RequirementError(missing)

		return metadata

###############################################################################

	def parse(self, data):

		"""
		Parses JSON-LD metadata into a Metadata Input Form
		"""

		for path in data:
			for entry in self.profile["graph"]:
				if path in entry["path"]:
					self.store[entry["name"][self.handle.lang]] = data[path][0]["value"]
					break

###############################################################################