# Simple HTTP File Server

A lightweight, standalone HTTP file server that lets you quickly share files and browse directories from any web browser.

## Features

- No setup required – Just run the executable.
- Works on any directory – Place the file in the folder you want to share.
- Supports folder navigation – Browse and download files easily.
- Custom port support – Change the listening port with a command-line switch.

---

## Usage

### Running the Server

- Place `file_server.exe` (or `file_server.py`) in the folder you want to share.

- Run the server:

  **Windows (EXE)**

  ```sh
  file_server.exe
  ```

  **Python (Source)**

  ```sh
  python file_server.py
  ```

- By default, the server runs on port 9097.

### Accessing the Server

- Open a browser and visit:
  ```
  http://localhost:9097/
  ```
- Click on files to download them.
- Click on folders to navigate deeper.

---

## Command-Line Options

### Change the Server Port

By default, the server runs on port 9097. To change the port, use:

```sh
file_server.exe --port 8080
```

This will start the server on port 8080 instead.

---

## Notes

- This is a temporary file server – it stops when you close the EXE.
- Works on Windows (EXE) and Python (if running from source).
- If sharing over a network, make sure your firewall allows incoming connections on the chosen port.

---

## License

This project is licensed under the MIT License.

