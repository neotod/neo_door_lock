class ServerUnreachable(Exception):
    def __init__(self, message, url):
        super().__init__(f'{message}\nurl: {url}')