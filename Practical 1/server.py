import socket
import os
import struct
import sys

HOST = '127.0.0.1'
PORT = 8080
CHUNK_SIZE = 4096

# Filename length is 4 bytes (unsigned int)
FILENAME_LENGTH_HEADER_SIZE = 4
# File size is 8 bytes (unsigned long long)
FILE_SIZE_HEADER_SIZE = 8

def receive_all(sock, n):
    data = b''
    while len(data) < n:
        try:
            packet = sock.recv(n - len(data))
            if not packet:
                raise ConnectionResetError("Connection closed by peer")
            data += packet
        except socket.error as e:
            print(f"Socket error during receiving: {e}")
            return None
    return data

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        server_socket.bind((HOST, PORT))
        
        server_socket.listen()
        print(f"Server listening on {HOST}:{PORT}")
        print("Waiting for a client to connect...")

        while True:
            conn, addr = server_socket.accept()
            print(f"\nAccepted connection from {addr[0]}:{addr[1]}")
            handle_client(conn, addr)

    except KeyboardInterrupt:
        print("\nServer shut down by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # 5. Close the server socket
        server_socket.close()

def handle_client(conn, addr):
    try:
        filename_len_header = receive_all(conn, FILENAME_LENGTH_HEADER_SIZE)
        if not filename_len_header or len(filename_len_header) < FILENAME_LENGTH_HEADER_SIZE:
            print("Failed to receive filename length header. Closing connection.")
            return

        filename_len = struct.unpack('!I', filename_len_header)[0]
        
        filename_bytes = receive_all(conn, filename_len)
        if not filename_bytes or len(filename_bytes) < filename_len:
            print("Failed to receive filename bytes. Closing connection.")
            return

        original_filename = filename_bytes.decode('utf-8')
        new_filename = f"RECEIVED_{os.path.basename(original_filename)}"
        print(f"Receiving file: '{original_filename}' (to be saved as '{new_filename}')")

        file_size_header = receive_all(conn, FILE_SIZE_HEADER_SIZE)
        if not file_size_header or len(file_size_header) < FILE_SIZE_HEADER_SIZE:
            print("ailed to receive file size header. Closing connection.")
            return

        file_size = struct.unpack('!Q', file_size_header)[0]
        print(f"Total size to receive: {file_size / (1024*1024):.2f} MB")

        bytes_received = 0
        
        with open(new_filename, 'wb') as f:
            while bytes_received < file_size:
                remaining_bytes = file_size - bytes_received
                
                bytes_to_read = min(CHUNK_SIZE, remaining_bytes)
                
                chunk = conn.recv(bytes_to_read)
                
                if not chunk:
                    print(f"Connection closed prematurely. Received {bytes_received} of {file_size} bytes.")
                    break
                
                f.write(chunk)
                bytes_received += len(chunk)

        print("\nFile transfer complete.")
        
        if bytes_received < file_size:
            os.remove(new_filename)
            print("Incomplete file deleted.")

    except struct.error as e:
        print(f"\nProtocol error (struct unpack failed): {e}")
    except ConnectionResetError:
        print("\nConnection forcibly closed by the remote host.")
    except Exception as e:
        print(f"\nAn error occurred during file transfer: {e}")
    finally:
        # 5. Close the connection
        print(f"Closing connection from {addr[0]}:{addr[1]}")
        conn.close()

if __name__ == '__main__':
    start_server()