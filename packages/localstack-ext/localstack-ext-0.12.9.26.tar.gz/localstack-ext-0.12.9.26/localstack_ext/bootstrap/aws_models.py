from localstack.utils.aws import aws_models
rOnKE=super
rOnKS=None
rOnKi=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  rOnKE(LambdaLayer,self).__init__(arn)
  self.cwd=rOnKS
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.rOnKi.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,rOnKi,env=rOnKS):
  rOnKE(RDSDatabase,self).__init__(rOnKi,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,rOnKi,env=rOnKS):
  rOnKE(RDSCluster,self).__init__(rOnKi,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,rOnKi,env=rOnKS):
  rOnKE(AppSyncAPI,self).__init__(rOnKi,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,rOnKi,env=rOnKS):
  rOnKE(AmplifyApp,self).__init__(rOnKi,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,rOnKi,env=rOnKS):
  rOnKE(ElastiCacheCluster,self).__init__(rOnKi,env=env)
class TransferServer(BaseComponent):
 def __init__(self,rOnKi,env=rOnKS):
  rOnKE(TransferServer,self).__init__(rOnKi,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,rOnKi,env=rOnKS):
  rOnKE(CloudFrontDistribution,self).__init__(rOnKi,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,rOnKi,env=rOnKS):
  rOnKE(CodeCommitRepository,self).__init__(rOnKi,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
