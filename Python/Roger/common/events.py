

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



class Sense:
	def Forward():
		pass

	def Spin():
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

	def Backward():
		pass

	def Collision():
		pass



class Did:
	def GoForward():
		pass

	def GoBackward():
		pass

	def Spin():
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

	def Backward():
		pass

	def Collision():
		pass









def watch(value):
	print(value)

e = EventNotifier()
e.subscribe(watch)
e.notify("aaa")

