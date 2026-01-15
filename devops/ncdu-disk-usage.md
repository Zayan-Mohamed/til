# Clean up Disk Space Interactively with ncdu

Standard disk usage commands (`du -h`) flood the terminal with text. `ncdu` (NCurses Disk Usage) provides a fast, interactive, cursor-based interface to browse directories and find what is eating your storage.



## Installation
On Ubuntu/Debian:
```bash
sudo apt install ncdu

```

## Usage

To scan the current directory:

```bash
ncdu

```

To scan the entire root filesystem (useful for full servers):

```bash
sudo ncdu /

```

## Key Controls

* **Up/Down**: Navigate files.
* **Right / Enter**: Enter directory.
* **Left**: Go back.
* **d**: Delete the selected file/directory (Ask for confirmation).
* **q**: Quit.

## Pro Tip: Remote Scanning

You can scan a remote server without installing `ncdu` on it, provided you have it locally and SSH access:

```bash
ssh user@remote-server "du -0c" | ncdu -f-

```
