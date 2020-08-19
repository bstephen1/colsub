from copy import deepcopy
	
#global constants 
#character to use for double letters
repeatChar = "X"
#alphabet 
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#amount of letters in a block (formatting)
block = 5
#blocks per line (formatting)
bpl = 15


#converts the message to form readable by the cipher
def getRawMessage(aMessage) :

	aMessage = aMessage.replace(" ", "")
	aMessage = aMessage.replace("\n", "")
	aMessage = aMessage.replace("\r", "")
	aMessage = replaceNumbers(aMessage)
	aMessage = aMessage.upper()	

	return aMessage
	

#replaces all numbers with their written equivalent
def replaceNumbers(aMessage) :
	aMessage = aMessage.replace("0", "zero")
	aMessage = aMessage.replace("1", "one")
	aMessage = aMessage.replace("2", "two")
	aMessage = aMessage.replace("3", "three")
	aMessage = aMessage.replace("4", "four")
	aMessage = aMessage.replace("5", "five")
	aMessage = aMessage.replace("6", "six")
	aMessage = aMessage.replace("7", "seven")
	aMessage = aMessage.replace("8", "eight")
	aMessage = aMessage.replace("9", "nine")
	return aMessage
	
	
#creates the key for substitution, using the key and filling in the rest of the alphabet
def createSubKey(aKey) :
	aKey = list(aKey)
	aKey.extend(list(alphabet))
	aKey = "".join(aKey)
	aKey = aKey.upper()
	aKey = removeDups(aKey)
	
	return aKey
	

#created the key for columnar transposition 
def createColKey(aKey) :
	aKey = aKey.replace(" ", "")
	aKey = aKey.upper()
	sortedKey = sorted(aKey)
	colKey = []
	#dictionary for dealing with duplicate letters
	frequency = {}
	
	for x in aKey :
		indx = sortedKey.index(x)
		if x in frequency :
			frequency[x] += 1
			indx += frequency[x]
		else: 
			frequency[x] = 0
		colKey.append(indx)
	
	return colKey		
	

#removes all the duplicate letters and numbers in a string
def removeDups(aString) :
	aString = aString.replace(" ", "")
	aString = list(aString)
	for x in range(len(aString) - 1) :
		y = x + 1
		while y < len(aString) : 
			if aString[x] == aString[y] :
				del aString[y]
				y -= 1
			y += 1
	aString = "".join(aString)
	return aString
	
	
#creates a matrix based on the length of the key (for enciphering)
def createMatrix(aMessage, aKey) :
	
	matrix = []
	col = []
	for x in aMessage :
		col.append(x)
		if len(col) == len(aKey) :
			matrix.append(deepcopy(col))
			col = []
			
	#add letters to fill the matrix if matrix is not full
	if len(col) != len(aKey) :
		x = 0
		while len(col) != len(aKey) :
			col.append(alphabet[x % len(alphabet)])
			x += 1
		matrix.append(deepcopy(col))
		
	return matrix
	
	
#enciphers the message
def encipher(subKey, colKey, aMessage) :

	#substitution
	subMes = []
	for x in aMessage :
		#protects against punctuation
		if ord(x) > 64 and ord(x) < 91 or ord(x) > 47 and ord(x) < 58 :
			subMes.append(subKey[alphabet.index(x)])
	subMes = "".join(subMes)
	
	
	#transposition
	newMes = []
	matrix = createMatrix(subMes, colKey)
	colKey = createColKey(colKey)
	
	#get the right column, then add it to the final string
	i = 0
	p = 0
	while p < len(colKey) :
		x = colKey[i]
		if x == p :
			for y in range(len(matrix)) :
				newMes.append(matrix[y][i])
			i = 0
			p += 1
			continue
		i += 1
	
	return format(newMes)

	
#deciphers the message
def decipher(subKey, colKey, aMessage) :	
	
	#transposition
	#set up empty matrix
	colKey = createColKey(colKey)
	cols = len(colKey)
	rows = len(aMessage) / cols
	matrix = [[]] * rows
	for x in range(len(matrix)) :
		matrix[x] = [0] * cols

	
	#get the right column, then add it to the matrix
	i = 0
	p = 0
	c = 0
	while p < len(colKey) :
		x = colKey[i]
		if x == p :
			for y in range(len(matrix)) :
				matrix[y][i] = aMessage[c]
				c += 1
			i = 0
			p += 1
			continue
		i += 1
	
	#transform the matrix into a string
	tranMes = []
	for x in matrix :
		for y in x :
			tranMes.append(y)
	
	#substitution
	newMes = []
	for x in tranMes :
		#protects against punctuation 
		if ord(x) > 64 and ord(x) < 91 or ord(x) > 47 and ord(x) < 58 :
			newMes.append(alphabet[subKey.index(x)])
	
	return format(newMes)

	
#formats the string to be in blocks 
def format(s) :
	mes = []
	for x in range(len(s)) :
		if not (x % (bpl * block)) and x != 0 :
			mes.append("\n")
			mes.append(s[x])
		elif x % block or x == 0 :
			mes.append(s[x])
		else :
			mes.append(" ")
			mes.append(s[x])
			
	mes = "".join(mes)
	return mes

	
#main 
def main() :
	
	print "\nWelcome to Substitution Permutation program.\n"
	sub = raw_input("Substitution key: ")
	subKey = createSubKey(sub)
	
	same = int(raw_input("Column transposition key: \n1 -- use same key\n2 -- use different key\n"))
	if same - 1 : 
		colKey = raw_input("Enter a key: ")
	else :
		colKey = sub
	
	#main loop
	cont = True
	while cont :
		choice = int(raw_input("1 -- encipher\n2 -- decipher\n3 -- encipher from file\n4 -- decipher from file\n5 -- quit\n"))
		if choice == 1 :
			message = raw_input("Enter a message to encipher: ")
			message = getRawMessage(message)
			print "Enciphered message:" , encipher(subKey, colKey, message)
		elif choice == 2 :
			message = raw_input("Enter a message to decipher: ")
			message = getRawMessage(message)
			print "Deciphered message:" , decipher(subKey, colKey, message)
		elif choice == 3 :
			print "Enciphering from \"encipher.txt\" to \"output.txt\"..."
			text = open("encipher.txt", "r")
			out = open("output.txt" , "w")
			message = getRawMessage(text.read()) 
			out.write(encipher(subKey, colKey, message))
			text.close()
			out.close()
		elif choice == 4 :
			print "Deciphering from \"decipher.txt\" to \"output.txt\"..."
			text = open("decipher.txt" , "r")
			out = open("output.txt" , "w")
			message = getRawMessage(text.read())
			out.write(decipher(subKey, colKey, message))
			text.close()
			out.close()
		elif choice ==  5 :
			cont = False
		else :
			print "Invalid symbol."
	
	
main()