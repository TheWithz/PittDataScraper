#!/usr/bin/python3
from configparser import ConfigParser

def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    params = parser.items(section)
    for param in params:
        db[param[0]] = param[1]
    return db
