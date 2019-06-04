import socket
import select
import errno

HEADER_LEN = 10
IP = "127.0.0.1"
PORT = 2000

my_username = input("Username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

username = my_username.encode("utf-8")
username_header = f"{len(username):<{HEADER_LEN}}".encode("utf-8")
client_socket.send(username_header + username)

#interiate forever
#send and recv message

while True:
	# make username 
	message = input(f"{my_username} > ")

	#sending the message
	if message :
		message = message.encode("utf-8")
		message_header = f"{len(message) :< {HEADER_LEN}}".encode("utf-8")
		client_socket.send(message_header + message)
	try:	
		while True:
			#receving message
			username_header = client_socket.recv(HEADER_LEN)
			#something went wrong
			if not len(username_header):
				print ("Connection closed by the server")
				sys.exit()
			#message will send to server
			username_length = int(username_header.decode("utf-8").strip())
			username = client_socket.recv(username_length).decode("utf-8")

			message_header = client_socket.recv(HEADER_LEN)
			message_length = int(message_header.decode("utf-8").strip())
			message = client_socket.recv(message_length).decode("utf-8")


			print(f"{username} > {message}")

	except IOError as e:
		#operating system related error
		if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:	
			print ('Reading error', str(e))
			sys.exit()
		continue	

	except Exception as e:
		print('General error', str(e))
		sys.exit()
		pass