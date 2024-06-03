import os
from flask import Flask, request, after_this_request, jsonify
import imgparser
app = Flask(__name__)


@app.route('/parseimg', methods=['POST'])
def hello_world():
    try:
        if 'file' not in request.files:
            return 'Файл не предоставлен'
        file = request.files['file']

        name = file.filename
        file.save("tmp/"+name)
        result = imgparser.process("tmp/"+name)
        print(result)

        # if os.path.exists(name):
        #    os.remove(name)

        return result
    except Exception as e:
        print(e)
        return jsonify({"STATUS": "BAD", "error": e}), 500


app.run(debug=True, host="0.0.0.0", port=5003)
