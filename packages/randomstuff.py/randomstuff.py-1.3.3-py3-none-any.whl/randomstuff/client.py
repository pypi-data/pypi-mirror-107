from .errors import *
from .constants import *
from .constants import _warn
from .joke import *
import aiohttp
import requests
import random

class Client:
	"""Represent a client
	
	Parameters
	----------
	key (str): Your API authentication key.
	version (str) (optional): The version number of API. It is 3 by default set it to 2 if you want to use v2.
	suppress_warnings (bool) (optional): If this is set to True, You won't get any console warnings. This does not suppress errors.

	Methods 
	-------

	get_ai_response(message: str, lang: str = 'en', type: str = 'stable'): Get random AI response.
	get_image(type: str = 'any'): Get random image.
	get_joke(type: str = 'any'): Get random joke.
	close(): Closes the session.

	"""
	def __init__(self, key: str, version: str = '3', suppress_warnings: bool = False):
		if not version in VERSIONS:
			raise VersionError("Invalid API version was provided. Use `2` or `3` only.")
			return

		self.version = "v"+version
		self.key = key
		self.suppress_warnings = suppress_warnings
		self.session = requests.Session()
		self.session.headers.update({'x-api-key': self.key})
		
		if self.version == 'v2':
			_warn(self, 'You are using v2 of API which is outdated and will soon be deprecated. To avoid feature issues and unstability issues, Please set `version` to "3" to use latest and supported version.\n')
		elif self.version == 'v4':
			_warn(self, "You are using v4 as your API version which is currently in beta state. You may face issues and errors.")

	def get_ai_response(self,
		message: str,
		lang: str = 'en',
		type: str = 'stable',
		plan: str = '',
		dev_name: str = 'PGamerX',
		bot_name: str = 'RSA',
		unique_id: str = ''
		):
		"""Gets AI response

		Parameters:
			message (str): The message to which response is required
			lang (str) (optional): The language in which response is required. By default this is english.
			type (str) (optional): The type of response. This is by default 'stable' and is recommended
								   to be stable.
			plan (str) (optional): If you have a plan for RandomAPI pass the plan's name in this argument. `randomstuff.constants.PLAN` for list of plans.
			dev_name (str) (optional): The developer name. Used in responses.
			bot_name (str) (optional): The bot's name. Used in responses.
			unique_id (str) (optional): This is used to save your identity in bot. Use a secure and combination of letters and numbers. Use `randomstuff.utils.generate_unique_id()` to generate one easily.

		Returns:
			str: The response.

		Raises:
			randomstuff.AuthError: The API key was invalid.
			randomstuff.PlanError: Invalid Plan
			randomstuff.VersionError: Unsupported or invalid version.
		"""
		if not plan in PLANS:
			raise PlanError(F"Invalid Plan. Choose from {PLANS}")
			return

		if self.version == 'v4':
			raise VersionError("v4 is a beta version with entirely different endpoint and parameters. Please use `Client.get_ai_response_beta()` for v4 until beta is over.")
			return

		if self.version == 'v2' and plan != None:
			raise VersionError(f"{self.version} does not support {plan} plan.")
			return
		
		if self.version == 'v2':
			response = self.session.get(f'{BASE_URL}/ai/response?message={message}&language={lang}&api_key={self.key}')
			return response.json()[0]

		params = {'message': message, 
		'lang': lang, 
		'type': type, 
		'bot_name': bot_name, 
		'dev_name': dev_name,
		'unique_id': unique_id}

		if self.version == 'v3' and plan == None:
			response = self.session.get(f'{BASE_URL}/v3/ai/response', params=params)
			if response.status_code == 401:
				raise AuthError(response.text)
				return
			return response.json()[0]['message']
		
		elif self.version == 'v3' and plan != None:
			response = self.session.get(f'{BASE_URL}/v3/{plan}/ai/response', params=params)
			if response.status_code == 401:
				raise AuthError(response.text)
				return
			return response.json()[0]['message']

		
	def get_ai_response_beta(self,
							message:str,
							uid:str='',
							language:str='en',
							bot:str='RSA',
							master:str='PGamerX',
							server:str='primary'):
		"""Gets AI response from v4 endpoint

		[WARNING] v4 is a beta version with entirely different endpoint and parameters. Consider using v3 for
		general use. Read the wiki for info about parameters of this function.

		Parameters:
			message (str): The message to which response is required
			uid (str) (optional): This is used to save your identity in bot. Use a secure and combination of letters and numbers. Use `randomstuff.utils.generate_unique_id()` to generate one easily.
			language (str) (optional): The language in which response is required. By default this is english.
			bot (str) (optional): The bot's name. Used in responses.
			master (str) (optional): The developer name. Used in responses.
			server (str) (optional): The server from which the response should be obtained. Please see the table below
		
			|-----------|----------------------------------------------------------------|
			|  Server   |                      Description                               |
			|:---------:|:--------------------------------------------------------------:|
			|  primary  |                     The main server.                           |
			|  backup   | Since this is a beta, this is backup server if primary is down.|
			|  unstable | The unstable server, Responses are very unstable in this one.  |
			|-----------|----------------------------------------------------------------|

		"""
		if not self.version == 'v4':
			raise VersionError("Only v4 supports this method.")
			return

		if not server in SERVERS:
			raise ServerError("Invalid type of server provided. Only {SERVERS} are supported")
			return

		if server in ['backup', 'unstable'] and language != 'en':
			raise ServerError(f"{server} does not support languages other then english.")
			return

		params = {'message': message,
				'uid': uid,
				'language': language,
				'bot': bot,
				'master': master,
				'server': server
			}
		response = self.session.get(f'{BASE_URL}/beta/ai', params=params)

		if response.status_code == 401:
			raise AuthError(response.text)
			return

		if response.status_code == 403:
			raise AuthError(response.text)
			return

		return response.json()[0]['message']
		

	def get_image(self, type: str = 'any'):
		"""Gets an image

		Parameters:
			type (str) (optional): The type of image. By default, it is 'any'.

		Returns:
			str: Link of image

		Raises:
			randomstuff.AuthError: The API key was invalid.
		"""
		if type == 'any':
			type = random.choice(IMAGE_TYPES)

		if self.version == 'v2' or self.version == 'v4':
			response = self.session.get(f'{BASE_URL}/image/{type}?api_key={self.key}')

		elif self.version == 'v3' or self.version == 'v4':
			response = self.session.get(f'{BASE_URL}/v3/image/{type}')

		return response.json()[0]

	def get_joke(self, type: str = 'any'):
		"""Gets a joke

		Parameters:
			type (str) (optional): The type of joke. By default, it is 'any'.

		Returns:
			randomstuff.Joke: The `randomstuff.Joke` object for the joke.

		Raises:
			randomstuff.AuthError: The API key was invalid.
		"""

		if self.version == 'v2' or self.version == 'v4':
			response = self.session.get(f'{BASE_URL}/joke/{type}?api_key={self.key}')

		elif self.version == 'v3' or self.version == 'v4':
			response = self.session.get(f'{BASE_URL}/v3/joke/{type}')

		if response.status_code == 401:
			raise AuthError(response.text)

		return Joke(response.json())

	def close(self):
		"""Closes the session"""
		self.session.close()

