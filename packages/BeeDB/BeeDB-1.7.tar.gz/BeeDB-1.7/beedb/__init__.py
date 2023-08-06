r"""BeeDB it is an easier way to make a simple database it my first package and 
i very proude of it, if you wanna contact me there are discord : PyFox#3890  SORRY FOR MY BAD GRAMMER"""


import os
import json


def set(obj:str,data,file="db.json"):
    if file in os.listdir(os.getcwd()):
        pass
    else:
        with open(os.path.join(os.getcwd(), file), 'w') as fp:
            fp.write("{}")


    #set
    with open(file,'r') as database:
        db = json.load(database)

    db[obj] = {}
    db[obj] = data

    with open(file,'w') as database:
        json.dump(db, database,indent=4)


def add(obj:str,data,file="db.json"):
    with open(file,'r') as database:
         db = json.load(database)

    obj = obj.replace('.',' ')
    obj = obj.split()

    if obj[0] in db:
        db[obj[0]][obj[1]] = data

    with open(file,'w') as database:
        json.dump(db, database,indent=4)


def push(obj:str,data,file="db.json"):
    with open(file,'r') as database:
        db = json.load(database)

    obj = obj.replace('.',' ')
    obj = obj.split()

    if obj[0] in db:
        if obj[1] not in db[obj[0]]:
            db[obj[0]][obj[1]] = [data]
        elif obj[1] in db[obj[0]]:
            db[obj[0]][obj[1]].append(data)

    with open(file,'w') as database:
        json.dump(db, database,indent=4)


def get(obj:str,file="db.json"):
    with open(file,'r') as database:
        db = json.load(database)


    obj = obj.replace('.',' ')
    obj = obj.split()

    if obj[0] in db:
        return db[obj[0]][obj[1]]


def delete(obj:str,file="db.json"):
    with open(file,'r') as database:
        db = json.load(database)


    obj = obj.replace('.',' ')
    obj = obj.split()

    if obj[0] in db:
        del db[obj[0]][obj[1]]


    with open(file,'w') as database:
        json.dump(db, database,indent=4)


def all(obj:str,file="db.json"):
    with open(file,'r') as database:
        db = json.load(database)


    return db[obj]


def dele(obj:str,file="db.json"):
    with open(file,'r') as database:
        db = json.load(database)


    del db[obj]


    with open(file,'w') as database:
        json.dump(db, database,indent=4)


def allfile(file="db.json"):
    with open(file,'r') as database:
        db = json.load(database)

    return db