import os
import random

import pytest

from helpers import create_file, generate_random_string


class TestFiles:
    @pytest.mark.parametrize("create_testfile", [generate_random_string()], indirect=True)
    def test_create_valid_file(self, create_testfile):
        """Check that it is possible to create a file with unique name and allowed length."""
        tmpdir, filename = create_testfile

        tmpdir_content = tmpdir.listdir()
        assert len(tmpdir_content) == 1, "More than one file under `tmpdir`"
        assert tmpdir_content[0] == os.path.join(tmpdir, filename), "Mismatch in filename"

    @pytest.mark.usefixtures('remove_testdir')
    @pytest.mark.parametrize('length', [0, random.randint(1, 255), random.randint(256, 4096)])
    def test_create_file_with_custom_length(self, tmpdir, length):
        """Check creation of files with custom length - 0, 1-255, >256."""
        os.chdir(tmpdir)
        filename = generate_random_string(length)

        try:
            create_file(filename)
        except Exception as e:
            if length == 0:
                assert e.__class__ == FileNotFoundError, f"Test failed with unexpected error: {e.__class__.__name__}"
            elif length > 255:
                assert e.__class__ == OSError, f"Test failed with unexpected error: {e.__class__.__name__}"
            else:
                pytest.xfail(f"Test failed with unexpected error: {e.__class__.__name__}")
        else:
            if 1 <= length <= 255:
                assert len(tmpdir.listdir()) == 1, "More than 1 file was created"
            else:
                pytest.xfail("Managed to create a file with unsupported length")

    @pytest.mark.usefixtures('remove_testdir')
    @pytest.mark.parametrize('result_length', [0, random.randint(1, 255), random.randint(256, 4096)])
    def test_rename_file(self, tmpdir, result_length):
        """Check renaming of the files to empty string, valid string, too long string"""
        os.chdir(tmpdir)
        filename = generate_random_string()
        create_file(filename)
        new_filename = generate_random_string(result_length)

        try:
            os.rename(filename, new_filename)
        except Exception as e:
            if result_length == 0:
                assert e.__class__ == FileNotFoundError, f"Test failed with unexpected error: {e.__class__.__name__}"
            elif result_length > 255:
                assert e.__class__ == OSError, f"Test failed with unexpected error: {e.__class__.__name__}"
            else:
                pytest.xfail(f"Test failed with unexpected error: {e.__class__.__name__}")
        else:
            if 1 <= result_length <= 255:
                assert len(tmpdir.listdir()) == 1, "More than 1 file was created"
            else:
                pytest.xfail("Managed to rename a file with unsupported length")

    @pytest.mark.usefixtures("create_testfile")
    def test_remove_existing_file(self, create_testfile):
        """Check deletion of existing file"""
        tmpdir, filename = create_testfile
        os.remove(os.path.join(tmpdir, filename))
        assert not len(tmpdir.listdir()), "Temporary file wasn't removed"

    @pytest.mark.usefixtures("create_testfile")
    def test_remove_not_existing_file(self, create_testfile):
        """Check deletion of not existing file"""
        tmpdir, filename = create_testfile
        os.remove(os.path.join(tmpdir, filename))  # remove the file

        try:
            os.remove(os.path.join(tmpdir, filename))  # attempt to remove it again
        except Exception as e:
            assert e.__class__.__name__ == "FileNotFoundError",\
                f"Test failed with unexpected error: {e.__class__.__name__}"
        else:
            pytest.xfail("Managed to remove not existing file")



