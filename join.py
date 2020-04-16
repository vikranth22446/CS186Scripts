from math import ceil

class SortHash:
	def __init__(self, numPages, numBuffers):
		self.numPages = numPages
		self.numBuffers = numBuffers

	def sort(self):
		B = self.numBuffers
		P = self.numPages
		runs = [P // B, B, P % B]
		i = 0
		while runs[0] + (runs[2] > 0) > 1:
			print("Pass {}: {} runs of {} pages, 1 run of {} pages".format(i, runs[0], runs[1], runs[2]))
			runs = [runs[0] // (B - 1), runs[1] * (B - 1), runs[2] + (runs[0] % (B - 1)) * runs[1]]
			i += 1
		print("Pass {}: {} runs of {} pages, 1 run of {} pages".format(i, runs[0], runs[1], runs[2]))
		ios = 2 * P * (i + 1)
		print("Total IO:", ios)
		return ios

	def hash(self):
		B = self.numBuffers
		ios = P = self.numPages
		parts = 1
		i = 0
		while P > B:
			parts *= B - 1
			P = ceil(P / (B - 1))
			print("Pass {}: {} partitions of {} pages".format(i, parts, P))
			ios += P * parts * 2
			i += 1
		ios += P * parts
		print("Total IO:", ios)
		return ios


class Join:
	def __init__(self, numPages1, numRecords1, numPages2, numRecords2, numBuffers=3):
		self.p1 = numPages1
		self.r1 = numRecords1
		self.p2 = numPages2
		self.r2 = numRecords2
		self.b = numBuffers

	def SNLJ(self):
		print("Relation 1 as outer: {}".format(self.p1 + self.r1 * self.p2))
		print("Relation 2 as outer: {}".format(self.p2 + self.r2 * self.p1))

	def PNLJ(self):
		print("Relation 1 as outer: {}".format(self.p1 + self.p1 * self.p2))
		print("Relation 2 as outer: {}".format(self.p2 + self.p2 * self.p1))

	def BNLJ(self):
		print("Relation 1 as outer: {}".format(self.p1 + ceil(self.p1 / (self.b - 2)) * self.p2))
		print("Relation 2 as outer: {}".format(self.p2 + ceil(self.p2 / (self.b - 2)) * self.p1))

	def hash(self):
		b, p1, p2 = self.b, self.p1, self.p2
		parts = 1
		ios = p1 + p2
		i = 0
		while p1 > b - 2 and p2 > b - 2:
			parts *= b - 1
			p1, p2 = ceil(p1 / (b - 1)), ceil(p2 / (b - 1))
			print("Pass {}: {} partitions".format(i, parts))
			print("  Relation 1: {} pages\n  Relation 2: {} pages".format(p1, p2))
			ios += (p1 + p2) * parts * 2
			i += 1
		print("Total IO:", ios)
		return ios

	def sort(self):
		ios = SortHash(self.p1, self.b).sort() + SortHash(self.p2, self.b).sort()
		print("Total IO:", ios + self.p1 + self.p2)


Join(100, 100 * 100, 50, 50 * 50, 20).sort()
