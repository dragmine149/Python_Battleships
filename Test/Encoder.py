import random

def Encode(data):
	newData = []
	IndexList = []
	for i in range(len(data)):
		Index = None
		while Index is None:
			Index = random.randint(0, len(data) - 1)
			if Index not in IndexList:
				IndexList.append(Index)
				newData.append(data[Index])
				continue
			Index = None

	returnData = ""
	for i in newData:
		returnData += i
	return returnData, IndexList

test1, List1 = Encode("Hello World")
test2, List2 = Encode("The quick brown fox jumps over the lazy dog")

print('----')
print(test1)
print(List1)
print('----')
print(test2)
print(List2)
print('----')

