# import libraries
import os
import shutil
from .pretty_print import console_log, print_table, task_processing
from datetime import datetime
from pathlib import Path
from typing import NoReturn, TYPE_CHECKING, Union
from ._validation_util import _validate_confirmation_inputs

if TYPE_CHECKING:
    from pathlib import PosixPath


class Files:
    def __init__(self):
        self.base_dir = Path.cwd()
        self.home_dir = Path.home()

    def _verify_path_exists(self, path_to_verify: 'PosixPath') -> bool:
        """
        Validate if the given path exists.

        This function is not meant to be accessed directly but users but instead
        meant as a utility for validating other library functionality.

        Args:
            path_to_verify (PosixPath): pathlib.PosixPath to validate

        Returns:
            (bool): defaults to False
                True: return True if the path exists
                False: return False if the path does not exist
        """

        if path_to_verify.exists():
            return True

        else:
            raise FileNotFoundError(f"'{path_to_verify}' is not a valid path")

    def _verify_path_size():
        # TODO
        return

    def _convert_path_type(self, path_to_convert: str) -> 'PosixPath':
        """
        Convert a sting type path to a PosixPath type.

        This function is not meant to be accessed directly but users but instead
        meant as a utility for validating other library functionality.

        Args:
            path_to_convert (str): path to file or directory

        Returns:
            path_to_convert (PosixPath): provided path converted to PosixPath type
        """

        if isinstance(path_to_convert, str):
            path_to_convert = Path(path_to_convert)

        return path_to_convert

    def update_path(self, attribute_name: str, attribute_path: str, is_dir: bool = False, is_file: bool = False) -> NoReturn:
        """
        Add a new attribute to the Files object and store a PosixPath value or
        update an existing path.
        Optionally, create the path at the same time as assigning the attribute.

        Args:
            attribute_name (str): name of the attribute to reference the path from the Files object
            attribute_path (str): string path to assign to the attribute

        Optional Args:
            is_dir (bool): set to True to create the path as a directory; defaults to False
            is_file (bool): set to True to create the path as a file; defaults to False

        Returns:
            NoReturn

        Raises:
            TypeError: raised if both is_dir and is_file are True
        """

        attribute_path = self._convert_path_type(attribute_path)
        setattr(self, attribute_name, attribute_path)

        if is_dir and is_file:
            raise TypeError('Both is_dir and is_file are true. Only one option may be selected.')

        elif is_dir:
            self.create_new_directory(attribute_path)

        elif is_file:
            self.create_new_file(attribute_path)

    def create_new_directory(self, dir_to_create: str) -> 'Path':
        """
        Create a new directory.
        """

        # if the directory provided is a string then convert it to a pathlib.PosixPath
        dir_to_create = self._convert_path_type(dir_to_create)

        # create the path
        dir_to_create.mkdir(parents=True, exist_ok=True)

    def create_new_file(self, file_to_create: str) -> 'Path':
        """
        Create a new file.
        """

        # if the file provided is a string then convert it to a pathlib.PosixPath
        file_to_create = self._convert_path_type(file_to_create)

        # create the path
        file_to_create.touch(exist_ok=True)

    def read_file(self, file_to_read: Union['PosixPath', str]) -> NoReturn:
        # TODO
        return

    def remove_directory(self, dir_to_rm: Union['PosixPath', str], force: bool = False) -> NoReturn:
        """
        Remove a directory and all of its contents.

        Args:
            dir_to_rm (PosixPath || str): path to directory

        Optional Args:
            force (bool): do not prompt for confirmation; defaults to False

        Returns:
            NoReturn
        """

        dir_to_rm = self._convert_path_type(dir_to_rm)
        self._verify_path_exists(dir_to_rm)

        if dir_to_rm.is_dir():
            confirmation = None
            if not force:
                while isinstance(confirmation, type(None)):
                    user_input = input(f"Remove '{dir_to_rm}' and all of its contents? (q to quit) [y/n]: ")
                    confirmation = _validate_confirmation_inputs(user_input)

                    if isinstance(confirmation, bool):
                        break

            if force or confirmation:
                shutil.rmtree(dir_to_rm)
                console_log(f"Remove directory: '{dir_to_rm}' successful.", 'informational')

    def remove_file(self, file_to_rm: Union['PosixPath', str], force: bool = False) -> NoReturn:
        """
        Remove a file.

        Args:
            file_to_rm (PosixPath || str): path to file

        Optional Args:
            force (bool): do not prompt for confirmation; defaults to False

        Returns:
            NoReturn
        """

        file_to_rm = self._convert_path_type(file_to_rm)
        self._verify_path_exists

        if file_to_rm.is_file():
            confirmation = None
            if not force:
                while isinstance(confirmation, type(None)):
                    user_input = input(f"Remove '{file_to_rm}'? (q to quit) [y/n]: ")
                    confirmation = _validate_confirmation_inputs(user_input)

                    if isinstance(confirmation, bool):
                        break

            if force or confirmation:
                os.remove(file_to_rm)
                console_log(f"Remove file: '{file_to_rm}' successful.", 'informational')

    def rotate_files(self, directory_to_clean: Union['PosixPath', str], days_old: int = 14, force: bool = False) -> NoReturn:
        """
        Remove files from a directory older than the specified days.
        Files older than the days_old parameters will be removed.

        Args:
            directory_to_clean (PosixPath || str): path to directory to remove files from

        Optional Args:
            days_old (int): number of days worth of files to keep; defaults to 14 days
            force (bool): do not prompt for confirmation; defaults to False

        Returns:
            NoReturn
        """

        directory_to_clean = self._convert_path_type(directory_to_clean)
        self._verify_path_exists(directory_to_clean)

        today = datetime.today()
        all_files_to_remove = list()
        for sub_file in directory_to_clean.iterdir():
            if sub_file.is_file():
                created_date = datetime.fromtimestamp(os.path.getmtime(sub_file))
                file_age = today - created_date

                if file_age.days > days_old:
                    all_files_to_remove.append(
                        (sub_file.name, str(created_date))
                    )

        if len(all_files_to_remove) > 0:
            if not force:
                console_log('-- FILES TO REMOVE --', 'warning')
                console_log(f'Source path: {directory_to_clean}')
                print_table(sorted(all_files_to_remove, reverse=True), ['File Name', 'Last Modified Date'], len(all_files_to_remove))

                confirmation = None
                while isinstance(confirmation, type(None)):
                    user_input = input('The above files will be removed. Continue? [y/n] (q to quit): ')
                    confirmation = _validate_confirmation_inputs(user_input)

                    if not confirmation:
                        print('false')
                    elif confirmation is None:
                        print('none')

            if force or confirmation:
                with task_processing('Cleaning up old files'):
                    for old_file in all_files_to_remove:
                        self.remove_file(Path.joinpath(directory_to_clean, old_file[0]))

        else:
            console_log(f'No files older than {days_old} days old found. Nothing to remove.', 'informational')

    def write_file():
        # TODO
        return


# Global create and fetch


def create_global_files_object() -> 'Files':
    """
    Instantiate a global Files object.

    Returns:
        FILES_OBJ (Files): instantiated Files object
    """

    global FILES_OBJ  # declare the global
    FILES_OBJ = Files()  # assign the global

    return FILES_OBJ


def get_global_files_object() -> 'Files':
    """
    Get the global Files object without instantiating a new instance.

    Returns:
        FILES_OBJ (Files): instantiated Files object

    Raises:
        NameError: raised if FILES_OBJ has not been created
    """

    # verify that the global FILES_OBJ has been created first
    if 'FILES_OBJ' not in globals():
        raise NameError("A global Files object has not yet been instantiated. Use 'create_global_files_object' to create one.")

    return FILES_OBJ
