import streamlit as st
import pandas as pd
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

# Title of the Streamlit application
st.title("Network Anomaly Detection Indicator")

# User input form
st.header("Network Anomaly Detection Prediction")

# protocoltype selection
protocoltype = st.selectbox("protocoltype", options=["Select your protocoltype", 'tcp' 'udp' 'icmp'], index=0)

# service selection
service = st.selectbox("service", options=["Select your service", 'ftp_data' 'other' 'private' 'http' 'remote_job' 'name' 'netbios_ns'
 'eco_i' 'mtp' 'telnet' 'finger' 'domain_u' 'supdup' 'uucp_path' 'Z39_50'
 'smtp' 'csnet_ns' 'uucp' 'netbios_dgm' 'urp_i' 'auth' 'domain' 'ftp'
 'bgp' 'ldap' 'ecr_i' 'gopher' 'vmnet' 'systat' 'http_443' 'efs' 'whois'
 'imap4' 'iso_tsap' 'echo' 'klogin' 'link' 'sunrpc' 'login' 'kshell'
 'sql_net' 'time' 'hostnames' 'exec' 'ntp_u' 'discard' 'nntp' 'courier'
 'ctf' 'ssh' 'daytime' 'shell' 'netstat' 'pop_3' 'nnsp' 'IRC' 'pop_2'
 'printer' 'tim_i' 'pm_dump' 'red_i' 'netbios_ssn' 'rje' 'X11' 'urh_i'
 'http_8001' 'aol' 'http_2784' 'tftp_u' 'harvest'], index=0)

# flag selection
flag = st.selectbox("flag", options=["Select your flag", 'SF' 'S0' 'REJ' 'RSTR' 'SH' 'RSTO' 'S1' 'RSTOS0' 'S3' 'S2' 'OTH'], index=0)

# Integer inputs
duration = st.number_input("Duration", min_value=0, step=1, format="%d")
srcbytes = st.number_input("Source Bytes", min_value=0, step=1, format="%d")
dstbytes = st.number_input("Destination Bytes", min_value=0, step=1, format="%d")
land = st.number_input("Land", min_value=0, step=1, format="%d")
wrongfragment = st.number_input("Wrong Fragment", min_value=0, step=1, format="%d")
urgent = st.number_input("Urgent", min_value=0, step=1, format="%d")
hot = st.number_input("Hot", min_value=0, step=1, format="%d")
numfailedlogins = st.number_input("Number of Failed Logins", min_value=0, step=1, format="%d")
loggedin = st.number_input("Logged In", min_value=0, step=1, format="%d")
numcompromised = st.number_input("Number Compromised", min_value=0, step=1, format="%d")
rootshell = st.number_input("Root Shell", min_value=0, step=1, format="%d")
suattempted = st.number_input("Su Attempted", min_value=0, step=1, format="%d")
numroot = st.number_input("Number of Root", min_value=0, step=1, format="%d")
numfilecreations = st.number_input("Number of File Creations", min_value=0, step=1, format="%d")
numshells = st.number_input("Number of Shells", min_value=0, step=1, format="%d")
numaccessfiles = st.number_input("Number of Access Files", min_value=0, step=1, format="%d")
numoutboundcmds = st.number_input("Number of Outbound Cmds", min_value=0, step=1, format="%d")
ishotlogin = st.number_input("Is Hot Login", min_value=0, step=1, format="%d")
isguestlogin = st.number_input("Is Guest Login", min_value=0, step=1, format="%d")
count = st.number_input("Count", min_value=0, step=1, format="%d")
srvcount = st.number_input("Srv Count", min_value=0, step=1, format="%d")
dsthostcount = st.number_input("Dst Host Count", min_value=0, step=1, format="%d")
dsthostsrvcount = st.number_input("Dst Host Srv Count", min_value=0, step=1, format="%d")
lastflag = st.number_input("Last Flag", min_value=0, step=1, format="%d")

