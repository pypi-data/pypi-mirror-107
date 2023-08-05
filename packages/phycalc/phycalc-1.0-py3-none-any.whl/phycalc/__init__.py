# Author: Snehashish Laskar
# Date: 25-5-2021
# Author email: snehashish.laskar@gmail.com

# Copyright (c) 2021 Snehashish Laskar

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


class CreateObject:

	def __init__(self, mass = 0, acceleration = 0, force = 0, velocity = 0, time =0, distance = 0, avg_speed = 0, speed = 0):
		self.mass = mass
		self.acceleration = acceleration
		self.force = force
		self.velocity = velocity
		self.time = time
		self.distance = distance
		self.avg_speed = avg_speed	

	def getAccelerationWithForce(self, unit=str):
		if self.force != 0 and self.mass != 0:
			return str(self.force/self.mass)+unit
		else:
			raise ValueError('To calculate acceleration with force and mass the object must have a mass and force')

	def getAccelerationWithVelocity(self, unit=str):
		if self.velocity != 0 and self.time != 0:
			return str(self.velocity/self.time)+unit
		else:
			raise ValueError('To calculate acceleration with velocity the object must have a velocity and time period')

	def getAvgSpeed(self, unit=str):
		if self.distance != 0 and self.time != 0:
			return str(self.distance/self.time)+unit

		else:
			raise ValueError('To calculate Average speed the distance and time need to be specified')

	def getDistanceCovered(self, unit=str):
		if self.avg_speed != 0 and self.time != 0:
			return str(self.avg_speed/self.time)+unit
		else:
			raise ValueError('To calculate the Distance covered the avgerage speed and time taken must be specified')

	def getDistanceCoveredFromAcceleration(self, unit=str):
		if self.acceleration != 0 and self.time != 0:
			return str((self.acceleration*(self.time*self.time))/2)+unit
		else:
			raise ValueError('To calculate the Distance covered the acceleration speed and time taken must be specified')

	def getMomentum(self, unit = str):
		if self.mass != 0 and self.velocity != 0:
			return str(self.mass*self.velocity)+unit
		else:
			raise ValueError('To calculate the Momentum the Object must have a mass and a velocity')

	def getImpulse(self, unit = str):
		if self.force != 0 and self.time != 0:
			return str(self.force*self.time)+unit
		else:
			raise ValueError('To calculate the Impulse the Object must have a force and a time period')






