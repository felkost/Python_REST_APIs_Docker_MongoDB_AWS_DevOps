import os
from pymongo import MongoClient
from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise RuntimeError("MONGO_URI is not set")
client = MongoClient(MONGO_URI)
db = client.get_database()  # або get_default_database, якщо в URI є /dbname
calls = db["inc_calls"] # collection to store inc calls

def checkPostedData(postedData, functionName):
    if (functionName == "inc"):
        if "x" not in postedData:
            return 400 #Missing parameter
        else:
            return 200
        
class Increament(Resource):
    def post(self):
        #If I am here, then the resouce Increament was requested using the method POST

        #Step 1: Get posted data:
        postedData = request.get_json()

        #Steb 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "inc")

        if (status_code!=200):
            retJson = {
                "Message": "An error happened",
                "Status Code":status_code
            }
            return jsonify(retJson)

        x = postedData["x"]
        x = int(x)
        
        #Step 2: Increament the posted data
        ret = x + 1
        
        if calls is not None:
            calls.insert_one({"x": x, "result": ret})
            
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return retMap#jsonify(retMap)
    
@app.route('/')
def hello():
    return "Hello from python-rest-apis-docker-mongodb-aws-devops!"

@app.route('/r_post', methods=['POST'])
def r_post():
    dataDict = request.get_json()
    x = dataDict.get('x', None)
    if x is not None:
        return {'result': x + 1}, 200#jsonify({'result': x + 1})
    else:
        return jsonify({'error': 'Missing "x" in request data'}), 400      
    return "Received POST request!"

api.add_resource(Increament, "/inc")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)