# Float inputs
serrorrate = st.number_input("S Error Rate", min_value=0.0, max_value=1.0, step=0.01, format="%.2f")
srvserrorrate = st.number_input("Srv S Error Rate", min_value=0.0, max_value=1.0, step=0.01, format="%.2f")
rerrorrate = st.number_input("R Error Rate", min_value=0.0, max_value=1.0, step=0.01, format="%.2f")
srvrerrorrate = st.number_input("Srv R Error Rate", min_value=0.0, max_value=1.0, step=0.01, format="%.2f")
samesrvrate = st.number_input("Same Srv Rate", min_value=0.0, max_value=1.0, step=0.01, format="%.2f")
diffsrvrate = st.number_input("Diff Srv Rate", min_value=0.0, max_value=1.0, step=0.01, format="%.2f")
srvdiffhostrate = st.number_input("Srv Diff Host Rate", min_value=0.0, max_value=1.0, step=0.01, format="%.2f")
dsthostsamesrvrate = st.number_input("Dst Host Same Srv Rate", min_value=0.0, max_value=1.0, step=0.01, format="%.2f")
dsthostdiffsrvrate = st.number_input("Dst Host Diff Srv Rate", min_value=0.0, max_value=1.0, step=0.01, format="%.2f")
dsthostsamesrcportrate = st.number_input("Dst Host Same Src Port Rate", min_value=0.0, max_value=1.0, step=0.01, format="%.2f")
dsthostsrvdiffhostrate = st.number_input("Dst Host Srv Diff Host Rate", min_value=0.0, max_value=1.0, step=0.01, format="%.2f")
dsthostserrorrate = st.number_input("Dst Host S Error Rate", min_value=0.0, max_value=1.0, step=0.01, format="%.2f")
dsthostsrvserrorrate = st.number_input("Dst Host Srv S Error Rate", min_value=0.0, max_value=1.0, step=0.01, format="%.2f")
dsthostrerrorrate = st.number_input("Dst Host R Error Rate", min_value=0.0, max_value=1.0, step=0.01, format="%.2f")
dsthostsrvrerrorrate = st.number_input("Dst Host Srv R Error Rate", min_value=0.0, max_value=1.0, step=0.01, format="%.2f")

# Prediction button
if st.button("Predict Anomaly"):
    # Check if all necessary fields are filled out (modify this to only include required fields as needed)
    if duration is None or srcbytes is None or dstbytes is None:
        st.error("Please make sure all required fields are filled.")
    else:
        # Collect data in dictionary format for the custom input fields
        data = {
            "duration": duration,
            "srcbytes": srcbytes,
            "dstbytes": dstbytes,
            "land": land,
            "wrongfragment": wrongfragment,
            "urgent": urgent,
            "hot": hot,
            "numfailedlogins": numfailedlogins,
            "loggedin": loggedin,
            "numcompromised": numcompromised,
            "rootshell": rootshell,
            "suattempted": suattempted,
            "numroot": numroot,
            "numfilecreations": numfilecreations,
            "numshells": numshells,
            "numaccessfiles": numaccessfiles,
            "numoutboundcmds": numoutboundcmds,
            "ishotlogin": ishotlogin,
            "isguestlogin": isguestlogin,
            "count": count,
            "srvcount": srvcount,
            "serrorrate": serrorrate,
            "srvserrorrate": srvserrorrate,
            "rerrorrate": rerrorrate,
            "srvrerrorrate": srvrerrorrate,
            "samesrvrate": samesrvrate,
            "diffsrvrate": diffsrvrate,
            "srvdiffhostrate": srvdiffhostrate,
            "dsthostcount": dsthostcount,
            "dsthostsrvcount": dsthostsrvcount,
            "dsthostsamesrvrate": dsthostsamesrvrate,
            "dsthostdiffsrvrate": dsthostdiffsrvrate,
            "dsthostsamesrcportrate": dsthostsamesrcportrate,
            "dsthostsrvdiffhostrate": dsthostsrvdiffhostrate,
            "dsthostserrorrate": dsthostserrorrate,
            "dsthostsrvserrorrate": dsthostsrvserrorrate,
            "dsthostrerrorrate": dsthostrerrorrate,
            "dsthostsrvrerrorrate": dsthostsrvrerrorrate,
            "lastflag": lastflag
        }

        # Convert the data to DataFrame if necessary
        pred_df = pd.DataFrame([data])
        st.write("Input Data:", pred_df)  # Display the DataFrame for confirmation

        try:
            # Initialize the prediction pipeline and make predictions
            predict_pipeline = PredictPipeline()
            results = predict_pipeline.predict(pred_df)

            # Display the result
            st.success(f"The predicted anomaly score is {results[0]}")
        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")

                                     
