import ctypes
import threading
import time

from ConfigManager import ConfManager
from Connector import Connector
from LogManager import LogManager
from PLTEManager import PLTEManager
from ProvMsg import GeneralQResMsg, HttpRes , MTYPE_SLEE_TO_SBRESTIF_RES, MTYPE_SLEE_TO_NBRESTIF_RES
from Receiver import Receiver
import sysv_ipc


usleep = lambda x: time.sleep(x/1000000.0)

class ResReceiver(Receiver):
    
    myQueue = None   
    __instance = None
    
    logger = LogManager.getInstance().get_logger()

    @staticmethod
    def getInstance():
        """ Static access method. """
        if ResReceiver.__instance == None:
            ResReceiver.__instance = ResReceiver()
        return ResReceiver.__instance 
        
    
    def __init__(self):
        Receiver.__init__(self)
        ResReceiver.logger.info("ResReceiver Init")
        
        try :

            myQueId = 0
            if ResReceiver.myQueue is None:
                    #IPC_CREAT : create or return key if it is allocated.
                    #IPC_CREX  : IPC_CREAT | IPC_EXCL 
                    #IPC_EXCL  : return -1 if there is already allocated.
                    myQueId = int(ConfManager.getInstance().getConfigData( ConfManager.MSGQUEUE_INFO , "RESTIF_S" ))
                    maxQSize = ConfManager.getInstance().getConfigData( ConfManager.MSGQUEUE_INFO , "MAX_QUEUE_SIZE" )
    
                    #ResReceiver.myQueue = sysv_ipc.MessageQueue(myQueId, sysv_ipc.IPC_CREAT, mode=0777, max_message_size = int(maxQSize) )
                    ResReceiver.myQueue = sysv_ipc.MessageQueue(myQueId, sysv_ipc.IPC_CREAT )                    
                    self.resReceiver = self
                    self.resReceiver.start()
            
        except Exception as e:
                ResReceiver.logger.error("msgQueue Connection Failed.. RESTIF_S QUEUE_ID[%d] SIZE[%s] %s" % (myQueId, maxQSize, e))

        return None


    def readMessage(self):
        try:
            
            if ResReceiver.myQueue is None:
                self.logger.error("msgQueue[MYQUEUE] Get Failed...")
                return
                                   
            #GenQMsg = GeneralQResMsg()      
            resMsg = HttpRes()
              
            (message, msgType) = ResReceiver.myQueue.receive(ctypes.sizeof(resMsg))
            mydata = ctypes.create_string_buffer( message )
            
            self.logger.error("ResReceiver Queue Read Message ..")

            if msgType == MTYPE_SLEE_TO_NBRESTIF_RES or msgType ==  MTYPE_SLEE_TO_SBRESTIF_RES :    

                # Server Mode( Handling Response Message )
                ctypes.memmove(ctypes.pointer(resMsg), mydata ,ctypes.sizeof(resMsg))
                
                #resMsg = GenQMsg.body
                headerMsg = resMsg.http_hdr
        
                # Receive Message Logging
                if ConfManager.getInstance().getLogFlag():
                    self.logger.info("===============================================");
                    self.logger.info("SLEE -> NBRESTIF")
                    self.logger.info("===============================================");
                    self.logger.info("QmsgType: %d" %msgType )
                    self.logger.info("tot_len : %s" %resMsg.tot_len )
                    self.logger.info("tid : %d" %resMsg.tid )
                    self.logger.info("msgId : %d" %resMsg.msgId )
                    self.logger.info("ehttp_idx : %d" %resMsg.ehttpf_idx )
                    self.logger.info("srcQid : %d" %resMsg.srcQid )
                    self.logger.info("srcSysId : %c" %resMsg.srcSysId )
                    self.logger.info("nResult : %d" %resMsg.nResult )
                    self.logger.info("jsonBody: %s" %resMsg.jsonBody )
                    self.logger.info("HEADER----------------------------------------");
                    self.logger.info("method: %d" %headerMsg.method )
                    self.logger.info("api_type: %d" %headerMsg.api_type )
                    self.logger.info("op_type: %d" %headerMsg.op_type )
                    self.logger.info("resource_type: %d" %headerMsg.resource_type )
                    self.logger.info("length: %d" %headerMsg.length )
                    self.logger.info("encoding: %c" %headerMsg.encoding )
                    self.logger.info("===============================================");

                
                #if msgType == PLTEMANAGER_TYPE: 
                PLTEManager.getInstance().receiveHandling(resMsg.nResult, resMsg.tid, resMsg )
        
        except Exception as e :
            self.logger.error("Msgrcv Failed..  %s" %e)
            time.sleep(1)
            
        
    def run(self):      
 
        try:                                
            while self.resReceiver == self:
                usleep(100)
                self.readMessage()
                 
        except Exception as e:
            self.logger.error(e)
#       self.readMessage()


