
class Service:
    
    # NSD Management
    NSD_ON_BOARDING = "/ns_descriptors"
    NSD_ENABLE      = "/ns_descriptors/{nsdInfoId}"
    NSD_DISABLE     = "/ns_descriptors/{nsdInfoId}"
    NSD_UPDATE      = "/ns_descriptors/{nsdInfoId}/update"
    NSD_DELETE      = "/ns_descriptors/{nsdInfoId}"
    NSD_QUERY       = "/ns_descriptors/{nsdInfoId}"
    
    # NS Lifecycle management
    NS_ID_CREATE     = "/nslcm/v1/ns_instances"
    # NS_ID_DELETE     = "/ns_descriptors/{nsdInfoId}"
    NS_INSTANTIATION = "/nslcm/v1/ns_instances/<string:nsInstanceId>/instantiate"
    NS_TERMINATION   = "/nslcm/v1/ns_instances/<string:nsInstanceId>/terminate"
    NS_SCALE        = "/nslcm/v1/ns_instances/<string:nsInstanceId>/scale"
    
    CREATE_PM_JOB    = "/nspm/v1/pm_jobs"
    QUERY_PM_JOB     = "/nspm/v1/pm_jobs/<string:pmJobId>/reports/<string:reportId>"


    
    # NFVO NBI
    NOTI_OF_LCM     = "/e2e/nslcm/v1/ns_instances/<string:ns_instance_id>/notification"


    def __init__(self):
            pass

# # NS Management
# api.add_resource(,'/ns_descriptors')
# api.add_resource(,'/ns_descriptors/{nsdInfoId}')
# api.add_resource(,'/ns_descriptors/{nsdInfoId}')
# api.add_resource(,'/ns_descriptors/{nsdInfoId}/update')
# api.add_resource(,'/ns_descriptors/{nsdInfoId}')
# api.add_resource(,'/ns_descriptors/{nsdInfoId}')
# 
# # NS Lifecycle management
# api.add_resource(,'/ns_instances')
# api.add_resource(,'/ns_instances/{nsInstanceId}')
# api.add_resource(,'/ns_instances/{nsInstanceId}/instantiate')
# api.add_resource(,'/ns_instances/{nsInstanceId}/terminate')
# api.add_resource(,'/ns_instances/{nsInstanceId}/update')
# api.add_resource(,'/ns_lcm_op_ops/{nsLcmOpOccId}/<<Task>>')
# api.add_resource(,'/ns_lcm_op_ops/{nsLcmOpOccId}/<<Task>>')
# 
# # NS Performance Management(PM)
# api.add_resource(,'/pm_jobs/{pmJobId}/reports/{reportId}')
# api.add_resource(,'/pm_jobs')
# api.add_resource(,'/pm_jobs')
# 
# # NS Fault Management
# api.add_resource(nsFaultManager,'/alarms/{alarmId}')
# api.add_resource(nsFaultManager,'/subscriptions')
# api.add_resource(nsFaultManager,'/subscriptions/{subscriptionId}')
# 
# # VNF Package Management
# api.add_resource(vnfManager,'/vnf_packages')
# api.add_resource(vnfManager,'/vnf_packages/{onboardedVnfPkgId}/package_content')
# api.add_resource(vnfManager,'/vnf_packages/{onboardedVnfPkgId}')
# api.add_resource(vnfManager,'/vnf_packages/{onboardedVnfPkgId}')
# api.add_resource(vnfManager,'/vnf_packages/{onboardedVnfPkgId}')
# api.add_resource(vnfManager,'/vnf_packages')
