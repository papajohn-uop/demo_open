# -*- coding: utf-8 -*-
# Description: exim netdata python.d module
# Author: Pawel Krupa (paulfantom)
# SPDX-License-Identifier: GPL-3.0-or-later

from bases.FrameworkServices.ExecutableService import ExecutableService
import json

import random
#EXIM_COMMAND = 'exim -bpc'
#EXIM_COMMAND = 'cat /home/ubuntu/papajohn/dummy_msg.txt'
#this is the good one EXIM_COMMAND = 'cat /home/ubuntu/papajohn/dummy_msg.txt'
#EXIM_COMMAND = '/home/ubuntu/papajohn/ws.js  10.1.13.10:9000 \'{\"message\":\"ue_get\"}\' '
EXIM_COMMAND = "/home/ubuntu/papajohn/wrap_plugin.sh "
#EXIM_COMMAND="  /home/ubuntu/papajohn/ws.js 172.16.10.203:9000 '{\"message\":\"ue_get\"}'  "#\> /home/ubuntu/papajohn/dummy_msg.txt"
#ORDER = [
#    'qemails',
#]

#CHARTS = {
#    'qemails': {
#        'options': [None, 'Exim Queue Emails', 'emails', 'queue', 'exim.qemails', 'line'],
#        'lines': [
#            ['emails', None, 'absolute']
#        ]
#    }
#}


items2removeFromJson= ['imeisv',
        'm_tmsi',
        'registered',
        'ue_aggregate_max_bitrate_dl',
        'ue_aggregate_max_bitrate_ul',
        'tac',
        'enb_id',
        'enb_ue_id',
        'mme_ue_id']

items2handle={
           'ip',
           'apn',
           'dl_total_bytes',
           'ul_total_bytes'}


