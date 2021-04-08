
class Response:

    def __init__(self):
        self.code = 200
        self.message = None
        self.result = {}
        self.data = {}
        self.page = 1
        self.pages = 1
        self.per_page = 20
        self.total = 0
        pass

    def set_result(self, code, message):
        self.code = code
        self.message = message
        self.result = {'code': self.code, 'message': self.message}

    def set_contents(self, data):
        self.data = data

    def set_page(self, page=1, per_page=20, pages=1, total=0):
        self.page = page
        self.per_page = per_page
        self.pages = pages
        self.total = total

    def send(self) -> (dict, int):
        return {
            'result': self.result,
            'data': self.data,
            'page': self.page,
            'pages': self.pages,
            'per_page': self.per_page,
            'total': self.total
        }, self.code
