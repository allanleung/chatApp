import socket
import select

HEADER_LEN = 10; 
IP = "127.0.0.1"
PORT = 2000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# allow to reconenct
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#bind to IP
server_socket.bind ((IP, PORT))
server_socket.listen()

#handle socket
socket_list = [server_socket]
#client list
clients = {}

#receve messages

def receive_message(client_socket):
	try:
		message_header = client_socket.recv(HEADER_LEN)

		# no data, return false
		if not len(message_header):
			return False

		message_length = int(message_header.decode("utf-8").strip())
		return {"header" : message_header, "data": client_socket.recv(message_length)}


	except:
		return False

while True:
	# select takes (read list, write list, socket we error on)
	read_socket, _, exception_sockets = select.select(socket_list, [], socket_list)

	for notified_socket in read_socket:
		if notified_socket == server_socket:
			client_socket, client_address = server_socket.accept()

			user = receive_message(client_socket)
			#disconnect
			if user is False:
				continue

			socket_list.append(client_socket)

			clients[client_socket] = user

			print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")

		else:

			message = receive_message(notified_socket)

			if message is False:
				print (f"Close connection from {clients[notified_socket]['data'].decode('utf-8')}")
				socket_list.remove(notified_socket)
				del clients[notified_socket]
				continue

			user = clients[notified_socket]
			print (f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

			for client_socket in clients:
				if client_socket != notified_socket:
					client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])


	for notified_socket in exception_sockets:
		socket_list.remove(notified_socket)
		del clients[notified_socket]