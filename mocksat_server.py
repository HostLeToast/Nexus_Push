import socket

def setup_server(host='0.0.0.0', port=9000):
    """Set up the server socket."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    return server

def handle_client(conn):
    """Handle the client connection."""
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Received: {data.decode()}")
            conn.sendall(b"ACK")
    finally:
        conn.close()

def main():
    server = setup_server()
    print("Server is listening...")
    conn, addr = server.accept()
    print(f"Connection from {addr}")

    handle_client(conn)

if __name__ == "__main__":
    main()
