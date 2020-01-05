

class EventNotifier:

	def __init__(self):
		self.event = [];

	def subscribe(self, f):
		self.event.append(f)

	def unsubscribe(self, f):
		self.event.remove(f)

	def notify(self, value):
		for f in self.event:
			f(value)


#eventually, we would like the executive
#to be able to create events and link a reaction to them

#Context is a set of events that can be loaded or unloaded
#  


#what to do when an event occurs
class Sense:
	def Forward():
		pass

	def Backward():
		pass

	def SpinLeft():
		pass

	def SpinRight():
		pass

	def TipForward():
		pass

	def TipBackward():
		pass

	def TipLeft():
		pass

	def TipRight():
		pass

	def Brake():
		pass

	def Bump():
		pass


#check if an event occurred
class Did:
	def GoForward():
		pass

	def GoBackward():
		pass

	def SpinLeft():
		pass

	def SpinRight():
		pass

	def TipForward():
		pass

	def TipBackward():
		pass

	def TipLeft():
		pass

	def TipRight():
		pass

	def Brake():
		pass

	def Bump():
		pass









def watch(value):
	print(value)

e = EventNotifier()
e.subscribe(watch)
e.notify("aaa")

