import argparse
import os
from pathlib import Path
from elftools.elf.elffile import ELFFile
from elftools.common.exceptions import ELFError


class InvalidELFFileError(Exception):
    pass


def parse_so_file(path, include_static):
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    functions = []

    try:
        with open(path, 'rb') as f:
            try:
                elffile = ELFFile(f)
            except ELFError as e:
                raise InvalidELFFileError(f"Invalid ELF file: {path}") from e

            symtab = elffile.get_section_by_name('.symtab')
            if not symtab:
                symtab = elffile.get_section_by_name('.dynsym')

            if symtab:
                for symbol in symtab.iter_symbols():
                    if symbol['st_info']['type'] == 'STT_FUNC':
                        binding = symbol['st_info']['bind']

                        if include_static:
                            if binding in ('STB_GLOBAL', 'STB_LOCAL', 'STB_WEAK'):
                                functions.append(symbol.name)
                        else:
                            if binding in ('STB_GLOBAL', 'STB_WEAK'):
                                functions.append(symbol.name)

    except FileNotFoundError:
        raise
    except InvalidELFFileError:
        raise
    except Exception as e:
        raise InvalidELFFileError(f"Error parsing ELF file: {path}") from e

    return functions


def find_so_files(directory):
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")

    so_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.so') or '.so.' in file:
                so_files.append(os.path.join(root, file))

    return so_files


def scan_directory(path, include_static, verbose):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Path not found: {path}")

    so_files = find_so_files(path)

    if verbose:
        result = []
        for so_file in so_files:
            try:
                functions = parse_so_file(so_file, include_static)
                for func in functions:
                    result.append((so_file, func))
            except (InvalidELFFileError, Exception):
                pass
        return result
    else:
        result = []
        for so_file in so_files:
            try:
                functions = parse_so_file(so_file, include_static)
                result.extend(functions)
            except (InvalidELFFileError, Exception):
                pass
        return result


def format_output(data, verbose):
    if not data:
        return ""

    if verbose:
        lines = []
        for filepath, func in data:
            lines.append(f"{filepath}: {func}")
        return "\n".join(lines)
    else:
        sorted_funcs = sorted(data)
        return "\n".join(sorted_funcs)


def parse_arguments(args):
    parser = argparse.ArgumentParser(
        description='List functions from shared objects on Linux'
    )

    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Path to .so file or directory (default: current directory)'
    )

    parser.add_argument(
        '-s',
        dest='include_static',
        action='store_true',
        help='Include static/local functions'
    )

    parser.add_argument(
        '-v',
        dest='verbose',
        action='store_true',
        help='Verbose mode (show file path for each function)'
    )

    return parser.parse_args(args)


def main():
    import sys
    args = parse_arguments(sys.argv[1:])

    path = args.path

    if os.path.isfile(path):
        try:
            functions = parse_so_file(path, args.include_static)
            output = format_output(functions, False)
            if output:
                print(output)
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        except InvalidELFFileError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    elif os.path.isdir(path):
        try:
            result = scan_directory(path, args.include_static, args.verbose)
            output = format_output(result, args.verbose)
            if output:
                print(output)
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Error: Path not found: {path}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
