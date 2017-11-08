import ctypes
import time

from ApiDefine import ResourceType
from ClientService import NfvoService, C_NsCreation, C_NsIntantication
from ConfigManager import ConfManager
from LogManager import LogManager
from ProvMsg import GeneralQReqMsg, MTYPE_SLEE_TO_SBRESTIF_REQ, HttpReq
from Receiver import Receiver
import sysv_ipc


usleep = lambda x: time.sleep(x/1000000.0)

class ReqReceiver(Receiver):
    
    myQueue = None   
    __instance = None
    
    logger = LogManager.getInstance().get_logger()

    @staticmethod
    def getInstance():
        """ Static access method. """
        if ReqReceiver.__instance == None:
            ReqReceiver.__instance = ReqReceiver()
        return ReqReceiver.__instance 
    
    def __init__(self):
        Receiver.__init__(self)
        ReqReceiver.logger.error("ReqReceiver Init")

        try :
            myQueId = 0
            if ReqReceiver.myQueue is None:
                    #IPC_CREAT : create or return key if it is allocated.
                    #IPC_CREX  : IPC_CREAT | IPC_EXCL 
                    #IPC_EXCL  : return -1 if there is already allocated.
                    myQueId = int(ConfManager.getInstance().getConfigData( ConfManager.MSGQUEUE_INFO , "RESTIF_C" ))    
                    maxQSize = ConfManager.getInstance().getConfigData( ConfManager.MSGQUEUE_INFO , "MAX_QUEUE_SIZE" )

                    #ReqReceiver.myQueue = sysv_ipc.MessageQueue(myQueId, sysv_ipc.IPC_CREAT, mode=0777 , max_message_size = int(maxQSize) )
                    ReqReceiver.myQueue = sysv_ipc.MessageQueue(myQueId, sysv_ipc.IPC_CREAT)
                    
                    self.reqReceiver = self
                    self.reqReceiver.start()
            
        except Exception as e:
                ReqReceiver.logger.error("msgQueue Connection Failed.. RESTIF_C QUEUE_ID[%d] %s" % (myQueId, e))

        return None


    def readMessage(self):
        try:
            
            if ReqReceiver.myQueue is None:
                self.logger.error("msgQueue[RESTIF_RECV] Get Failed...")
                return
            
            #GenQMsg = GeneralQReqMsg()
            reqMsg = HttpReq()
        
            (message, msgType) = ReqReceiver.myQueue.receive(ctypes.sizeof(reqMsg))
            mydata = ctypes.create_string_buffer( message )
            
            #reqMsg = GenQMsg.body

            if msgType == MTYPE_SLEE_TO_SBRESTIF_REQ:    
                # Client Mode ( Handling Request Message )
                
                ctypes.memmove(ctypes.pointer(reqMsg), mydata ,ctypes.sizeof(reqMsg))
                            
                # Receive Message Logging
                if ConfManager.getInstance().getLogFlag():
                    headerMsg = reqMsg.http_hdr      
                    info = reqMsg.info
                                  
                    self.logger.info("===============================================")
                    self.logger.info("SLEE -> SBRESTIF")
                    self.logger.info("===============================================")
                    self.logger.info("msgType: %d" %msgType )
                    self.logger.info("tot_len : %s" %reqMsg.tot_len )
                    self.logger.info("msgId : %d" %reqMsg.msgId )
                    self.logger.info("tid : %d" %reqMsg.tid )
                    self.logger.info("ehttp_idx : %d" %reqMsg.ehttpf_idx )
                    self.logger.info("srcQid : %d" %reqMsg.srcQid )
                    self.logger.info("srcSysId : %c" %reqMsg.srcSysId )
                    self.logger.info("jsonBody: %s" %reqMsg.jsonBody )
                    self.logger.info("HEADER-----------------------------------------")
                    self.logger.info("method: %d" %headerMsg.method )
                    self.logger.info("api_type: %d" %headerMsg.api_type )
                    self.logger.info("op_type: %d" %headerMsg.op_type )
                    self.logger.info("resource_type: %d" %headerMsg.resource_type )
                    self.logger.info("length: %d" %headerMsg.length )
                    self.logger.info("encoding: %c" %headerMsg.encoding )
                    self.logger.info("INFO  -----------------------------------------")
                    self.logger.info("NFVO_IP: %s" %info.nfvo_ip )
                    self.logger.info("NFVO_PORT: %d" %info.nfvo_port )                   
                    self.logger.info("===============================================")

                
                if headerMsg.resource_type == ResourceType.NSLCM_NS_INSTANCES:
                    clientReq = C_NsCreation(reqMsg)
                elif headerMsg.resource_type == ResourceType.NSLCM_INSTANTIATE_NS_TASK:
                    clientReq = C_NsIntantication(reqMsg)
                                        
                clientReq.start()

                return 
        
        except Exception as e :
            self.logger.error("Msgrcv Failed..  %s" %e)
            time.sleep(1)
            
        
    def run(self):      
 
        try:                                
            while self.reqReceiver == self:
                usleep(100)
                self.readMessage()
                 
        except Exception as e:
            self.logger.error(e)
#       self.readMessage()


