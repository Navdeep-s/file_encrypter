## file_ecnrypter ##
This is an encryptiong software to encrypt you files using another file as a key
its working principle is simple, it just takes bitwise xor of your file with the key file 
it save the file with extension .enc

to use this make sure you have numpy installed on your system

## [Usage] ##

- python3 encrypt_files.py "complete_path_of_the_file"
- then you have to paste the proper path of key file 


- to decrypt the file follow the same procedure as above with the same key file 
- file will appear with .enc.enc extension just remove these extention by renamnig the file 
- you will get your decrypted file

## [Note] ##
this could be a one time pad if your key file is greater than the file needed to encrypt and content of the key file is unknown.
If this is the case nobody can break the encryption not even God without the key file
for reasons search why one time pad is unbreakable
