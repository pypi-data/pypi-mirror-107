import sys
CqWhJ=object
CqWhI=staticmethod
CqWhR=False
CqWhr=Exception
CqWhL=None
CqWhV=input
CqWhO=list
import json
import logging
import getpass
from localstack.config import CONFIG_FILE_PATH,load_config_file
from localstack.constants import API_ENDPOINT
from localstack.utils.common import to_str,safe_requests,save_file,load_file
LOG=logging.getLogger(__name__)
class AuthProvider(CqWhJ):
 @CqWhI
 def name():
  raise
 def get_or_create_token(self,username,password,headers):
  pass
 def get_user_for_token(self,token):
  pass
 @CqWhI
 def providers():
  return{c.name():c for c in AuthProvider.__subclasses__()}
 @CqWhI
 def get(provider,raise_error=CqWhR):
  provider_class=AuthProvider.providers().get(provider)
  if not provider_class:
   msg='Unable to find auth provider class "%s"'%provider
   LOG.warning(msg)
   if raise_error:
    raise CqWhr(msg)
   return CqWhL
  return provider_class()
class AuthProviderInternal(AuthProvider):
 @CqWhI
 def name():
  return 'internal'
 def get_or_create_token(self,username,password,headers):
  data={'username':username,'password':password}
  response=safe_requests.post('%s/user/signin'%API_ENDPOINT,json.dumps(data),headers=headers)
  if response.status_code>=400:
   return
  try:
   result=json.loads(to_str(response.content or '{}'))
   return result['token']
  except CqWhr:
   pass
 def read_credentials(self,username):
  print('Please provide your login credentials below')
  if not username:
   sys.stdout.write('Username: ')
   sys.stdout.flush()
   username=CqWhV()
  password=getpass.getpass()
  return username,password,{}
 def get_user_for_token(self,token):
  raise CqWhr('Not implemented')
def login(provider,username=CqWhL):
 auth_provider=AuthProvider.get(provider)
 if not auth_provider:
  providers=CqWhO(AuthProvider.providers().keys())
  raise CqWhr('Unknown provider "%s", should be one of %s'%(provider,providers))
 username,password,headers=auth_provider.read_credentials(username)
 print('Verifying credentials ... (this may take a few moments)')
 token=auth_provider.get_or_create_token(username,password,headers)
 if not token:
  raise CqWhr('Unable to verify login credentials - please try again')
 configs=load_config_file()
 configs['login']={'provider':provider,'username':username,'token':token}
 save_file(CONFIG_FILE_PATH,json.dumps(configs))
def logout():
 configs=json_loads(load_file(CONFIG_FILE_PATH,default='{}'))
 configs['login']={}
 save_file(CONFIG_FILE_PATH,json.dumps(configs))
def json_loads(s):
 return json.loads(to_str(s))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
