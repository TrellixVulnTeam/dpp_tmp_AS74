#!/usr/bin/python2


#-Import required modules----------------------------------------------------
import os
import sys
import time
import subprocess 
import argparse
#import threading
import multiprocessing
import SimpleHTTPServer
import SocketServer
#import pylibmount as mnt

#-Global Vars----------------------------------------------------------------


#-Build the ArgParser--------------------------------------------------------

def build_arg_parse():
  AppParser = argparse.ArgumentParser()

  AppParser.add_argument("--iso-path", type=str, required=True,
    help="Required: Set path to dvd iso file.")

  AppParser.add_argument("--repo-path", type=str, required=False,
    help="Optional: Set repo path on dvd iso")

  AppParser.add_argument("--mount-point", type=str, required=True,
    help="Required: Set mount point. Else a standard path will be used")

  args = AppParser.parse_args()
  return(args)

#-Main tool class-------------------------------------------------------------
class repo:
  isoPath = None
  mntPoint = None
  mntOk = False
  newMnt = False
  repoPath = "/"
  repoReady = False
  httpPort = 8000
  curServer = None
  repoUrl = "http://127.0.0.1:"+str(httpPort)+"/"
  

  #-Initializer-----------------------------------
  def __init__(self):
    print('- New repo object created.')
  

  #-Class methods---------------------------------
  def print_obj_config(self):
    print('- Your configuration:')
    print('  - Path to iso file:         '+str(self.isoPath))
    print('  - Mount point:             '+str(self.mntPoint))
    print('  - Path to repo on dvd iso:  '+str(self.repoPath))
    print('  - Ready for execution:      '+str(self.repoReady))
  
  #---------------------------------------
  def set_iso_path(self, isoPath):
    if not os.path.isfile(isoPath):
      print('  ERROR: Path to iso file (%s) is not valid.' %isoPath)
      return False
    
    spObj = subprocess.Popen("file "+isoPath, shell=True, stdout=subprocess.PIPE)
    spRes = spObj.stdout.read()
    if 'DOS/MBR boot' not in spRes:
      print('  ERROR: Path (%s) seams to be no valid os iso.' %isoPath)
      return False

    self.isoPath = isoPath

  #---------------------------------------
  def set_repo_path(self, repoPath):
   
    repoPath = repoPath.replace(" ", "")
    if '/' not in repoPath or not repoPath.startswith('/'):
      print('  WARN: Path (%s) must be in a valid format and must start with a "/".' %repoPath)
      return False

    if not repoPath.endswith('/'):
      repoPath = repoPath+'/'
    self.repoPath = repoPath

  #---------------------------------------
  def set_mount_point(self, mntPoint):
   
    mntPoint = mntPoint.replace(" ", "")
    if '/' not in mntPoint or not mntPoint.startswith('/'):
      print('  WARN: Mount point (%s) must be in a valid format and start with a "/".' %mntPoint)
      return False
    
    if mntPoint.endswith("/"):
      mntPoint = mntPoint[:-1]

    if not os.path.isdir(mntPoint):
      try:
        os.makedirs(mntPoint)
        self.newMnt = True
      except:
        print('  ERROR: Fail to create mount point (%s).' %mntPoint )
        return False

    if os.path.ismount(mntPoint):
      print('  ERROR: Mount point (%s) already in use!' %mntPoint )
      return False

    tmpFileList = os.listdir(mntPoint)
    if len(tmpFileList) > 0:
      print('  ERROR: Mount point (%s) is not empty!' %mntPoint )
      return False

    self.mntPoint = mntPoint

  #---------------------------------------
  def mount_iso(self):
    if self.isoPath == None or self.mntPoint == None: 
      return False

    spObj = subprocess.Popen(
      "mount -t iso9660 -o loop "+self.isoPath+" "+self.mntPoint, 
      shell=True, 
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE
    )
    spStdOut = spObj.stdout.read()
    spStdErr = spObj.stderr.read()
    # print('STDOUT: ',spStdOut)
    # print('STDERR: ',spStdErr)

    if "mounted read-only" not in spStdErr and len(spStdErr) > 0:
      print('  ERROR: Unable to mount DVD (%s).' %self.isoPath )
      return False 
    
    #finalRepoPath = os.path.join(self.mntPoint, self.repoPath ) # Geht in python2 net richtig :(
    finalRepoPath = self.mntPoint + self.repoPath 
    finalRepoPath = finalRepoPath.replace("//", "/")
    try:
      dirAry = os.listdir(finalRepoPath)
    except:
      print('  ERROR: Repo path (%s) does not exist.' %finalRepoPath )
      return False
    
    if "repodata" not in dirAry:
      print('  ERROR: There is no RPM Repo in path (%s).' %finalRepoPath )
      return False

    self.mntOk = True

  #---------------------------------------
  def umount_iso(self):

    if not self.mntOk or self.mntPoint == None or not os.path.ismount(str(self.mntPoint)):
      print('  WARN: No DVD mounted. nothing todo.' )
      return 
    
    spObj = subprocess.Popen(
      "umount "+self.mntPoint+" -f ",
      shell=True, 
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE
    )
    spStdOut = spObj.stdout.read()
    spStdErr = spObj.stderr.read()
    
    if len(spStdErr) > 0:
      print('  WARN: Something went wrong while umount %s.' %self.mntPoint )
      return False
    else:
      return True

  #---------------------------------------
  def chk_config_ready(self):

    if self.isoPath == None: return False
    if self.mntPoint == None: return False
    if not self.mntOk: return False
    #Spache for more checks ;)

    self.repoReady = True

  #---------------------------------------
  def start_http_server(self):
    if not self.repoReady:
      return False

    def start_thread(mntPoint):
      os.chdir(mntPoint)
      SrvHandler = SimpleHTTPServer.SimpleHTTPRequestHandler
      SrvHttpd = SocketServer.TCPServer(("", self.httpPort), SrvHandler)
      SrvHttpd.serve_forever()

    fullRepoPath = self.mntPoint + '/' + self.repoPath
    fullRepoPath = fullRepoPath.replace("//", "/")

    curServer = multiprocessing.Process(target=start_thread, args=(fullRepoPath,))
    curServer.daemon = True 
    curServer.start()
    self.curServer = curServer
  
  #---------------------------
  def stop_http_serve(self):
    time.sleep(2)
    if self.curServer == None:
      print('  WARN: No http server running. nothing todo.' )
      return 
    else:
      self.curServer.terminate()
  
  #---------------------------
  def curl_content_test(self):
    spObj = subprocess.Popen(
      "curl "+self.repoUrl, 
      shell=True, 
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE
    )
    spStdOut = spObj.stdout.read()
    print(spStdOut)

  #---------------------------------------
  
  def import_content(self):
    
    productName = "palim"
    productDescription = "Just for Testing"
    satelliteOrg = "Default Organization"

    repoName = "palim repo"
    repoContent = "yum" 
    repoViaHttp = "true"
    repoUrl = self.repoUrl


    productObj = {
      "--name": productName,
      "--description": productDescription,
      "--organization": satelliteOrg,
    }
    repoObj = {
      "--name": repoName,
      "--content-type": repoContent,
      "--publish-via-http": repoViaHttp,
      "--url": repoUrl,
      "--product": productName,
      "--organization": satelliteOrg,
    }

    satCmd = 'hammer product create'
    for key, val in productObj.items():
      satCmd += ' ' + key + ' "' + val + '"' 
    print(satCmd)

    satCmd = 'hammer repository create'
    for key, val in repoObj.items():
      if val == "true":
        cusVal = 'true'
      else:
        cusVal = '"'+val+'"'

      satCmd += ' ' + key + ' ' + cusVal
    print(satCmd)

  

#-App Runner------------------------------------------------------------------
if __name__ == '__main__':
  args = build_arg_parse()
  myRepo = repo()

  # print(args)
  myRepo.set_iso_path(args.iso_path)
  myRepo.set_mount_point(args.mount_point) 
  if args.repo_path:
    myRepo.set_repo_path(args.repo_path) 
    
  myRepo.mount_iso()
  myRepo.chk_config_ready()
  myRepo.print_obj_config()
  
  myRepo.start_http_server()
  myRepo.curl_content_test()
  myRepo.import_content()

  myRepo.stop_http_serve()
  myRepo.umount_iso()
  

#-----------------------------------------------------------------------------

