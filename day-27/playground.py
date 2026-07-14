def add(*args):
	total = sum(args)
	print(total)


add(1,1,1,1,1,1)

def calculate(n,**kwargs):
	# for k,v in kwargs.items():
	# 	print(k)
	# 	print(v)
	n += kwargs['add']
	n *= kwargs['multiply']
	print(n)
calculate(2,add=3, multiply=5)


class Car:
	def __init__(self, **kwargs):
		self.make = kwargs.get('make')
		self.model = kwargs.get('model')
		self.year = kwargs.get('year')

my_car = Car(make="Ford", model="Taurus", year=2001)

print(my_car.make, my_car.model, my_car.year)
