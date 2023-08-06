# import libraries
import configparser
import pytest

from json.decoder import JSONDecodeError
from munchie.file_muncher import FileMuncher
from pathlib import Path
from typing import Any, Dict, List, Union
from yaml.parser import ParserError
from yaml.scanner import ScannerError

FILES_OBJ = FileMuncher()
TEST_FILES = Path.joinpath(Path.cwd(), 'tests/_test-files')
TEST_READ_FILES = Path.joinpath(Path.cwd(), 'tests/_test-files/_read-files')
TEST_WRITE_FILES = Path.joinpath(Path.cwd(), 'tests/_test-files/_write-files')


def _get_test_contents(test_name: str) -> Union[Dict[str, Any], List[Any], None, str]:
    """
    Return the dictionary of test contents for validating.

    Args:
        test_name (str): the name of the function

    Returns:
        test_contents (dict | list | None | str): the valid contents based on the current test
    """

    test_contents = None  # placeholder for test_contents

    if test_name in ['csv']:
        # list of dictionaries
        test_contents = [
            {'Year': '2015', 'Make': 'Ford', 'Model': 'Focus', 'Cost': '14000'},
            {'Year': '2015', 'Make': 'Mazda', 'Model': 'Miata', 'Cost': '17000'}
        ]

    elif test_name in ['cfg', 'conf', 'ini', 'json']:
        # dictionary | dictionary of dictionaries
        test_contents = {
            'default': {'testing': 'True'},
            'vehicle one': {'year': '2015', 'make': 'Ford', 'model': 'Focus', 'cost': '14000'},
            'vehicle two': {'year': '2015', 'make': 'Mazda', 'model': 'Miata', 'cost': '17000'}
        }

    elif test_name in ['nfo', 'text', 'txt']:
        # list of strings
        test_contents = [
            'vehicle one:', 'year: 2015', 'make: Ford', 'model: Focus', 'cost: 14000', '',
            'vehicle two:', 'year: 2015', 'make: Mazda', 'model: Miata', 'cost: 17000'
        ]

    elif test_name in ['yaml', 'yml']:
        # dictionary of list and dictionaries
        test_contents = {
            'vehicles': ['2015 Ford Focus ST', '2015 Mazda Miata Club Edition'],
            'vehicle 1': {'Year': 2015, 'Make': 'Ford', 'Model': 'Focus', 'Cost': 14000},
            'vehicle 2': {'Year': 2015, 'Make': 'Mazda', 'Model': 'Miata', 'Cost': 17000}
        }

    return test_contents


# Verify default class attributes
# -------------------------------


def test_default_base_dir() -> None:
    """Validate the base directory."""

    assert FILES_OBJ.base_dir == Path.cwd()  # current working directory is the same from both files


def test_default_home_path() -> None:
    """Validate the home directory."""

    assert FILES_OBJ.home_dir == Path.home()  # user home directory is the same from both files


# Verify error messages
# ---------------------


def test__get_file_extension_not_supported() -> None:
    """Validate TypeError when an unsupported file extensionn is provided."""

    with pytest.raises(TypeError):                                # verify steps raise TypeError
        test_path = Path.joinpath(TEST_WRITE_FILES, 'test.test')  # set a new temp file path
        FILES_OBJ._get_file_extension(test_path)                  # get the file extension of the path


def test__get_file_extension_no_extension() -> None:
    """Validate AttributeError when path does not specify a file extension."""

    with pytest.raises(AttributeError):                      # verify steps raise TypeError
        test_path = Path.joinpath(TEST_WRITE_FILES, 'test')  # set a new temp file path
        FILES_OBJ._get_file_extension(test_path)             # get the file extension of the path


def test__read_csv_file_missing_header() -> None:
    """Validate IndexError when given an invalid csv format."""

    with pytest.raises(IndexError):
        test_path = Path.joinpath(TEST_READ_FILES, 'test_csv_error.csv')  # set a new temp file path
        FILES_OBJ.read_file(test_path)                                    # read in the file contents


