import requests
from .http import Http

class Util:
	async def __getToken(self):
		auth_response = requests.post("https://auth.roblox.com/v1/logout", headers = {"cookie": f".ROBLOSECURITY={self.cookie}"})
		self.token = None

		if auth_response.status_code == 403:
			if "x-csrf-token" in auth_response.headers:
				self.token = auth_response.headers["x-csrf-token"]
				return True
			else:
				return False
		else:
			return False

	async def login(self, cookie):
		self.cookie = cookie
		r = self.__getToken()

		if r:
			print("Logged in!")
		else:
			print("Failure to login!")