#!/usr/bin/python2


#-Import required modules----------------------------------------------------
import os
import sys
import time
import subprocess 
import argparse
#import threading
import multiprocessing
import socket
import SimpleHTTPServer
import SocketServer
from getpass import getpass
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

  AppParser.add_argument("--http-port", type=int, required=False,
    help="Optional: Set http port for repo web server")

  AppParser.add_argument("--satellite-org", type=str, required=False,
    help="Optional: Set Satellite organization name")
  
  AppParser.add_argument("--satellite-product", type=str, required=False,
    help="Optional: Set Satellite product name")

  AppParser.add_argument("--satellite-repo", type=str, required=False,
    help="Optional: Set Satellite repo name")

  args = AppParser.parse_args()
  return(args)

#-Helpers class---------------------------------------------------------------
class helpers:
  
  #-Initializer-----------------------------------
  def __init__(self):
    inf = "new helpers class generated"

  #---------------------------------------
  def chk_port(self, port):
    curSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    res = curSock.connect_ex(('localhost', port))
    curSock.close()
    if res == 0:
      return False
    else:
      return True

  #---------------------------------------
  def mount_iso(self, isoPath, mntPoint):
    spObj = subprocess.Popen(
      "mount -t iso9660 -o loop "+isoPath+" "+mntPoint, 
      shell=True, 
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE
    )
    spStdOut = spObj.stdout.read()
    spStdErr = spObj.stderr.read()
    # print('STDOUT: ',spStdOut)
    # print('STDERR: ',spStdErr)

    if "read-only" not in spStdErr and len(spStdErr) > 0:
      return False 
    else:
      return True
  
  #---------------------------------------
  def umount_iso(self, mntPoint):
    spObj = subprocess.Popen(
      "umount "+mntPoint+" -f ",
      shell=True, 
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE
    )
    spStdOut = spObj.stdout.read()
    spStdErr = spObj.stderr.read()
    
    if len(spStdErr) > 0: return False
    else: return True

  #---------------------------------------
  def chk_hammer(self):
    spObj = subprocess.Popen(
      "hammer --help", 
      #"curl --help", 
      shell=True, 
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE
    )
    spRes = spObj.stderr.read()
    if len(spRes) > 0: return False
    else: return True  

#-----------------------------------------------------------------------------


