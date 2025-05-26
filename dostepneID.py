from pandas import *
import load

def dostepne_ID(DID):
  """
  Funkcja aktualizuje set wszystkich dostępnych ID.
  
  Args:
    DID (set(int)): set wszystkich dostępnych ID.

  Returns:
    newDID (set(int)): zaktualizowany set wszystkich dostępnych ID.
  """
  lines = load.get_database_path()
  filedata = read_csv(lines[1], encoding='cp1250')
  newDID = DID - set(filedata['ID'].values)
  return newDID

DID = set(range(1000,9999))
DID = dostepne_ID(DID)
