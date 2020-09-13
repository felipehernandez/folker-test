from folker.logger.file_test_logger import FileTestLogger


class FileSequentialTestLogger(FileTestLogger):

    def __init__(self, file_name: str) -> None:
        super().__init__(file_name)
