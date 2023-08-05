import requests

class Instance:

	endpoint = "https://www.labymod.net/api/change"
	endpoint_visibility = "https://www.labymod.net/api/change"

	def __init__(self,cookie):
		self.cookies = dict(LABY_SESSION_ID = cookie)

		self.headers = {
			"accept": "*/*",
			"accept-encoding": "gzip, deflate, br",
			"accept-language": "en-US,en;q=0.9,sv;q=0.8",
			"cache-control": "no-cache",
			"dnt": "1",
			"user-agent": "Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0",
			"origin": "https://www.labymod.net",
			"pragma": "no-cache",
			"referer": "https://www.labymod.net/dashboard",
			"sec-fetch-dest": "empty",
			"sec-fetch-mode": "cors",
			"sec-fetch-site": "same-origin",
			"x-requested-with": "XMLHttpRequest",
			"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
		}

		self.body = ""

		# Payload
		self.addEncodedFormData("item", 700508)
		self.addEncodedFormData("site","control")

	# -----------------------------------

	# Add URLEncoded form data (x-www-form-urlencoded)
	def addEncodedFormData(self,key,value):
		body = "&"

		# Remove '&' delimiter for first item
		if(self.body == ""):
			body = ""

		body += f"{key}={value}"

		self.body += body

	# -----------------------------------

	def update(self,value):
		self.addEncodedFormData("type", "multi")
		self.addEncodedFormData("value",value)

		request = requests.post(Instance.endpoint,
			headers = self.headers,
			cookies = self.cookies,
			data = self.body
		)

		# Raise exception if request fails
		request.raise_for_status()


	def update_visibility(self, value):
		if (type(value) != int):
			if (value == "show"):
				value = 1
			else:
				value = 0

		self.addEncodedFormData("type", "switch")
		self.addEncodedFormData("value", value)

		request = requests.post(Instance.endpoint_visibility,
								headers=self.headers,
								cookies=self.cookies,
								data=self.body
								)

		request.raise_for_status()