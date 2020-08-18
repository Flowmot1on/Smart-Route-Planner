# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 12:13:58 2019

@author: SADELABS02
"""
#import re
#import datetime
#import time
import pandas as pd
import numpy as np
import configparser 
import pyodbc
import os
import testimg
import matplotlib.pyplot as plt

#print ("\n".join(s for s in os.listdir() if sub.lower() in s.lower()))


config = configparser.ConfigParser()
config.read('config.ini')  
conn = pyodbc.connect(Driver = config['MsSqlDB']['Driver'],
                           Server = config['MsSqlDB']['Server'],
                           Database = config['MsSqlDB']['Database'],
                           User = config['MsSqlDB']['user'],
                           Password = config['MsSqlDB']['pass'],
                           Trusted_connection =config['MsSqlDB']['Trusted_connection'])

def readData(conn):
    configure()
    conn = conn
    GpsLog = pd.read_sql_query("SELECT * FROM GTS.GpsLog ", conn)
    GpsLog = pd.read_sql_query("SELECT * FROM GTS.RouteGps ", conn)

    

def scalizer(i,cordinates,numberOfSens):
    if(cordinates[0]+numberOfSens/10000)> GpsLog.Latitude[i] >(cordinates[0]-numberOfSens/10000) and (cordinates[1]+numberOfSens/10000)> GpsLog.Longitude[i] >(cordinates[1]-numberOfSens/10000):
        return True
    else:
        return False

def create(conn,param_array,RouteId,DeviceId):
    print("Report Row Created")
    cursor = conn.cursor()
    cursor.execute("exec [GTS].[SPCreateRouteLogId] ?,?,?",[param_array,RouteId,DeviceId])
    
    conn.commit()

def create1(conn,deviceId,RouteId,enDate,exDate):
    print("Report Row Created")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO GTS.BadRoutes (DeviceId,RouteId,EnterDate,ExitDate) VALUES (?,?,?,?); ",[deviceId,RouteId,enDate,exDate])
    
    conn.commit()

if __name__ == '__main__':
    readData(conn)
    
    
    start = [37.3425361046308, 27.259098445855102]
    
    test = {'routeId': [113], 'startLat': [start[0]], 'startlong': [start[1]], 'duration': [2759]}
    
    data1 = pd.DataFrame(test)
    
    text_file = open("guzergah.txt", "r")
    
    exec("Pattern = [{}]".format(text_file.read().replace('"', '')))
    
    text_file.close()
    
    ptrn = pd.DataFrame(columns = ['routeId', 'startLat', 'startlong', 'duration', "cordinates"])
    
    
    ptrn.at[0,"routeId"] = test["routeId"][0]
    ptrn.at[0,"startLat"] = test["startLat"][0]
    ptrn.at[0,"startlong"] = test["startlong"][0]
    ptrn.at[0,"duration"] = test["duration"][0]
    ptrn.at[0,"cordinates"] = Pattern
    Charminar_top_attraction_lats, Charminar_top_attraction_lons = zip(*ptrn.cordinates[0])    
    
    plt.plot(Charminar_top_attraction_lats, Charminar_top_attraction_lons)
    
    plt.ylim((27.22, 27.30))
    plt.xlim((37.34, 37.41))
    
    text = str(ptrn.routeId[0]) + "pattern.png" 
    exec("plt.savefig('%s')" % text)
    plt.close()
    
    
    
    """ 
    for firm in firms.FirmId:
        dvc = devices[devices['FirmId'] == firm].reset_index(drop=True)
        rts = routes[routes['FirmId'] == firm].reset_index(drop=True)
        RGeofence = RouteGeofence[RouteGeofence['FirmId'] == firm].reset_index(drop=True)
        Geofences = Geofences[Geofences['FirmId'] == firm].reset_index(drop=True)
        
        
                
        for device in dvc.DeviceId: 
    """
    device = 2922
    
    GL = GpsLog.copy()

    GL = GL.sort_values('LogDate').reset_index(drop = True)
    
    GL = GL[GL['DeviceId'] == device].reset_index(drop = True)
    


    #data1 = data1.drop_duplicates(subset = ['routeId'])  
        
    x=0
    
    for i in GpsLog.index:

        if(i < len(GpsLog.index+1)-1):
    
            GpsLog.at[i+1, 'TripDuration'] = (GpsLog.LogDate[i+1]-GpsLog.LogDate[i]).total_seconds()
    i = 0
    temp = []
    temp1 = []
    temp2 = []
    df = pd.DataFrame(columns = ['deviceId','Ids','Lar','Long','StartEnd'])
    
    while (i < len(GpsLog)):
            
        if (scalizer(i,Pattern[0],3)):
    
                          
                #if ((Pattern[-1][0]-0.0003)> GpsLog.Latitude[i] >(Pattern[-1][0]+0.0003) and (Pattern[-1][1]-0.0003)> GpsLog.Longitude[i] > (Pattern[-1][1]+0.0003)):
            
                 #   end = GpsLog.Latitude[i]
              
            b=0    
            while (((i+b+1) < len(GpsLog.index)  and not (scalizer(i+b,Pattern[-1],1)))):
                """
                if (GpsLog.GeofenceId[i+b+1] == start or GpsL og.GeofenceId[i+b] == GpsLog.GeofenceId[i+b+1]):
                    print(1)
                    
                else: 
                """  
                
                temp2.append(GpsLog.GpsLogId[i+b])
                temp1.append(GpsLog.Latitude[i+b])
                temp.append(GpsLog.Longitude[i+b])
                
                
                
                b+=1
    
    
            temp2.append(GpsLog.GpsLogId[i+b])
            temp1.append(GpsLog.Latitude[i+b])
            temp.append(GpsLog.Longitude[i+b]) 
            df.at[i, 'deviceId'] = GpsLog.DeviceId[i]       
            df.at[i, 'Ids'] = temp2
            df.at[i, 'Lar'] = temp1
            df.at[i, 'Long'] = temp
            df.at[i, 'count'] = len (temp)
            df.at[i, 'Duration'] = ( GpsLog.LogDate[df.Ids[i][-1]-1] - GpsLog.LogDate[df.Ids[i][0]-1] ).total_seconds()
            df.at[i, 'StartEnd'] = [temp1[0],temp[0]]
            
            temp=[]
            temp1=[]
            temp2=[]
            b+=1
            i+=1
    
           
        i+=1        
    
    df = df.reset_index(drop=True)   
    
    
    rt =[]
    a = 0
    for i in df.index:          
        if ((i < len(df.index)-1) and (df.Ids[i][-1] == df.Ids[i+1][-1])):
            df.at[i, 'queue'] = a
        else:
            
            df.at[i, 'queue'] = a
            a+=1
        for j in data1.index:
            if (df.StartEnd[i][0]+0.0003)> data1.startLat[j] >(df.StartEnd[i][0]-0.0003) and (df.StartEnd[i][1] + 0.0003)> data1.startlong[j] >(df.StartEnd[i][1]-0.0003):
                rt.append(data1.routeId[j])
        
        df.at[i, 'routeId'] = data1.routeId[j]
            
    df = df.drop_duplicates(subset = 'queue',keep = 'last').reset_index(drop=True)
    #######################################
    for i in df.index:

        exec("plt.plot(df.Lar[%s],df.Long[%s])" % (i,i))
        text = str(device) + str(i) + 'plot.png'
        plt.ylim((27.22, 27.30))
        plt.xlim((37.34, 37.41))
        exec("plt.savefig('%s')" % text)
        plt.close()





    
                        
            
            
            
            