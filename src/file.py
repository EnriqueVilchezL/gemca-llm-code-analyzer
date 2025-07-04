class File:
    def __init__(self, path: str, extension: str = None, content: str = None):
        """
        Initialize a File object.
        :param path: str, path to the file
        :param extension: str, file extension
        :param content: str, file content
        """
        self.path = path
        self.extension = extension
        self.content = content

    def __repr__(self):
        return f"File(path={self.path}, extension={self.extension}, content={self.content})"
