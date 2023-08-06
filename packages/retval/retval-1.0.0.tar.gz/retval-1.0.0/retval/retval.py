'''RetVal is a module for flexible return values and error checking without exceptions'''

# Common error constants

ErrOK = ''
ErrNoError = ''

# Often used to indicate data that is incorrectly formatted, such as a bad e-mail address string
ErrBadData = 'ErrBadData'

ErrBadValue = 'ErrBadValue'
ErrBadType = 'ErrBadType'
ErrBusy = 'ErrBusy'
ErrEmptyData = 'ErrEmptyData' # Sometimes more helpful than ErrBadData or ErrBadValue
ErrExceptionThrown = 'ErrExceptionThrown'
ErrExists = 'ErrExists'
ErrFilesystemError = 'ErrFilesystemError'
ErrInit = 'ErrInit' # Uninitialized object
ErrNotFound = 'ErrNotFound'
ErrOSError = 'ErrOSError'
ErrOutOfRange = 'ErrOutOfRange'
ErrPermissions = 'ErrPermissions'

ErrNetworkError = 'ErrNetworkError'
ErrServerError = 'ErrServerError'
ErrClientError = 'ErrClientError'

ErrInternalError = 'ErrInternalError'
ErrUnexpected = 'ErrUnexpected' # This should be needed only in rare cases
ErrUnimplemented = 'ErrUnimplemented'

class RetVal:
	'''The RetVal class enables better error checking and variable return values'''
	def __init__(self, value=ErrOK, info=''):
		self._fields = { '_error': value, '_info': info }
	
	def __contains__(self, key):
		return key in self._fields

	def __delitem__(self, key):
		del self._fields[key]

	def __getitem__(self, key):
		return self._fields[key]
	
	def __iter__(self):
		return self._fields.__iter__()
	
	def __setitem__(self, key, value):
		self._fields[key] = value
	
	def __str__(self):
		out = list()
		out.append('Error: ' + self._fields['_error'])
		out.append('Info: ' + self._fields['_info'])

		for k,v in self._fields.items():
			if k in ['_error', '_info']:
				continue
			out.append('%s: %s' % (k,v))
		
		return '\n'.join(out)

	def set_error(self, value, info=''):
		'''Sets the error value of the object'''

		self._fields['_error'] = value
		self._fields['_info'] = info
		return self

	def error(self) -> str:
		'''Gets the error value of the object'''
		
		return self._fields['_error']

	def fields(self) -> list:
		'''Returns a list of the attached data fields in the object'''
		
		out = self._fields
		del out['_error']
		del out['_info']
		
		return out

	def set_info(self, value):
		'''Sets the extra error information of the object.'''
		
		self._fields['_info'] = value
		return self

	def info(self) -> str:
		'''Gets the error value of the object'''

		return self._fields['_info']

	def set_value(self, name: str, value):
		'''Adds a field to the object'''
		
		if name == '_error':
			return False
		
		self._fields[name] = value
		return self

	def set_values(self, values: dict):
		'''Adds multiple dictionary fields to the object.'''
		
		for k,v in values.items():
			if k in [ '_error', '_info' ]:
				return False
			self._fields[k] = v
		
		return self
	
	def has_value(self, s: str) -> bool:
		'''Tests if a specific value field has been returned'''
		
		return s in self._fields
	
	def empty(self):
		'''Empties the object of all values and clears any errors'''
		
		self._fields = { '_error':ErrOK, '_info':'' }
		return self

	def count(self) -> int:
		'''Returns the number of values contained by the return value'''
		
		return len(self._fields) - 2

	def wrap_exception(self, e: Exception):
		'''Quickly wraps an exception into the instance. The actual Exception object is returned 
		in 'exception' and the type of Exception is stored in 'exctype'. The return code is set to 
		ErrExceptionThrown. The info field is set to the string value of the exception.'''

		self._fields = {
			'_error': ErrExceptionThrown,
			'_info': str(e),
			'exctype': type(e).__name__,
			'exception': e,
		}
		return self
