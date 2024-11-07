from flask import Flask, render_template, request, jsonify
import pandas as pd
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

app = Flask(__name__)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Collect form data
        input_data = {
            'duration': int(request.form.get('duration')),
            'protocoltype': request.form.get('protocoltype'),
            'service': request.form.get('service'),
            'flag': request.form.get('flag'),
            'srcbytes': int(request.form.get('srcbytes')),
            'dstbytes': int(request.form.get('dstbytes')),
            'land': int(request.form.get('land')),
            'wrongfragment': int(request.form.get('wrongfragment')),
            'urgent': int(request.form.get('urgent')),
            'hot': int(request.form.get('hot')),
            'numfailedlogins': int(request.form.get('numfailedlogins')),
            'loggedin': int(request.form.get('loggedin')),
            'numcompromised': int(request.form.get('numcompromised')),
            'rootshell': int(request.form.get('rootshell')),
            'suattempted': int(request.form.get('suattempted')),
            'numroot': int(request.form.get('numroot')),
            'numfilecreations': int(request.form.get('numfilecreations')),
            'numshells': int(request.form.get('numshells')),
            'numaccessfiles': int(request.form.get('numaccessfiles')),
            'numoutboundcmds': int(request.form.get('numoutboundcmds')),
            'ishotlogin': int(request.form.get('ishotlogin')),
            'isguestlogin': int(request.form.get('isguestlogin')),
            'count': int(request.form.get('count')),
            'srvcount': int(request.form.get('srvcount')),
            'serrorrate': float(request.form.get('serrorrate')),
            'srvserrorrate': float(request.form.get('srvserrorrate')),
            'rerrorrate': float(request.form.get('rerrorrate')),
            'srvrerrorrate': float(request.form.get('srvrerrorrate')),
            'samesrvrate': float(request.form.get('samesrvrate')),
            'diffsrvrate': float(request.form.get('diffsrvrate')),
            'srvdiffhostrate': float(request.form.get('srvdiffhostrate')),
            'dsthostcount': int(request.form.get('dsthostcount')),
            'dsthostsrvcount': int(request.form.get('dsthostsrvcount')),
            'dsthostsamesrvrate': float(request.form.get('dsthostsamesrvrate')),
            'dsthostdiffsrvrate': float(request.form.get('dsthostdiffsrvrate')),
            'dsthostsamesrcportrate': float(request.form.get('dsthostsamesrcportrate')),
            'dsthostsrvdiffhostrate': float(request.form.get('dsthostsrvdiffhostrate')),
            'dsthostserrorrate': float(request.form.get('dsthostserrorrate')),
            'dsthostsrvserrorrate': float(request.form.get('dsthostsrvserrorrate')),
            'dsthostrerrorrate': float(request.form.get('dsthostrerrorrate')),
            'dsthostsrvrerrorrate': float(request.form.get('dsthostsrvrerrorrate')),
            'lastflag': int(request.form.get('lastflag'))
        }

        # Create a CustomData instance and convert it to a DataFrame
        data_instance = CustomData(**input_data)
        input_df = data_instance.get_data_as_data_frame()

        # Initialize prediction pipeline and make a prediction
        predict_pipeline = PredictPipeline()
        prediction = predict_pipeline.predict(input_df)

        # Return prediction result
        return jsonify({"prediction": str(prediction[0])})

    except Exception as e:
        # Handle errors and return them as JSON
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
