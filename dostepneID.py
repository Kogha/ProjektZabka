from pandas import *
import load

def dostepne_ID(DID):
  lines = load.get_database_path()
  filedata = read_csv(lines[1], encoding='cp1250')
  newDID = DID - set(filedata['ID'].values)
  return newDID

DID = set(range(1000,9999))
DID = dostepne_ID(DID)
