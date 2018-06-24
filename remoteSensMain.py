import paho.mqtt.client as mqtt

from pyspectator.processor import Cpu
from pyspectator.memory import VirtualMemory
from time import sleep

from lib import argparser as marg
import ipaddress as ipa

#client = mqtt.Client("Sensor1")
#client.connect("192.168.0.14")

#client.publish("temperature/house","25°C")

#cpu = Cpu(monitoring_latency=1)
#mem = VirtualMemory(1)
#print (cpu.name)
#print (cpu.count)
#print

#wait time to update sensor data locally
readDelayMin = 1 #seconds
readDelayMax = 100#seconds
refrRateDefault = 1#seconds



class SysSensorElement:
    def __init__(self):
        self.cpu = Cpu(monitoring_latency=readDelayMin)
        self.memoryVirt = VirtualMemory(monitoring_latency=readDelayMin)

        self.CpuTempServiceName = "cputemp"
        self.CpuLoadServiceName = "cpuload"
        self.MemoriesServiceName = "memories"

        print('System cpu name: '+str(self.cpu.name))
        print('System cpu count: '+str(self.cpu.count))


    def get_cpu_load(self):
        # requires refresh of the object via new constractor. Otherwise remains constant
        self.cpu = Cpu(monitoring_latency=readDelayMin)
        return self.cpu.load
    def get_cpu_temp(self):
        # requires refresh of the object via new constractor. Otherwise remains constant
        self.cpu = Cpu(monitoring_latency=readDelayMin)
        return self.cpu.temperature
    def get_mem_virtual(self):
        #requires refresh of the object via new constractor. Otherwise remains constant
        self.memoryVirt = VirtualMemory(monitoring_latency=readDelayMin)
        return (self.memoryVirt.used, self.memoryVirt.available)

class dataPublisher:
    def __init__(self, ipv4, port, sensor_inst, services_to_publish):
        self.client = mqtt.Client("ResourceSensor")
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        try:
           ipa.ip_address(ipv4)
        except Exception as e:
            print(e)

        self.hostAddress = ipv4

        #assign True/False to each service accordingly to input values
        for pair in services_to_publish:
            if sensor_inst.CpuTempServiceName in pair:
                self.bCpuTemp = pair[1]
            if sensor_inst.CpuLoadServiceName in pair:
                self.bCpuLoad = pair[1]
            if sensor_inst.MemoriesServiceName in pair:
                self.bMemories = pair[1]


#TODO: check port
        self.port = port
        #self.serviceName = "SysMonitor"

#TODO: check on_connect doesn't strike
    def on_connect(client, userdata, flags, rc):
        if rc==0:
            print("Connection established")
        else:
            print("Connection is not successful with return code: "+str(rc))

    def on_disconnect(client, userdata, rc):
        if rc != 0:
            print("Sensor client disconnected")

    def connect_to_broker(self):
        self.client.connect(self.hostAddress, self.port, keepalive=60)

    def publish_resources(self, sensor):

        if self.bCpuTemp:
            self.client.publish(sensor.CpuTempServiceName, str(sensor.get_cpu_temp()))
        if self.bCpuLoad:
            self.client.publish(sensor.CpuLoadServiceName, str(sensor.get_cpu_load()))
        if self.bMemories:
            self.client.publish(sensor.MemoriesServiceName, str(sensor.get_mem_virtual()))


#run argument parser
arg_parser = marg.InputArguments()
args = arg_parser.parser.parse_args()


#TODO: check all arguments properly

if (args.refr <= readDelayMin or args.refr >= readDelayMax):
    refrRate = refrRateDefault
else:
    refrRate = args.refr

#check inputs
systemSensor = SysSensorElement()
dp = dataPublisher(args.host, args.p, systemSensor,
                   ((systemSensor.CpuTempServiceName, True),
                    (systemSensor.CpuLoadServiceName, True),
                    (systemSensor.MemoriesServiceName, True)))

dp.connect_to_broker()
while True:
    dp.publish_resources(systemSensor)
    sleep(refrRate)