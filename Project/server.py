import socket
import threading


class Server:
    """
    This is main class, which is used to starting server, and handling all messages.
    """
    def __init__(self):
        # This standard class initiating function is used to start the server by calling start_server func
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.username_lookup = {}
        self.start_server()

    def start_server(self):
        # This function is used to setup and start the server
        host = socket.gethostbyname(socket.gethostname())
        port = int(input('Enter port to run the server on --> '))

        self.s.bind((host, port))
        self.s.listen(100)

        print('Running on host: '+str(host))
        print('Running on port: '+str(port))

        while True:
            c, addr = self.s.accept()

            username = c.recv(1024).decode()

            print('New connection. Username: '+str(username))
            self.broadcast('New person joined the room. Username: '+username)

            self.username_lookup[c] = username

            self.clients.append(c)

            threading.Thread(target=self.handle_client, args=(c, )).start()

    def broadcast(self, msg):
        for connection in self.clients:
            connection.send(msg.encode())

    def handle_client(self, c):
        while True:
            try:
                msg = c.recv(1024)

            except:
                c.shutdown(socket.SHUT_RDWR)
                self.clients.remove(c)
                print(str(self.username_lookup[c])+' left the room.')
                self.broadcast(str(self.username_lookup[c])+' has left the room.')
                break

            if msg.decode() != '':
                print('New message: '+str(msg.decode()))
                for connection in self.clients:
                    if connection != c:
                        connection.send(msg)


# Starting the server by defining Server class
server = Server()
