'''
Submission by: Tejaswi Paruchuri
AUS ID: 1213268054
Author of the Code: Tejaswi Paruchuri
'''

import pandas as pd
import time
import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-source", metavar="LAX", dest='source', default='LAX', help="source airport name", type=str)
parser.add_argument('-destination', help="Destination airport name", metavar='JFK', action='store', dest='destination', default="JFK", type=str)
parser.add_argument('-fileName', help='csv file name with flight details', metavar='/home/tejaswi/Documents/FOA/Project/Flights_Details.csv or just csv file name if it is at same location as .py file ', action='store', dest='filename', default="Flights_Details.csv", type=str)

class Capacity:
	def __init__(self,source,destination,fileName):
		self.time_Hour_FlightDetailsDict={}
		self.airCraftNotFound=[]
		self.initialise_Dictionary()
		self.update_Dictionary(fileName)
		if(len(self.airCraftNotFound)>0):
			print self.airCraftNotFound," aircraft capacities list not there in aircraft_Capacity dictionary. Please add capacity to the dictionary and rerun the program"
			#return
		#self.print_Dictionary()
		Total_Capacity=self.find_AugmentedPath(source,destination)
		print "\nTotal Capacity is : ",Total_Capacity
		if(len(self.airCraftNotFound)>0):
			print self.airCraftNotFound," aircraft capacities list not there in aircraft_Capacity dictionary. Please add capacity to the dictionary and rerun the program for accurate capacity"
		#self.print_Dictionary()

	def initialise_Dictionary(self):	
		'''The below code will just create a dictionary with 24 nodes (while generally represent time in hours). Each node will have details related to source location and source flight details'''
		for i in range(0,24):
			self.time_Hour_FlightDetailsDict[i]={}
			self.time_Hour_FlightDetailsDict[i]["Source_Fligth_Details"]=[]
			self.time_Hour_FlightDetailsDict[i]["Source_location"]=[]
		return

	def update_Dictionary(self,fileName):
		'''This function will update every flight details that is read from flight_Details.csv in key based on the start time of the flight that is returned from getConvertedTime function. Source_location will have source of the flight where as source flight details will have a list of [source,destination,capacity,exact landing time,exact starting time and landing time hour]'''
		try:
			data=pd.read_csv(fileName)
		except:
			print "File Not Found. Please give correct location as input in args. Please use flightCapacities_1213268054.py -h for more details"
			return
		for i in range(0,data.shape[0]):	
			start_exact_time,start_time=self.getConvertedTime(data.loc[i][2])
			land_exact_time,land_time=self.getConvertedTime(data.loc[i][3])
			duration=land_exact_time-start_exact_time
			Capacity=self.getCapacity(data.loc[i][4])
			self.time_Hour_FlightDetailsDict[start_time]["Source_Fligth_Details"].append([data.loc[i][0],data.loc[i][1],Capacity,land_exact_time,start_exact_time,land_time])
			self.time_Hour_FlightDetailsDict[start_time]["Source_location"].append(data.loc[i][0])
		return
	
	def getConvertedTime(self,data_Time):
		'''This function will get the hour node by rounding to nearest hour i.e., if time is >=10:30 it is rounded to 11 otherwise it's rounded to 10. It will finally return exact time in minutes and hour'''
		if 'PM' not in data_Time.upper() and 'AM' not in data_Time.upper():
			hour=int(data_Time.split(':')[0])
			minutes=int(data_Time.split(':')[-1])
		elif 'AM' in data_Time.upper() and '12' in data_Time.split(':')[0]:
			hour=0
			minutes=int(data_Time.split(':')[1].split(' ')[0])
		elif 'AM' in data_Time.upper():
			hour=int(data_Time.split(':')[0])
			minutes=int(data_Time.split(':')[1].split(' ')[0])
		elif 'PM' in data_Time.upper() and '12' in data_Time.split(':')[0]:
			hour=12
			minutes=int(data_Time.split(':')[1].split(' ')[0])
		else:
			hour=int(data_Time.split(':')[0])+12
			minutes=int(data_Time.split(':')[1].split(' ')[0])
		exact_time=hour*60+minutes
		if minutes>=30 and hour!=23:
			hour+=1
		return exact_time,hour

	def getCapacity(self,Aircraft_type):
		'''This functionw will return capacity based on the aircraft type. If aircraft is found in aircraft_Capacity it will return value otherwise it will return 0'''
		aircraft_Capacity= {"A220":105,"A319":128,"A321":185,"A320":150,"A321neo":196,"A330-200":230,"A330-300":290,"A330-900neo":280,"A350-900":300,"717-200":110,"737-700":126,"737-800":165,"737-900":180,"737-900ER":180,"737-Max 9": 180,"757-200":180,"757-300":230,"767-300":200,"767-300ER":225,"767-400ER": 240,"777-200":270,"777-200ER":270,"777-200LR": 280,"777-300": 300,"787-8": 235,"787-9": 280,"Embraer 170":72,"Embraer 175 (E 75)":78,"Embraer 190 ":100,"McDonnell Douglas MD-88": 150,"McDonnell Douglas MD-90-30": 150,"CRJ 700":75,"MD-88":150,"MD-90":150,"CRJ 900":75,"Canadair Regional Jet 900":75,"Canadair Regional Jet 700":75,"Embraer 175":78,"Embraer E175":78,"Embraer 175 (Enhanced Winglets)":78,"757-232":295,"757":295,"CRJ-200":50,"Boeing 717":134,"Bombardier CS100":145,"Canadian Regional Jet 700": 75 }
		try:
			if int(Aircraft_type):
				return int(Aircraft_type)
		except ValueError:
			for i,value in enumerate(aircraft_Capacity.keys()):
				if value in Aircraft_type:
					return int(aircraft_Capacity[value])
			if Aircraft_type not in self.airCraftNotFound:
				self.airCraftNotFound.append(Aircraft_type)
			return 0
		if Aircraft_type not in self.airCraftNotFound:
			self.airCraftNotFound.append(Aircraft_type)
		return 0

	def print_Dictionary(self):
		'''This function will just print the dictionary details'''
		count=0
		for keys,values in self.time_Hour_FlightDetailsDict.items():
			print keys,"\t Source_location:",values["Source_location"],"\tStart Flight details:",values["Source_Fligth_Details"],"\n"
			count+=len(values["Source_Fligth_Details"])
		print "Total nodes:",count
		return

	def find_AugmentedPath(self,source,sink):
		'''This function will check for the augmented paths. It will check for the source in the key. Once the source flight is found we will update source to land location and as we have landing time hour in source flight details we will directly go to node that flight has landed. From there we will again check for fligt starting at source till we reach destination. If destination is not found even after going through all the nodes it does mean we can't find a path from source location to destination locations using the augmented path we are following. If path is found we are updating capacity all the nodes of augmented path by taking minimum capacity. If the capacity of any node is zero we are removing the node. If path is not found we are removing the last node of the path as we are not able to find feasible flight to destination from that location.So even if we take another path and reach this location then also we wont reach the destination if we take this last fligh of the augmented path. We will repeat this process till we are not getting any path. At one point it will end since if we are not able to reach destination because of some unfeasible flight we are removing it from the source_flights_details and source_location'''
		Total_Capacity=0
		while(1):
			location=source
			path=[]
			visited=[]
			min_capacity=float('inf')
			key=0
			reached_time=0
			while key<24:
				if (location in self.time_Hour_FlightDetailsDict[key]["Source_location"])  and (location not in visited):
	       				index=0
					for flight in self.time_Hour_FlightDetailsDict[key]["Source_Fligth_Details"]:
						if location in flight[0] and flight[1] not in visited and reached_time<flight[4]:
							visited.append(key)
							visited.append(index)
							visited.append(location)							
							path.append(location)
							location = flight[1]
							capacity= flight[2]
							reached_time=flight[3]
							if capacity < min_capacity :
								min_capacity = capacity
							break
							key+=flight[5]-1
						index+=1
				key+=1
				if location == sink:
					Total_Capacity+=min_capacity		
					path.append(location)
					print "\nAugmented_Path: ",path," with Minimum Capacity: ",min_capacity
					self.reduce_MinCapacity_Visited(visited,'success',min_capacity)	
					break
			if location!=sink:
				if len(visited)==0:
					return Total_Capacity
				self.reduce_MinCapacity_Visited(visited,'failed',min_capacity)
		return Total_Capacity
	def reduce_MinCapacity_Visited(self,list_visited,status,min_capacity):
		'''if path is found to detination This function will update the capacity  in source_flight_details by decreasing the capacity by minimum capacity of that augmented path. During this atleast one node capacity will become 0 in that case we are removing that flight details from source flight details and source_location so that it won't be considered in future. In case if path is not found to destination this funcition will remove the last flight in the visited path in source_flight_details and source_location as last flight is not feasible to reach the destination. Even if we come to this flight in future using some other flight if won't definitely find path to destination again making that path not useful.So removing this path will help in finding some other feasible flights to destination'''
		if(status=='success'):
			i=0
			while i<len(list_visited):
				self.time_Hour_FlightDetailsDict[list_visited[i]]["Source_Fligth_Details"][list_visited[i+1]][2]-=min_capacity
				if self.time_Hour_FlightDetailsDict[list_visited[i]]["Source_Fligth_Details"][list_visited[i+1]][2]==0:
					self.time_Hour_FlightDetailsDict[list_visited[i]]["Source_location"].remove(list_visited[i+2])
					self.time_Hour_FlightDetailsDict[list_visited[i]]["Source_Fligth_Details"]=self.time_Hour_FlightDetailsDict[list_visited[i]]["Source_Fligth_Details"][0:list_visited[i+1]]+self.time_Hour_FlightDetailsDict[list_visited[i]]["Source_Fligth_Details"][list_visited[i+1]+1:]
				i=i+3
		else:
			self.time_Hour_FlightDetailsDict[list_visited[len(list_visited)-3]]["Source_location"].remove(list_visited[len(list_visited)-1])
			self.time_Hour_FlightDetailsDict[list_visited[len(list_visited)-3]]["Source_Fligth_Details"]=self.time_Hour_FlightDetailsDict[list_visited[len(list_visited)-3]]["Source_Fligth_Details"][0:list_visited[len(list_visited)-2]]+self.time_Hour_FlightDetailsDict[list_visited[len(list_visited)-3]]["Source_Fligth_Details"][list_visited[len(list_visited)-2]+1:]	
		return
    

if __name__ == "__main__":
	start_time=time.time()
	args = parser.parse_args()
	Capacity(args.source,args.destination,args.filename)
	print "Timetaken to execute: ",time.time()-start_time
        



        
