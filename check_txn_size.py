#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os
import codecs
import subprocess
 
MAX_BYTES = 512000000
DEBUG = False
svnlook = 'C:\\Program Files\\VisualSVN Server\\bin\\svnlook'
 
def printUsage():
  sys.stderr.write('Usage: %s "$REPOS" "$TXN" ' % sys.argv[0])

def getMetadata(repos, txn):
  byTx = list()
  for root, dirs, files in os.walk(os.path.join(repos , 'db\\transactions'), topdown=False):
    meta = dict()
    byTx.append(meta)
    for name in files:
      if not name.startswith('node') or name.endswith('children') or name.endswith('props'):
        continue
      file_name = os.path.join(root, name)
      meta[name] = dict()
      file = None
      try: 
        file = codecs.open(file_name, "r", "utf-8")
        for line in open(file_name).readlines():
          line = line.replace("\n", "").split(":")
          if len(line) > 1:
            key = line[0].strip()
            value = line[1].strip()
            value = value
            if key == 'type' and value != 'file':
               meta.pop(name)
               break
            meta[name][key] = value
      finally:
         if file:
           file.close()
  return byTx
 
def getFileSize(value, repos, txn, svnlook):
  #size = "C:\\Program Files\\VisualSVN Server\\bin\\svnlook" + "-r" + txn + "filesize" + repos + $file
  #cmd = [svnlook, 'changed', '-t', txn, repos]
  #proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
  #proc.wait()
  #changed_data = proc.stdout.readlines()
  #for line in changed_data:
       # For Python3, use print(line)
       #print(line)
  return int(value.split(' ')[3])

def commit_changes():
    cmd = ('svnlook', 'changed', repos, '-t', txn)
    out = check_output(cmd).splitlines()

    for line in out:
        yield line.split()

def filesize(path, rev=None, trans=None):
    cmd = ['svnlook', 'filesize', repos, path]
    if rev:     cmd.extend(('-r', str(rev)))
    elif trans: cmd.extend(('-t', str(trans)))

    out = check_output(cmd)
    return out.rstrip()		
 
def printDebugInfo(repos, txn):
  for root, dirs, files in os.walk(repos, topdown=False):
    sys.stderr.write(root+", filesize="+str(os.stat(root)[6])+"\n\n")
    for name in files:
      sys.stderr.write(name+", filesize="+str(os.stat(root+'/'+name)[6])+"\n")
 
def checkTransactionSize(repos, txn, svnlook):
  meta = getMetadata(repos, txn)[0]
  fail = False
  for entry in meta.values():
    size = getFileSize(entry['text'], repos, txn, svnlook)
    if size > MAX_BYTES:
      sys.stderr.write("File %s has %d MB and is larger than the limit (%d MB)\n" % (entry['cpath'], size/1000000, MAX_BYTES/1000000)) 
      fail = True
 
  if fail:
    sys.exit(1)
  
if __name__ == "__main__":
  #Check that we got a repos and transaction with this script
  if len(sys.argv) != 3:
    printUsage()
    sys.exit(2)
  else:
    repos = sys.argv[1]
    txn = sys.argv[2]
 
  if DEBUG: printDebugInfo(repos, txn)
  checkTransactionSize(repos, txn, svnlook)