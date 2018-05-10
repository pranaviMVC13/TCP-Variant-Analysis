#!/usr/bin/python2


from __future__ import division
import sys
import os
import matplotlib.pyplot as plt

N0 = 0
N1 = 1
N2 = 2
N3 = 3
N4 = 4
N5 = 5
N6 = 6




BANDWIDTH = 12 # Mbps
Pkt_Size = 1000 # Byte

"""
Splits each line of generated trace file and creating a tuple.
"""


def isVar(traceLine):
   return len(traceLine.split()) == 7

def isEvent(traceLine):
   return len(traceLine.split()) == 12

def getVar(traceLine):
   values = traceLine.split()
   new_values = ( float(values[0]), int(values[1]), int(values[2]), int(values[3]),	int(values[4]), values[5], float(values[6]))
   return new_values


def get_pair(valStr):
   vals = valStr.split(".")
   return (int(vals[0]), int(vals[1]))
      
def getEvent(traceLine):
   values = traceLine.split()   
   new_values = (values[0],float(values[1]),int(values[2]),int(values[3]),values[4],int(values[5]),values[6],int(values[7]),get_pair(values[8]), get_pair(values[9]),int(values[10]),int(values[11]))
           
   return new_values

"""
Creates a results file with values of average throughput, average RTT
Computes drop rate using drop count and sent count.
"""

def writeResults(fileName, flowID, averageThroughput, averageRTT, dropCount, sentCount):
   vals=fileName.split("_")
   #exp1
   #resFile=vals[0]
   #bandwidth=vals[1]
   
   #exp2,exp3
   
   #resFile=vals[0]+"_"+vals[1]+"_"+ str(flowID)
   #bandwidth=vals[2]
   #exp3
   resFile=vals[0]+"_"+vals[1]+"_"+ str(flowID)
   bandwidth=10

   
   resultFileName = resFile + "_" + str(flowID)
   resultFile = open("./Results/" + resultFileName, 'a')
   if sentCount != 0:
       dropRate = round(dropCount/sentCount, 4)
   else:
       dropRate= 0
   
   line = str(bandwidth)+ " " + str(averageThroughput) + " " + str(averageRTT) + " " + str(dropRate) + " " + str(dropCount) + " " + str(sentCount)
   resultFile.write(line + "\n")
   resultFile.close()
   print (resultFileName + " -> Flow " + str(flowID))
   print ("Average throughput: " + str(averageThroughput) + "Mbps")
   print ("Average delay: " + str(averageRTT) + "s")
   print ("packet drop: "  + str(dropCount))
   print ("packet sent: " + str(sentCount))
   print ("drop rate: " + str(round(dropCount/sentCount, 4)))
   print ("\n")

"""
Iterates over all trace files and calculates performance metrics for each flow ID.
"""

def calculate_All(flowID):

   rootPath = './trFiles'   

   for trFile in os.listdir(rootPath):
      print('Reading trace file:',trFile)
      trFilePath = os.path.join(rootPath, trFile)
      calculate(trFilePath, flowID)
   

