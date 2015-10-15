import dropbox
import os
import datetime

class Dropbox(object):
  def __init__(self,dropbox_token,file_name,dropbox_path_to_upload):
    self.dropbox_token = dropbox_token
    self.file_name = str(file_name)
    self.path = str(dropbox_path_to_upload)
    
  def upload_to_dropbox(self):
    client = dropbox.client.DropboxClient(self.dropbox_token)
    with open(self.file_name, 'rb') as f:
      response = client.put_file(self.path+self.file_name, f)
      folder_metadata = client.metadata(self.path)
      f, metadata = client.get_file_and_metadata(self.path+self.file_name)
    print "Uploaded to Dropbox - File: %-35s  Uploaded at: %30s" %s(str(self.file_name),str(datetime.datetime.now()))
  
  def delete_original(self):
    try:
      os.remove(self.file_name)
    except OSError:
      pass