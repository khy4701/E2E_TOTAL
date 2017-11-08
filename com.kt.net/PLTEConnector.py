# -*- coding: utf-8 -*-
import ctypes

from ApiDefine import ResourceType
from ConfigManager import ConfManager
from Connector import Connector
from LogManager import LogManager
import PLTEConnector
from PLTEManager import PLTEManager
from ProvMsg import GeneralQResMsg, GeneralQReqMsg, MTYPE_NBRESTIF_TO_SLEE_REQ, \
    MTYPE_NBRESTIF_TO_SLEE_RES, MTYPE_SBRESTIF_TO_SLEE_RES, HttpReq, HttpRes, \
    MTYPE_SBRESTIF_TO_SLEE_REQ
import sysv_ipc


class PLTEConnector(Connector):
    
    __instance = None
    
    logger = LogManager.getInstance().get_logger()

    @staticmethod
    def getInstance():
        """ Static access method. """
        if PLTEConnector.__instance == None:
            PLTEConnector.__instance = PLTEConnector()
        return PLTEConnector.__instance 

    def __init__(self):
        self.logger.debug('PLTEConnector Init')
        Connector.__init__(self, PLTEManager.getInstance())

        self.plteQueId = int(ConfManager.getInstance().getConfigData( ConfManager.MSGQUEUE_INFO , "PLTEIB" ))
        try :                
                maxQSize = ConfManager.getInstance().getConfigData( ConfManager.MSGQUEUE_INFO , "MAX_QUEUE_SIZE" )
                self.plteQueue = sysv_ipc.MessageQueue(self.plteQueId, max_message_size = int(maxQSize) )
                    
        except Exception as e:
                self.logger.error("msgQueue Connection Failed.. PLTE QUEUE_ID[%d] SIZE[%s]" % (self.plteQueId, maxQSize))


    # NBI, SBI
    def sendMessage(self, apiName, httpReqMsg):
        
        self.logger.info("Send Message..!")
        
        #GenQMsg = GeneralQReqMsg()        
        #GenQMsg.body = httpReqMsg
                
        pData = ctypes.cast(ctypes.byref(httpReqMsg), ctypes.POINTER(ctypes.c_char * ctypes.sizeof(httpReqMsg)))

        try:
            if self.plteQueue is not None :
                
                if httpReqMsg.http_hdr.resource_type == ResourceType.NSLCM_NOTIFICATION_ENDPOINT:
                    self.plteQueue.send( pData.contents.raw, True, MTYPE_SBRESTIF_TO_SLEE_REQ  )
                else:                    
                    self.plteQueue.send( pData.contents.raw, True, MTYPE_NBRESTIF_TO_SLEE_REQ)
                    

        except Exception as e:
            self.logger.error("sendMessage Error! %s" % e)
            return False

        info = httpReqMsg.info
        header = httpReqMsg.http_hdr

        if ConfManager.getInstance().getLogFlag():
            self.logger.info("===============================================")
            self.logger.info("NBRESTIF -> SLEE")
            self.logger.info("===============================================")
            self.logger.info("API_NAME : " + str(apiName))
            self.logger.info("mType : " + str(MTYPE_NBRESTIF_TO_SLEE_REQ))
            self.logger.info("totlen  : "+ str(httpReqMsg.tot_len))
            self.logger.info("msgId   : "+ str(httpReqMsg.msgId))
            self.logger.info("ehttp_idex   : "+ str(httpReqMsg.ehttpf_idx))
            self.logger.info("tid   : "+ str(httpReqMsg.tid))
            self.logger.info("srcQid  : "+ str(httpReqMsg.srcQid))
            self.logger.info("srcSysId: "+ str(httpReqMsg.srcSysId))
            self.logger.info("HEADER----------------------------------------")
            self.logger.info("header.method   : "+ str(header.method))
            self.logger.info("header.api_type : "+ str(header.api_type))
            self.logger.info("header.op_type  : "+ str(header.op_type))
            self.logger.info("header.resource_type : "+ str(header.resource_type))
            self.logger.info("header.length : "+ str(header.length))
            self.logger.info("header.encoding : "+ str(header.encoding))
            self.logger.info("INFO ----------------------------------------")
            self.logger.info("info.ns_instance_id : "+ str(info.ns_instance_id))
            self.logger.info("info.nfvo_ip : "+ str(info.nfvo_ip))
            self.logger.info("info.nfvo_port : "+ str(info.nfvo_port))
            self.logger.info("===============================================")
            
        return True


    # SBI
    def sendResMessage(self, apiName, resMsg):
                
        #GenQMsg = GeneralQResMsg()        
        #GenQMsg.body = resMsg
            
        pData = ctypes.cast(ctypes.byref(resMsg), ctypes.POINTER(ctypes.c_char * ctypes.sizeof(resMsg)))
        try:
            if self.plteQueue is not None :
                
                # MSG TYPE Check!
                self.plteQueue.send( pData.contents.raw, True, MTYPE_SBRESTIF_TO_SLEE_RES )
                
        except Exception as e:
            self.logger.error("sendMessage Error! %s" % e)
            return False

        header = resMsg.http_hdr
        
        if ConfManager.getInstance().getLogFlag():
            self.logger.info("===============================================")
            self.logger.info("SBRESTIF -> SLEE")
            self.logger.info("===============================================")
            self.logger.info("API_NAME : " + str(apiName))
            self.logger.info("mType : " + str(MTYPE_SBRESTIF_TO_SLEE_RES))
            self.logger.info("totlen  : "+ str(resMsg.tot_len))
            self.logger.info("msgId   : "+ str(resMsg.msgId))
            self.logger.info("ehttp_idex   : "+ str(resMsg.ehttpf_idx))
            self.logger.info("tid   : "+ str(resMsg.tid))
            self.logger.info("srcQid  : "+ str(resMsg.srcQid))
            self.logger.info("srcSysId: "+ str(resMsg.srcSysId))
            self.logger.info("RESTCODE : " + str(resMsg.nResult) )
            self.logger.info("BODY   : " + resMsg.jsonBody)
            self.logger.info("HEADER----------------------------------------")
            self.logger.info("header.method   : "+ str(header.method))
            self.logger.info("header.api_type : "+ str(header.api_type))
            self.logger.info("header.op_type  : "+ str(header.op_type))
            self.logger.info("header.resource_type : "+ str(header.resource_type))
            self.logger.info("header.length : "+ str(header.length))
            self.logger.info("header.encoding : "+ str(header.encoding))
            self.logger.info("===============================================")
            
        return True

    
# if __name__ == '__main__':
#       
#     if PLTEConnector.logger is None :
#         print 'None..'
#           
#     # PLTEConnector.logger = LogManager.getInstance()
#       
#     conn = PLTEConnector()    
#     conn.sendMessage()
