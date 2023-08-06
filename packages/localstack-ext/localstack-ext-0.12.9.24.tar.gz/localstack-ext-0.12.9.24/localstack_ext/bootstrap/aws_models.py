from localstack.utils.aws import aws_models
xiFwv=super
xiFwX=None
xiFwP=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  xiFwv(LambdaLayer,self).__init__(arn)
  self.cwd=xiFwX
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.xiFwP.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,xiFwP,env=xiFwX):
  xiFwv(RDSDatabase,self).__init__(xiFwP,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,xiFwP,env=xiFwX):
  xiFwv(RDSCluster,self).__init__(xiFwP,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,xiFwP,env=xiFwX):
  xiFwv(AppSyncAPI,self).__init__(xiFwP,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,xiFwP,env=xiFwX):
  xiFwv(AmplifyApp,self).__init__(xiFwP,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,xiFwP,env=xiFwX):
  xiFwv(ElastiCacheCluster,self).__init__(xiFwP,env=env)
class TransferServer(BaseComponent):
 def __init__(self,xiFwP,env=xiFwX):
  xiFwv(TransferServer,self).__init__(xiFwP,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,xiFwP,env=xiFwX):
  xiFwv(CloudFrontDistribution,self).__init__(xiFwP,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,xiFwP,env=xiFwX):
  xiFwv(CodeCommitRepository,self).__init__(xiFwP,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
