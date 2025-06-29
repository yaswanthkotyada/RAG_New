from flask import Flask
from flask_cors import CORS

from sending_req import send_req_bp
app=Flask(__name__,static_folder="files", static_url_path='/files')

CORS(app, resources={r"/answer": {"origins": "*"}}) 
@app.route('/')
def home_page():
    return "welecome to Rag chatbot"

app.register_blueprint(send_req_bp)


if __name__=="__main__":
    app.run(debug=True)