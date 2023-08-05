from localstack.utils.aws import aws_models
WLiHy=super
WLiHM=None
WLiHG=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  WLiHy(LambdaLayer,self).__init__(arn)
  self.cwd=WLiHM
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.WLiHG.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,WLiHG,env=WLiHM):
  WLiHy(RDSDatabase,self).__init__(WLiHG,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,WLiHG,env=WLiHM):
  WLiHy(RDSCluster,self).__init__(WLiHG,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,WLiHG,env=WLiHM):
  WLiHy(AppSyncAPI,self).__init__(WLiHG,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,WLiHG,env=WLiHM):
  WLiHy(AmplifyApp,self).__init__(WLiHG,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,WLiHG,env=WLiHM):
  WLiHy(ElastiCacheCluster,self).__init__(WLiHG,env=env)
class TransferServer(BaseComponent):
 def __init__(self,WLiHG,env=WLiHM):
  WLiHy(TransferServer,self).__init__(WLiHG,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,WLiHG,env=WLiHM):
  WLiHy(CloudFrontDistribution,self).__init__(WLiHG,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,WLiHG,env=WLiHM):
  WLiHy(CodeCommitRepository,self).__init__(WLiHG,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
