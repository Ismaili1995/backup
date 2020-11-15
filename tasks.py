from pydrive.auth import GoogleAuth,ServiceAccountCredentials
from pydrive.drive import GoogleDrive
from googleapiclient.discovery import build 
from starlette.responses import FileResponse

import os, glob

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../key/system-backup-1-53687ddf7502.json"
google_login = GoogleAuth()
scope = ['https://www.googleapis.com/auth/drive']
google_login.credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secrets.json', scope)
drive = GoogleDrive(google_login)
service = build('drive', 'v3', credentials=google_login.credentials) 


def delete_file(file_id):
    file_to_delete = drive.CreateFile({'id': file_id})
    file_name = file_to_delete['title']
    file_to_delete.Delete()
    return "file: " + file_name + " has successfully Deleted from the Drive"
   

def download_file(file_id):
    file_to_download = drive.CreateFile({'id': file_id})
    os.chdir("../download")
    file_to_download.GetContentFile(str(file_to_download['title']))
    return file_to_download['title']
    return FileResponse(str(file_to_download['title'])
    )


def upload_file():
    message = ""
    for doc in glob.glob("*"):
    #Uploads a file to the Google Drive.
        if doc != 'client_secrets.json':
            source_file_name = os.getcwd()+"/"+str(doc)
            with open(source_file_name,"r") as f:
                file_name = os.path.basename(f.name)
                file_drive = drive.CreateFile({'title': file_name })  
                file_drive.SetContentFile(source_file_name) 
                file_drive.Upload()
                if file_drive:
                    message = message + "," + file_name
                else:
                    message = "failed"
                file_drive = None          
    # has to call email or sms  function to notify after process being done
    return "The files: " + message + " has been uploaded"


def get_files():
    resource = service.files()
    files = resource.list(pageSize=1000, fields="files(id, name)").execute() 
    return files