#!/usr/bin/env python

import sys,os
import codecs
import subprocess
 
MAX_BYTES = 512119155
DEBUG = False

 
def printUsage():
  sys.stderr.write('Usage: %s "$REPOS" "$TXN" ' % sys.argv[0])

def getMetadata(repos, txn):
  byTx = list()
  txnDir = txn + '.txn'
  for root, dirs, files in os.walk(os.path.join(repos , 'db\\transactions', txnDir), topdown=False):
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
        for line in open(file_name, ecoding="utf-8").readlines():
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
 
def getFileSize(value):
  return int(value.split(' ')[3])

def printDebugInfo(repos, txn):
  meta = getMetadata(repos, txn)[0]
  sys.stderr.write("\n")
  for entry in meta.values():
     sys.stderr.write("\t%s = %s bytes\n" % (entry['cpath'], getFileSize(entry['text'])))
  sys.stderr.write("\n")
 
def checkTransactionSize(repos, txn):
  meta = getMetadata(repos, txn)[0]
  fail = False
  for entry in meta.values():
    size = getFileSize(entry['text'])
    if size > MAX_BYTES:
      sys.stderr.write("File %s has %d and is larger than the limit (%d)\n" % (entry['cpath'], size/1000000, MAX_BYTES/1000000)) 
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
  checkTransactionSize(repos, txn)
