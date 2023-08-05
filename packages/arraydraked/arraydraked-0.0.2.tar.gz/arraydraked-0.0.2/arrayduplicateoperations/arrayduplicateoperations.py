def arraycheck(arr):
	if(len(arr) == len(set(arr))):
		return True
	else:
		return False

def dictCreator(arr):
	dct = {}
	for e in arr:
		if e in dct.keys():
			dct[e] +=1
		else:
			dct[e] = 1
	return dct