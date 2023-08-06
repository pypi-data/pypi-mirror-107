# Cipher-Python-Package

## Summary of the Python Package
This package encrypts your text using Hill Cipher Technique.
Hill ciphers are an application of linear algebra to cryptology (the science of
making and breaking codes and ciphers).
## Algorithm:
Let the order of the encryption key be N (as it is a square matrix).
Your text is divided into batches of length N and converted to numerical vectors
by a simple mapping starting with A=0 and so on.
 
The key is then multiplied with the newly created batch vector to obtain the
encoded vector. After each multiplication modular 36 calculations are performed
on the vectors so as to bring the numbers between 0 and 36 and then mapped with
their corresponding alphanumerics.
 
While decrypting, the decrypting key is found which is the inverse of the
encrypting key modular 36. The same process is repeated for decrypting to get
the original message back.


  
### Implementation:
`from pycipher import HillCipher` <br />
`obj = HillCipher("beaf")` <br />
`print(hc.encrypt("Love Python"))` <br />
`print(hc.decrypt("PITTOO"))` <br />

### References:
https://apprendre-en-ligne.net/crypto/hill/Hillciph.pdf


  

