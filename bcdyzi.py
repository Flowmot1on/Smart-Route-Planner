# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 09:43:39 2019

@author: SKYNET
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
import gmplot
import re
import timeit
import time

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


def readData():
    configure()
    GL = pd.read_sql_query("SELECT * FROM GTS.GpsLog ", conn)
    RouteGps = pd.read_sql_query("SELECT * FROM GTS.RouteGps ", conn)
    firms = pd.read_sql_query("SELECT * FROM GTS.Firm Where CalculationType = 2", conn)
    devices = pd.read_sql_query("SELECT * FROM GTS.Device ", conn)
    routes = pd.read_sql_query("SELECT * FROM GTS.Route ", conn)
    return GL,RouteGps,firms,devices,routes




def scalizer(i,cordinates,numberOfSens):
    st = False
    if(cordinates[0]+numberOfSens/10000)> GL.Latitude[i] >(cordinates[0]-numberOfSens/10000) and (cordinates[1]+numberOfSens/10000)> GL.Longitude[i] >(cordinates[1]-numberOfSens/10000):
        
        st = True
    
    else:
    
        st = False
    return st
def checkpoint(i):
    state = False
    
    global ePoint
    global sPoint
    for a in helper.index:
        # scalizerParametre
        if (scalizer(i,helper.startCor[a],3)):
            
            ePoint = helper.endCor[a]
            sPoint = helper.startCor[a]
            #print(a)  
            state = True
            break
            
        else:
            state = False
        
    return state

def create(conn,param_array,RouteId,DeviceId):
    print("Report Row Created")
    cursor = conn.cursor()
    cursor.execute("exec [GTS].[?????] ?,?,?",[param_array,RouteId,DeviceId])
    
    conn.commit()

def create1(conn,deviceId,startId,endId,routeId,accurancy,ısThreshold):
    global setr
    setr = False
    while True:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO GTS.RouteGpsLog (DeviceId,StartGpsLogId,EndGpsLogId,RouteId,Accurancy,IsThreshold) VALUES (?,?,?,?,?,?); ",[deviceId,startId,endId,routeId,accurancy,ısThreshold])
            
            setr = True
        except Exception:
        
            time.sleep(5)
        if(setr):
            
            conn.commit()
            print("Report Row Created")
            break
    
    
    
    