class AsyncClient:
	"""Represent an async client. This is same as `randomstuff.Client` but is suitable for async programs.
	
	Parameters
	----------
	key (str): Your API authentication key.
	version (str) (optional): The version number of API. It is 3 by default set it to 2 if you want to use v2.
	suppress_warnings (bool) (optional): If this is set to True, You won't get any console warnings. This does not suppress errors.


	Methods 
	-------

	async get_ai_response(message: str, lang: str = 'en', type: str = 'stable'): Get random AI response.
	async get_image(type: str = 'any'): Get random image.
	async get_joke(type: str = 'any'): Get random joke.
	async close(): Closes the session.
	
	"""
	def __init__(self, key: str, version: str = '3', suppress_warnings: bool = False):
		if not version in VERSIONS:
			raise VersionError("Invalid API version was provided. Use `2` or `3` only.")
			return

		self.version = "v"+version
		self.key = key
		self.suppress_warnings = suppress_warnings
		self.session = aiohttp.ClientSession(headers={'x-api-key': self.key})

		if self.version == 'v2':
			_warn(self, 'You are using v2 of API which is outdated and will soon be deprecated. To avoid feature issues and unstability issues, Please set `version` to "3" to use latest and supported version. To stop these warnings, Set `suppress_warnings` to `True`.\n')

		elif self.version == 'v4':
			_warn(self, "You are using v4 as your API version which is currently in beta state. You may face issues and errors.")


	async def get_ai_response(self,
		message: str,
		lang: str = 'en',
		type: str = 'stable',
		plan: str = '',
		bot_name: str = 'RSA',
		dev_name: str = 'PGamerX',
		unique_id: str = ''):
		"""
		This function is a coroutine
		----------------------------

		Gets AI response.
	
		Parameters:
			message (str): The message to which response is required
			lang (str) (optional): The language in which response is required. By default this is english.
			type (str) (optional): The type of response. This is by default 'stable' and is recommended
								   to be stable.
			plan (str) (optional): If you have a plan for RandomAPI pass the plan's name in this argument. `randomstuff.constants.PLAN` for list of plans.
			dev_name (str) (optional): The developer name. Used in responses.
			bot_name (str) (optional): The bot's name. Used in responses.
			unique_id (str) (optional): This is used to save your identity in bot. Use a secure and combination of letters and numbers. Use `randomstuff.utils.generate_unique_id()` to generate one easily.

		Returns:
			str: The response.

		Raises:
			randomstuff.AuthError: The API key was invalid.
		"""
		if not plan in PLANS:
			raise PlanError(f"Invalid Plan. Choose from {PLANS}")
			return

		if self.version == 'v4':
			raise VersionError("v4 is a beta version with entirely different endpoint and parameters. Please use `Client.get_ai_response_beta()` for v4 until beta is over.")
			return

		if self.version == 'v2' and plan != None:
			raise VersionError(f"v2 does not support {plan} plan.")
			return
		
		if self.version == 'v2':
			response = await self.session.get(f'{BASE_URL}/ai/response?message={message}&language={lang}&api_key={self.key}')
			return (await response.json())[0]


		params = {'message': message, 
		'lang': lang, 
		'type': type,
		'bot_name': bot_name,
		'dev_name': dev_name,
		'unique_id': unique_id}

		if self.version == 'v3' and plan == None:			
			response = await self.session.get(f'{BASE_URL}/v3/ai/response', params=params)
			
			if response.status == 401:
				raise AuthError(response.text)
				return
			return (await response.json())[0]['message']

		elif self.version == 'v3' and plan != None:
			response = await self.session.get(f'{BASE_URL}/v3/{plan}/ai/response', params=params)
			
			if response.status == 401:
				raise AuthError(response.text)
				return

			return (await response.json())[0]['message']

	async def get_ai_response_beta(self,
							message:str,
							uid:str='',
							language:str='en',
							bot:str='RSA',
							master:str='PGamerX',
							server:str='primary'):
		"""
		This function is a coroutine
		~~~~~~~~~~~~~~~~~~~~~~~~~~~~

		Gets AI response from v4 endpoint

		[WARNING] v4 is a beta version with entirely different endpoint and parameters. Consider using v3 for
		general use. Read the wiki for info about parameters of this function.

		Parameters:
			message (str): The message to which response is required
			uid (str) (optional): This is used to save your identity in bot. Use a secure and combination of letters and numbers. Use `randomstuff.utils.generate_unique_id()` to generate one easily.
			language (str) (optional): The language in which response is required. By default this is english.
			bot (str) (optional): The bot's name. Used in responses.
			master (str) (optional): The developer name. Used in responses.
			server (str) (optional): The server from which the response should be obtained. Please see the table below
		
			|-----------|----------------------------------------------------------------|
			|  Server   |                      Description                               |
			|:---------:|:--------------------------------------------------------------:|
			|  primary  |                     The main server.                           |
			|  backup   | Since this is a beta, this is backup server if primary is down.|
			|  unstable | The unstable server, Responses are very unstable in this one.  |
			|-----------|----------------------------------------------------------------|

		"""
		if not self.version == 'v4':
			raise VersionError("Only v4 supports this method.")
			return

		if not server in SERVERS:
			raise ServerError("Invalid type of server provided. Only {SERVERS} are supported")
			return

		if server in ['backup', 'unstable'] and language != 'en':
			raise ServerError(f"{server} does not support languages other then english.")
			return


		params = {'message': message,
				'uid': uid,
				'language': language,
				'bot': bot,
				'master': master,
				'server': server
			}
		response = await self.session.get(f'{BASE_URL}/beta/ai', params=params)

		if response.status == 401:
			raise AuthError(response.text)
			return

		if response.status == 403:
			raise AuthError(response.text)
			return

		return (await response.json())[0]['message']



	async def get_image(self, type: str = 'any'):
		"""
		This function is a coroutine
		----------------------------

		Gets an image

		Parameters:
			type (str) (optional): The type of image. By default, it is 'any'.

		Returns:
			str: Link of image

		Raises:
			randomstuff.AuthError: The API key was invalid.
		"""
		if type == 'any':
			type = random.choice(IMAGE_TYPES)

		if self.version == 'v2':
			response = await self.session.get(f'{BASE_URL}/image/{type}?api_key={self.key}')

		elif self.version == 'v3' or self.version == 'v4':
			response = await self.session.get(f'{BASE_URL}/v3/image/{type}')

		if response.status == 401:
			raise AuthError(response.text)

		return (await response.json())[0]

	async def get_joke(self, type: str = 'any'):
		"""
		This function is a coroutine
		----------------------------

		Gets a joke

		Parameters:
			type (str) (optional): The type of joke. By default, it is 'any'.

		Returns:
			randomstuff.Joke: The `randomstuff.Joke` object for the joke.

		Raises:
			randomstuff.AuthError: The API key was invalid.
		"""
		if self.version == 'v2':
			response = await self.session.get(f'{BASE_URL}/joke/{type}?api_key={self.key}')

		elif self.version == 'v3' or self.version == 'v4':
			response = await self.session.get(f'{BASE_URL}/v3/joke/{type}')
		
		if response.text == 401:
			raise AuthError(response.text)

		return Joke(await response.json())

	async def close(self):
		"""
		This function is a coroutine
		----------------------------

		Closes a session

		"""
		await self.session.close()