def test__read_ini_file_missing_header() -> None:
    """Validate IndexError when given an invalid ini format."""

    with pytest.raises(configparser.ParsingError):                        # verify steps raise configparser.ParsingError
        test_path = Path.joinpath(TEST_READ_FILES, 'test_ini_error.ini')  # set a new temp file path
        FILES_OBJ.read_file(test_path)                                    # read in the file contents


def test__read_json_file_invalid_json() -> None:
    """Validate JSONDecodeError when given an invalid json format."""

    with pytest.raises(JSONDecodeError):                                    # verify steps raise JSONDecodeError
        test_path = Path.joinpath(TEST_READ_FILES, 'test_json_error.json')  # set a new temp file path
        FILES_OBJ.read_file(test_path)                                      # read in the file contents


def test__read_yaml_file_parser_error() -> None:
    """Validate ScannerError when given an invalid yaml format."""

    with pytest.raises(ParserError):                                               # verify steps raise ParserError
        test_path = Path.joinpath(TEST_READ_FILES, 'test_yaml_parser_error.yaml')  # set a new temp file path
        FILES_OBJ.read_file(test_path)                                             # read in the file contents


def test__read_yaml_file_scanner_error() -> None:
    """Validate ScannerError when given an invalid yaml format."""

    with pytest.raises(ScannerError):                                               # verify steps raise ScannerError
        test_path = Path.joinpath(TEST_READ_FILES, 'test_yaml_scanner_error.yaml')  # set a new temp file path
        FILES_OBJ.read_file(test_path)                                              # read in the file contents


def test_read_file_does_not_exist() -> None:
    """Validate FileNotFoundError error is raised when the given path does not exist."""

    with pytest.raises(FileNotFoundError):                                      # verify steps raise FileNotFoundError
        test_path = Path.joinpath(TEST_READ_FILES, 'test_does_not_exist.test')  # set a new temp file path
        FILES_OBJ.read_file(test_path)                                          # read in the file contents


def test_read_path_is_not_a_file() -> None:
    """Validate TypeError is raised when the path is not to a file."""

    with pytest.raises(TypeError):            # verify steps raise TypeError
        FILES_OBJ.read_file(TEST_READ_FILES)  # read in the file contents


def test_update_path_isdir_and_isfile() -> None:
    """Validate TypeError when both is_dir and is_file are True."""

    with pytest.raises(TypeError):                          # verify the steps raise a TypeError
        test_path = Path.joinpath(TEST_FILES, 'test_path')  # set a new temp file path
        # create a new class attribute set to the test path with both is_dir and is_file set to True
        FILES_OBJ.update_path(attribute_name='new_attr', attribute_path=test_path, is_dir=True, is_file=True)


def test__verify_path_exists_does_not_exist_error() -> None:
    """Validate FileNotFoundError is raised when the path does not exist."""

    with pytest.raises(FileNotFoundError):                            # verify the steps raise a FileNotFoundError
        test_path = Path.joinpath(TEST_READ_FILES, 'test_path.test')  # set a new temp file path
        FILES_OBJ._verify_path_exists(test_path)                      # check if the path exists


def test__verify_path_size_empty_file_error() -> None:
    """Validate EOFError is raised when the file has no contents."""

    with pytest.raises(EOFError):                                           # verify the steps raise a EOFError
        test_path = Path.joinpath(TEST_READ_FILES, 'empty_file_error.txt')  # set a new temp file path
        FILES_OBJ._verify_path_size(test_path)                              # check if the path has contents


# Verify functionality
# --------------------


def test_create_new_directory() -> None:
    """Validate creating a new directory."""

    test_path = Path.joinpath(TEST_FILES, 'test_create_new_directory')  # set a new temp directory path
    FILES_OBJ.create_new_directory(test_path)                           # use the class to create a new directory

    assert test_path.exists() is True                                   # verify the new directory exists
    FILES_OBJ.remove_directory(test_path, True)                         # cleanup after verification


