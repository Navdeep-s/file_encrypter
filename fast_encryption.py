import sys,os
import numpy as np
from timeit import default_timer as timer
import multiprocessing
import queue




def xor(key, data):
	if(len(data)<len(key)):
		key = key[:len(data)]
	data = np.frombuffer(data, dtype=np.byte)
	key = np.frombuffer(key, dtype=np.byte)

	# Pad the key to match the data length
	key = np.pad(key, (0, len(data) - len(key)), 'wrap')

	return np.bitwise_xor(key, data)



def small_chunk(start, end, key, key_size,data):
    # print("start = ",start,"end=",end)
    for index in range(start, end):
        data[index] = key[index % key_size] ^ data[index]

    return data


def create_lists(data_size,n):
    middle=data_size//n
    list_starting=[x*middle for x in range(n)]
    list_ending=[x*middle for x in range(1,n)]
    list_ending.append(data_size)
    # print(list_starting,list_ending)
    return list_starting,list_ending








def encrypt_file(file_path,key,key_size):


	




	print("name of the file is", file_path)


	magic_number=100000000
	statinfo = os.stat(file_path)
	size = statinfo.st_size
	number_of_times = int(size/100000000)+1

	file = open(file_path+".enc","wb")


	data_file = open(file_path,"rb")

	print()
	for u in range(number_of_times):
		data = data_file.read(magic_number)
		file.write(bytearray(xor(key,data)))

	data = data_file.read(magic_number)
	file.write(bytearray(xor(key,data)))
	data_file.close()
	file.close()








class Consumer(multiprocessing.Process):

    def __init__(self, task_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        

    def run(self):
        pname = self.name

        while not self.task_queue.empty():

            file_path,key,key_size = self.task_queue.get()

            print("{} is working ......".format(self.name))
            process_queue(file_path,key,key_size)
            self.task_queue.task_done()
            


# class MyThread(multiprocessing.Process):
# 	def __init__(self,task_que):
# 		multiprocessing.Process.__init__(self)
# 		self.task_que =task_que


# 	def run(self):
# 		process_queue(self.task_que)



def process_queue(file_path,key,key_size):
		encrypt_file(file_path,key,key_size)
		os.remove(file_path)




def encrypt_folder(folder_path,key,key_size,no_process=5):
	start = timer()
	list_of_files=os.listdir(folder_path)
	if(len(list_of_files)==1):
		encrypt_file(os.path.join(folder_path,list_of_files[0]),key,key_size)
		os.remove(os.path.join(folder_path,list_of_files[0]))
		return

	tasks = multiprocessing.JoinableQueue()

	for file in list_of_files:
	    if not os.path.isdir(os.path.join(folder_path,file)):
	    	tasks.put((os.path.join(folder_path,file),key,key_size))
	    	 

	all_process=[Consumer(tasks) for i in range(no_process)]

	for consumer in all_process:
		consumer.start()

	tasks.join()

	duration = timer() - start
	print(duration)




if __name__=="__main__":

	if len(sys.argv) > 1:
		file_path = sys.argv[1]

	else:
		file_path = os.getcwd()
		# print("[ USAGE ]: {} path_of_file".format(sys.argv[0]))
		# sys.exit(0)

	key_path= input("path of the decoding file\n")
	if os.path.exists(file_path) and os.path.exists(key_path) and not(os.path.isdir(key_path)) :
		image = open(key_path,"rb")
		key=image.read()
		key_size=len(key)
		image.close()
		

		if os.path.isdir(file_path):
			encrypt_folder(file_path,key,key_size)
			print("Done..")

		else:
			encrypt_file(file_path,key,key_size)
	else:
		# print(os.path.exists(file_path))
		# print(os.path.exists(key_path))
		# print(file_path)
		# print(key_path)
		print("error occured in file encryption ")
		sys.exit(1)
