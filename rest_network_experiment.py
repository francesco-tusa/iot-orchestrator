#!/usr/bin/python

from network_experiment import SimpleNetworkExperiment
import time
import os
from shutil import copy
from monitoring import Monitoring


class RestSimpleNetworkExperiment(SimpleNetworkExperiment):
       def __init__(self, conn, conf_file, setName, duration, consumer_host, tcpdump_if, consumer_port, consumer_url):
           self.consumer_host = consumer_host
           self.consumer_port = consumer_port
           self.consumer_url = consumer_url
           SimpleNetworkExperiment.__init__(self, conn, conf_file, setName, duration, tcpdump_if, consumer_port)
 

       def startConsumer(self):
           print('Starting Processing function')
           consumer_path = '/home/uceeftu/lattice/'
           command = 'screen -dmS restConsumer java -cp ' + \
                     consumer_path + '/jars/monitoring-bin-core-2.0.1.jar' + ':' + \
                     consumer_path + '/libs/controller/simple-4.1.21.jar ' + \
                     'mon.lattice.appl.dataconsumers.RestDataConsumer ' + self.consumer_port + ' ' + self.consumer_url

           print(command)
           result = self.clusterMgmHost.run(command)

           if result.ok == True:
              command = 'screen -list | grep restConsumer'
              result = self.clusterMgmHost.run(command, hide=True)
              self.consumer_PID = result.stdout.strip().split('.')[0].strip()
              print('Consumer successfully started => PID: ' + self.consumer_PID)
           

       def stopConsumer(self):
           print('Stopping Processing function')
           command = 'kill ' + self.consumer_PID
           result = self.clusterMgmHost.run(command)
           if result.ok == True:
              print('Consumer successfully shut down')
