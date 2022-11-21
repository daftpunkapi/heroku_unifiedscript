# Load Dependencies/Libraries
from flask import Flask, request, json, Response
from pymongo import MongoClient


# Create Connect with MongoDB
class MongoAPI:
    def __init__(self, data):
        self.client = MongoClient("mongodb+srv://daft:punk@mergedev.iiiixxn.mongodb.net/?retryWrites=true&w=majority")  
        database = "Ticket_Common_Model"
        collection = data
        cursor = self.client[database]
        self.collection = cursor[collection]
        # self.data = data



# This method will allow us to read all of the documents present in our collection. Line number 3 is used to reformat the data. The output of the collection object is of datatype dictionary
    def read(self,params):
        # status = params["status"]
        # pagesize = params["pages"]
        
        if "status" in params:
            documents = self.collection.find({"status" : params["status"]})
            output = [{item: data[item] for item in data if item != '_id'} for data in documents] #removing the MongoDB generated ID
            return output
        else:
            documents = self.collection.find()
            output = [{item: data[item] for item in data if item != '_id'} for data in documents] #removing the MongoDB generated ID
            return output



# Create a Flask Server
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False



# HTTP Method via Flask Routes
@app.route('/tickets', methods=['GET'])
def mongo_read():
    data = request.headers['Account-Token']
    # status = request.args.get('status')
    params = request.args
    params = params.to_dict(flat = True)  
                        
    obj1 = MongoAPI(data)
    response = obj1.read(params)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

# Running the Flask Server/App
if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port=5001)
    from os import environ
    app.run(debug=True, host='0.0.0.0', port=environ.get("PORT", 5000))
   

