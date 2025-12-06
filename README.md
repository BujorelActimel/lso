# lso

Like the `ls` command, but instead of listing directories and files, it lists the available functions from shared objects on Linux.

## Overview

`lso` extracts and displays function names from `.so` files. It recursively scans directories by default and filters for function symbols only.

## Installation

```bash
uv sync
```

Or with pip:

```bash
pip install .
```

## Usage

```bash
lso [OPTIONS] [FILE|DIRECTORY]
```

### Arguments

- `FILE` - Path to a specific `.so` file
- `DIRECTORY` - Path to a directory (scans recursively for `.so` files)
- No argument - Scans current directory recursively

### Options

- `-s` - Include static/local functions (default: only global/exported functions)
- `-v` - Verbose mode (show file path for each function)
- `-h` - Print help message

## Examples

### Scan current directory
```bash
lso
```
Output:
```
malloc
free
pthread_create
my_custom_function
```

### Scan specific directory
```bash
lso /usr/lib/
```

### Scan specific .so file
```bash
lso /lib/x86_64-linux-gnu/libc.so.6
```

### Include static functions
```bash
lso -s mylib.so
```
Output:
```
public_function
_internal_helper
static_function
```

### Verbose mode
```bash
lso -v /usr/lib/
```
Output:
```
/usr/lib/libssl.so.3: SSL_read
/usr/lib/libssl.so.3: SSL_write
/usr/lib/libcrypto.so.3: EVP_EncryptInit
/usr/lib/libcrypto.so.3: EVP_DecryptInit
```
