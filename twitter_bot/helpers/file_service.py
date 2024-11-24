from loguru import logger
from pathlib import Path


class FileService:
    def __init__(self, file_path: str):
        """
        Initializes the file service with the given file path.
        """
        self.file_path = Path(file_path)

        # Ensure the file exists
        self.file_path.touch(exist_ok=True)

    def append_to_file(self, content: str):
        """
        Appends content to the file.
        """
        try:
            with self.file_path.open("a") as file:
                file.write(content + "\n")
            logger.debug(f"Appended content to file: {content}")
        except Exception as e:
            logger.error(f"Failed to append to file: {e}")
