
class EventNotifier:

	def __init__(self):
		self.event = []

	def subscribe(self, f):
		self.event.append(f)

	def unsubscribe(self, f):
		self.event.remove(f)

	def notify(self, value):
		for f in self.event:
			f(value)


# eventually, we would like the executive
# to be able to create events and link a reaction to them

# Context is a set of events that can be loaded or unloaded
#  


# what to do when an event occurs
class Sense:
	def forward(self):
		pass

	def backward(self):
		pass

	def spinleft(self):
		pass

	def spinright(self):
		pass

	def tipforward(self):
		pass

	def tipbackward(self):
		pass

	def tipleft(self):
		pass

	def tipright(self):
		pass

	def brake(self):
		pass

	def bump(self):
		pass


# check if an event occurred
class Did:
	def goforward(self):
		pass

	def gobackward(self):
		pass

	def spinleft(self):
		pass

	def spinright(self):
		pass

	def tipforward(self):
		pass

	def tipbackward(self):
		pass

	def tipleft(self):
		pass

	def tipright(self):
		pass

	def brake(self):
		pass

	def bump(self):
		pass









def watch(value):
	print(value)

e = EventNotifier()
e.subscribe(watch)
e.notify("aaa")