class Service(ExecutableService):
    
    def __init__(self, configuration=None, name=None):
        ExecutableService.__init__(self, configuration=configuration, name=name)
        #self.order = ORDER
        self.order = list()
        #self.definitions = CHARTS
        self.definitions = dict()
        self.command = EXIM_COMMAND
        #Simulation data
        self.data=None
        #data in json format
        self.json=None
        #json of stripped data to display
	self.ues_json=None
        #values to show at graphs
	self.values=dict()

    #open simulation file
    def openSimFile(self):
        raw_data = self._get_raw_data()#[0]
        if not raw_data:
            self.data=None
        raw_data.pop(0)
        raw_data.pop(0)
        raw_data.pop(0)
        raw_data.pop(0)
        raw_data.pop(0)
        raw_data.pop(0)
        raw_data.pop(0)
        self.data=raw_data

    #close simulation file
    def closeSimFile(self):
       
        #count how many ues
        ues_count=len(self.json['ue_list'])
        #get ues
        ues_json=self.json['ue_list']
        ####################################
	#######SIMULATION
	#change upload and download values 
	for index in range(ues_count):
	    tmp_ue=ues_json[index]      
	    if 'bearers' in tmp_ue:
	        #get bearers
	        tmp_bearers=tmp_ue['bearers']
	        tmp_bearer_count=len(tmp_ue['bearers'])

	        for bear_index in range(tmp_bearer_count):
		    #get each bearer
		    tmp_bearer=tmp_bearers[bear_index]
		    if tmp_bearer['ul_total_bytes']:
		        tmp_bearer['ul_total_bytes']=tmp_bearer['ul_total_bytes']+random.randint(200,1200)
		    if tmp_bearer['dl_total_bytes']:
		        tmp_bearer['dl_total_bytes']=tmp_bearer['ul_total_bytes']+random.randint(2000,12000)

        #with open('/home/papajohn/REPOSITORIES/netdata/dummy_msg.txt', 'w') as outfile:
        with open('/home/ubuntu/papajohn/dummy_msg.txt', 'w') as outfile:
            json.dump(self.json, outfile)
	#######################################3
	
    #create json from data
    def createJson(self):
        
        tmp_data=None
        data=None
        self.debug("********************************")
        self.debug(self.data)
        self.debug("********************************")
        tmp_data="".join(self.data)
        self.debug(tmp_data)
        self.debug("********************************")

        self.debug(tmp_data[176])  
        
        
        #data =tmp_data.read()[176:]  # json.load(json_file)
        data =json.loads(tmp_data[176:])  # json.load(json_file)
        self.json=data
        return;
        with open('/home/ubuntu/papajohn/dummy_msg.txt') as json_file:
            data =json_file.read()[173:]  # json.load(json_file)
        #self.debug(data)
        self.debug(data[0])  
        self.debug(data[1])  
        self.debug(data[2])  
        self.debug(data[3])  
        self.json=json.loads(data)
        #self.debug(self.json)
    #get the ues from json data


    def stripJson(self):
        #count how many ues
        ues_count=len(self.json['ue_list'])
        #get ues
        self.ues_json=self.json['ue_list']
        #this is not deed at the moment
        for index in range(ues_count):
            for key in items2removeFromJson:
                if key  in  self.ues_json[index]:
                    del self.ues_json[index][key]

    
    #create charts for mme/ue_get
    def mme_ue_get_charts(self):
        #case 1:
        #1 chart per bearer, per ue
        #self.create_charts_absolute(False,self.ues_json)
        self.create_charts_incremental(False,self.ues_json)

    def _get_data(self):
        """
        Format data received from shell command
        :return: dict
        """
        raw_data = self._get_raw_data()
        
        self.debug("*************************")
        self.debug(raw_data)
        if not raw_data:
            self.debug('No data')
            self.debug('-------------------------------->1')
            #return None

        self.data=raw_data
        self.debug('-------------------------------->1')
        self.debug(raw_data)
        self.debug('-------------------------------->2')

	#open file with simulation data
        #self.openSimFile()

        #create initial json
        self.createJson()

        #strip initial json and get ues
        self.stripJson()
       
        #start creating charts
        self.mme_ue_get_charts()        

        tmp=int(self.json['ue_list'][1]['bearers'][0]['ul_total_bytes'])
        #change value
        self.json['ue_list'][1]['bearers'][0]['ul_total_bytes']=tmp+random.randint(20,100)
        self.debug('-->',tmp)
        self.debug('********************')
        self.debug('********************')
        self.debug(self.json['ue_list'][0]['bearers'][0]['ul_total_bytes'])
        self.debug('********************')
  	#close file with simulation data
        #self.closeSimFile()
    
   
        try:
            #return {'emails': tmp}
            #return {'ue_0_bearer_1_ul': 11}
            # for non zero valuesretVal = {x:y for x,y in self.values.items() if y!=0}
            return self.values
            #return retVal
        except (ValueError, AttributeError):
            return None
                                 

    def create_charts_absolute(self,aggregate, server_list):
        if aggregate:
            order = ['dns_group']
            definitions = {
                'dns_group': {
                    'options': [None, 'Bytes', 'bytes', 'radio', 'bytes_up_or_down', 'line'],
                    'lines': []
                }
            }
            for ns in server_list:
                dim = [
                    '_'.join(['ns', ns.replace('.', '_')]),
                    ns,
                    'absolute',
                ]
                definitions['dns_group']['lines'].append(dim)

            self.order= order
	    self.definitions=definitions
        else:
            order=list()
            definitions = dict()
            #order = [''.join(['dns_', ns.replace('.', '_')]) for ns in server_list]
            ues_count=len(self.json['ue_list'])
	    for index in range(ues_count):
		tmp_ue=self.ues_json[index]      
		#get data for each bearer 
		tmp_bearer_count=0
		if 'bearers' in tmp_ue:
		    #get bearers
		    tmp_bearers=tmp_ue['bearers']
		    tmp_bearer_count=len(tmp_ue['bearers'])
		
		    for bear_index in range(tmp_bearer_count):
			#get each bearer
			tmp_bearer=tmp_bearers[bear_index]
                        tmp_order='_'.join(('ue',str(index),'bearer',str(bear_index),'__'))
                        ul_line= '_'.join(('ue',str(index),'bearer',str(bear_index),'ul'))
                        dl_line= '_'.join(('ue',str(index),'bearer',str(bear_index),'dl'))
                        order.append(tmp_order)
		        definitions[tmp_order] = {
		            'options': [None, 'DNS Response Time', 'ms', tmp_order, 'dns_query_time.response_time', 'area'],
		            'lines': [
		                [
		                    ul_line,
		                    ul_line,
		                    'absolute',
                                ],
				[
		                    dl_line,
		                    dl_line,
		                    'absolute'
		                ]
		            ]
		        }
			#create a dict with the values for each line 
			#TODO: Once this works create the this dict on another function and use as required
			self.values[ul_line] = tmp_bearer['ul_total_bytes'] 
			self.values[dl_line] = tmp_bearer['dl_total_bytes'] 

            self.order= order
	    self.definitions=definitions


    def create_charts_incremental(self,aggregate, server_list):
        if aggregate:
            order = ['dns_group']
            definitions = {
                'dns_group': {
                    'options': [None, 'Bytes ', 'bytes', 'Amarisoft DEMO', 'bytes_up_or_down', 'line'],
                    'lines': []
                }
            }
            for ns in server_list:
                dim = [
                    '_'.join(['ns', ns.replace('.', '_')]),
                    ns,
                    'absolute',
                ]
                definitions['dns_group']['lines'].append(dim)

            self.order= order
	    self.definitions=definitions
        else:
            order=list()
            definitions = dict()
            #order = [''.join(['dns_', ns.replace('.', '_')]) for ns in server_list]
            ues_count=len(self.json['ue_list'])
	    for index in range(ues_count):
		tmp_ue=self.ues_json[index]      
		#get data for each bearer 
		tmp_bearer_count=0
		if 'bearers' in tmp_ue:
		    #get bearers
		    tmp_bearers=tmp_ue['bearers']
		    tmp_bearer_count=len(tmp_ue['bearers'])
		
		    for bear_index in range(tmp_bearer_count):
			#get each bearer
			tmp_bearer=tmp_bearers[bear_index]
                        #tmp_order='_'.join(('INCR_ue',str(index),'bearer',str(bear_index),'__'))
                        tmp_order='_'.join((tmp_ue['imsi'],tmp_bearer['ip']))
                        ul_line= 'upload'.join(('ue',str(index),'bearer',str(bear_index),'ul'))
                        dl_line= 'download'.join(('ue',str(index),'bearer',str(bear_index),'dl'))
                        order.append(tmp_order)
		        definitions[tmp_order] = {
		            'options': [None, 'Bytes', 'bytes', tmp_order, 'bytes', 'area'],
		            'lines': [
		                [
		                    ul_line,
		                    ul_line,
		                  #  'absolute',
                                    'incremental'
		                ],
				[
		                    dl_line,
		                    dl_line,
		                  #  'absolute',
                                    'incremental'
		                ]
		            ]
		        }
			#create a dict with the values for each line 
			#TODO: Once this works create the this dict on another function and use as required
			self.values[ul_line] = tmp_bearer['ul_total_bytes'] 
			self.values[dl_line] = tmp_bearer['dl_total_bytes'] 

            self.order= order
	    self.definitions=definitions


