import socket

def setup_client(host='raspberrypi.local', port=9000):
    """Set up the client socket."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    return client

def send_and_receive_data(client, message):
    """Send data to the server and receive a response."""
    try:
        client.sendall(message.encode())
        response = client.recv(1024)
        print(f"Received: {response.decode()}")
    finally:
        client.close()

def main():
    client = setup_client()
    send_and_receive_data(client, "Hello from Ground Station")

if __name__ == "__main__":
    main()
