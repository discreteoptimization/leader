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

userId = 123100000
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

remove_user_query = 'DELETE FROM ' + database \
    + '.`user` WHERE courseraUserID >= ' + str(userId)

remove_result_query = 'DELETE FROM ' + database \
    + '.`result` WHERE courseraUserID >= ' + str(userId)

data = ()

# Insert new employee

cursor.execute(remove_user_query, data)

cnx.commit()

# Insert new employee

cursor.execute(remove_result_query, data)

cnx.commit()

