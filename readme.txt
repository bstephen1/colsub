substitution permutation cipher decryption/encryption program

The program encrypts/decrypts text using substitution followed by columnar transposition

When running the program, the user inputs a key that will be used until the program stops, first for the substitution, then for the transposition
If the matrix is not full, the program will run the the alphabet to fill it
The program also replaces all numbers with their written equivalent (eg, '1' is 'one')

There are 5 options in the main loop:
	encipher -- enter a string to be enciphered 
	decipher -- enter a string to be deciphered
	encipher from file -- enciphers the text in "encipher.txt" and writes the result to "output.txt"
	decipher from file -- deciphers the text in "decipher.txt" and writes the result to "output.txt"
	quit -- end the program
	

encipher.txt is the text from the difficult substitution cipher, decipher.txt is the encryption of that text using the key 'tomato' for substitution and 'potato' for transposition, and output.txt is the decryption (the original text again)
