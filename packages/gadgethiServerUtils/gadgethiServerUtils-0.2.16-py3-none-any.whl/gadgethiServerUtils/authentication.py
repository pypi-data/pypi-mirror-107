import datetime
from Cryptodome.Hash import SHA256, HMAC
from base64 import b64decode, b64encode

class GadgethiAuthenticationStandardEncryption():
	# First the header should increase two fields (1) key (2) secret (3) time
	# key and the secret will be given 
	# You need to put key, time, hmac_result in the header file 
	# Please call authentication to get the need information dictionary in the header file
	def __init__(self,key,secret):
		self.key = str(key) 
		self.secret = str(secret)

	def HMAC256_digest(self,secret,string,mode='base64'):
		# we give secret type is string
		if type(secret) != bytes:
			secret = secret.encode()
		h = HMAC.new(secret, digestmod=SHA256)
		if string != bytes:
			string = string.encode()
		h.update(string)
		if mode != 'base64':
			return h.hexdigest()
		else:
			b64 = b64encode(bytes.fromhex(h.hexdigest())).decode()
			return b64

	def HMAC256_encryption(self, time_shift):
		# We standardize Taipei as the standard time
		localtime = int(datetime.datetime.utcnow().timestamp()) + (time_shift*60*60)
		encryption_result = self.HMAC256_digest(self.secret,self.key+str(localtime))
		return encryption_result

	def time_standard(self, time_shift):
		return int(datetime.datetime.utcnow().timestamp()) + (time_shift*60*60)

	def authentication_encryption(self, time_shift=8):
		authentication_dictionary = {}
		authentication_dictionary['Gadgethi-Key'] = self.key
		authentication_dictionary['Hmac256-Result'] = self.HMAC256_encryption(time_shift)
		authentication_dictionary['time'] = str(self.time_standard(time_shift))
		return authentication_dictionary

"""
Performs gadgethi HMAC256 
verification. 
"""
class GadgethiHMAC256Verification():
	"""
	TODO:
		Standardize the time zone issue. Make
		time_helper independent. 
	"""
	def __init__(self, encrypted_message):
		"""
		- Input:
			The encrypted message that you want
		to verified
		"""
		self.encrypted_message = encrypted_message
		self.return_message = 'Verification Passed'

	def HMAC256_digest(self,secret,message,mode='base64'):
		"""
		This is the main HMAC256 digest function
		to encrypt the input message with 
		the secret and turn it to hex digest. 
		(or other modes)
		"""
		if type(secret) != bytes:
			secret = secret.encode()
		h = HMAC.new(secret, digestmod=SHA256)
		if message != bytes:
			message = message.encode()
		h.update(message)
		if mode != 'base64':
			return h.hexdigest()
		else:
			b64 = b64encode(bytes.fromhex(h.hexdigest())).decode()
			return b64

	def accepting_time_range(self, time, time_shift,interval):
		"""
		This is the helper function to check whether the time
		is within the interval. -> this should either use 
		third party function or write it in time_helper. 
		"""
		localtime = int(datetime.datetime.utcnow().timestamp()) + (time_shift*60*60)
		if localtime - interval < int(time) < localtime + interval:
			return True
		else:
			self.return_message = 'time_range error'
			return False

	def hmac256_verification(self, secret, message, mode="base64"):
		"""
		This is the raw hmac256 verification
		function. Returns true if the encrypted message
		equals the message after applying hmac256. 
		"""
		encryption_result = self.HMAC256_digest(secret, message, mode=mode)
		if encryption_result == self.encrypted_message:
			return True
		else:
			self.return_message = 'hmac256_verification error'
			return False

	def gserver_authentication(self, message, time, time_shift=8,interval=30,secret='gadgethi'):
		"""
		This is the verfication function
		for gserver http handler. 
		- Input:
			* message: the message to be verified. 
			* time: the current time
		"""
		if self.hmac256_verification(secret, message) and self.accepting_time_range(time, time_shift, interval):
			return {"indicator":True,"message":self.return_message}
		else:
			return {"indicator":False,"message":self.return_message}

if __name__ == "__main__":
	g = GadgethiAuthenticationStandardEncryption("nanshanddctablet", "gadgethi")
	print(g.HMAC256_digest(g.secret,g.key+"1619644177"))