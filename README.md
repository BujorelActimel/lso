# ls-so

like the ls command, but instead of listing directories and files, it 
lists the available functions from a shared object on linux

## Usage

lso [FILE/DIRECTORY]

## Examples:

No file/directory specified - scan the current directory for all the .so files and list the functions and the files they are from
```bash
lso
```

Directory as argument - scan the directory for all the .so files and list the functions and the files they are from
```bash
lso dir/
```

Shared object file as argument - scan the .so file and list the functions from this file
```bash
lso file.so
```
