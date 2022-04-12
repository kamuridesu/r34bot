from datetime import datetime
import os


class Logger:
	def __init__(self, filename: str) -> None:
		self.filename = filename

	def save(self, content: str) -> bool:
		arg = "w"
		if os.path.isfile(filename):
			arg = "a"
		with open(self.filename, arg) as f:
			f.write(content)

	def info(self, content: str) -> None:
		out = datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " [INFO] " + content
		print(out)
		self.save(out)

	def error(self, content: str) -> None:
		out = datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " [ERROR] " + content
		print(out)
		self.save(out)
