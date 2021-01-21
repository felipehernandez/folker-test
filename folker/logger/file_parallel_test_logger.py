from folker.logger.file_test_logger import FileTestLogger


class FileParallelTestLogger(FileTestLogger):

    def __init__(self, file_name: str) -> None:
        super().__init__(file_name)

    def _log(self, text, end=None):
        self._delayed_log(text=text, end=end)
