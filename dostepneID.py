from pandas import *

def dostepne_ID(DID):
  filedata = read_csv("customers.csv")
  newDID = DID - set(filedata['ID'].values)
  filedata.close()
  return newDID

DID = set(range(1000,9999))
DID = dostepne_ID(DID)
