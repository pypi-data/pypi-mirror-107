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

import colorama

###############################################################################

class CoscineException(Exception):
	def __init__(self, msg=None):
		text = colorama.Fore.RED + "ERROR" + colorama.Fore.YELLOW
		if msg:
			text += ": " + msg
		Exception.__init__(self, text)

###############################################################################

class KeyError(CoscineException):
	def __init__(self, msg=None):
		CoscineException.__init__(self, msg)

###############################################################################

class ValueError(CoscineException):
	def __init__(self, msg=None):
		CoscineException.__init__(self, msg)

###############################################################################

class RequirementError(CoscineException):
	def __init__(self, requirements):
		msg = "Required field missing:\n%s" % "\n".join(requirements)
		CoscineException.__init__(self, msg)

###############################################################################

class VocabularyError(CoscineException):
	def __init__(self, value):
		msg = "Value [%s] not in Vocabulary!" % value
		CoscineException.__init__(self, msg)

###############################################################################

class NotFound(CoscineException):
	def __init__(self, msg=None):
		text = msg + " not found!"
		CoscineException.__init__(self, text)

###############################################################################

class ConnectionError(CoscineException):
	def __init__(self):
		CoscineException.__init__(self, "Unable to reach Coscine!")

###############################################################################

class ServerError(CoscineException):
	def __init__(self):
		CoscineException.__init__(self)