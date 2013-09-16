#!/usr/bin/python
# -*- coding: utf-8 -*-

import mysql.connector
from mysql.connector import errorcode

from mako.template import Template
from mako.lookup import TemplateLookup

mylookup = TemplateLookup(directories=['.'])

assignmentsTmpl = Template(filename='assignments.tmpl', lookup=mylookup)
assignmentPartTableTmpl = Template(filename='assignmentPartTable.tmpl',
                                   lookup=mylookup)
assignmentAllTableTmpl = Template(filename='assignmentAllTable.tmpl',
                                  lookup=mylookup)
assignmentStartTmpl = Template(filename='assignmentStart.tmpl',
                               lookup=mylookup)
assignmentEndTmpl = Template(filename='assignmentEnd.tmpl',
                             lookup=mylookup)

# assignmentTmpl = Template(filename='header.tmpl')
# FooterTmpl = Template(filename='footer.tmpl')

# user='coursera_testing'
# password='testing is fun'
# host='mysqldb.discreteoptimization.com'
# database='coursera_results'

user = 'testing'
password = 'testing is fun'
host = 'dopt-results.cwf0g50wotli.us-east-1.rds.amazonaws.com'
database = 'dopt_results'

cnx = None
cursor = None

try:
    cnx = mysql.connector.connect(user=user, password=password,
                                  host=host, database=database)

    # print(self.cnx)

    cursor = cnx.cursor()
except mysql.connector.Error, err:

    # print(self.cursor)

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print 'Something is wrong your username or password'
        print err
        exit()
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print 'Database does not exists'
        print err
        exit()
    else:
        print err
        exit()

userIdStart = 123100000
partIds = [
    '8zVuNh0L',
    'eaOs8z3l',
    'pxIsuCQe',
    'clCLq0Vb',
    '2gHetJOV',
    'ASSX0Lq4',
    'OXs89Owz',
    'AO0FA8y8',
    ]

add_result_query = 'INSERT INTO ' + database \
    + '.`result` (`ID`, `courseraUserID`, `assignmentID`, `partID`, `quality`, `proof`, `time`) VALUES (NULL, %s, %s, %s, %s, %s, %s)'

add_user_query = 'INSERT INTO ' + database \
    + '.`user` (`userID`, `courseraUserID`, `userName`) VALUES (NULL, %s, %s)'

for i in range(2000, 20001):
    userId = userIdStart + i
    user_data = (userId, 'nobody_' + str(userId))

    # Insert new employee

    cursor.execute(add_user_query, user_data)

    # user_index = cursor.lastrowid

    # cnx.commit()

    for pid in partIds:
        result_data = (
            userId,
            4,
            pid,
            92345678.901 + i,
            0,
            0.999,
            )

        # Insert new employee

        cursor.execute(add_result_query, result_data)

        # user_index = cursor.lastrowid

    cnx.commit()

