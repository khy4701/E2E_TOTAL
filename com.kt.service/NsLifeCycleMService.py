import time

from flask import request, json
import flask
from flask_restful import Resource

from ApiDefine import ApiDefine, MethodType, ApiType, OPType, ResourceType, \
    ContentEncoding
from LogManager import LogManager
from PLTEManager import PLTEManager
from ProvMsg import HttpHeader, HttpInfo
from ServiceManager import ServiceManager


class NsIdCreation(Resource, ServiceManager):

    logger = LogManager.getInstance().get_logger()
        
    def post(self):
        
        # 1. [WEB->RESTIF] RECEIVE PROCESS
        try:    
            content = request.get_json(force=True)
            data = json.dumps(content)
        except Exception as e:
            data = ''          

        # 2. [WEB->RESTIF] RECEIVE LOGGING       
        ServiceManager.RecvLogging(self.logger, data, request)
                        
        # 3. [RESTIF->APP] MAKE SEND STRUCT
        header = HttpHeader()
        header.method = ServiceManager.getMethodType(request.method)
        header.api_type = ApiType.NSLCM_API_TYPE
        header.resource_type = ResourceType.NSLCM_NS_INSTANCES
        header.op_type = OPType.Create_NS_Identifier_OP_TYPE
        header.encoding = ContentEncoding.PLAIN
        
        Info = ServiceManager.getHttpInfo()
        
        self.logger.info(type(MethodType.POST_METHOD_TYPE))
        self.clientId = PLTEManager.getInstance().getClientReqId()
        reqMsg = ServiceManager.setApiToStructMsg(request, data, self.clientId, header, Info)
                
        # 4. [RESTIF->APP] SEND QUEUE MESSAGE(RELAY)
        PLTEManager.getInstance().sendCommand(ApiDefine.NS_ID_CREATE, self, reqMsg)
                                        
        # 5. WAIT                
        self.receiveReqId = -1
        while self.clientId != self.receiveReqId:
            try:
                time.sleep(1)
            except Exception as e:
                self.logger.error(e)
        
        # 6. [RESTIF->WEB] SEND LOGGING
        ServiceManager.SendLogging(self.logger, self.resMsg)

        # 7. [RESTIF->WEB] SEND RESPONSE        
        return flask.Response(
            self.resMsg.jsonBody,
                       # mimetype=content_type,
            status=self.rspCode
        )
    
    # overide method
    def setComplete(self, rspCode, reqId, rcvMsg):
        self.resMsg = rcvMsg
        self.rspCode = rspCode
        self.receiveReqId = reqId
    

class NsInstantiation(Resource, ServiceManager):
    logger = LogManager.getInstance().get_logger()
    
    def post(self,nsInstanceId ):
        
        # 1. [WEB->RESTIF] RECEIVE PROCESS
        try:        
            content = request.get_json(force=True)
            data = json.dumps(content)
        except Exception as e:
            data = ''          
            
        # 2. [WEB->RESTIF] RECEIVE LOGGING       
        ServiceManager.RecvLogging(self.logger, data, request)

        # 3. [RESTIF->APP] MAKE SEND STRUCT
        header = HttpHeader()
        header.method = ServiceManager.getMethodType(request.method)
        header.api_type = ApiType.NSLCM_API_TYPE
        header.resource_type = ResourceType.NSLCM_INSTANTIATE_NS_TASK
        header.op_type = OPType.Instantiate_NS_OP_TYPE
        header.encoding = ContentEncoding.PLAIN
                        
        Info = ServiceManager.getHttpInfo(nsInstanceId)
                        
        self.clientId = PLTEManager.getInstance().getClientReqId()
        reqMsg = ServiceManager.setApiToStructMsg(request, data, self.clientId, header, Info )
        #reqMsg.info.ns_instance_id = nsInstanceId
                
        # 4. [RESTIF->APP] SEND QUEUE MESSAGE(RELAY)
        PLTEManager.getInstance().sendCommand(ApiDefine.NS_INSTANTIATION, self, reqMsg)
                                        
        # 5. WAIT                
        self.receiveReqId = -1
        while self.clientId != self.receiveReqId:
            try:
                time.sleep(1)
            except Exception as e:
                self.logger.error(e)
        
        # 6. [RESTIF->WEB] SEND LOGGING
        ServiceManager.SendLogging(self.logger, self.resMsg)

        # 7. [RESTIF->WEB] SEND RESPONSE        
        return flask.Response(
            self.resMsg.jsonBody,
                       # mimetype=content_type,
            status=self.rspCode
        )

    
    # overide method
    def setComplete(self, rspCode, reqId, rcvMsg):
        self.resMsg = rcvMsg
        self.rspCode = rspCode
        self.receiveReqId = reqId    
        
        
