import os
import evaluate

"""
Computes different performance metrics for Tahoe, Reno and Cubic in a single flow.
"""
def Experiment1(times):

    count = 0    
    while (count < times):
        protocols = ['Tahoe','Reno','Cubic']
        
        for protocol in protocols:
            for i in range(1, 10, 1):
                bandwidth = i
                cmd = 'ns experiment1.tcl ' + "{" + protocol + "}" + " " + str(bandwidth)                
                output = os.popen(cmd)
        print ("Calculating Stats.... ")

        # computes metrics for a single flow
        evaluate.calculate_All(0)
        count = count + 1

"""
Computes different performance metrics for Cubic, Tahoe and Reno using two flows.
"""

def Experiment2(times):
    count = 0
    while (count < times):
        protocolPair1 = ('Cubic','Tahoe')
        protocolPair2 = ('Cubic','Reno')
        protocolPair3 = ('Cubic','Cubic')

        protocols = [protocolPair1,protocolPair2,protocolPair3]
        
        for protocolPair in protocols:
            for i in range(1, 10, 1):
                bandwidth = i
                protocol1 = protocolPair[0]
                protocol2 = protocolPair[1]
                cmd = 'ns experiment2.tcl ' + "{" + protocol1 + "}" + " " + "{" + protocol2 + "}" + " " + str(bandwidth) 
                
                output = os.popen(cmd)
        print('Calculating Stats.....')
        # computes metrics using two flows.
        evaluate.calculate_All(0)        
        evaluate.calculate_All(1)
        count = count + 1

"""
Computes impact of queuing methods RED and DropTail on TCP Cubic.
"""

def Experiment3(times):
    count = 0
    while (count < times):
        protocolPair1 = ('Cubic','RED')
        protocolPair2 = ('Cubic','DropTail')
 
        protocols = [protocolPair1,protocolPair2]
        
        for protocolPair in protocols:
            for i in range(1,10, 1):
                bandwidth = i
                protocol1 = protocolPair[0]
                protocol2 = protocolPair[1]
                cmd = 'ns experiment3.tcl ' + "{" + protocol1 + "}" + " " + "{" + protocol2 + "}" + " " + str(bandwidth) 
                output = os.popen(cmd)
        evaluate.calculate_All(0)
        evaluate.calculate_All(1)
        count = count + 1
        

#Experiment1(1)
#Experiment2(1)
Experiment3(1)


