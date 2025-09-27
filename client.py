import socket, ssl, os, hashlib

HOST = 'localhost'
PORT = 5050
CERTFILE = 'cert.pem'
FILES_DIR = "files_to_send"

def sha256sum(filename):
    h = hashlib.sha256()
    with open(filename, "rb") as f:
        while chunk := f.read(4096):
            h.update(chunk)
    return h.hexdigest()

def send_file(filepath):
    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)
    filehash = sha256sum(filepath)

    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations(CERTFILE)

    with socket.create_connection((HOST, PORT)) as sock:
        with context.wrap_socket(sock, server_hostname=HOST) as ssock:
            print(f"🔑 Securely connected to {HOST}:{PORT}")

            # Send metadata
            ssock.sendall(filename.encode() + b"\n")
            ssock.sendall(f"{filesize}\n".encode())
            ssock.sendall(f"{filehash}\n".encode())

            # Send file
            with open(filepath, "rb") as f:
                ssock.sendall(f.read())

            print(f"📤 Sent {filename} ({filesize} bytes) with hash {filehash}")

def choose_file():
    files = os.listdir(FILES_DIR)
    if not files:
        print("⚠️ No files found in 'files_to_send/' directory.")
        return None

    print("📂 Available files:")
    for i, f in enumerate(files, 1):
        print(f"{i}. {f}")

    choice = int(input("\nEnter the number of the file to send: "))
    if 1 <= choice <= len(files):
        return os.path.join(FILES_DIR, files[choice-1])
    else:
        print("❌ Invalid choice.")
        return None

if __name__ == "__main__":
    filepath = choose_file()
    if filepath:
        send_file(filepath)

