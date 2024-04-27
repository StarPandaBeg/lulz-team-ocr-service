import os
from flask import Flask, request, after_this_request
import imgparser
app = Flask(__name__)

@app.route('/parseimg', methods=['POST'])
def hello_world():
    if 'file' not in request.files:
        return 'Файл не предоставлен'
    file = request.files['file']
    
    file.save(file.filename)
    result = imgparser.process(file.filename)
    os.remove(file.filename)

    return result

app.run(debug=True, host="0.0.0.0", port=5003)