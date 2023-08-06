from localstack.utils.aws import aws_models
psNBL=super
psNBn=None
psNBx=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  psNBL(LambdaLayer,self).__init__(arn)
  self.cwd=psNBn
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.psNBx.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,psNBx,env=psNBn):
  psNBL(RDSDatabase,self).__init__(psNBx,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,psNBx,env=psNBn):
  psNBL(RDSCluster,self).__init__(psNBx,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,psNBx,env=psNBn):
  psNBL(AppSyncAPI,self).__init__(psNBx,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,psNBx,env=psNBn):
  psNBL(AmplifyApp,self).__init__(psNBx,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,psNBx,env=psNBn):
  psNBL(ElastiCacheCluster,self).__init__(psNBx,env=env)
class TransferServer(BaseComponent):
 def __init__(self,psNBx,env=psNBn):
  psNBL(TransferServer,self).__init__(psNBx,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,psNBx,env=psNBn):
  psNBL(CloudFrontDistribution,self).__init__(psNBx,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,psNBx,env=psNBn):
  psNBL(CodeCommitRepository,self).__init__(psNBx,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
