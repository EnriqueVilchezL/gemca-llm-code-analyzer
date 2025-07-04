import requests
import logging
from collections import deque

from file import File


class GitHubRepositoryFetcher:
    def __init__(
        self,
        repository: str,
        token: str | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        """
        Initialize the GitHubFetcher with a repository and an optional logger.
        :param repository: str, GitHub repository in the format 'owner/repo'
        :param logger: logging.Logger, optional logger for logging messages
        """
        self.repository: str = repository
        self.list_files_url: str = (
            "https://api.github.com/repos/{repository}/contents/{path}"
        )
        self.download_file_url: str = (
            "https://raw.githubusercontent.com/{repository}/{branch}/{file_path}"
        )
        self.logger: logging.Logger | None = logger
        self.token: str | None = token
        self.headers: dict[str, str] = (
            {"Authorization": f"token {self.token}"} if token else {}
        )

    def _log(self, message: str) -> None:
        """
        Log a message if a logger is provided.
        :param message: str, message to log
        """
        if self.logger:
            self.logger.info(message)
        else:
            print(message)

    def list_files(self, path: str = "", verbose: bool = False) -> list[File]:
        """
        List all files in the GitHub repository iteratively using a queue.
        :param path: str, path to the directory in the repository
        :param verbose: bool, if True, print the file paths
        :return: list of File objects
        """
        url: str = self.list_files_url.format(repository=self.repository, path=path)

        if verbose:
            self._log(f"Listing files in {self.repository} at path: {path}")

        # Initialize queue with the starting directory path
        queue = deque([path])
        files: list[str] = []

        while queue:
            current_path = queue.popleft()

            # Fetch the contents of the current directory
            response = requests.get(
                url.format(repository=self.repository, path=current_path),
                headers=self.headers,
            )
            response.raise_for_status()

            items: list[dict] = response.json()

            for item in items:
                if item["type"] == "file":
                    files.append(item["path"])
                elif item["type"] == "dir":
                    queue.append(item["path"])

        if verbose:
            self._log(f"Found {len(files)} files in {self.repository} at path: {path}")

        file_objects: list[File] = []
        for file_path in files:
            if verbose:
                print(f"File path: {file_path}")
            file_extension: str | None = (
                file_path.split(".")[-1] if "." in file_path else None
            )
            file_objects.append(File(path=file_path, extension=file_extension))

        return file_objects

    def get_all_files(
        self,
        allowed_extensions: list[str] | None = None,
        verbose: bool = False,
    ) -> list[File]:
        """
        Get all files in the GitHub repository recursively.
        :param allowed_extensions: list of allowed file extensions
        :param verbose: bool, if True, print the file paths
        :return: list of filtered File objects
        """
        if allowed_extensions is None:
            allowed_extensions = []

        files: list[File] = self.list_files(verbose=verbose)
        filtered_files: list[File] = [
            file
            for file in files
            if file.extension
            and any(file.extension.endswith(ext) for ext in allowed_extensions)
        ]

        for file in filtered_files:
            file.content = self.get_file_content(file.path, verbose=verbose)

        if verbose:
            if allowed_extensions:
                self._log(
                    f"Got {len(filtered_files)} files with allowed extensions {allowed_extensions} in {self.repository}"
                )
            else:
                self._log(f"Got {len(filtered_files)} files in {self.repository}")

        return filtered_files

    def get_file_content(
        self, file_path: str, branch: str = "master", verbose: bool = False
    ) -> str:
        """
        Gets a file from the GitHub repository.
        :param file_path: str, path to the file in the repository
        :param branch: str, branch name
        :param verbose: bool, if True, print the file content
        :return: str, content of the file
        """
        url: str = self.download_file_url.format(
            repository=self.repository, branch=branch, file_path=file_path
        )

        if verbose:
            self._log(f"Fetching file from {url}")

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        if verbose:
            self._log(f"Fetched file content from {url}")

        return response.text