class NsIdTermination(Resource, ServiceManager):
    logger = LogManager.getInstance().get_logger()

    def post(self,nsInstanceId):

        # 1. [WEB->RESTIF] RECEIVE PROCESS
        try:
            content = request.get_json(force=True)
            data = json.dumps(content)
        except Exception as e:
            data = ''     
                 
        # 2. [WEB->RESTIF] RECEIVE LOGGING       
        ServiceManager.RecvLogging(self.logger, data, request)
                        
        # 3. [RESTIF->APP] MAKE SEND STRUCT
        header = HttpHeader()
        header.method = ServiceManager.getMethodType(request.method)
        header.api_type = ApiType.NSLCM_API_TYPE
        header.resource_type = ResourceType.NSLCM_TERMINATE_NS_TASK
        header.op_type = OPType.Terminate_NS_OP_TYPE
        header.encoding = ContentEncoding.PLAIN

        Info = ServiceManager.getHttpInfo()
        
        self.clientId = PLTEManager.getInstance().getClientReqId()
        reqMsg = ServiceManager.setApiToStructMsg(request, data, self.clientId, header, Info )
                
        # 4. [RESTIF->APP] SEND QUEUE MESSAGE(RELAY)
        PLTEManager.getInstance().sendCommand(ApiDefine.NS_TERMINATION, self, reqMsg)
                                        
        # 5. WAIT                
        self.receiveReqId = -1
        while self.clientId != self.receiveReqId:
            try:
                time.sleep(1)
            except Exception as e:
                self.logger.error(e)
        
        # 6. [RESTIF->WEB] SEND LOGGING
        ServiceManager.SendLogging(self.logger, self.resMsg)

        # 7. [RESTIF->WEB] SEND RESPONSE        
        return flask.Response(
            self.resMsg.jsonBody,
                       # mimetype=content_type,
            status=self.rspCode
        )

    
    # overide method
    def setComplete(self, rspCode, reqId, rcvMsg):
        self.resMsg = rcvMsg
        self.rspCode = rspCode
        self.receiveReqId = reqId    
        
        
class NsScale(Resource, ServiceManager):
    logger = LogManager.getInstance().get_logger()

    def post(self,nsInstanceId):

        # 1. [WEB->RESTIF] RECEIVE PROCESS
        try:
            content = request.get_json(force=True)
            data = json.dumps(content)
        except Exception as e:
            data = ''          
            
        # 2. [WEB->RESTIF] RECEIVE LOGGING       
        ServiceManager.RecvLogging(self.logger, data, request)
                        
        # 3. [RESTIF->APP] MAKE SEND STRUCT
        header = HttpHeader()
        header.method = ServiceManager.getMethodType(request.method)
        header.api_type = ApiType.NSLCM_API_TYPE
        header.resource_type = ResourceType.NSLCM_SCALE_NS_TASK
        header.op_type = OPType.Scale_NS_OP_TYPE
        header.encoding = ContentEncoding.PLAIN
        
        Info = ServiceManager.getHttpInfo()

        self.clientId = PLTEManager.getInstance().getClientReqId()
        reqMsg = ServiceManager.setApiToStructMsg(request, data, self.clientId, header, Info )
                
        # 4. [RESTIF->APP] SEND QUEUE MESSAGE(RELAY)
        PLTEManager.getInstance().sendCommand(ApiDefine.NS_SCALE, self, reqMsg)
                                        
        # 5. WAIT                
        self.receiveReqId = -1
        while self.clientId != self.receiveReqId:
            try:
                time.sleep(1)
            except Exception as e:
                self.logger.error(e)
        
        # 6. [RESTIF->WEB] SEND LOGGING
        ServiceManager.SendLogging(self.logger, self.resMsg)

        # 7. [RESTIF->WEB] SEND RESPONSE        
        return flask.Response(
            self.resMsg.jsonBody,
                       # mimetype=content_type,
            status=self.rspCode
        )

    
    # overide method
    def setComplete(self, rspCode, reqId, rcvMsg):
        self.resMsg = rcvMsg
        self.rspCode = rspCode
        self.receiveReqId = reqId    

#api.add_resource(NsIdTermination, Service.NS_TERMINATION )
#api.add_resource(NsScale, Service.NS_SCALE )
