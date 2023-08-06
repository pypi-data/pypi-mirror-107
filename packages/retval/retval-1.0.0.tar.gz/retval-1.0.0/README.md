# retval

A MIT-licensed Python module for better function return values without exceptions.

## Description

This module provides RetVal, a class which powers up how you handle errors and return values. With RetVal you can:

- Use more specific error codes
- Pull from a small library of common errors
- Provide context information with errors
- Create your own errors quickly -- no more writing custom Exception classes
- Return a variable number of data values from functions

## Status

The module is production stable and in active use.

## Usage

Most usage of RetVal revolves around using the constructor to quickly package error information. 

```python
import json
from retval import RetVal, ErrBadType, ErrEmptyData, ErrExists

# Creating new error constants is super simple
ErrDecryptionFailure = 'decryption failure'

def save(self, path: str) -> RetVal:
	'''Saves the key to a file'''

	if not path:
		# The second argument, which may be omitted, is for context information for the developer.
		# It is not intended to be user-facing.
		return RetVal(ErrEmptyData, 'path may not be empty')
	
	if os.path.exists(path):
		return RetVal(ErrExists, f"{path} exists")

	try:
		fhandle = open(path, 'w')
		json.dump({ 'SecretKey' : self.get_key() }, fhandle, ensure_ascii=False, indent=1)
		fhandle.close()
	
	except Exception as e:
		# This little gem allows you to elegantly handle any exception the same way as any other
		# error
		return RetVal().wrap_exception(e)

	return RetVal()


def decrypt(self, encrypted_data: str) -> RetVal:
	'''Decrypts Base85-encoded encrypted data and returns it as bytes in the 'data' field.'''
	# It is highly recommended to mention returned fields in the docstring.

	if not encrypted_data:
		return RetVal(ErrEmptyData)
	
	if not isinstance(encdata, str):
		return RetVal(ErrBadType)

	secretbox = nacl.secret.SecretBox(self.key.raw_data())
	try:
		decrypted_data = secretbox.decrypt(encrypted_data, encoder=Base85Encoder)
	except:
		return RetVal(ErrDecryptionFailure)
	
	return RetVal().set_value('data', decrypted_data)
```

Unless your code uses a lot of different error messages, for maximum code clarity it is recommended to import the RetVal class and any error codes used directly into your code as demonstrated above. An empty constructor indicates success. Call-chaining is the most efficient way to return a single value using RetVal, as demonstrated in `decrypt()`, and multiple values can be call-chained using `set_values()`.

Because RetVal is intended to be treated as a dictionary with some extra features, using a RetVal returned from a function is very simple.

```python
pubkey = PublicKey(organization_key)
status = pubkey.encrypt(tagstr.encode())
if status.error():
	return status

return status['data']
```

The `encrypt()` function called in the above example is similar to `decrypt()`, taking `bytes` and returning a RetVal containing the encrypted data in the `data` field. Most of the time, dealing with a function which returns a RetVal is just a matter of checking for an error state and returning the entire RetVal object if there is one and accessing the data in the object if there isn't.

## History

This module exists because I was inspired to think about Python error-handling and return values after spending more than a little time learning Go. Go errors are little more than strings, which isn't great, but they are often paired with other return values. If no error is returned, then the other return value is safe to consider as valid. Go also doesn't have very many built-in error codes and are not very well documented. RetVal takes from the good and builds upon it. It integrates pretty easily into existing code and the extra contextual information makes debugging significantly easier. Is it Pythonic? Most likely not. I don't care... it's made error-handling easier for me and I'm sure it will for you, too.

## Building

This is a very simple but useful module. Running `python setup.py install` should be the thing needed.
