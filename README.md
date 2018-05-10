# TCP-Variant-Analysis

# Goal 
To study the performance of different TCP variants and find out the better performing variant for each metric and during different network conditions. Also, to perform an in-depth study of TCP Cubic Implementation to improve its fairness for different metrics.

# Experiments:

1. In this experiment, we have compared the throughput, congestion window, latency and  drop rate of Reno, Tahoe and Cubic under the same network conditions (bandwidth etc) in a single flow. 

2. In this experiment, we have compared the fairness of following congestion algorithms -Reno,and Cubic protocols.
    a. Cubic against Cubic.
    b. Cubic against Reno
    c. Cubic against Tahoe
    
3. In this experiment, we have studied the impact of RED(Random Early Detection) on tcp cubic.


# Set Up:
We have used NS2 Network Simulator for the experiments to analyze the TCP variants. NS2 supports transport layer protocols like TCP, UDP etc. NS2 supports different TCP variants like Tahoe, Reno, Vegas, New Vegas, Cubic etc.

# Pre-Requisite:
Please include and empty 'trfile', 'evaluate' and 'results' folders as the code assumes that folders are already created and starts dumping the files into the respective folders.

