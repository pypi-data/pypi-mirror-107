from localstack.utils.aws import aws_models
ohuxg=super
ohuxn=None
ohuxq=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  ohuxg(LambdaLayer,self).__init__(arn)
  self.cwd=ohuxn
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.ohuxq.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,ohuxq,env=ohuxn):
  ohuxg(RDSDatabase,self).__init__(ohuxq,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,ohuxq,env=ohuxn):
  ohuxg(RDSCluster,self).__init__(ohuxq,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,ohuxq,env=ohuxn):
  ohuxg(AppSyncAPI,self).__init__(ohuxq,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,ohuxq,env=ohuxn):
  ohuxg(AmplifyApp,self).__init__(ohuxq,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,ohuxq,env=ohuxn):
  ohuxg(ElastiCacheCluster,self).__init__(ohuxq,env=env)
class TransferServer(BaseComponent):
 def __init__(self,ohuxq,env=ohuxn):
  ohuxg(TransferServer,self).__init__(ohuxq,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,ohuxq,env=ohuxn):
  ohuxg(CloudFrontDistribution,self).__init__(ohuxq,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,ohuxq,env=ohuxn):
  ohuxg(CodeCommitRepository,self).__init__(ohuxq,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
