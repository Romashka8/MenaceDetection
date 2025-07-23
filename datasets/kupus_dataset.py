# -------------------------------------------------------------------------------------------------------

import os
import pathlib

import json

from datetime import datetime

import numpy as np
import pandas as pd

# -------------------------------------------------------------------------------------------------------

class KupusDataset:

	def __init__(self):

		updir = pathlib.PurePath(__file__).parent.parent

		self.headers = []
		self.headers_shape = (0, 0)
		self.headers_link = os.path.join(updir, "data/kupus_headers.json")

		self.comments = []
		self.comments_shape = (0, 0)
		self.comments_link = os.path.join(updir, "data/kupus_comments")

		self.flud_map = None
		
		with open(os.path.join(updir, "parser/config/kupus.json"), "r") as file:
			self.config = dict(json.loads(file.read()))

	def get_headers(self):

		with open(self.headers_link, "r") as file:
			headers = dict(json.loads(file.read()))

		for topic in headers:
			for flud in headers[topic]:
				data = headers[topic][flud]
				self.headers.append([
					self.config["header_map"][topic], topic,
					flud, data[0],
					datetime.strptime(data[1], "%Y-%m-%dT%H:%M:%SZ"), datetime.strptime(data[2], "%Y-%m-%dT%H:%M:%SZ")
				])

		self.headers_shape = (len(self.headers), len(self.headers[0]))

		return pd.DataFrame(self.headers,
							columns=["topic name", "topic link", "flud name", "flud link", "start date", "latest update"]
						)
	
	def __form_flud_map(self):

		if len(self.headers) > 0:

			self.flud_map = {}

			for row in self.headers:
				self.flud_map[row[3]] = row[2]

		else:

			self.get_headers()
			self.__form_flud_map()

	def get_comments(self):

		self.__form_flud_map()

		for batch in pathlib.Path(self.comments_link).iterdir():
			if batch.is_file():
			
				with open(batch, "r") as file:
					comments = dict(json.loads(file.read()))

				topic = list(comments.keys())[0]

				for comment in comments[topic]:
					flud_link = comment[0]
					
					for msg in comment[1]:

						self.comments.append([
							self.config["header_map"][topic], topic,
							self.flud_map[flud_link], flud_link,
							msg[0].strip(), datetime.strptime(msg[1], "%Y-%m-%dT%H:%M:%SZ")
						])

		self.comments_shape = (len(self.comments), len(self.comments[0]))

		return pd.DataFrame(self.comments,
							columns=["topic name", "topic link", "flud name", "flud link", "message", "publish date"]
						)

# -------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

	dataset = KupusDataset()
	SAVE_DIR = pathlib.PurePath(__file__).parent.parent

	dataset.get_headers().to_excel(os.path.join(SAVE_DIR, "data/kupus_headers.xlsx"), index=False)
	dataset.get_comments().to_excel(os.path.join(SAVE_DIR, "data/kupus_comments.xlsx"), index=False)

# -------------------------------------------------------------------------------------------------------
