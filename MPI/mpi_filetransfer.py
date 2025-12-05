import os
import sys
from mpi4py import MPI

# Get the communicator, rank, and size
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Define the root process (usually rank 0)
ROOT_RANK = 0

def transfer_file_mpi():
    if rank == ROOT_RANK:
        if len(sys.argv) != 2:
            print(f"Usage on Root: mpirun -n <num_procs> python {os.path.basename(__file__)} <filepath_to_send>", file=sys.stderr)
            # Send an empty string or None to signal error/exit to workers
            filepath = None
            # Broadcast the filepath (None in case of error)
            comm.bcast(filepath, root=ROOT_RANK)
            return

        filepath = sys.argv[1]

        if not os.path.exists(filepath):
            print(f"Root Error: File not found at path: {filepath}", file=sys.stderr)
            # Send an empty string or None to signal error/exit to workers
            filepath = None
            comm.bcast(filepath, root=ROOT_RANK)
            return

        filename = os.path.basename(filepath)
        file_size = os.path.getsize(filepath)

        print(f"Root process (Rank {rank})")
        print(f"Sending file: '{filename}'")
        print(f"Size: {file_size / (1024*1024):.2f} MB")

        # Read file content
        with open(filepath, 'rb') as f:
            file_content = f.read()

        # Broadcast the file name (str)
        comm.bcast(filename, root=ROOT_RANK)

        # Broadcast the file content (bytes)
        print(f"Broadcasting {file_size} bytes of content...")
        comm.bcast(file_content, root=ROOT_RANK)

        print("File broadcast complete.")

    else:
        filename = comm.bcast(None, root=ROOT_RANK)

        if filename is None:
            print(f"Worker {rank}: Error. Exiting.")
            return

        new_filename = f"Received rank {rank}_{filename}"
        print(f"Worker {rank}: File saved as '{new_filename}'")

        # Receive the file content
        file_content = comm.bcast(None, root=ROOT_RANK)

        if file_content is None:
             print(f"Worker {rank}: Error during content reception. Exiting.")
             return

        # Write content to a new file
        print(f"Worker {rank}: Writing {len(file_content)} bytes to disk...")
        with open(new_filename, 'wb') as f:
            f.write(file_content)

        print(f"Worker {rank}: File transfer complete. Saved as '{new_filename}'.")


if __name__ == '__main__':
    transfer_file_mpi()
