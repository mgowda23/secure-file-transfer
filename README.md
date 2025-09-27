📦 Secure File Transfer Tool

A lightweight Python-based client-server application for transferring files securely using TLS encryption.
Supports SHA256 integrity verification, SQLite logging, and a simple CLI file picker for easy use.

🚀 Features

🔒 TLS-encrypted sockets for secure file transfer

✅ SHA256 integrity check to verify file integrity

🗂️ CLI file selection from files_to_send/ directory

📝 Transfer logs stored in SQLite (transfers.db)

🛑 Graceful shutdown with Ctrl+C (frees port immediately)

📂 Files automatically stored in received_files/

🛠️ Tech Stack

Language: Python 3.10+

Libraries: socket, ssl, sqlite3, hashlib

Database: SQLite (lightweight logging)

Security: TLS/SSL, SHA256 file verification

📂 Project Structure
secure-transfer/
│── client.py          # CLI tool to pick and send files
│── server.py          # Secure TLS server to receive files
│── db.py              # SQLite logging functions
│── cert.pem           # TLS certificate (self-signed)
│── key.pem            # TLS private key
│── transfers.db       # Logs of file transfers
│── files_to_send/     # Put files here to send
│── received_files/    # Received files stored here
│── README.md          # Project documentation
│── docs/
    └── secure_file_transfer_architecture_clean.png  # System workflow diagram

⚡ Quick Start
1️⃣ Clone Repository
git clone https://github.com/your-username/secure-transfer.git
cd secure-transfer

2️⃣ Generate TLS Certificates
openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem


Use localhost as Common Name (CN).

3️⃣ Initialize Database
python db.py

4️⃣ Run Server
python server.py


Server starts at localhost:5050 and waits for clients.

5️⃣ Run Client
python client.py


You’ll see a list of files in files_to_send/.

Pick one by number → it will be securely transferred.

📊 Transfer Logs

Transfers are saved in transfers.db with:

id

filename

filesize

timestamp

status (SUCCESS / FAILED if hash mismatch)

Check logs using SQLite:

sqlite3 transfers.db
sqlite> SELECT * FROM transfers;

🖼️ Architecture

🔮 Future Enhancements

🌐 Web dashboard (Flask) to view logs & transfers

🔑 User authentication for clients

📤 Multi-file batch transfer

📊 Transfer analytics (graphs of file sizes & frequency)

👨‍💻 Author

Mithun V Gowda
📍 Binghamton, NY | LinkedIn