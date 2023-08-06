from threading import Thread
from random import randint

def gen_thread_name() -> str:
	return 'easy_thread_{0}'.format(randint(1,1000000))

class EasyThreadUtils(Thread):
	def __init__(self,func):
		Thread.__init__(self)
	
		self.name = gen_thread_name()
		self.func = func
	def run(self):
		self.func()