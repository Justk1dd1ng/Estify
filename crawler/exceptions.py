class PlatformError(Exception):
    def __init__(self, platform: str):
        self.platform = platform
        self.message = f'No instructions found for platform {platform}'
        super().__init__(self.message)