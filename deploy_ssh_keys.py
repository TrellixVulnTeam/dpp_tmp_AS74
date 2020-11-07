#!/usr/bin/python3

#-Import needed modules-------------------------------------
import os, sys
import getpass
import socket
from errno import ECONNREFUSED

try:
  import paramiko
except:
  exit('Paramiko Client module for ptyhon3 is needed. Please install it first.')

#-Set globals-----------------------------------------------
CurPath = os.path.dirname(os.path.realpath(__file__))

#-SSH deployer Class----------------------------------------
class ssh_deploy:
  sshHost = str
  sshUsr = str
  sshPwd = str
  sshKey = str
  pubKey = str

  #-Initializer------------------------------------
  def __init__(self):
    print('- New ssh deploy object created')

  #-Helpers----------------------------------------
  def try_usr_std_path(self):
    stdPath = '/home/'+str(self.sshUsr)+'/.ssh/id_rsa.pub' 
    if os.path.isfile(stdPath):
      try: 
        readChk = open(stdPath, 'r')
        readChk.close()
      except:
        return False
      return stdPath
    else:
      return False
  #--------------------------------
  def check_deploy_ready(self):
    chk = []
    if self.sshHost == str:
      chk.append('ssh host')
    if self.sshUsr == str:
      chk.append('ssh user')
    if self.pubKey == str:
      chk.append('public key')
    if self.sshPwd == str and self.sshKey == str:
      chk.append('ssh password or ssh key')
    
    return chk
  
  #-------------------------------
  def ssh_port_scan(self, target, port=22):
    try:
      curSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      socketTimeout = 5
      curSock.settimeout(socketTimeout)
      curSock.connect((target, port))
      return True
    except socket.error as err:
        if err.errno == ECONNREFUSED:
            return False



  #-Main Methodes----------------------------------

  def set_ssh_host(self, curHost=False):
    if type(curHost) is not str:
      print('- SSH host not set or in wrong format.', "\n  Try String" )
      return

    if not self.ssh_port_scan(curHost):
      print('- SSH host not reachable' )
      return
    else:
      self.sshHost = curHost

  #------------------------------------
  def set_ssh_user(self, usr=False):
    if type(usr) is str:
      self.sshUsr = usr.replace(' ', '')
    else:
      curUsr = getpass.getuser()
      print('- Username not defined or in wrong format.', "\n  Proceed with current user: "+curUsr )
      self.sshUsr = curUsr
  
  #------------------------------------
  def set_public_key(self, keyPath=False):
    chk = True
    keyStr = ''
    if type(keyPath) is str:
      curKeyPath = keyPath.replace(' ', '')
      curKeyPath = keyPath.replace('//', '/')
      try:
        curKeyPath = os.path.abspath(keyPath)
        readChk = open(curKeyPath, 'r')
        keyStr = readChk.read()
        readChk.close()
      except:
        chk = False
      
      if not keyStr.startswith('ssh-rsa'): 
        chk = False
      
    else:
      chk = False

    if chk:
      self.pubKey = curKeyPath
    else:
      print('- Invalid public key or file not readable.', "\n  Trying standard public key path...")
      methRes = self.try_usr_std_path()
      if not methRes:
        print('- Unable to use standard public key.', "\n  E.g. try another path.")
        return
      else:
        self.pubKey = methRes
      
  #------------------------------------
  def set_ssh_password(self, curPwd=False):
    if type(curPwd) is not str or len(curPwd) < 1:
      print('- Invalid password input.', "\n  Please try again with string input.")
      return
    else:
      self.sshPwd = curPwd

  #------------------------------------
  def set_ssh_key(self, keyPath=False):
    chk = True
    keyStr = ''

    if type(keyPath) is str:
      curKeyPath = keyPath.replace(' ', '')
      curKeyPath = keyPath.replace('//', '/')
      try:
        curKeyPath = os.path.abspath(keyPath)
        readChk = open(curKeyPath, 'r')
        keyStr = readChk.read()
        readChk.close()
      except:
        chk = False
      
      if '-BEGIN RSA PRIVATE KEY-' not in keyStr or '-END RSA PRIVATE KEY' not in keyStr: 
        chk = False
    else:
      chk = False

    if chk:
      self.sshKey = curKeyPath
    else:
      print('- Invalid ssh key or file not readable.')
      return
  
  #------------------------------------
  def deploy_execute(self):
    chkResAry = self.check_deploy_ready()
    if len(chkResAry) > 0:
      print('- Please set set following parameters first: ' + ', '.join(chkResAry))
      return
    
    sshCli = paramiko.SSHClient()
    sshCli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if os.path.isfile(str(self.sshKey)):
      keyObj = paramiko.RSAKey.from_private_key_file(self.sshKey)
      sshCli.connect(self.sshHost, username=self.sshUsr, pkey=keyObj)
    else:
      sshCli.connect(self.sshHost, username=self.sshUsr, password=self.sshPwd)

    stdin, stdout, stderr = sshCli.exec_command('ls -lah /')
    stdout=stdout.readlines()
    print("".join(stdout))
    
    # sshCli.exec_command('mkdir -p ~/.ssh/')
    # sshCli.exec_command('echo "%s" > ~/.ssh/authorized_keys' % key)
    # sshCli.exec_command('chmod 644 ~/.ssh/authorized_keys')
    # sshCli.exec_command('chmod 700 ~/.ssh/')
    
    sshCli.close()



#-App Runner------------------------------------------------
if __name__ == '__main__':
  testObj = ssh_deploy()
  #testObj.set_ssh_user('ec2-user')
  testObj.set_ssh_user()
  #testObj.set_public_key('../testkey.pub')
  testObj.set_public_key()
  #testObj.set_ssh_password('Oviss1234!')
  testObj.set_ssh_key('/home/scm/.ssh/id_rsa')
  testObj.set_ssh_host('mgmt1')
  test = testObj.check_deploy_ready()
  testObj.deploy_execute()

  print(testObj.sshUsr, testObj.pubKey, testObj.sshPwd, testObj.sshKey, str(test))

