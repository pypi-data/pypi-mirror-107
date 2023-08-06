from fastapi_restful import Resource


class Heartbeat(Resource):
    def get(self):
        return 'OK'