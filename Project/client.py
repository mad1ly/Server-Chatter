import socket
import threading


class Client:
    """
    This class is used to connect to your server
    """
    def __init__(self):
        # Initiating Client class
        self.username = input('Enter your name --> ')
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.create_connection()

    def create_connection(self):
        # Creating connection to server
        while 1:
            try:
                host = input('Enter host ip --> ')
                port = int(input('Enter port --> '))
                self.s.connect((host, port))
                break

            except:
                print("Couldn't connect to server")

        self.s.send(self.username.encode())
        print("Connection is Successful")
        
        message_handler = threading.Thread(target=self.handle_messages,args=())
        message_handler.start()

        input_handler = threading.Thread(target=self.input_handler,args=())
        input_handler.start()

    def handle_messages(self):
        # Receiving messages
        while 1:
            print(self.s.recv(1204).decode())

    def input_handler(self):
        # Sending messages
        while 1:
            self.s.send((self.username+' - '+input()).encode())


# Starting the client by defining Client class
client = Client()
