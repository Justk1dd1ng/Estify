from typing import Dict
from datetime import datetime


class BucketObject:

    def __init__(self, content: Dict):
        self.content = content

    @property
    def key(self) -> str:
        return self.content.get('Key')

    @property
    def name(self) -> str:
        return self.key.split('/')[-1]

    @property
    def last_modified(self) -> datetime:
        return self.content.get('LastModified')