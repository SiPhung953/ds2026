import socket
import os
import struct
import sys

HOST = '127.0.0.1'
PORT = 8080
CHUNK_SIZE = 4096

FILENAME_LENGTH_HEADER_SIZE = 4
FILE_SIZE_HEADER_SIZE = 8

def send_file(filepath):
    # Validate file
    if not os.path.exists(filepath):
        print(f"File not found at path: {filepath}")
        return
    
    filename = os.path.basename(filepath)
    filename_bytes = filename.encode('utf-8')
    filename_len = len(filename_bytes)
    file_size = os.path.getsize(filepath)

    if filename_len > 2**32 - 1:
        print("Filename is too long")
        return
    
    print(f"Sending file: '{filename}'")
    print(f"Size: {file_size / (1024*1024):.2f} MB")

    # Create and connect socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect to the server
        client_socket.connect((HOST, PORT))
        print(f"Connected to server at {HOST}:{PORT}")
        
        filename_len_header = struct.pack('!I', filename_len)
        client_socket.sendall(filename_len_header)
        
        client_socket.sendall(filename_bytes)
        
        file_size_header = struct.pack('!Q', file_size)
        client_socket.sendall(file_size_header)
        
        bytes_sent = 0
        with open(filepath, 'rb') as f:
            while bytes_sent < file_size:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break 
                
                client_socket.sendall(chunk)
                bytes_sent += len(chunk)

        print("File transfer initiated.")
        
    except ConnectionRefusedError:
        print(f"Connection refused. Ensure the server is running on {HOST}:{PORT}.")
    except socket.error as e:
        print(f"Socket error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Close the socket
        print("Closing client socket.")
        client_socket.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python file_client.py <filepath>")
        sys.exit(1)
        
    file_to_send = sys.argv[1]
    send_file(file_to_send)