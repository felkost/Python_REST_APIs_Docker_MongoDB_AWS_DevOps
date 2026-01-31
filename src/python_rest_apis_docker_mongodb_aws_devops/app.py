from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

def checkPostedData(postedData, functionName):
    if (functionName == "inc"):
        if "x" not in postedData:
            return 401 #Missing parameter
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
        
        #Step 2: Multiply the posted data
        ret = x + 1
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
        return jsonify({'error': 'Missing "x" in request data'}), 305      
    return "Received POST request!"

api.add_resource(Increament, "/inc")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)