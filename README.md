# Secure File Transfer

Python client-server tool for sending files over TLS, with SHA-256 integrity checks and SQLite transfer logs.

## Features

- TLS-encrypted sockets
- SHA-256 verification of received files
- CLI picker for files in `files_to_send/`
- Transfer logs in SQLite (`transfers.db`)
- Graceful shutdown with Ctrl+C

## Stack

Python 3.10+ · `socket` · `ssl` · `sqlite3` · `hashlib`

## Quick start

```bash
git clone https://github.com/mgowda23/secure-file-transfer.git
cd secure-file-transfer
openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem
python db.py
python server.py
```

In a second terminal:

```bash
python client.py
```

Use `localhost` as the certificate Common Name. The server listens on `localhost:5050`. Received files land in `received_files/`.

## Logs

```bash
sqlite3 transfers.db "SELECT * FROM transfers;"
```

Fields: id, filename, filesize, timestamp, status (`SUCCESS` or `FAILED` on hash mismatch).
