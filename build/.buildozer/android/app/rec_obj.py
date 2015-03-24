'''
@author jaronhalt

All this class is for is to be able to do things like:
	(( See RecObj.test() )) 
	>>> ro = RecObj()
	>>> ro.a.b.c.d.e = 1
	>>> ro
	{'a': {'b': {'c': {'d': {'e': 1}}}}}

Keep in mind that any aggregate is passed by reference unless explicitly noted otherwise.

'''

import json

class RecObj(dict):
	'''
	Each arg in args must be a dict-like object
	'''
	def __init__(self, *args, **kwargs):
		for arg in args:
			for k,v in arg.iteritems():
				self.__setattr__(k,v)
		for k,v in kwargs.iteritems():
			self.__setattr__(k,v)

	def __str__(self):
		return json.dumps(self, indent=2)

	def __getattr__(self, attr):
		if attr in self:
			attribute = super(RecObj, self).__getitem__(attr)
			return attribute
		else:
			self.__setattr__(attr, RecObj())
			return self.__getattr__(attr)

	def __setattr__(self, attr, value):
		attr = attr.replace(' ','_')
		#make everything recursive
		if type(value) == dict:
			value = RecObj(value)
		super(RecObj, self).__setitem__(attr, value)

	def __iter__(self):
		for key, value in super(RecObj, self).iteritems():
			yield key, value

	def __eq__(self,other):
		if len(self.keys()) == 0:
			return None == other
		else:
			return self == other

	def func(self):
		return 'function called'

	@property
	def res(self):
		self._res = 'property accessed'
		return self._res

	@staticmethod
	def test():
		ro = RecObj({'a':1, 'b':2, 'c':{'d':3, 'e':4, 'f':{'g':5}}}, what='nothing', brother=RecObj(b=909))
		
		ro.a = 2
		assert ro.a == ro.b
		assert ro.c.d < ro.c.f.g
		ro.c.d = 10
		print ro
		assert ro.c.d > ro.c.f.g
		ro.a = ro.c.f
		ro.b = ro.c
		assert ro.b.f is ro.c.f
		assert ro.b['f'].g == 5
		print ro.what
		ro.nothing = ro.what
		ro.brother.b = ro.b
		assert 'function called' == ro.func()
		assert 'property accessed' == ro.res

		empty1 = RecObj()
		empty2 = RecObj()

		assert empty2 == empty1 == None
		assert empty1.a.b.c == None

		assert {} == dict(empty2.e.f.g)

		return ro


if __name__ == '__main__':
	print RecObj.test()
