import os
import random

import pytest

from helpers import generate_random_string


class TestDirectories:
    @pytest.mark.parametrize("create_testdir", [generate_random_string()], indirect=True)
    def test_create_valid_directory(self, create_testdir):
        """Check that it is possible to create a directory with unique name and allowed length."""
        tmpdir, dir_name = create_testdir
        tmpdir_content = tmpdir.listdir()

        assert len(tmpdir_content) == 1, "More than one directory were created under `tmpdir`"
        assert tmpdir_content[0] == os.path.join(tmpdir, dir_name), "Directory name mismatch"

    @pytest.mark.parametrize("create_testdir", [generate_random_string()], indirect=True)
    def test_create_directory_with_existing_name(self, create_testdir):
        """Check that creation of directory with existing name isn't allowed."""
        tmpdir, dir_name = create_testdir

        try:
            os.mkdir(os.path.join(tmpdir, dir_name))
        except Exception as e:
            assert e.__class__ == FileExistsError, f"Test failed with unexpected error: {e.__class__.__name__}"
        else:
            pytest.xfail("Managed to create a folder with existing name")

    @pytest.mark.usefixtures('remove_testdir')
    @pytest.mark.parametrize('length', [0, random.randint(1, 255), random.randint(256, 4096)])
    def test_create_directory_with_custom_length(self, tmpdir, length):
        """Check creation of directories with custom length - 0, 1-255, >256."""
        dir_name = generate_random_string(length)

        try:
            os.mkdir(os.path.join(tmpdir, dir_name))
        except Exception as e:
            if length == 0:
                assert e.__class__ == FileExistsError, f"Test failed with unexpected error: {e.__class__.__name__}"
            elif length > 255:
                assert e.__class__ == OSError, f"Test failed with unexpected error: {e.__class__.__name__}"
            else:
                pytest.xfail(f"Test failed with unexpected error: {e.__class__.__name__}")
        else:
            if 1 <= length <= 255:
                assert len(tmpdir.listdir()) == 1, "More than 1 directory was created"
            else:
                pytest.xfail("Managed to create a directory with unsupported length")

    @pytest.mark.usefixtures('remove_testdir')
    @pytest.mark.parametrize('result_length', [0, random.randint(1, 255), random.randint(256, 4096)])
    def test_rename_directory(self, tmpdir, result_length):
        """Check renaming of the directories to empty string, valid string, too long string"""
        dir_name = generate_random_string()
        tmpdir.mkdir(dir_name)
        os.chdir(tmpdir)  # to avoid using os.path.join(...) for `dir_name` and `new_dir_name`
        new_dir_name = generate_random_string(result_length)

        try:
            os.rename(dir_name, new_dir_name)
        except Exception as e:
            if result_length == 0:
                assert e.__class__ == FileNotFoundError, f"Test failed with unexpected error: {e.__class__.__name__}"
            elif result_length > 255:
                assert e.__class__ == OSError, f"Test failed with unexpected error: {e.__class__.__name__}"
            else:
                pytest.xfail(f"Test failed with unexpected error: {e.__class__.__name__}")
        else:
            if 1 <= result_length <= 255:
                assert len(tmpdir.listdir()) == 1, "More than one directory were created under `tmpdir`"
            else:
                pytest.xfail("Managed to rename a directory with unsupported length")

    @pytest.mark.usefixtures("create_testdir")
    def test_move_directory(self, create_testdir):
        """Check moving of folder from one parent to another.
        Hierarchy before move: tmpdir -> test_dir -> child_dir
        After move: tmpdir -> test_dir, child_dir

        """
        tmpdir, dir_name = create_testdir
        child_dir_name = "child_dir"
        abs_child_path_before = os.path.join(tmpdir, dir_name, child_dir_name)
        abs_child_path_after = os.path.join(tmpdir, child_dir_name)
        os.mkdir(abs_child_path_before)
        os.replace(abs_child_path_before, abs_child_path_after)

        tmpdir_content = tmpdir.listdir()

        assert len(tmpdir_content) == 2, f"Wrong number of directories under `tmpdir`: {len(tmpdir_content)}"
        assert abs_child_path_after in tmpdir_content, f"No child directory `{child_dir_name}` under `tmpdir`"

    @pytest.mark.usefixtures("create_testdir")
    def test_remove_existing_directory(self, create_testdir):
        """Check deletion of existing directory"""
        tmpdir, _ = create_testdir
        tmpdir.remove()

        assert not tmpdir.check(), "Temporary directory wasn't removed"

    def test_remove_not_existing_directory(self, tmpdir):
        """Check deletion of not existing directory"""
        tmpdir.remove()  # remove current directory

        try:
            os.rmdir(tmpdir)  # attempt to remove it again
        except Exception as e:
            assert e.__class__.__name__ == "FileNotFoundError",\
                f"Test failed with unexpected error: {e.__class__.__name__}"
        else:
            pytest.xfail("Managed to remove not existing directory")
