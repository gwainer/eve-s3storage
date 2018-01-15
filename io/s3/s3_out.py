from datetime import datetime
from io import BytesIO


class S3Out(object):
    def __init__(self, file: bytes, content_type: str, upload_date: datetime, length: int):
        self.file = file
        self.content_type = content_type
        self.upload_date = upload_date
        self.length = length

    def __iter__(self):
        return BytesIO(self.file)

    def read(self):
        with open(self.file, mode='rb') as file:
            f = file.read()
            return bytearray(f)