#-Main tool class-------------------------------------------------------------
class repo:
  myHelpers = helpers()
  isoPath = None
  mntPoint = None
  mntOk = False
  newMnt = False
  repoPath = "/"
  repoReady = False
  httpPort = None
  curServer = None
  repoUrl = "http://127.0.0.1"
  satOrg = "Default Organization"
  satProd = "Custom Yum Repos" 
  satRepo = None

  #-Initializer-----------------------------------
  def __init__(self):
    print('- New repo object created.')
    self.httpPort = self.find_free_port()


  #-Class methods---------------------------------
  def print_obj_config(self):
    print('- Your configuration:')
    print('  - Path to iso file:         '+str(self.isoPath))
    print('  - Mount point:              '+str(self.mntPoint))
    print('  - Path to repo on dvd iso:  '+str(self.repoPath))
    print('  - Http port:                '+str(self.httpPort))
    print('  - Satellite organization:   '+str(self.satOrg))
    print('  - Satellite product:        '+str(self.satProd))
    print('  - Satellite repository:     '+str(self.satRepo))
    print('  - Ready for execution:      '+str(self.repoReady))
  
  #---------------------------------------
  def find_free_port(self):
    i = 8000
    chk = True
    while chk:
      if self.myHelpers.chk_port(i):
        chk = False
        return i 
      else:
        i +=1
        
  #---------------------------------------
  def set_iso_path(self, isoPath):
    if not os.path.isfile(isoPath):
      print('  ERROR: Path to iso file (%s) is not valid.' %isoPath)
      return False
    
    spObj = subprocess.Popen("file "+isoPath, shell=True, stdout=subprocess.PIPE)
    spRes = spObj.stdout.read()
    if 'DOS/MBR boot' not in spRes and 'bootable' not in spRes:
      print('  ERROR: Path (%s) seams to be no valid os iso.' %isoPath)
      return False

    self.isoPath = isoPath
    if self.satRepo == None:
      self.satRepo = isoPath.split("/")[-1]

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
  def set_http_port(self, httpPort):
    chkRes = self.myHelpers.chk_port(httpPort)
    if not chkRes:
      print("  WARN: Unable to use port ("+str(httpPort)+"). Continue with slternative port ("+str(self.httpPort)+")" )
    else:
      self.httpPort = httpPort

  #---------------------------------------
  def mount_iso(self):
    if self.isoPath == None or self.mntPoint == None: 
      return False

    mntRes = self.myHelpers.mount_iso(self.isoPath, self.mntPoint)
    if not mntRes:
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
    
    umntRes = self.myHelpers.umount_iso(self.mntPoint)
    if not umntRes:
      print('  WARN: Something went wrong while umount %s.' %mntPoint )
    

  #---------------------------------------
  def chk_config_ready(self):

    if self.isoPath == None: return False
    if self.mntPoint == None: return False
    if not self.mntOk: return False
    if self.satRepo == None: return False
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
    time.sleep(3)
    if self.curServer == None:
      print('  WARN: No http server running. nothing todo.' )
      return 
    else:
      self.curServer.terminate()
  
  #---------------------------
  def curl_content_test(self):
    spObj = subprocess.Popen(
      "curl "+self.repoUrl+":"+str(self.httpPort),
      shell=True, 
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE
    )
    spStdOut = spObj.stdout.read()
    print(spStdOut)

  #---------------------------------------
  
  def import_content(self):
    if not self.repoReady:
      return False

    chkHammer = self.myHelpers.chk_hammer()
    if not chkHammer:
      print('  WARN: Satellite Hammer-Cli not available on this system.' )
      usrAnswer = raw_input('  Continue serving repo data via http? (yes/no): ')
      if usrAnswer == "yes":
        print("STOP: via CTL + c")
        try: 
          while True: 
            time.sleep(10)
        except KeyboardInterrupt: 
          print('STOPPED!')
          return
      else:
        return
    else:
      admPwd = getpass('  Please provide Satellite admin password: ')

    #-------------------------------
    repoUrl = self.repoUrl+":"+str(self.httpPort)

    productObj = {
      "--name": self.satProd,
      "--description": self.satProd,
      "--organization": self.satOrg
    }
    repoObj = {
      "--name": self.satRepo,
      "--content-type": "yum",
      "--publish-via-http": "true",
      "--url": repoUrl,
      "--product": self.satProd,
      "--organization": self.satOrg
    }
    syncObj = {
      "--name": self.satRepo,
      "--product": self.satProd,
      "--organization": self.satOrg
    }

    satCmd = 'hammer --password "'+admPwd+'" product create'
    for key, val in productObj.items():
      satCmd += ' ' + key + ' "' + val + '"' 
    print(satCmd)
    spObj = subprocess.Popen( satCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
    spStdOut = spObj.stdout.read()
    spStdErr = spObj.stderr.read()
    print('  Status: ')
    print("  - "+spStdOut + spStdErr)

    satCmd = 'hammer --password "'+admPwd+'" repository create'
    for key, val in repoObj.items():
      if val == "true" or val == "false":
        cusVal = val
      else:
        cusVal = '"'+val+'"'
      satCmd += ' ' + key + ' ' + cusVal
    print(satCmd)
    spObj = subprocess.Popen( satCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
    spStdOut = spObj.stdout.read()
    spStdErr = spObj.stderr.read()
    print("  - "+spStdOut + spStdErr)

    satCmd = 'hammer --password "'+admPwd+'" repository synchronize'
    for key, val in syncObj.items():
      if val == "true" or val == "false":
        cusVal = val
      else:
        cusVal = '"'+val+'"'
      satCmd += ' ' + key + ' ' + cusVal
    print(satCmd)
    spObj = subprocess.Popen( satCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
    spStdOut = spObj.stdout.read()
    spStdErr = spObj.stderr.read()
    print("  - "+spStdOut + spStdErr)

    
  

#-App Runner------------------------------------------------------------------
if __name__ == '__main__':
  
  argsMap = {
    "iso_path": "set_iso_path",
    "mount_point": "set_mount_point",
    "repo_path": "set_repo_path",
    "http_port": "set_http_port"
  } 

  args = build_arg_parse()
  myRepo = repo()

  # print(args)
  for arg, func in argsMap.items():
    try:
      argVal = getattr(args, arg)
      fwFunc = getattr(myRepo, func)
      fwFunc(argVal)
    except:
      inf = "Nothing todo"
    
  myRepo.mount_iso()
  myRepo.chk_config_ready()
  myRepo.print_obj_config()
  
  myRepo.start_http_server()
  #myRepo.curl_content_test()
  myRepo.import_content()

  myRepo.stop_http_serve()
  myRepo.umount_iso()
  

#-----------------------------------------------------------------------------

