import zipfile
import logging
from file import File


class ZipFileProcessor:
    def __init__(
        self,
        zip_file_path: str,
        logger: logging.Logger | None = None,
    ) -> None:
        """
        Initialize the ZipFileProcessor with a local zip file and an optional logger.
        :param zip_file_path: str, path to the local zip file
        :param logger: logging.Logger, optional logger for logging messages
        """
        self.zip_file_path: str = zip_file_path
        self.logger: logging.Logger | None = logger

    def _log(self, message: str) -> None:
        """
        Log a message if a logger is provided.
        :param message: str, message to log
        """
        if self.logger:
            self.logger.info(message)
        else:
            print(message)

    def get_all_files(
        self,
        allowed_extensions: list[str] | None = None,
        verbose: bool = False,
    ) -> list[File]:
        """
        Extract all files from the local zip file and filter by allowed extensions.
        :param allowed_extensions: list of allowed file extensions
        :param verbose: bool, if True, print the file paths
        :return: list of filtered File objects
        """
        if allowed_extensions is None:
            allowed_extensions = []

        for i, ext in enumerate(allowed_extensions):
            allowed_extensions[i] = ext.lstrip(".")

        file_objects: list[File] = []

        with zipfile.ZipFile(self.zip_file_path, "r") as zip_ref:
            # List all files in the zip archive
            files = zip_ref.namelist()

            for file_path in files:
                # Check if the file has an allowed extension
                file_extension: str = (
                    file_path.split(".")[-1] if "." in file_path else ""
                )

                if file_path.startswith("__MACOSX"):
                    continue

                if allowed_extensions and file_extension not in allowed_extensions:
                    continue

                if verbose:
                    self._log(f"File path: {file_path}")

                file_objects.append(File(path=file_path, extension=file_extension))

        if verbose:
            self._log(f"Found {len(file_objects)} files in zip: {self.zip_file_path}")

        for file in file_objects:
            file.content = self.get_file_content(file.path, verbose=verbose)

        return file_objects

    def get_file_content(self, file_path: str, verbose: bool = False) -> str:
        """
        Get the content of a file from the local zip file.
        :param file_path: str, path to the file in the zip
        :param verbose: bool, if True, print the file content
        :return: str, content of the file
        """
        with zipfile.ZipFile(self.zip_file_path, "r") as zip_ref:
            with zip_ref.open(file_path) as file:
                content = file.read().decode("utf-8")

                if verbose:
                    self._log(f"Fetched content from file {file_path}")

                return content
