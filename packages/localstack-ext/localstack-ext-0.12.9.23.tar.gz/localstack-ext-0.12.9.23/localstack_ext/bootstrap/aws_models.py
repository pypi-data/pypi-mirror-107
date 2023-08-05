from localstack.utils.aws import aws_models
GVQtm=super
GVQti=None
GVQtJ=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  GVQtm(LambdaLayer,self).__init__(arn)
  self.cwd=GVQti
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.GVQtJ.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,GVQtJ,env=GVQti):
  GVQtm(RDSDatabase,self).__init__(GVQtJ,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,GVQtJ,env=GVQti):
  GVQtm(RDSCluster,self).__init__(GVQtJ,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,GVQtJ,env=GVQti):
  GVQtm(AppSyncAPI,self).__init__(GVQtJ,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,GVQtJ,env=GVQti):
  GVQtm(AmplifyApp,self).__init__(GVQtJ,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,GVQtJ,env=GVQti):
  GVQtm(ElastiCacheCluster,self).__init__(GVQtJ,env=env)
class TransferServer(BaseComponent):
 def __init__(self,GVQtJ,env=GVQti):
  GVQtm(TransferServer,self).__init__(GVQtJ,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,GVQtJ,env=GVQti):
  GVQtm(CloudFrontDistribution,self).__init__(GVQtJ,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,GVQtJ,env=GVQti):
  GVQtm(CodeCommitRepository,self).__init__(GVQtJ,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
