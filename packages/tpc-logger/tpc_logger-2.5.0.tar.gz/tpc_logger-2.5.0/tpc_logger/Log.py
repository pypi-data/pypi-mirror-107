#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""log.py: Create a logger. On the console print INFO level logs
		   Also create a log file with DEBUG level logs
			"""

__author__ = "Jerome DELMAR"

import logging
from colorama import Fore, Back
from colorama import init as color_init
from logging.handlers import RotatingFileHandler

import inspect

class Log:

	def __init__(self):

		color_init(autoreset=True)
		# création de l'objet logger qui va nous servir à écrire dans les logs
		self.logger = logging.getLogger()
		# on met le niveau du logger à DEBUG, comme ça il écrit tout
		self.logger.setLevel(logging.DEBUG)

		# création d'un formateur qui va ajouter le temps, le niveau
		# de chaque message quand on écrira un message dans le log
		formatter = logging.Formatter(
			'%(asctime)s || %(levelname)s || %(message)s')
		# création d'un handler qui va rediriger une écriture du log vers
		# un fichier en mode 'append', avec 1 backup et une taille max de 10Mo
		self.file_handler = RotatingFileHandler('activity.log', 'a', 10000000, 1)
		# on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
		# créé précédement et on ajoute ce handler au logger
		self.file_handler.setLevel(logging.DEBUG)
		self.file_handler.setFormatter(formatter)
		self.logger.addHandler(self.file_handler)

		# création d'un second handler qui va rediriger chaque écriture de log
		# sur la console
		self.stream_handler = logging.StreamHandler()
		self.stream_handler.setLevel(logging.INFO)
		formatter_stream = logging.Formatter(
			'%(asctime)s || %(levelname)s || %(message)s')
		self.stream_handler.setFormatter(formatter_stream)
		self.logger.addHandler(self.stream_handler)


	def __give_details(self):
		"""
			Return the filename , the line number and the function name of the function which call the logger
		"""

		frame,filename,line_number,function_name,lines,index = inspect.stack()[2]## [2] --> Mean the parent function 

		try:
			filename = filename.split("/")
			filename = filename[-1]
		except:
			pass

		try:
			filename = filename.split("\\")
			filename = filename[-1]
		except:
			pass

		return " || ["+str(filename)+":"+str(line_number)+" "+str(function_name)+"() ] "


	def parse_args(self, *args):
		final_var = ""
		try:
			for arg in args:

				parse_arg = ""
				parse_arg = str(arg)
				parse_arg = parse_arg.encode('utf8').decode('utf-8')
				final_var = final_var + parse_arg
			return final_var

		except Exception as e:
			self.logger.error(
				"TPC logger modules: impossible to convert variable and log them : " + str(e))


	def info(self, *args):
		new_format = logging.Formatter('%(asctime)s ||' + Fore.CYAN + ' %(levelname)s ' + Fore.RESET + '|| %(message)s')
		self.logger.handlers[1].setFormatter(new_format)
		to_log = self.parse_args(*args, self.__give_details())
		self.logger.info(to_log)


	def error(self, *args):
		new_format = logging.Formatter('%(asctime)s ||' + Fore.RED + ' %(levelname)s ' + Fore.RESET + '|| %(message)s')
		self.logger.handlers[1].setFormatter(new_format)
		to_log = self.parse_args(*args, self.__give_details())
		self.logger.error(to_log)


	def debug(self, *args):
		new_format = logging.Formatter('%(asctime)s ||' + Fore.GREEN + ' %(levelname)s ' + Fore.RESET + '|| %(message)s')
		self.logger.handlers[1].setFormatter(new_format)
		to_log = self.parse_args(*args, self.__give_details())
		self.logger.debug(to_log)


	def warning(self, *args):
		new_format = logging.Formatter('%(asctime)s ||' + Fore.YELLOW + ' %(levelname)s ' + Fore.RESET + '|| %(message)s')
		self.logger.handlers[1].setFormatter(new_format)
		to_log = self.parse_args(*args, self.__give_details())
		self.logger.warning(to_log)


	def critical(self, *args):
		new_format = logging.Formatter('%(asctime)s ||' + Fore.MAGENTA + Back.WHITE + ' %(levelname)s ' + Fore.RESET + Back.RESET + '|| %(message)s')
		self.logger.handlers[1].setFormatter(new_format)
		to_log = self.parse_args(*args, self.__give_details())
		self.logger.critical(to_log)


	def setLevel(self, level, handler='stream'):
		'''
			Chose which level of log you want to see in your different handlers by sending the minimal level of log and the handler name.
			If the handler is not provided, it will set the level of the terminal by default. Otherwise, you can set handler at 'file' to 
			set the level of your file handler.
		params:
			level (string): The minimum level of log you want to write into your handler.
			handler (string): The handler name who should be set, the stream handler is the defalut value.
		'''

		if handler == 'stream':
			i = 1
		elif handler == 'file':
			i = 0
		else:
			raise ValueError('Handler {0} not supported.'.format(handler))

		if str(level).upper() == "DEBUG":
			self.logger.handlers[i].setLevel(logging.DEBUG)
		if str(level).upper() == "INFO":
			self.logger.handlers[i].setLevel(logging.INFO)
		if str(level).upper() == "WARNING":
			self.logger.handlers[i].setLevel(logging.WARNING)
		if str(level).upper() == "ERROR":
			self.logger.handlers[i].setLevel(logging.ERROR)
		if str(level).upper() == "CRITICAL":
			self.logger.handlers[i].setLevel(logging.CRITICAL)

log = Log()