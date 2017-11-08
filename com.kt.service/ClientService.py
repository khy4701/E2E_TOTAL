import copy
import ctypes
import json
import threading

import requests

from ConfigManager import ConfManager
from LogManager import LogManager
from PLTEManager import PLTEManager
from ProvMsg import HttpRes, HTTPF_MSG_BUFSIZE
from ApiDefine import ApiDefine


class C_NsCreation(threading.Thread):
    
    __instance = None
    
    logger = LogManager.getInstance().get_logger()
    
    def __init__(self, httpMsg):
        super(C_NsCreation, self).__init__()
        self.reqMsg = httpMsg
    
    def run(self):
                
                        
        info   = self.reqMsg.info        
        ip = info.nfvo_ip
        port = info.nfvo_port
                
        #url='http://localhost:5555/departments/abc/123'
        url="http://"+str(ip)+":"+str(port)+"/e2e/nslcm/v1/ns_instances"
        #head = {'Content-type':'application/json', 'Accept':'application/json'} 
        #head = {'Content-type':'application/json'} 
        head = {'Content-type':'application/x-www-form-urlencoded', 'Accept':'application/json'} 

        # 1. [RESTIF->EXT] INPUT REQUSET MESSAGE ( httpReq -> REST API )
    
        payload = self.reqMsg.jsonBody
        
        # 2. [RESTIF->EXT] CLIENT SEND LOGGING        
        if ConfManager.getInstance().getLogFlag():
            self.logger.info("===============================================");
            self.logger.info("RESTIF -> [EXT]")
            self.logger.info("===============================================");
            self.logger.info("URL : " + url)
            self.logger.info("HEADER : " + str(head))
            self.logger.info("TID : " + str(self.reqMsg.tid)) # TID
            self.logger.info("BODY : "  + str(payload))
            self.logger.info("===============================================");
            
            
        # 3. [RESTIF->EXT] SEND DATA
        try:
            # payld = json.dumps(payload)
            #restAPI = requests.post(url,headers=head,data=payld)
            restAPI = requests.post(url,headers=head,data=payload)
            
        # 4. [EXT->RESTIF] RECEIVE LOGGING        
            if ConfManager.getInstance().getLogFlag():
                self.logger.info("===============================================");
                self.logger.info("[EXT] -> RESTIF")
                self.logger.info("===============================================");
                self.logger.info("URL : " + str(restAPI.url))
                self.logger.info("TID : " + str(self.reqMsg.tid)) # TID
                self.logger.info("RESULT : " + str(restAPI.status_code))
                self.logger.info("HEADER : "  + str(restAPI.headers))                   # resData.headers['Content-Length']
                self.logger.info("BODY : "  + str(restAPI.text))
                self.logger.info("===============================================");
            
        except Exception as e:
            # Error Exception -> if External Server is not connected..
            self.logger.info(e)
            return 
            
            
        # 5. [RESTIF->APP] INPUT RESPONSE MESSAGE ( REST API -> httpRes )
        resMsg = HttpRes()

        try:    
            resMsg.msgId = self.reqMsg.msgId
            resMsg.tid = self.reqMsg.tid
            resMsg.ehttpf_idx = self.reqMsg.ehttpf_idx
            resMsg.srcQid = self.reqMsg.srcQid
            resMsg.srcSysId = self.reqMsg.srcSysId
            resMsg.nResult = restAPI.status_code
            resMsg.jsonBody = restAPI.text
            
            resMsg.http_hdr = copy.deepcopy(self.reqMsg.http_hdr)
            resMsg.http_hdr.length = len(resMsg.jsonBody)
            resMsg.tot_len = ctypes.sizeof(HttpRes) - HTTPF_MSG_BUFSIZE + resMsg.http_hdr.length
                    
        except Exception as e :
            resMsg.nResult = 400 
            resMsg.jsonBody = "{Internal Server Error}"
            self.logger.info(e)

            # 6. [RESTIF->APP] SEND AND LOGGING
        PLTEManager.getInstance().sendResCommand( ApiDefine.NS_ID_CREATE , resMsg )



class C_NsIntantication(threading.Thread):
    
    __instance = None
    
    logger = LogManager.getInstance().get_logger()
    
    def __init__(self, httpMsg):
        super(C_NsIntantication, self).__init__()
        self.reqMsg = httpMsg
    
    def run(self):
                
                        
        info   = self.reqMsg.info        
        ip = info.nfvo_ip
        port = info.nfvo_port
        
                        
        #url='http://localhost:5555/departments/abc/123'
        url="http://"+str(ip)+":"+str(port)+"/e2e/nslcm/v1/ns_instances/"+info.ns_instance_id+"/instantiate"
        head = {'Content-type':'application/x-www-form-urlencoded', 'Accept':'application/json'} 

        # 1. [RESTIF->EXT] INPUT REQUSET MESSAGE ( httpReq -> REST API )
    
        payload = self.reqMsg.jsonBody
        
        # 2. [RESTIF->EXT] CLIENT SEND LOGGING        
        if ConfManager.getInstance().getLogFlag():
            self.logger.info("===============================================");
            self.logger.info("RESTIF -> [EXT]")
            self.logger.info("===============================================");
            self.logger.info("URL : " + url)
            self.logger.info("HEADER : " + str(head))
            self.logger.info("TID : " + str(self.reqMsg.tid)) # TID
            self.logger.info("BODY : "  + str(payload))
            self.logger.info("===============================================");
            
            
        # 3. [RESTIF->EXT] SEND DATA
        try:
            # payld = json.dumps(payload)
            #restAPI = requests.post(url,headers=head,data=payld)
            restAPI = requests.post(url,headers=head,data=payload)
            
        # 4. [EXT->RESTIF] RECEIVE LOGGING        
            if ConfManager.getInstance().getLogFlag():
                self.logger.info("===============================================");
                self.logger.info("[EXT] -> RESTIF")
                self.logger.info("===============================================");
                self.logger.info("URL : " + str(restAPI.url))
                self.logger.info("TID : " + str(self.reqMsg.tid)) # TID
                self.logger.info("RESULT : " + str(restAPI.status_code))
                self.logger.info("HEADER : "  + str(restAPI.headers))                   # resData.headers['Content-Length']
                self.logger.info("BODY : "  + str(restAPI.text))
                self.logger.info("===============================================");
            
        except Exception as e:
            # Error Exception -> if External Server is not connected..
            self.logger.info(e)
            return 
            
            
        # 5. [RESTIF->APP] INPUT RESPONSE MESSAGE ( REST API -> httpRes )
        resMsg = HttpRes()

        try:    
            resMsg.msgId = self.reqMsg.msgId
            resMsg.tid = self.reqMsg.tid
            resMsg.ehttpf_idx = self.reqMsg.ehttpf_idx
            resMsg.srcQid = self.reqMsg.srcQid
            resMsg.srcSysId = self.reqMsg.srcSysId
            resMsg.nResult = restAPI.status_code
            resMsg.jsonBody = restAPI.text
            
            resMsg.http_hdr = copy.deepcopy(self.reqMsg.http_hdr)
            resMsg.http_hdr.length = len(resMsg.jsonBody)
            resMsg.tot_len = ctypes.sizeof(HttpRes) - HTTPF_MSG_BUFSIZE + resMsg.http_hdr.length
                    
        except Exception as e :
            resMsg.nResult = 400 
            resMsg.jsonBody = "{Internal Server Error}"
            self.logger.info(e)

            # 6. [RESTIF->APP] SEND AND LOGGING
        PLTEManager.getInstance().sendResCommand( ApiDefine.NS_INSTANTIATION , resMsg )