def test_create_new_file() -> None:
    """Validate creating a new file."""

    test_path = Path.joinpath(TEST_FILES, 'create_new_file.temp')  # set a new temp file path
    FILES_OBJ.create_new_file(test_path)                           # use the class to create the new file

    assert test_path.exists() is True                              # verify the new file exists
    FILES_OBJ.remove_file(test_path, True)                         # cleanup after verification


def test_read_csv_file() -> None:
    """Validate reading a csv file."""

    test_path = Path.joinpath(TEST_READ_FILES, 'test_csv.csv')  # set a new temp file path
    test_read_contents = FILES_OBJ.read_file(test_path)         # read in the file contents
    valid_contents = _get_test_contents(test_name='csv')        # get the valid contents for comparison

    assert test_read_contents == valid_contents                 # verify the contents match


def test_read_cfg_file() -> None:
    """Validate reading a .cfg file."""

    test_path = Path.joinpath(TEST_READ_FILES, 'test_cfg.cfg')  # set a new temp file path
    test_read_contents = FILES_OBJ.read_file(test_path)         # read in the file contents
    valid_contents = _get_test_contents(test_name='cfg')        # get the valid contents for comparison

    assert test_read_contents == valid_contents                 # verify the contents match


def test_read_conf_file() -> None:
    """Validate reading a .conf file."""

    test_path = Path.joinpath(TEST_READ_FILES, 'test_conf.conf')  # set a new temp file path
    test_read_contents = FILES_OBJ.read_file(test_path)           # read in the file contents
    valid_contents = _get_test_contents(test_name='conf')         # get the valid contents for comparison

    assert test_read_contents == valid_contents                   # verify the contents match


def test_read_ini_file() -> None:
    """Validate reading a .ini file."""

    test_path = Path.joinpath(TEST_READ_FILES, 'test_ini.ini')  # set a new temp file path
    test_read_contents = FILES_OBJ.read_file(test_path)         # read in the file contents
    valid_contents = _get_test_contents(test_name='ini')        # get the valid contents for comparison

    assert test_read_contents == valid_contents                 # verify the contents match


def test_read_json_file() -> None:
    """Validate reading a .json file."""

    test_path = Path.joinpath(TEST_READ_FILES, 'test_json.json')  # set a new temp file path
    test_read_contents = FILES_OBJ.read_file(test_path)           # read in the file contents
    valid_contents = _get_test_contents(test_name='json')         # get the valid contents for comparison

    assert test_read_contents == valid_contents                   # verify the contents match


def test_read_nfo_file() -> None:
    """Validate reading a .nfo file."""

    test_path = Path.joinpath(TEST_READ_FILES, 'test_nfo.nfo')  # set a new temp file path
    test_read_contents = FILES_OBJ.read_file(test_path)         # read in the file contents
    valid_contents = _get_test_contents(test_name='nfo')        # get the valid contents for comparison

    assert test_read_contents == valid_contents                 # verify the contents match


def test_read_text_file() -> None:
    """Validate reading a .text file."""

    test_path = Path.joinpath(TEST_READ_FILES, 'test_text.text')  # set a new temp file path
    test_read_contents = FILES_OBJ.read_file(test_path)           # read in the file contents
    valid_contents = _get_test_contents(test_name='text')         # get the valid contents for comparison

    assert test_read_contents == valid_contents                   # verify the contents match


def test_read_txt_file() -> None:
    """Validate reading a .txt file."""

    test_path = Path.joinpath(TEST_READ_FILES, 'test_txt.txt')  # set a new temp file path
    test_read_contents = FILES_OBJ.read_file(test_path)         # read in the file contents
    valid_contents = _get_test_contents(test_name='txt')        # get the valid contents for comparison

    assert test_read_contents == valid_contents                 # verify the contents match


