import pytest
from pathlib import Path
import lso


class TestParseSingleFile:
    def test_parse_simple_so_returns_all_functions(self, simple_so):
        result = lso.parse_so_file(simple_so, include_static=False)

        assert "add" in result
        assert "subtract" in result
        assert "multiply" in result
        assert "hello_world" in result

    def test_parse_mixed_so_without_static_flag(self, mixed_so):
        result = lso.parse_so_file(mixed_so, include_static=False)

        assert "public_function" in result
        assert "another_public" in result

        assert "helper" not in result
        assert "internal_calc" not in result
        assert "cleanup" not in result

    def test_parse_mixed_so_with_static_flag(self, mixed_so):
        result = lso.parse_so_file(mixed_so, include_static=True)

        assert "public_function" in result
        assert "another_public" in result

        assert "helper" in result
        assert "internal_calc" in result
        assert "cleanup" in result

    def test_parse_excludes_variables(self, with_vars_so):
        result = lso.parse_so_file(with_vars_so, include_static=False)

        assert "increment_counter" in result
        assert "get_counter" in result
        assert "reset_counter" in result

        assert "global_counter" not in result
        assert "global_message" not in result
        assert "global_pi" not in result

    def test_parse_empty_so(self, empty_so):
        result = lso.parse_so_file(empty_so, include_static=False)

        assert "add" not in result
        assert "multiply" not in result

    def test_parse_nonexistent_file(self):
        with pytest.raises(FileNotFoundError):
            lso.parse_so_file("/nonexistent/file.so", include_static=False)

    def test_parse_non_elf_file(self, tmp_path):
        fake_so = tmp_path / "fake.so"
        fake_so.write_text("This is not an ELF file")

        with pytest.raises(Exception):
            lso.parse_so_file(str(fake_so), include_static=False)


class TestDirectoryScanning:
    def test_find_so_files_in_fixtures_dir(self, fixtures_dir):
        result = lso.find_so_files(str(fixtures_dir))

        assert len(result) >= 4
        so_names = [Path(p).name for p in result]
        assert "simple.so" in so_names
        assert "mixed.so" in so_names
        assert "with_vars.so" in so_names
        assert "empty.so" in so_names

    def test_find_so_files_excludes_non_so(self, tmp_path):
        (tmp_path / "test.so").touch()
        (tmp_path / "test.c").touch()
        (tmp_path / "Makefile").touch()
        (tmp_path / "README.md").touch()

        result = lso.find_so_files(str(tmp_path))

        assert len(result) == 1
        assert result[0].endswith("test.so")

    def test_find_so_files_recursive(self, tmp_path):
        (tmp_path / "lib1.so").touch()
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "lib2.so").touch()
        nested = subdir / "nested"
        nested.mkdir()
        (nested / "lib3.so").touch()

        result = lso.find_so_files(str(tmp_path))

        assert len(result) == 3
        so_names = [Path(p).name for p in result]
        assert "lib1.so" in so_names
        assert "lib2.so" in so_names
        assert "lib3.so" in so_names

    def test_find_versioned_so_files(self, tmp_path):
        (tmp_path / "libssl.so").touch()
        (tmp_path / "libssl.so.3").touch()
        (tmp_path / "libc.so.6").touch()
        (tmp_path / "libpthread.so.0").touch()
        (tmp_path / "libfoo.so.1.2.3").touch()
        (tmp_path / "notlib.txt").touch()

        result = lso.find_so_files(str(tmp_path))

        assert len(result) == 5
        so_names = [Path(p).name for p in result]
        assert "libssl.so" in so_names
        assert "libssl.so.3" in so_names
        assert "libc.so.6" in so_names
        assert "libpthread.so.0" in so_names
        assert "libfoo.so.1.2.3" in so_names
        assert "notlib.txt" not in so_names

    def test_scan_directory_aggregates_functions(self, fixtures_dir):
        result = lso.scan_directory(str(fixtures_dir), include_static=False, verbose=False)

        assert "add" in result
        assert "multiply" in result
        assert "public_function" in result
        assert "get_counter" in result

    def test_scan_directory_with_verbose(self, fixtures_dir):
        result = lso.scan_directory(str(fixtures_dir), include_static=False, verbose=True)

        assert len(result) > 0
        assert all(isinstance(item, tuple) and len(item) == 2 for item in result)

        files = set(item[0] for item in result)
        assert any("simple.so" in f for f in files)
        assert any("mixed.so" in f for f in files)

    def test_scan_empty_directory(self, tmp_path):
        result = lso.scan_directory(str(tmp_path), include_static=False, verbose=False)

        assert result == []

    def test_scan_directory_with_static_flag(self, fixtures_dir):
        without_static = lso.scan_directory(str(fixtures_dir), include_static=False, verbose=False)
        with_static = lso.scan_directory(str(fixtures_dir), include_static=True, verbose=False)

        assert len(with_static) > len(without_static)
        assert "helper" not in without_static
        assert "helper" in with_static
