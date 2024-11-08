import os
import sys
import pandas as pd
from src.logger import logging
from src.exception import CustomException
from src.utils import load_object

class PredictPipeline:
    def __init__(self):
        pass
    
    def predict(self, features: pd.DataFrame) -> pd.Series:
        try:
            model_path=os.path.join("artifacts","model.pkl")
            preprocessor_path=os.path.join('artifacts','preprocessor.pkl')
            print("Before Loading")
            model=load_object(file_path=model_path)
            preprocessor=load_object(file_path=preprocessor_path)
            print("After Loading")
            data_scaled=preprocessor.transform(features)
            preds=model.predict(data_scaled)
            return preds
        
        except Exception as e:
            raise CustomException(e, sys) from e

class CustomData:
    def __init__(
        self,
        duration: int,
        protocoltype: str,
        service: str,
        flag: str,
        srcbytes: int,
        dstbytes: int,
        land: int,
        wrongfragment: int,
        urgent: int,
        hot: int,
        numfailedlogins: int,
        loggedin: int,
        numcompromised: int,
        rootshell: int,
        suattempted: int,
        numroot: int,
        numfilecreations: int,
        numshells: int,
        numaccessfiles: int,
        numoutboundcmds: int,
        ishotlogin: int,
        isguestlogin: int,
        count: int,
        srvcount: int,
        serrorrate: float,
        srvserrorrate: float,
        rerrorrate: float,
        srvrerrorrate: float,
        samesrvrate: float,
        diffsrvrate: float,
        srvdiffhostrate: float,
        dsthostcount: int,
        dsthostsrvcount: int,
        dsthostsamesrvrate: float,
        dsthostdiffsrvrate: float,
        dsthostsamesrcportrate: float,
        dsthostsrvdiffhostrate: float,
        dsthostserrorrate: float,
        dsthostsrvserrorrate: float,
        dsthostrerrorrate: float,
        dsthostsrvrerrorrate: float,
        lastflag: int
    ):
        self.duration = duration
        self.protocoltype = protocoltype
        self.service = service
        self.flag = flag
        self.srcbytes = srcbytes
        self.dstbytes = dstbytes
        self.land = land
        self.wrongfragment = wrongfragment
        self.urgent = urgent
        self.hot = hot
        self.numfailedlogins = numfailedlogins
        self.loggedin = loggedin
        self.numcompromised = numcompromised
        self.rootshell = rootshell
        self.suattempted = suattempted
        self.numroot = numroot
        self.numfilecreations = numfilecreations
        self.numshells = numshells
        self.numaccessfiles = numaccessfiles
        self.numoutboundcmds = numoutboundcmds
        self.ishotlogin = ishotlogin
        self.isguestlogin = isguestlogin
        self.count = count
        self.srvcount = srvcount
        self.serrorrate = serrorrate
        self.srvserrorrate = srvserrorrate
        self.rerrorrate = rerrorrate
        self.srvrerrorrate = srvrerrorrate
        self.samesrvrate = samesrvrate
        self.diffsrvrate = diffsrvrate
        self.srvdiffhostrate = srvdiffhostrate
        self.dsthostcount = dsthostcount
        self.dsthostsrvcount = dsthostsrvcount
        self.dsthostsamesrvrate = dsthostsamesrvrate
        self.dsthostdiffsrvrate = dsthostdiffsrvrate
        self.dsthostsamesrcportrate = dsthostsamesrcportrate
        self.dsthostsrvdiffhostrate = dsthostsrvdiffhostrate
        self.dsthostserrorrate = dsthostserrorrate
        self.dsthostsrvserrorrate = dsthostsrvserrorrate
        self.dsthostrerrorrate = dsthostrerrorrate
        self.dsthostsrvrerrorrate = dsthostsrvrerrorrate
        self.lastflag = lastflag

    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "duration": [self.duration],
                "protocoltype": [self.protocoltype],
                "service": [self.service],
                "flag": [self.flag],
                "srcbytes": [self.srcbytes],
                "dstbytes": [self.dstbytes],
                "land": [self.land],
                "wrongfragment": [self.wrongfragment],
                "urgent": [self.urgent],
                "hot": [self.hot],
                "numfailedlogins": [self.numfailedlogins],
                "loggedin": [self.loggedin],
                "numcompromised": [self.numcompromised],
                "rootshell": [self.rootshell],
                "suattempted": [self.suattempted],
                "numroot": [self.numroot],
                "numfilecreations": [self.numfilecreations],
                "numshells": [self.numshells],
                "numaccessfiles": [self.numaccessfiles],
                "numoutboundcmds": [self.numoutboundcmds],
                "ishotlogin": [self.ishotlogin],
                "isguestlogin": [self.isguestlogin],
                "count": [self.count],
                "srvcount": [self.srvcount],
                "serrorrate": [self.serrorrate],
                "srvserrorrate": [self.srvserrorrate],
                "rerrorrate": [self.rerrorrate],
                "srvrerrorrate": [self.srvrerrorrate],
                "samesrvrate": [self.samesrvrate],
                "diffsrvrate": [self.diffsrvrate],
                "srvdiffhostrate": [self.srvdiffhostrate],
                "dsthostcount": [self.dsthostcount],
                "dsthostsrvcount": [self.dsthostsrvcount],
                "dsthostsamesrvrate": [self.dsthostsamesrvrate],
                "dsthostdiffsrvrate": [self.dsthostdiffsrvrate],
                "dsthostsamesrcportrate": [self.dsthostsamesrcportrate],
                "dsthostsrvdiffhostrate": [self.dsthostsrvdiffhostrate],
                "dsthostserrorrate": [self.dsthostserrorrate],
                "dsthostsrvserrorrate": [self.dsthostsrvserrorrate],
                "dsthostrerrorrate": [self.dsthostrerrorrate],
                "dsthostsrvrerrorrate": [self.dsthostsrvrerrorrate],
                "lastflag": [self.lastflag]
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)

