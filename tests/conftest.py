import pytest
import subprocess
from pathlib import Path


@pytest.fixture(scope="session", autouse=True)
def build_test_shared_objects():
    fixtures_dir = Path(__file__).parent / "fixtures"

    result = subprocess.run(
        ["make", "clean"],
        cwd=fixtures_dir,
        capture_output=True,
        text=True
    )

    result = subprocess.run(
        ["make", "all"],
        cwd=fixtures_dir,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        pytest.fail(f"Failed to build test shared objects:\n{result.stderr}")

    expected_sos = ["simple.so", "mixed.so", "with_vars.so", "empty.so"]
    for so_file in expected_sos:
        so_path = fixtures_dir / so_file
        if not so_path.exists():
            pytest.fail(f"Expected .so file not created: {so_path}")

    yield

    subprocess.run(["make", "clean"], cwd=fixtures_dir, capture_output=True)


@pytest.fixture
def fixtures_dir():
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def simple_so(fixtures_dir):
    return str(fixtures_dir / "simple.so")


@pytest.fixture
def mixed_so(fixtures_dir):
    return str(fixtures_dir / "mixed.so")


@pytest.fixture
def with_vars_so(fixtures_dir):
    return str(fixtures_dir / "with_vars.so")


@pytest.fixture
def empty_so(fixtures_dir):
    return str(fixtures_dir / "empty.so")