"""
checks Events in the traceFile
"""
def calculate(trFilePath, flowID):
   trFile = open(trFilePath, 'r')
   trFileName = trFilePath.split("/")[-1]
   print(trFileName)
   totalDelay = 0 
   delayCount = 0 
   lastEnqueueTime = 0 
   queueSize = 0 
   dropCount = 0 
   sentCount = 0
   FLOW = flowID
   INTERVAL = 0.5 
   STARTPOINT = 0 
   STARTPOINT_drop = 2 
   lastTime = 0 
   intervalData = 0 
   totalDate = 0 
   SHORTDELAY = 0.005 
   LONGDELAY = 0.04 
   BASERTT = (LONGDELAY + 2 * SHORTDELAY) * 2 
  

   # creates evaluation files of CWND, throughput, RTT and queue.
   cwndFileName = 'cwnd_' +trFileName+'_'+ str(flowID)
   throughputFileName = 'throughput_' +trFileName+ '_'+str(flowID)
   rttFileName = 'RTT_' + trFileName +'_'+str(flowID)
   queueFileName = 'queue'+trFileName
   cwndFile = open("./Evaluate/" + cwndFileName,'w')
   throughputFile = open("./Evaluate/" + throughputFileName,'w')
   rttFile = open("./Evaluate/" + rttFileName,'w')
   queueFile = open("./Evaluate/" + queueFileName,'w')

   # iterates over all lines of a trace file.
   for line in trFile:
      
      if isVar(line):

         (time, snode, dummy, dummy, flow, varname, cwnd) = getVar(line)

         # adds to a cwnd file if the file Name contains cwnd.
         if (time >= STARTPOINT and varname == "cwnd_"):
            if ((FLOW == 0 and snode == N0) or (FLOW == 1 and snode == N4)):
               cwndFile.write(str(time) + " " + str(cwnd) + "\n")

      elif isEvent(line):

         (event, time, sendnode, dest, dummy, size, dummy, flow, dummy, dummy, dummy, packetID) = getEvent(line)

         # writes the queue file.
         if (sendnode == N1 and dest == N2 and size >= 1000):
            if (event == "+"):
               queueSize += 1
               lastEnqueueTime = time
               queueFile.write(str(time) + " " + str(queueSize) + "\n")
            elif (event == "-"):
               queueSize -= 1
               queueFile.write(str(time) + " " + str(queueSize) + "\n")
            elif (event == "d"):
               if (time == lastEnqueueTime):
                  queueSize -= 1
               queueFile.write(str(time) + " " + str(queueSize) + "\n")

           

            if (flow == FLOW):
               # computes throughput if the first value of traceFile is "r" and writes in throughput file.
               if (event == "r"): 
                  if (STARTPOINT == 0):
                     STARTPOINT = time
                  if (time < lastTime + INTERVAL):
                     intervalData += size
                     totalDate += size
                  else:
                     intervalThroughput = 8*intervalData/(1000000*(time - lastTime))
                     time = round(time, 2)
                     intervalThroughput = round(intervalThroughput, 2)
                     if(time > STARTPOINT):
                        throughputFile.write(str(time) + " " + str(intervalThroughput) + "\n")
                     lastTime = time
                     intervalData = size
                     totalDate += size

               # computes rtt( by checking first value of trace file, computes queueDelay and RTT and writes in rttFile.
               elif (event == "+"): 
                  time = round(time, 2)
                  queueDelay = queueSize*Pkt_Size*8/(BANDWIDTH*1000000)
                  RTT = round(BASERTT + queueDelay, 4)
                  totalDelay += RTT
                  delayCount += 1
                  if(time > STARTPOINT):
                     rttFile.write(str(time) + " " + str(RTT) + "\n")
               elif (event == "-"):
                  sentCount += 1
                  time = round(time, 2)
                  queueDelay = queueSize*Pkt_Size*8/(BANDWIDTH*1000000)
                  RTT = round(BASERTT + queueDelay, 4)
                  totalDelay += RTT
                  delayCount += 1
                  if(time > STARTPOINT):
                     rttFile.write(str(time) + " " + str(RTT) + "\n")
               elif (event == "d"): 
              
                  queueDelay = queueSize*Pkt_Size*8/(BANDWIDTH*1000000)
                  RTT = round(BASERTT + queueDelay, 4)
                  totalDelay += RTT
                  delayCount += 1
                  if(time > STARTPOINT):
                     rttFile.write(str(time) + " " + str(RTT) + "\n")
                  if(time > STARTPOINT_drop):
                     dropCount += 1
 
   trFile.close()
   cwndFile.close()
   throughputFile.close()
   queueFile.close()
   rttFile.close()


   # Calculates average throughput, delay
   print (lastTime, totalDate,STARTPOINT)
   if (lastTime - STARTPOINT)!=0:
       averageThroughput = 8*totalDate/(1000000*(lastTime - STARTPOINT))
       averageThroughput = round(averageThroughput, 2)
   
   else:
       averageThroughput=0
   if delayCount!=0:
       averageRTT = round(totalDelay/delayCount, 4)
   else:
       averageRTT=0
   # writes all the performance metric values.
   writeResults(trFileName, FLOW, averageThroughput, averageRTT, dropCount, sentCount)


calculate_All(0)
calculate_All(1)
