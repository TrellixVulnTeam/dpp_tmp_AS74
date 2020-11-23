**Environment conditions:**

 - Git Repo Host: ktigitrepo (10.180.36.141)
 - Git User: iiot_orch
 - Repos Home: /home/iiot_orch/
 - Repo Dir: container_orchestration
 - Remote Host (Satellite): vaf28p1003.wob.vw.vwg (21.7.132.181)
 - External HowTo: [Git - Setting Up the Server (git-scm.com)](https://git-scm.com/book/en/v2/Git-on-the-Server-Setting-Up-the-Server)
<br>
## Git Repo Host configuration:
**Cretation of a separate user for git operation via ssh:**
```console
(as root)$ useradd iiot_orch 
(as root)$ su iiot_orch
$ cd ~
$ mkdir .ssh && chmod 700 .ssh
$ touch .ssh/authorized_keys
$ chmod 600 .ssh/authorized_keys
$ cat /PATH/TO/REMOTE-USER-1/PRIVKEY.pem >> ~/.ssh/authorized_keys
$ cat /PATH/TO/REMOTE-USER-x/PRIVKEY.pem >> ~/.ssh/authorized_keys
$ exit
```
<br>

**Installation of common git client:**
*git client is included in the AppStream RPM Repo on the Rhel8 install DVD*
```console
(as root)$ yum install git
```
<br>

**Creation of a bare git repo:**
```console
(as iiot_orch) $ mkdir /home/iiot_orch/container_orchestration
(as iiot_orch) $ cd /home/iiot_orch/container_orchestration
(as iiot_orch) $ git init --bare
```
<br>

## Clone git repo from remote host
**Configure git host ssh access:**
```console
(as remote-users) $ vi ~/.ssh/config
```
<br>

***The following lines were added:***
```console
Host ktigitrepo 
	HostName 10.180.36.141
	User iiot_orch 
```
<br>

**Clone repo via ssh:**
```console
(as remote-users) $ git clone  ktigitrepo:/home/iiot_orch/container_orchestration
```
