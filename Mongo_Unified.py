# Load Dependencies/Libraries
from flask import Flask, request, json, Response, jsonify
from pymongo import MongoClient 
import pymongo
# import pandas as pd

# Create user defined class MongoAPI
class MongoAPI:
    def __init__(self, data):
        self.client = MongoClient("mongodb+srv://daft:punk@mergedev.iiiixxn.mongodb.net/?retryWrites=true&w=majority")  
        database = "Ticket_Common_Model"
        collection = data
        cursor = self.client[database]
        self.collection = cursor[collection]

# This method will fetch the documents from the collection that match the params criteria
# The requested documents are also paginated
    def read(self,params):
        
        page_size = 5
        offset = 0
       
        if "page_size" in params:
            page_size = int(params["page_size"])
            del params["page_size"] 
        else:
            pass
        
        if "offset" in params:
            offset = int(params["offset"])
            del params["offset"]
        else:
            pass
    
        # cursor pointing to only ONE document which is 'offset' element of the filtered and sorted collection
        last_id = self.collection.find(params).sort('_id', 1)[offset] 
        
        # finding the documents that match our parameter criteria and is greater than ObjectID of last_id
        # also '_id':0 ensures that ObectId is not returned in the document query
        # documents are limited as per the page size
        documents = self.collection.find({'$and': [params,{'_id': {'$gte' : last_id['_id']}}]},{'_id':0}).sort('_id', 1).limit(page_size)
        
        output =[]
        for i in documents:
            output.append(i)
    
        next_url = '/tickets?page_size=' + str(page_size) + '&offset=' + str(offset + page_size)
        prev_url = '/tickets?page_size=' + str(page_size) + '&offset=' + str(offset - page_size)
        
        return jsonify({'prev_url': prev_url, 'next_url': next_url, 'result': output})
    
# Create a Flask Server
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# HTTP Method via Flask Routes
@app.route('/tickets', methods=['GET'])
def mongo_read():
    data = request.headers['Account-Token']
    params = request.args
    params = params.to_dict(flat = True)  
                        
    obj1 = MongoAPI(data)
    response = obj1.read(params)
    return response

# Running the Flask Server/App
if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port=5003)
    from os import environ
    app.run(debug=True, host='0.0.0.0', port=environ.get("PORT", 5000))
