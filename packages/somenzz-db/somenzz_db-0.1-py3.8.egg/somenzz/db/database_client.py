from database_interface import DataBaseInterface

class DataBaseClient(object):

    def __init__(self,client):
        if not isinstance(client,DataBaseInterface):
            raise Exception("Bad Interface")
        self._client = client
    
    def connect(self):
        self._client.connect()

    def read(self,sql,params = ()):
        return self._client.read(sql,params)

    def read_map(self,sql,params = ()):
        return self._client.read_map(sql,params)
    
    def write(self,sql,params = ()):
        return self._client.write(sql,params)
