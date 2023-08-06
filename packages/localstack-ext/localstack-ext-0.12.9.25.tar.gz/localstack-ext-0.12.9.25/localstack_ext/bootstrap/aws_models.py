from localstack.utils.aws import aws_models
nreSq=super
nreSp=None
nreSh=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  nreSq(LambdaLayer,self).__init__(arn)
  self.cwd=nreSp
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.nreSh.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,nreSh,env=nreSp):
  nreSq(RDSDatabase,self).__init__(nreSh,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,nreSh,env=nreSp):
  nreSq(RDSCluster,self).__init__(nreSh,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,nreSh,env=nreSp):
  nreSq(AppSyncAPI,self).__init__(nreSh,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,nreSh,env=nreSp):
  nreSq(AmplifyApp,self).__init__(nreSh,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,nreSh,env=nreSp):
  nreSq(ElastiCacheCluster,self).__init__(nreSh,env=env)
class TransferServer(BaseComponent):
 def __init__(self,nreSh,env=nreSp):
  nreSq(TransferServer,self).__init__(nreSh,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,nreSh,env=nreSp):
  nreSq(CloudFrontDistribution,self).__init__(nreSh,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,nreSh,env=nreSp):
  nreSq(CodeCommitRepository,self).__init__(nreSh,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
