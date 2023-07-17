"""Pytest test suite for the filesystem module."""

import pathlib

import pytest
from hypothesis import given, strategies
from rich.tree import Tree

from chasten import filesystem


def test_valid_directory() -> None:
    """Confirm that a valid directory is found."""
    directory_str = "./tests/"
    directory = pathlib.Path(directory_str)
    confirmation = filesystem.confirm_valid_directory(directory)
    assert confirmation is True


def test_invalid_directory() -> None:
    """Confirm that a valid directory is found."""
    directory_str = "./testsNOT/"
    directory = pathlib.Path(directory_str)
    confirmation = filesystem.confirm_valid_directory(directory)
    assert confirmation is False


def test_valid_file() -> None:
    """Confirm that a valid directory is found."""
    file_str = "./tests/test_filesystem.py"
    this_file = pathlib.Path(file_str)
    confirmation = filesystem.confirm_valid_file(this_file)
    assert confirmation is True


def test_invalid_file() -> None:
    """Confirm that a valid directory is found."""
    file_str = "./tests/test_filesystemNOT.py"
    this_file_not = pathlib.Path(file_str)
    confirmation = filesystem.confirm_valid_file(this_file_not)
    assert confirmation is False


@given(directory=strategies.builds(pathlib.Path))
@pytest.mark.fuzz
def test_fuzz_confirm_valid_directory_using_builds(directory: pathlib.Path) -> None:
    """Confirm that the function does not crash."""
    filesystem.confirm_valid_directory(directory=directory)


@given(file=strategies.builds(pathlib.Path))
@pytest.mark.fuzz
def test_fuzz_confirm_valid_file_using_builds(file: pathlib.Path) -> None:
    """Confirm that the function does not crash."""
    filesystem.confirm_valid_file(file=file)


def test_create_directory_tree(tmpdir):
    """Confirm that creation of the textual directory tree works."""
    # create a temporary directory
    tmp_dir = pathlib.Path(tmpdir)
    # create some files and directories
    (tmp_dir / "file1.txt").touch()
    (tmp_dir / "subdir1").mkdir()
    (tmp_dir / "subdir2").mkdir()
    (tmp_dir / "subdir2" / "file2.txt").touch()
    # call the function under test
    tree = filesystem.create_directory_tree_visualization(tmp_dir)
    # confirm that the output is a rich tree object
    assert isinstance(tree, Tree)
    # confirm the directory name in root node
    assert tree.label == f":open_file_folder: {tmp_dir.as_posix()}"
    # confirm that the child nodes contain the expected dirs and files
    dirs = [node.label for node in tree.children if ":open_file_folder:" in node.label]  # type: ignore
    files = [node.label for node in tree.children if ":page_facing_up:" in node.label]  # type: ignore
    assert set(dirs) == {
        f":open_file_folder: {p.name}" for p in tmp_dir.iterdir() if p.is_dir()
    }
    assert set(files) == {
        f":page_facing_up: {p.name}" for p in tmp_dir.iterdir() if p.is_file()
    }


@given(directory=strategies.builds(pathlib.Path))
@pytest.mark.fuzz
def test_fuzz_create_directory_tree(directory):
    """Confirm that the file system directory tree creation works."""
    tree = filesystem.create_directory_tree_visualization(directory)
    # confirm that it is a rich tree object
    assert isinstance(tree, Tree)
    # confirm that it has the fully-qualified name as the main label
    assert tree.label == f":open_file_folder: {directory.as_posix()}"
    dirs = []
    files = []
    # build up a list of all of the directories and files
    for node in tree.children:
        if ":open_file_folder:" in node.label:  # type: ignore
            dirs.append(node.label[19:])  # type: ignore
        else:
            files.append(node.label[17:])  # type: ignore
    # confirm that it contains all of the directory and file names
    assert set(dirs) == set(p.name for p in directory.iterdir() if p.is_dir())
    assert set(files) == set(p.name for p in directory.iterdir() if p.is_file())
