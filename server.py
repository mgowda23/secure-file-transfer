import socket, ssl, os, hashlib, signal, sys
from db import log_transfer

HOST = 'localhost'
PORT = 5050
CERTFILE = 'cert.pem'
KEYFILE = 'key.pem'
SAVE_DIR = "received_files"

os.makedirs(SAVE_DIR, exist_ok=True)

def sha256sum(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(4096):
            h.update(chunk)
    return h.hexdigest()

def start_server():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)

    # create base socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(5)
    print(f"🔒 Secure server listening on {HOST}:{PORT}...")

    # cleanup function on Ctrl+C
    def shutdown(sig, frame):
        print("\n🛑 Shutting down server gracefully...")
        sock.close()
        sys.exit(0)

    # attach Ctrl+C handler
    signal.signal(signal.SIGINT, shutdown)

    with context.wrap_socket(sock, server_side=True) as ssock:
        while True:
            conn, addr = ssock.accept()
            print(f"[+] Connection from {addr}")

            # Read metadata
            filename = conn.recv(1024).decode().strip()
            filesize = int(conn.recv(1024).decode().strip())
            expected_hash = conn.recv(1024).decode().strip()

            filepath = os.path.join(SAVE_DIR, filename)
            with open(filepath, "wb") as f:
                data = conn.recv(filesize)
                f.write(data)

            actual_hash = sha256sum(filepath)

            if actual_hash == expected_hash:
                print(f"✅ Received {filename} ({filesize} bytes) — Integrity Verified")
                log_transfer(filename, filesize, "SUCCESS")
            else:
                print(f"❌ Hash mismatch for {filename}!")
                log_transfer(filename, filesize, "FAILED")

            conn.close()

if __name__ == "__main__":
    start_server()

