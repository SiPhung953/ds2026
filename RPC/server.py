from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import os

HOST = '127.0.0.1'
PORT = 8000
UPLOAD_DIR = 'server_uploads'

# Create the directory for uploaded files if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

def upload_file(file_data: xmlrpc.client.Binary, filename: str) -> bool:
    try:
        # Extract the raw bytes from the Binary object
        binary_data = file_data.data

        # Construct the full path to save the file
        save_path = os.path.join(UPLOAD_DIR, filename)

        # Write the binary data to the file
        with open(save_path, 'wb') as f:
            f.write(binary_data)

        print(f"\n[SERVER] Successfully received and saved file: '{filename}'")
        print(f"[SERVER] Size: {len(binary_data) / (1024*1024):.2f} MB")
        return True

    except Exception as e:
        print(f"\n[SERVER] An error occurred during file upload: {e}")
        return False

def start_server():
    """Starts the XML-RPC server."""
    print(f"Starting XML-RPC Server on {HOST}:{PORT}...")
    with SimpleXMLRPCServer((HOST, PORT), allow_none=True) as server:
        server.register_introspection_functions()

        # Register the remote procedure
        server.register_function(upload_file, 'upload_file')

        print("Server ready. Waiting for RPC calls. Press Ctrl+C to exit.")
        server.serve_forever()

if __name__ == '__main__':
    try:
        start_server()
    except KeyboardInterrupt:
        print("\nServer shutting down.")
    except Exception as e:
        print(f"\nServer error: {e}")
