import os
import socket
import threading
import argparse
import urllib.parse
import datetime  # Added for timestamp logging

# Default server port
DEFAULT_PORT = 9097

# Function to generate the HTML directory listing (ASCII-Only)
def generate_file_listing(directory):
    # Get absolute path of directory to avoid directory traversal issues
    directory = os.path.abspath(directory)

    # Ensure the requested directory is within the working directory
    base_directory = os.path.abspath(os.getcwd())
    if not directory.startswith(base_directory):
        return "403 Forbidden", "You are not allowed to access this directory."

    # List files & folders
    items = os.listdir(directory)
    items.sort()  # Sort alphabetically

    # Relative path for navigation
    relative_path = os.path.relpath(directory, base_directory)

    # Navigation links
    file_links = []
    if relative_path != ".":
        file_links.append('<li><a href="../">[..] Parent Directory</a></li>')  # Parent directory link

    for item in items:
        full_path = os.path.join(directory, item)
        encoded_name = urllib.parse.quote(item)

        if os.path.isdir(full_path):
            file_links.append(f'<li>[DIR] <a href="{encoded_name}/">{item}/</a></li>')  # ASCII Folder Indicator
        else:
            file_links.append(f'<li>[FILE] <a href="{encoded_name}">{item}</a></li>')  # ASCII File Indicator

    return "200 OK", f"""
    <html>
    <head><title>Simple File Server</title></head>
    <body>
        <h2>Index of /{relative_path}</h2>
        <ul>
            {''.join(file_links) if file_links else '<li>No files available</li>'}
        </ul>
    </body>
    </html>
    """

# Function to log client requests
def log_request(client_address, requested_path):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {client_address} requested {requested_path}")

# Function to handle incoming HTTP requests
def handle_client(client_socket, client_address):
    try:
        request = client_socket.recv(1024).decode('utf-8')
        if not request:
            return

        # Extract the requested file path
        request_line = request.splitlines()[0]
        _, path, _ = request_line.split()

        # Decode URL to properly handle spaces and special characters
        decoded_path = urllib.parse.unquote(path).lstrip("/")

        # Log the request
        log_request(client_address, decoded_path)

        # Resolve requested path relative to current working directory
        requested_path = os.path.abspath(os.path.join(os.getcwd(), decoded_path))

        # Serve directories or files
        if os.path.isdir(requested_path):
            status, response_body = generate_file_listing(requested_path)
            response_headers = (
                f"HTTP/1.1 {status}\r\n"
                "Content-Type: text/html\r\n"
                "Content-Length: {}\r\n"
                "Connection: close\r\n\r\n"
            ).format(len(response_body))

            client_socket.sendall(response_headers.encode('utf-8') + response_body.encode('utf-8'))

        elif os.path.isfile(requested_path):
            with open(requested_path, "rb") as file:
                file_data = file.read()

            response_headers = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: application/octet-stream\r\n"
                f"Content-Length: {len(file_data)}\r\n"
                f"Content-Disposition: attachment; filename=\"{os.path.basename(requested_path)}\"\r\n"
                "Connection: close\r\n\r\n"
            )

            client_socket.sendall(response_headers.encode('utf-8') + file_data)

        else:
            # File not found response
            response_body = "404 Not Found"
            response_headers = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/plain\r\n"
                "Content-Length: {}\r\n"
                "Connection: close\r\n\r\n"
            ).format(len(response_body))

            client_socket.sendall(response_headers.encode('utf-8') + response_body.encode('utf-8'))

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client_socket.close()

# Function to start the server
def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(5)

    print(f"[*] Server started on port {port}")
    print(f"[*] Access via: http://localhost:{port}/")
    
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address[0]))
        client_thread.start()

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Simple HTTP File Server with Folder Navigation & Logging")
parser.add_argument("-p", "--port", type=int, default=DEFAULT_PORT, help="Port to run the server on (default: 9097)")
args = parser.parse_args()

# Start the server
start_server(args.port)
