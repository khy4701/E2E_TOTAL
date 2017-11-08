import time

from flask import request, json
import flask
from flask_restful import Resource

from ApiDefine import ApiDefine, ApiType, ResourceType, OPType, ContentEncoding, \
    MethodType
from LogManager import LogManager
from PLTEManager import PLTEManager
from ProvMsg import HttpHeader
from ServiceManager import ServiceManager


class NotiOfLcm(Resource, ServiceManager):

    logger = LogManager.getInstance().get_logger()
    
    def post(self, ns_instance_id):

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
        header.resource_type = ResourceType.NSLCM_NOTIFICATION_ENDPOINT
        header.op_type = OPType.Notify_OP_TYPE
        header.encoding = ContentEncoding.PLAIN
        
        Info = ServiceManager.getHttpInfo(ns_instance_id)
        
        self.clientId = PLTEManager.getInstance().getClientReqId()
        reqMsg = ServiceManager.setApiToStructMsg(request, data, self.clientId, header, Info)
        
        # 4. [RESTIF->APP] SEND QUEUE MESSAGE(RELAY)
        PLTEManager.getInstance().sendCommand(ApiDefine, self, reqMsg)
                                        
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
        