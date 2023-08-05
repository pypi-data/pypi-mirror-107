def dictCreator(arr):
	dct = {}
	for e in arr:
		if e in dct.keys():
			dct[e] +=1
		else:
			dct[e] = 1
	return dct

arr = ['a','a','b','c','c']
print(dictCreator(arr))