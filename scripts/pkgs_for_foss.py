#!/usr/libexec/platform-python

import os, sys
import csv

#-Check if installer modules for python are available--- 

try: 
  import yum
  yumOk = True
except:
  yumOk = False
  
try: 
  import dnf
  dnfOk = True
except:
  dnfOk = False

#-------------------------
if not yumOk and not dnfOk:
  exit("Yum and DNF not found! Are you on a RedHat/CentOS System?")

#-------------------------------------------------------

#-The csv File Thong------------------------------------
csvCols = ['Name', 'Full PKG name', 'Architecture', 'Version', 'Release', 'Source URL', 'From', 'From Repo', 'Short description']
csvPath = "installed_yum_packages.csv"
csvFileObj = open(csvPath, 'w')
csvWriter = csv.DictWriter(csvFileObj, fieldnames=csvCols)
csvWriter.writeheader()

#-The yum vatriant--------------------------------------
if yumOk:
  print("Using YUM Module: ")

  yumObj = yum.YumBase()
  pkgList = yumObj.rpmdb.returnPackages()

  for pkg in pkgList:
    curDict = {
      'Name': pkg.name,
      'Full PKG name': pkg.nevra,
      'Architecture': pkg.arch,
      'Version': str(pkg.version),
      'Release': pkg.release,
      'Source URL': pkg.url,
      'From': pkg.committer,
      'From Repo': pkg.ui_from_repo,
      'Short description': pkg.summary
    }
    csvWriter.writerow(curDict)

  csvFileObj.close()

#-The dnf vatriant--------------------------------------
elif dnfOk:
  print("Using DNF Module: ")

  loop = ['a', 'arch', 'base', 'baseurl', 'buildtime', 'changelogs', 'chksum', 'conflicts', 'debug_name', 'debugsource_name', 'description', 'downloadsize', 'e', 'enhances', 'epoch', 'evr', 'evr_cmp', 'evr_eq', 'evr_gt', 'evr_lt', 'files', 'getDiscNum', 'get_advisories', 'get_delta_from_evr', 'group', 'hdr_chksum', 'hdr_end', 'idx', 'installed', 'installsize', 'installtime', 'license', 'localPkg', 'location', 'medianr', 'name', 'obsoletes', 'packager', 'pkgdir', 'pkgtup', 'provides', 'r', 'reason', 'recommends', 'relativepath', 'release', 'remote_location', 'repo', 'repoid', 'reponame', 'requires', 'requires_pre', 'returnIdSum', 'rpmdbid', 'size', 'source_debug_name', 'source_name', 'sourcerpm', 'suggests', 'summary', 'supplements', 'ui_from_repo', 'url', 'v', 'verifyLocalPkg', 'version']

  dnfObj = dnf.Base()
  dnfObj.fill_sack()

  pkgQry = dnfObj.sack.query()
  pkgObj = pkgQry.installed()
  #pkgObj = pkgObj.filter(name='ansible')

  pkgList = list(pkgObj)
  for pkg in pkgList:

    curDict = {
      'Name': pkg.name,
      'Full PKG name': pkg.name+'-'+pkg.evr+'.'+pkg.arch,
      'Architecture': pkg.arch,
      'Version': str(pkg.version),
      'Release': pkg.release,
      'Source URL': pkg.url,
      'From': pkg.packager,
      'From Repo': pkg.ui_from_repo,
      'Short description': pkg.summary
    }
    csvWriter.writerow(curDict)

  csvFileObj.close()


