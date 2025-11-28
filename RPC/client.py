import xmlrpc.client
import os
import sys

HOST = '127.0.0.1'
PORT = 8000
SERVER_URL = f"http://{HOST}:{PORT}"

def send_file(filepath):
    if not os.path.exists(filepath):
        print(f"File not found at path: {filepath}")
        return

    filename = os.path.basename(filepath)
    file_size = os.path.getsize(filepath)

    print(f"File to send: '{filename}'")
    print(f"Size: {file_size / (1024*1024):.2f} MB")

    try:
        # Establish the connection (proxy) to the remote server
        proxy = xmlrpc.client.ServerProxy(SERVER_URL)

        # Read the entire file content as raw binary data
        with open(filepath, 'rb') as f:
            file_content = f.read()

        binary_data_to_send = xmlrpc.client.Binary(file_content)

        print("Initiating remote procedure call...")

        success = proxy.upload_file(binary_data_to_send, filename)

        if success:
            print("[CLIENT] RPC call successful. File uploaded.")
        else:
            print("[CLIENT] RPC call failed on the server side.")

    except ConnectionRefusedError:
        print(f"\n[CLIENT] Connection refused. Ensure the server is running on {HOST}:{PORT}.")
    except Exception as e:
        print(f"\n[CLIENT] An unexpected RPC error occurred: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python rpc_client.py <path_to_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    send_file(file_path)
