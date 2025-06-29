from flask import Blueprint, request
from flask_restful import Api, Resource
import json
from operations import generate_query_embedding, retrieve_top_k_chunks, combine_retrview_chunks
from reterview_lat import generate_response_with_cohere,generate_response_with_llam2
send_req_bp=Blueprint("send_req",__name__)
api=Api(send_req_bp)


class ProcessTheQuery(Resource):
    def post(self):
        try:
            data=request.json
            print(f"data:{data}")
            query=data.get("query",None)
            if not query:
                print("required data not provide")
                return {"status":"fail","message":"please provide query"}, 400
            query_embedding = generate_query_embedding(query)
            distances, indices = retrieve_top_k_chunks(query_embedding, k=5)
            with open("metadata.json","r") as f:
                metadata=json.load(f)
            top_k_context=combine_retrview_chunks(indices=indices, metadata=metadata, k=5)
            print(f"Combined Context:{top_k_context}" ) 
            response = generate_response_with_llam2(top_k_context, query)
            print(f"generated response:{response}")
            return {"status":"success","message":"query fetched successfully","response":response}, 200
        except Exception as e:
            print(f"exception:{e}")
            return e
        
        

api.add_resource(ProcessTheQuery,"/answer")