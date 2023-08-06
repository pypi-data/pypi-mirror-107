import argparse

from oauth2client import client ,tools, file
import httplib2

from pathlib import Path

from googleapiclient.discovery import build
from google.oauth2 import service_account


class Connection():
  def __init__(self,file_path = 'client_secret.json'):
    self.file_path = file_path
    self.dir_check()
    
  def dir_check(self):
      if Path('./credentials/').is_dir():
          pass
      else:
          Path('./credentials/').mkdir()
  
  def authenticate(self,scope,token_name):
    """Initializes the analyticsreporting service object.

    Returns:
      analytics an authorized analyticsreporting service object.
    """
    # Parse command-line arguments.
    #DO I Need this? 
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[tools.argparser])
    flags = parser.parse_args([])

    # Set up a Flow object to be used if we need to authenticate.
    flow = client.flow_from_clientsecrets(
        self.file_path, scope=scope,
        message=tools.message_if_missing(self.file_path))

    # Prepare credentials, and authorize HTTP object with them.
    # If the credentials don't exist or are invalid run through the native client
    # flow. The Storage object will ensure that if successful the good
    # credentials will get written back to a file.
    storage = file.Storage(f"./credentials/{token_name}.dat")
    credentials = storage.get()
    if credentials is None or credentials.invalid:
      credentials = tools.run_flow(flow, storage, flags)
    http = credentials.authorize(http=httplib2.Http())

    return http


  def gsc(self):
    scope_list = ['https://www.googleapis.com/auth/webmasters.readonly']
    return build('webmasters', 'v3', http=self.authenticate(scope_list,'search_console'))


  def ga(self):
    scope_list = ['https://www.googleapis.com/auth/analytics.readonly']
    return build('analyticsreporting', 'v4', http=self.authenticate(scope_list,'analytics'))


  def cal(self):
    scope_list = ['https://www.googleapis.com/auth/calendar']
    return build('calendar', 'v3', http=self.authenticate(scope_list,'calendar'))


  def sheets(self):
    scope_list = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/spreadsheets']
    return build('sheets', 'v4', http=self.authenticate(scope_list,'sheets'))
  
  
  def gbq(self,sa_file_path = 'gbq-sa.json'):
    return service_account.Credentials.from_service_account_file(sa_file_path)


  def gmail(self):
    scope_list = ['https://mail.google.com/']
    return build('gmail', 'v1', http=self.authenticate(scope_list,'gmail'))