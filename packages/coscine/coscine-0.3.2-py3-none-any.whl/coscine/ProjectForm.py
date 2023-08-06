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

from collections.abc import MutableMapping
from .exceptions import *
from .FormFlags import FormFlags

###############################################################################

KEYS = [
	{
		"name": {
			"de": "Projektname",
			"en": "Project Name"
		},
		"flags": FormFlags.REQUIRED,
		"field": "ProjectName"
	},
	{
		"name": {
			"de": "Anzeigename",
			"en": "Display Name"
		},
		"flags": FormFlags.REQUIRED,
		"field": "DisplayName"
	},
	{
		"name": {
			"de": "Projektbeschreibung",
			"en": "Project Description"
		},
		"flags": FormFlags.REQUIRED,
		"field": "Description"
	},
	{
		"name": {
			"de": "Principal Investigators",
			"en": "Principal Investigators"
		},
		"flags": FormFlags.REQUIRED,
		"field": "PrincipleInvestigators"
	},
	{
		"name": {
			"de": "Projektstart",
			"en": "Project Start"
		},
		"flags": FormFlags.REQUIRED,
		"field": "StartDate"
	},
	{
		"name": {
			"de": "Projektende",
			"en": "Project End"
		},
		"flags": FormFlags.REQUIRED,
		"field": "EndDate"
	},
	{
		"name": {
			"de": "Disziplin",
			"en": "Discipline"
		},
		"flags": FormFlags.REQUIRED | FormFlags.CONTROLLED,
		"field": "Discipline"
	},
	{
		"name": {
			"de": "Teilnehmende Organisation",
			"en": "Participating Organizations"
		},
		"flags": FormFlags.CONTROLLED,
		"field": "Organization"
	},
	{
		"name": {
			"de": "Projektschlagwörter",
			"en": "Project Keywords"
		},
		"flags": FormFlags.NONE,
		"field": "Keywords"
	},
	{
		"name": {
			"de": "Sichtbarkeit",
			"en": "Visibility"
		},
		"flags": FormFlags.REQUIRED | FormFlags.CONTROLLED,
		"field": "Visibility"
	},
	{
		"name": {
			"de": "Grant ID",
			"en": "Grant ID"
		},
		"flags": FormFlags.NONE,
		"field": "GrantId"
	},
	{
		"name": {
			"de": "Features",
			"en": "Features"
		},
		"flags": FormFlags.CONTROLLED,
		"field": "Features"
	}
]

###############################################################################

class ProjectForm(MutableMapping):

	"""
	Coscine Input Form for creating and editing projects
	"""

###############################################################################

	def __init__(self, handle, parent = None, data = None):
		self.store = {}
		self._keys = {}
		self.handle = handle
		disciplines = handle.get_disciplines()
		organizations = handle.get_organizations()
		visibility = handle.get_visibility()
		features = handle.get_features()
		self.vocabulary = {
			"Discipline": disciplines,
			"Organization": organizations,
			"Visibility": visibility,
			"Features": features
		}
		self.parent = parent
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

		if self._keys[key]["flags"] & FormFlags.REQUIRED:
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

		if self._keys[key]["flags"] & FormFlags.CONTROLLED:
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
			"    Coscine Project Form\n" \
			"_______________________________\n\n" \
			" [R: Required] [C: Controlled]\n" \
			"-------------------------------\n" \
			+ "\n".join(entries) + \
			"\n_______________________________\n"
		return format

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
		for key in KEYS:
			self._keys[key["name"][self.handle.lang]] = key
			if key["flags"] & FormFlags.CONTROLLED:
				key["vocabulary"] = self.vocabulary[key["field"]]

###############################################################################

	def generate(self):

		"""
		Generates JSON-LD formatted representation of project data

		Raises
		-------
		RequirementError
			When one or more required fields have not been set
		
		Returns
		--------
		JSON-LD formatted project data
		"""

		data = {}
		missing = []
		for key in self._keys:
			value = self._keys[key]
			if key not in self.store:
				if self.is_required(key):
					missing.append(key)
			else:
				data[value["field"]] = self.store[key]

		if missing:
			raise RequirementError(missing)

		if self.parent:
			data["ParentId"] = self.parent["id"]

		return data

###############################################################################