def test_read_yaml_file() -> None:
    """Validate reading a .yaml file."""

    test_path = Path.joinpath(TEST_READ_FILES, 'test_yaml.yaml')  # set a new temp file path
    test_read_contents = FILES_OBJ.read_file(test_path)           # read in the file contents
    valid_contents = _get_test_contents(test_name='yaml')         # get the valid contents for comparison

    assert test_read_contents == valid_contents                   # verify the contents match


def test_read_yml_file() -> None:
    """Validate reading a .yml file."""

    test_path = Path.joinpath(TEST_READ_FILES, 'test_yml.yml')  # set a new temp file path
    test_read_contents = FILES_OBJ.read_file(test_path)         # read in the file contents
    valid_contents = _get_test_contents(test_name='yml')        # get the valid contents for comparison

    assert test_read_contents == valid_contents                 # verify the contents match


def test_remove_directory() -> None:
    """Validate removing a directory and the contents."""

    test_path = Path.joinpath(TEST_FILES, 'test_remove_directory')                     # set a new temp directory path
    FILES_OBJ.create_new_directory(test_path)                                          # use the class to create a new directory

    count = 0                                                                          # placeholder for count
    while count < 10:                                                                  # loop until count is equal to 10
        FILES_OBJ.create_new_file(Path.joinpath(test_path, f'test_file{count}.test'))  # create a new file for each count
        count += 1                                                                     # increment the count

    FILES_OBJ.remove_directory(test_path, True)                                        # cleanup after verification
    assert test_path.exists() is False                                                 # verify the new directory does not exist


def test_remove_file() -> None:
    """Validate removing a file."""

    test_path = Path.joinpath(TEST_FILES, 'test_remove_file.temp')  # set a new temp file path
    FILES_OBJ.create_new_file(test_path)                            # use the class to create the new file
    FILES_OBJ.remove_file(test_path, True)                          # cleanup after verification

    assert test_path.exists() is False                              # verify the new file does not exist


def test_rotate_files() -> None:
    """Validate rotating files."""

    test_path = Path.joinpath(TEST_FILES, 'test_remove_directory')                     # set a new temp directory path
    FILES_OBJ.create_new_directory(test_path)                                          # use the class to create a new directory

    count = 0                                                                          # placeholder for count
    while count < 10:                                                                  # loop until count is equal to 10
        FILES_OBJ.create_new_file(Path.joinpath(test_path, f'test_file{count}.test'))  # create a new file for each count
        count += 1                                                                     # increment the count

    FILES_OBJ.rotate_files(test_path, days_old=0, force=True)                          # cleanup after verification

    count_of_files = int(0)                                                            # placeholder for count of remaining files
    for sub_file in test_path.iterdir():                                               # begin loop over the directory contents
        if sub_file.is_file():                                                         # if the item in the directory is a file
            count_of_files += 1                                                        # add the count to remaining

    assert count_of_files == 0                                                         # verify no files are remaining in the directory
    FILES_OBJ.remove_directory(test_path, True)                                        # cleanup after verification


def test_update_path_add_new_attribute() -> None:
    """Validate adding new class attributes."""

    test_path = Path.joinpath(TEST_FILES, 'test_path')  # set a new temp file path
    FILES_OBJ.update_path('new_attr', test_path)        # create a new class attribute set to the test path

    assert getattr(FILES_OBJ, 'new_attr') == test_path  # verify the new attribute path exists and is set to the test path


def test_update_path_modify_path() -> None:
    """Validate modifing the path to an existing attribute."""

    test_path = Path.joinpath(TEST_FILES, 'test_path')  # set a new temp file path
    FILES_OBJ.update_path('home_dir', test_path)        # create a new class attribute set to the test path

    assert getattr(FILES_OBJ, 'home_dir') == test_path  # verify the new attribute path exists and is set to the test path


