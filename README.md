# 🚀 Multi-Threaded TCP Port Scanner & Banner Grabber

A fast, custom-built multi-threaded TCP port scanner and service banner grabber written in Python. Built with an interactive terminal interface, regular expression validation, and high-speed concurrent execution to help you quickly map networks and identify active services.


## ✨ Features

- ⚡ **Super Fast Multi-Threading:** Uses Python's `concurrent.futures` thread pooling to scan hundreds of ports simultaneously instead of sequentially.
- 🔍 **Service Banner Grabbing:** Interrogates open ports to capture initial welcome messages or software headers (e.g., HTTP server types, versions).
- 🛡️ **Foolproof Input Validation:** Interactive terminal loops powered by Regular Expressions (`re`) ensure you enter valid IPv4 addresses and port ranges.
- 📊 **Export Options:** Automatically prompts you to export discovered results cleanly into a CSV spreadsheet or a plain text report.
- 🧩 **Zero-Dependency Code:** Built entirely with pure Python standard libraries—no `pip install` required.

---

<p align="center">
  <img src="./demo.gif" alt="Terminal Demo" width="100%" />
</p>

## 🛠️ Requirements & Dependencies

This script is written in pure Python 3 and uses **only standard built-in libraries** (`socket`, `concurrent.futures`, `csv`, `re`, `datetime`). You don't need to install any external pip packages!

- **Python 3.x** installed on your system.

---

## 🚀 How to Run

1. **Clone or download this repository to your local machine:**
```
   git clone https://github.com/Y6THAY/python-port-scanner.git
   cd python-port-scanner
```
2. Run the script using Python 3:
```
  python3 scanner.py
```

3. Follow the interactive prompts in your terminal to specify your target IP address and port range (e.g., 1-1024)

<br>

# 📜 License & Copyright
Copyright © 2026 Yannich Thay. All rights reserved.

**Disclaimer:** This tool is intended for educational purposes, authorized security auditing, and network management only. Do not scan systems without explicit permission.
