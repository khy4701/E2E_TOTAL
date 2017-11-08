from abc import abstractmethod
import copy
import ctypes

from ApiDefine import MethodType, ApiType, OPType, ContentEncoding, ResourceType
from ConfigManager import ConfManager
from ProvMsg import HttpReq, HttpHeader, HttpInfo, HTTPF_MSG_BUFSIZE


class ServiceManager:
        
    @abstractmethod    
    def setComplete(self, reqId, rcvMsg):
        pass
    
    @staticmethod
    def getMethodType(reqMethod):
        
        if reqMethod == "POST":
            return MethodType.POST_METHOD_TYPE
        elif reqMethod == "GET":
            return MethodType.GET_METHOD_TYPE
        elif reqMethod == "PUT":
            return MethodType.PUT_METHOD_TYPE
        elif reqMethod == "PATCH":
            return MethodType.PATCH_METHOD_TYPE        
        elif reqMethod == "DELETE":
            return MethodType.DELETE_METHOD_TYPE
        else:
            return MethodType.UNKNOWN_METHOD_TYPE
            
        
    @staticmethod
    def setApiToStructMsg(reqAPI, rcvJsonBody, reqId, header, info ):

        httpMsg =  HttpReq()

        header.length = len(rcvJsonBody)
        
        httpMsg.msgId = 111
        httpMsg.tid   = reqId
        httpMsg.ehttpf_idx = 71
        httpMsg.srcQid = 111
        httpMsg.srcSysId = '1'
        httpMsg.info = copy.deepcopy(info)                 
        httpMsg.http_hdr = copy.deepcopy(header)
        httpMsg.jsonBody = copy.deepcopy(rcvJsonBody)
        
        httpMsg.tot_len = ctypes.sizeof(HttpReq) - HTTPF_MSG_BUFSIZE +header.length  #ctypes.sizeof(httpMsg) # need..
        
        return httpMsg

    
    @staticmethod
    def RecvLogging(logger, data, reqAPI):
        if ConfManager.getInstance().getLogFlag():
            logger.info("===============================================");
            logger.info("[WEB] -> RESTIF")
            logger.info("===============================================");
            logger.info("REQUEST URL : " + reqAPI.url)
            logger.info("BODY : "  + data)
            logger.info("===============================================");
            
    @staticmethod
    def SendLogging(logger, resMsg):
        if ConfManager.getInstance().getLogFlag():
            logger.info("===============================================");
            logger.info("RESTIF -> [WEB]")
            logger.info("===============================================");
            logger.info("TID : " + str(resMsg.tid))
            logger.info("RESCODE : " + str(resMsg.nResult))
            logger.info("BODY : "  + str(resMsg.jsonBody))
            logger.info("===============================================");
            
    @staticmethod
    def getHttpInfo(ns_instance_id="None", nfvo_ip ="None", nfvo_port = 0):
        
        Info = HttpInfo()
        Info.ns_instance_id = ns_instance_id
        Info.nfvo_ip = nfvo_ip
        Info.nfvo_port = nfvo_port
        
        return Info