def test_update_path_add_and_create_new_directory() -> None:
    """Validate adding a new class attribute and creating the directory path."""

    test_path = Path.joinpath(TEST_FILES, 'test_path')          # set a new temp file path
    FILES_OBJ.update_path('new_attr', test_path, is_dir=True)   # create a new class attribute set to the test path and create the directory

    assert getattr(FILES_OBJ, 'new_attr') == test_path          # verify the new attribute path exists and is set to the test path
    assert test_path.exists() is True                           # verify the path exists in the filesystem
    FILES_OBJ.remove_directory(test_path, True)                 # cleanup after verification


def test_update_path_add_and_create_new_file() -> None:
    """Validate adding a new class attribute and creating the file path."""

    test_path = Path.joinpath(TEST_FILES, 'test_path.test')     # set a new temp file path
    FILES_OBJ.update_path('new_attr', test_path, is_file=True)  # create a new class attribute set to the test path and create the file

    assert getattr(FILES_OBJ, 'new_attr') == test_path          # verify the new attribute path exists and is set to the test path
    assert test_path.exists() is True                           # verify the path exists in the filesystem
    FILES_OBJ.remove_file(test_path, True)                      # cleanup after verification


def test_write_csv_file() -> None:
    """Validate writing a .csv file."""

    test_path = Path.joinpath(TEST_WRITE_FILES, 'test_csv.csv')  # set a new temp file path
    test_write_contents = _get_test_contents('csv')              # get the valid contents for comparison
    FILES_OBJ.write_file(test_write_contents, test_path)         # write the contents to the test path

    assert test_path.exists() is True                            # verify the test path exists
    test_read_contents = FILES_OBJ.read_file(test_path)          # read in the file contents

    assert test_write_contents == test_read_contents             # verify the contents match
    FILES_OBJ.remove_file(test_path, force=True)                 # cleanup after verification


def test_write_cfg_file() -> None:
    """Validate writing a .cfg file."""

    test_path = Path.joinpath(TEST_WRITE_FILES, 'test_cfg.cfg')  # set a new temp file path
    test_write_contents = _get_test_contents('cfg')              # get the valid contents for comparison
    FILES_OBJ.write_file(test_write_contents, test_path)         # write the contents to the test path

    assert test_path.exists() is True                            # verify the test path exists
    test_read_contents = FILES_OBJ.read_file(test_path)          # read in the file contents

    assert test_write_contents == test_read_contents             # verify the contents match
    FILES_OBJ.remove_file(test_path, force=True)                 # cleanup after verification


def test_write_conf_file() -> None:
    """Validate writing a .conf file."""

    test_path = Path.joinpath(TEST_WRITE_FILES, 'test_conf.conf')  # set a new temp file path
    test_write_contents = _get_test_contents('conf')               # get the valid contents for comparison
    FILES_OBJ.write_file(test_write_contents, test_path)           # write the contents to the test path

    assert test_path.exists() is True                              # verify the test path exists
    test_read_contents = FILES_OBJ.read_file(test_path)            # read in the file contents

    assert test_write_contents == test_read_contents               # verify the contents match
    FILES_OBJ.remove_file(test_path, force=True)                   # cleanup after verification


def test_write_ini_file() -> None:
    """Validate writing a .ini file."""

    test_path = Path.joinpath(TEST_WRITE_FILES, 'test_ini.ini')  # set a new temp file path
    test_write_contents = _get_test_contents('ini')              # get the valid contents for comparison
    FILES_OBJ.write_file(test_write_contents, test_path)         # write the contents to the test path

    assert test_path.exists() is True                            # verify the test path exists
    test_read_contents = FILES_OBJ.read_file(test_path)          # read in the file contents

    assert test_write_contents == test_read_contents             # verify the contents match
    FILES_OBJ.remove_file(test_path, force=True)                 # cleanup after verification


