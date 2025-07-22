# -------------------------------------------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup

from typing import List

import re

import tqdm

import logging

# -------------------------------------------------------------------------------------------------------

class OnlineParser:

	def __init__(self, config):
		
		self.config = config

	def parse_html(self, url):

		page = requests.get(url)
		soup = BeautifulSoup(page.content, "html.parser")

		return soup

	def parse_headers(self, url, deep=1):

		pass

	def parse_comments(self, url, deep=1):

		pass

# -------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

	pass

# -------------------------------------------------------------------------------------------------------
