# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 17:12:33 2020

@author: SADELABS02
"""


#import re
#import datetime
import time
import pandas as pd
import numpy as np
import configparser 
import pyodbc

#print ("\n".join(s for s in os.listdir() if sub.lower() in s.lower()))

def configure():
    config = configparser.ConfigParser()
    config.read('config.ini')  
    global conn
    conn = pyodbc.connect(Driver = config['MsSqlDB']['Driver'],
                               Server = config['MsSqlDB']['Server'],
                               Database = config['MsSqlDB']['Database'],
                               User = config['MsSqlDB']['user'],
                               Password = config['MsSqlDB']['pass'],
                               Trusted_connection =config['MsSqlDB']['Trusted_connection'])

def readLog(deviceId):
    configure()
    query = "EXEC SP_getDeviceLog {}".format(deviceId)
    log = pd.read_sql_query(str(query), conn)
    
    return log

def readClients():
    configure()
    devices = pd.read_sql_query("EXEC SP_getDevices", conn)
    
    return devices

def create1(conn,deviceId,startId,endId,routeId,accurancy,ısThreshold):
    
    cursor = conn.cursor()
    cursor.execute("INSERT INTO GTS.RouteGpsLog (DeviceId,StartGpsLogId,EndGpsLogId,RouteId,Accurancy,IsThreshold) VALUES (?,?,?,?,?,?); ",[deviceId,startId,endId,routeId,accurancy,ısThreshold])
    conn.commit()
    print("Report Row Created")
    
    
    

if __name__ == '__main__':

    con = True
    while (con):
        try:
            
            df_clients = readClients()
            con = False
        except Exception as e:
            print (e)
            time.sleep(5)
        
        
    for clnt in np.unique(df_clients.clientId):
        
        objects = df_clients[df_clients['clientId'] == clnt].reset_index(drop=True)
        
        for obj in np.unique(objects.objectId): 
        
            devices = objects[objects['objectId'] == obj].reset_index(drop=True)
            
            for dvc in devices.deviceId:
                con = True
                while (con):
                    try:
                        
                        df = readLog(1)
                        con = False
                    except Exception as e:
                        print (e)
                        time.sleep(5)
                        
                    
                
        
                