from flask import Flask, request, render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

application = Flask(__name__)

app = application

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        # Fetch data from the form, using network-related fields
        data = CustomData(
            duration=int(request.form.get('duration')),
            protocol_type=request.form.get('protocol_type'),
            service=request.form.get('service'),
            flag=request.form.get('flag'),
            src_bytes=int(request.form.get('src_bytes')),
            dst_bytes=int(request.form.get('dst_bytes')),
            land=int(request.form.get('land')),
            wrong_fragment=int(request.form.get('wrong_fragment')),
            urgent=int(request.form.get('urgent')),
            hot=int(request.form.get('hot')),
            num_failed_logins=int(request.form.get('num_failed_logins')),
            logged_in=int(request.form.get('logged_in')),
            num_compromised=int(request.form.get('num_compromised')),
            root_shell=int(request.form.get('root_shell')),
            su_attempted=int(request.form.get('su_attempted')),
            num_root=int(request.form.get('num_root')),
            num_file_creations=int(request.form.get('num_file_creations')),
            num_shells=int(request.form.get('num_shells')),
            num_access_files=int(request.form.get('num_access_files')),
            num_outbound_cmds=int(request.form.get('num_outbound_cmds')),
            is_hot_login=int(request.form.get('is_hot_login')),
            is_guest_login=int(request.form.get('is_guest_login')),
            count=int(request.form.get('count')),
            srv_count=int(request.form.get('srv_count')),
            serror_rate=float(request.form.get('serror_rate')),
            srv_serror_rate=float(request.form.get('srv_serror_rate')),
            rerror_rate=float(request.form.get('rerror_rate')),
            srv_rerror_rate=float(request.form.get('srv_rerror_rate')),
            same_srv_rate=float(request.form.get('same_srv_rate')),
            diff_srv_rate=float(request.form.get('diff_srv_rate')),
            srv_diff_host_rate=float(request.form.get('srv_diff_host_rate')),
            dst_host_count=int(request.form.get('dst_host_count')),
            dst_host_srv_count=int(request.form.get('dst_host_srv_count')),
            dst_host_same_srv_rate=float(request.form.get('dst_host_same_srv_rate')),
            dst_host_diff_srv_rate=float(request.form.get('dst_host_diff_srv_rate')),
            dst_host_same_src_port_rate=float(request.form.get('dst_host_same_src_port_rate')),
            dst_host_srv_diff_host_rate=float(request.form.get('dst_host_srv_diff_host_rate')),
            dst_host_serror_rate=float(request.form.get('dst_host_serror_rate')),
            dst_host_srv_serror_rate=float(request.form.get('dst_host_srv_serror_rate')),
            dst_host_rerror_rate=float(request.form.get('dst_host_rerror_rate')),
            dst_host_srv_rerror_rate=float(request.form.get('dst_host_srv_rerror_rate'))
        )

        # Get data in dataframe format
        pred_df = data.get_data_as_data_frame()
        print(pred_df)
        print("Before Prediction")

        # Make prediction
        predict_pipeline = PredictPipeline()
        print("Mid Prediction")
        results = predict_pipeline.predict(pred_df)
        print("After Prediction")

        # Render the results on the home page
        return render_template('home.html', results=results[0])

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)

  