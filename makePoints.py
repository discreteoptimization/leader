#!/usr/bin/python
# -*- coding: utf-8 -*-

import mysql.connector
from mysql.connector import errorcode

import sys
import os
from subprocess import Popen, PIPE

from leader import *
config = load_config()

import time
startTime = time.time()


import boto.sns

sns_conn = boto.sns.connect_to_region(aws_access_key_id=config.access_key,
                                      aws_secret_access_key=config.secret_key,
                                      region_name='us-east-1')

graded_assignment_ids = "(1, 2, 3, 4, 5, 8)"

def getSingleData(cursor, sql):
    cursor.execute(sql, ())
    results = cursor.fetchall()
    return results[0][0]


def getVectorData(cursor, sql, index):
    cursor.execute(sql, ())
    results = cursor.fetchall()
    return [r[index] for r in results]

def getPointData(cursor, days):
    pointsEver = getVectorData(cursor,'SELECT `ptbl`.courseraUserID, SUM(`ptbl`.points) AS total FROM (SELECT `submission`.`courseraUserID`, `submission`.`partID`, MAX(`submission`.`grade`) AS points FROM `'+config.database+'`.`submission` WHERE `submission`.`assignmentID` IN '+graded_assignment_ids+' AND DATEDIFF(NOW(),`submission`.`timestamp`) > '+str(days)+' GROUP BY `submission`.`courseraUserID`, `submission`.`partID`) AS ptbl GROUP BY `ptbl`.`courseraUserID` HAVING total > 1 ORDER BY total DESC;',1)
    return pointsEver


cnx = None
cursor = None

try:
    cnx = mysql.connector.connect(user=config.user_name, password=config.password,
                                  host=config.host, database=config.database)

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


timePoints = [-1,7,14,21]

for t in timePoints:
    pointsEver = getPointData(cursor, t)
    pointsTotal = sum(pointsEver)
    print 'Time',t,'Points Total:', pointsTotal

    fileName = 'points'+str(max(t,0))+'.data'
    output = open(fileName, 'w')
    output.write(','.join([str(d) for d in pointsEver]) + '\n')
    output.close()


namePrefix = 'none'
cmd = ['R', 'CMD', 'BATCH', '--no-save', '--no-restore', '--args '+namePrefix, 'points.r',]
process = Popen(cmd, stdout=PIPE)
(stdout, stderr) = process.communicate()
##print 'R',stdout
##print 'R',stderr

cmd = ['convert', '-density', '200', 'points.pdf', '-resize', '900', 'points.png']
process = Popen(cmd, stdout=PIPE)
(stdout, stderr) = process.communicate()
##print 'R',stdout
##print 'R',stderr

endTime = time.time()


subject = 'Points Plot Built'
message = 'time: '+str(endTime-startTime)+'\n';

print 'subject:',subject
print 'body:',message
publication = sns_conn.publish(config.topicarn, message, subject=subject)