if __name__ == '__main__':


    while True:
        try:
            GpsLog,RouteGps,firms,devices,routes = readData()
            break
        except Exception:
            time.sleep(30)

    
    helper = pd.DataFrame(columns = ['routeId', 'startCor', 'endCor', 'duration', 'optiParameter'])
    
    
    for i in np.unique(RouteGps.RouteId):
        helper.at[i,"optiParameter"] = [min(RouteGps[RouteGps.RouteId == i].Latitude.tolist()),max(RouteGps[RouteGps.RouteId == i].Latitude.tolist()),min(RouteGps[RouteGps.RouteId == i].Longitude.tolist()),max(RouteGps[RouteGps.RouteId == i].Longitude.tolist())]
        
        exec("Pattern%s = RouteGps[RouteGps.RouteId == i]" % i)
        plt.plot(RouteGps[RouteGps.RouteId == i].Latitude.tolist(),RouteGps[RouteGps.RouteId == i].Longitude.tolist())
    
        plt.ylim(helper.optiParameter[i][2] -0.01, helper.optiParameter[i][3]+0.01)
        plt.xlim(helper.optiParameter[i][0] -0.01, helper.optiParameter[i][1]+0.01)
        
        text ='PngArguments/Patterns/'+ str(i) + "pattern.png" 
        exec("plt.savefig('%s')" % text)
        plt.close()
        
        startPoint = [RouteGps[RouteGps.RouteId == i].Latitude.tolist()[0],RouteGps[RouteGps.RouteId == i].Longitude.tolist()[0]]
        endPoint = [RouteGps[RouteGps.RouteId == i].Latitude.tolist()[-1],RouteGps[RouteGps.RouteId == i].Longitude.tolist()[-1]]
        
        helper.at[i,"routeId"] = i
        
        helper.at[i,"startCor"] = startPoint
        
        helper.at[i,"endCor"] = endPoint
        
        helper.at[i,"duration"] = routes[routes['RouteId'] == i].Duration.tolist()[0]      
        
        helper.at[i,"patternPath"] = text
        
    helper = helper.reset_index(drop=True)
    
    """    
    startLats, startLongs = zip(*helper.startCor.tolist())    
    
    endLats, endLongs = zip(*helper.endCor.tolist())    
    """
    
    for firm in firms.FirmId:
        
        dvc = devices[devices['FirmId'] == firm].reset_index(drop=True)
        rts = routes[routes['FirmId'] == firm].reset_index(drop=True)

        for device in dvc.DeviceId: 
            
            GL = GpsLog.copy()
        
            GL = GL.sort_values('LogDate').reset_index(drop = True)
            
            GL = GL[GL['DeviceId'] == device].reset_index(drop = True)
            
        
                
            x=0
            
            for i in GL.index:
        
                if(i < len(GL.index+1)-1):
            
                    GL.at[i+1, 'TripDuration'] = (GL.LogDate[i+1]-GL.LogDate[i]).total_seconds()
            i = 0
            temp = []
            temp1 = []
            temp2 = []
            df = pd.DataFrame(columns = ['deviceId','Ids','Lar','Long','StartEnd','duration'])
            
            

            while (i < len(GL)):
                
                c = i 
                if (checkpoint(c)):

                    
                      
                    b=0    
                    while (((i+b+1) < len(GL.index)  and not (scalizer(i+b,ePoint,3)))):
                        """
                        if (GL.GeofenceId[i+b+1] == start or GpsL og.GeofenceId[i+b] == GL.GeofenceId[i+b+1]):
                            print(1)
                            
                        else: 
                        """  
                        
                        temp2.append(int(GL.GpsLogId[i+b]))
                        temp1.append(GL.Latitude[i+b]+ 0.0000001)
                        temp.append(GL.Longitude[i+b]+ 0.0000001)
                        
                        
                        
                        b+=1
            
            
                    temp2.append(int(GL.GpsLogId[i+b]))
                    temp1.append(GL.Latitude[i+b]+ 0.0000001)
                    temp.append(GL.Longitude[i+b]+ 0.0000001) 
                    df.at[i, 'deviceId'] = int(GL.DeviceId[i])       
                    df.at[i, 'Ids'] = temp2
                    df.at[i, 'Lar'] = temp1
                    df.at[i, 'Long'] = temp
                    df.at[i, 'count'] = len (temp)
                    df.at[i, 'duration'] = ( GL[GL.GpsLogId == temp2[-1]].LogDate.tolist()[0] - GL[GL.GpsLogId == temp2[0]].LogDate.tolist()[0] ).total_seconds()
                    #print(i)
                    df.at[i, 'StartEnd'] = [temp1[0],temp[0]]
                    
                    temp=[]
                    temp1=[]
                    temp2=[]
                    b+=1
                    i+=1
            
                   
                i+=1        
               
                
  
            
            df = df.reset_index(drop=True)   
            exec("{} = df.copy()".format(f'df_{device}'))
            exec("{} = GL.copy()".format(f'gl_{device}'))
    
    
            
            
            rt =[]
            a = 0
            for i in df.index:          
                if ((i < len(df.index)-1) and (df.Ids[i][-1] == df.Ids[i+1][-1])):
                    df.at[i, 'queue'] = a
                else:
                    
                    df.at[i, 'queue'] = a
                    a+=1
                for j in helper.index:
                    if ((df.StartEnd[i][0]+0.0003)> helper.startCor[j][0] >(df.StartEnd[i][0]-0.0003) and (df.StartEnd[i][1] + 0.0003)> helper.startCor[j][1] >(df.StartEnd[i][1]-0.0003)):
                    
                        rt.append(helper.routeId[j])
                
                        df.at[i, 'routeId'] = int(helper.routeId[j])
                #db.Threshold
                #if (df.duration[i] < helper[helper.routeId == df.routeId[i]].duration.tolist()[0] - routes[routes.RouteId == df.routeId[i]].ThresholdTime.tolist()[0]   or df.duration[i] > helper[helper.routeId == df.routeId[i]].duration.tolist()[0] + routes[routes.RouteId == df.routeId[i]].ThresholdTime.tolist()[0]):
                    
                if (df.duration[i] < helper[helper.routeId == df.routeId[i]].duration.tolist()[0] - 600  or df.duration[i] > helper[helper.routeId == df.routeId[i]].duration.tolist()[0] + 600):
                
                    #df.at[i, 'routeId'] = 0
                    
                    df.at[i, 'IsThreshold'] =   1

                else:

                    df.at[i, 'IsThreshold'] =  0
                    
                        
            df = df.drop_duplicates(subset = 'queue',keep = 'last').reset_index(drop=True)
            #######################################
            start = timeit.default_timer()
            
            for i in df.index:
                
                if(df.routeId[i] != 0 ):
                    exec("plt.plot(df.Lar[%s],df.Long[%s])" % (i,i))
                    text ='PngArguments/Plots/'+ str(device) + str(i) + 'plot.png'
                    plt.ylim((helper[helper.routeId == df.routeId[i]].optiParameter.tolist()[0][2]-0.01, helper[helper.routeId == df.routeId[i]].optiParameter.tolist()[0][3]+0.01))
                    plt.xlim((helper[helper.routeId == df.routeId[i]].optiParameter.tolist()[0][0]-0.01, helper[helper.routeId == df.routeId[i]].optiParameter.tolist()[0][1]+0.01))
                
                    exec("plt.savefig('%s')" % text)
                    plt.close()
                
                    df.at[i,'plotPath'] = text
                    
                    
                    df.at[i,'accurancy'] = testimg.structural_sim(df.plotPath[i], helper[helper.routeId == df.routeId[i]].patternPath.tolist()[0])
                """
                for j in helper.index:
                    liste.append(testimg.structural_sim(df.plotPath[i], helper[helper.routeId == df.routeId[i]].patternPath.tolist()[0]))
                    liste1.append(helper.routeId[j])
                        
                    
                    max_value = max(liste)
                    max_index = liste.index(max_value)
                """
                liste = []
                liste1 = []

            
            
            stop = timeit.default_timer()   
        
            print('Time: ', stop - start) 
            exec("{} = df.copy()".format(f'df_{device}'))
            exec("{} = GL.copy()".format(f'gl_{device}'))
          
    
            for i in df.index:

                create1(conn,df.deviceId[i],df.Ids[i][0],df.Ids[i][-1],df.routeId[i],df.accurancy[i],df.IsThreshold[i])

            
            
    """        
    gmap3 = gmplot.GoogleMapPlotter(37.3546, 27.6454, 7) 
  
    # scatter method of map object  
    # scatter points on the google map 
    gmap3.scatter( df_2412.Lar[3],df_2412.Long[3], '# FF0000', size = 40, marker = False ) 
      
    # Plot method Draw a line in 
    # between given coordinates 
    gmap3.plot(df_2412.Lar[3], df_2412.Long[3],'cornflowerblue', edge_width = 2.5) 
      
    gmap3.draw("C:\\Users\\SADELABS02\\Desktop\\testtest\\map13.html")
            
            """