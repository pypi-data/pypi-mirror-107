import requests

class ApiTrigger:
    def __init__(self, method, url, data) -> None:
        self.method = method
        self.url = url
        self.data = data

    def execute(self):
        authorization = None
        res = requests.request(self.method, self.url, data=self.data,  headers={
        "Content-type":"application/json", 
        "Authorization": authorization})
        return res