def test_write_json_file() -> None:
    """Validate writing a .json file."""

    test_path = Path.joinpath(TEST_WRITE_FILES, 'test_json.json')  # set a new temp file path
    test_write_contents = _get_test_contents('json')               # get the valid contents for comparison
    FILES_OBJ.write_file(test_write_contents, test_path)           # write the contents to the test path

    assert test_path.exists() is True                              # verify the test path exists
    test_read_contents = FILES_OBJ.read_file(test_path)            # read in the file contents

    assert test_write_contents == test_read_contents               # verify the contents match
    FILES_OBJ.remove_file(test_path, force=True)                   # cleanup after verification


def test_write_nfo_file() -> None:
    """Validate writing a .nfo file."""

    test_path = Path.joinpath(TEST_WRITE_FILES, 'test_nfo.nfo')  # set a new temp file path
    test_write_contents = _get_test_contents('nfo')              # get the valid contents for comparison
    FILES_OBJ.write_file(test_write_contents, test_path)         # write the contents to the test path

    assert test_path.exists() is True                            # verify the test path exists
    test_read_contents = FILES_OBJ.read_file(test_path)          # read in the file contents

    assert test_write_contents == test_read_contents             # verify the contents match
    FILES_OBJ.remove_file(test_path, force=True)                 # cleanup after verification


def test_write_text_file() -> None:
    """Validate writing a .text file."""

    test_path = Path.joinpath(TEST_WRITE_FILES, 'test_text.text')  # set a new temp file path
    test_write_contents = _get_test_contents('text')               # get the valid contents for comparison
    FILES_OBJ.write_file(test_write_contents, test_path)           # write the contents to the test path

    assert test_path.exists() is True                              # verify the test path exists
    test_read_contents = FILES_OBJ.read_file(test_path)            # read in the file contents

    assert test_write_contents == test_read_contents               # verify the contents match
    FILES_OBJ.remove_file(test_path, force=True)                   # cleanup after verification


def test_write_txt_file() -> None:
    """Validate writing a .txt file."""

    test_path = Path.joinpath(TEST_WRITE_FILES, 'test_txt.txt')  # set a new temp file path
    test_write_contents = _get_test_contents('txt')              # get the valid contents for comparison
    FILES_OBJ.write_file(test_write_contents, test_path)         # write the contents to the test path

    assert test_path.exists() is True                            # verify the test path exists
    test_read_contents = FILES_OBJ.read_file(test_path)          # read in the file contents

    assert test_write_contents == test_read_contents             # verify the contents match
    FILES_OBJ.remove_file(test_path, force=True)                 # cleanup after verification


def test_write_yaml_file() -> None:
    """Validate writing a .yaml file."""

    test_path = Path.joinpath(TEST_WRITE_FILES, 'test_yaml.yaml')  # set a new temp file path
    test_write_contents = _get_test_contents('yaml')               # get the valid contents for comparison
    FILES_OBJ.write_file(test_write_contents, test_path)           # write the contents to the test path

    assert test_path.exists() is True                              # verify the test path exists
    test_read_contents = FILES_OBJ.read_file(test_path)            # read in the file contents

    assert test_write_contents == test_read_contents               # verify the contents match
    FILES_OBJ.remove_file(test_path, force=True)                   # cleanup after verification


def test_write_yml_file() -> None:
    """Validate writing a .yml file."""

    test_path = Path.joinpath(TEST_WRITE_FILES, 'test_yml.yml')  # set a new temp file path
    test_write_contents = _get_test_contents('yml')              # get the valid contents for comparison
    FILES_OBJ.write_file(test_write_contents, test_path)         # write the contents to the test path

    assert test_path.exists() is True                            # verify the test path exists
    test_read_contents = FILES_OBJ.read_file(test_path)          # read in the file contents

    assert test_write_contents == test_read_contents             # verify the contents match
    FILES_OBJ.remove_file(test_path, force=True)                 # cleanup after verification
