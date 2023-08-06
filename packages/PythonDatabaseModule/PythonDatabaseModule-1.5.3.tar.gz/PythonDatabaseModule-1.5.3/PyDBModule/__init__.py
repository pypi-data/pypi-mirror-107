import os

def Data(name,location):
    global names
    global locations
    names = name
    locations = location
    try:
        global newpath
        newpath = f'{location}\${name}' 
        if not os.path.exists(newpath):
            os.makedirs(newpath)
    except Exception as e:
        return print(f"Error-11395:{e}")
            
def CreateTableData(databaseName,databaseLocation,tableName):
    try:
        global newTablepath
        newpath = f'{databaseLocation}\${databaseName}\_{tableName}' 
        if not os.path.exists(newpath):
            os.makedirs(newpath)
    except Exception as e:
        return print(f"Error-12395:{e}")
        
def InsertDataTable(databaseName,databaseLocation,tableName,TableData):
    try:
        if os.path.exists(f"{databaseLocation}\${databaseName}\_{tableName}\{TableData}.tabledata"):
            pass
        else:
            with open(f"{databaseLocation}\${databaseName}\_{tableName}\{TableData}.tabledata", "a") as db:
                db.close()
    except Exception as e:
        return print(f"Error-13395:{e}")

def SetupDataTable(databaseName,databaseLocation,tableName,TableData):
    os.remove(f"{databaseLocation}\${databaseName}\_{tableName}\{TableData}.tabledata")
    

def WriteDataTable(databaseName,databaseLocation,tableName,TableData,msgData,msg):
    try:
        #os.remove(f"{databaseLocation}\${databaseName}\_{tableName}\{TableData}.tabledata")
        with open(f"{databaseLocation}\${databaseName}\_{tableName}\{TableData}.tabledata", "a") as db:
            
            db.write(f"{msgData} = {msg}"+ "\n")
            db.close()
    except Exception as e:
        return print(f"Error-14395:{e}")
    
def ReadDataTable(databaseName,databaseLocation,tableName,TableData):
    try:
        with open(f"{databaseLocation}\${databaseName}\_{tableName}\{TableData}.tabledata", "r") as db:
            TableDataRead = db.read()
            return TableDataRead
    except Exception as e:
        return print(f"Error-15395:{e}")

def DeleteTableData(databaseName,databaseLocation,tableName,TableData):
    try:
        path = f"{databaseLocation}\${databaseName}\_{tableName}\{TableData}.tabledata"
        os.remove(path)
    except Exception as e:
        return print(f"Error-16395:{e}")

def DeleteTable(databaseName,databaseLocation,tableName):
    try:
        path = f"{databaseLocation}\${databaseName}\_{tableName}"
        os.remove(path)
    except Exception as e:
        return print(f"Error-17395:{e}")
    
def DeleteDataBase(databaseName,databaseLocation):
    try:
        path = f"{databaseLocation}\${databaseName}"
        os.remove(path)
    except Exception as e:
        return print(f"Error-18395:{e}")


