class ServerUnreachable(Exception):
    def __init__(self, message, url):
        super().__init__(f'{message}\nurl: {url}')

class JsonNeeded(Exception): # Wood needed ma lord :D
    def __init__(self) -> None:
        self.msg = 'Provide JSON for your post request!'
        super().__init__(self.msg)