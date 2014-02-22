#!/usr/bin/python
# -*- coding: utf-8 -*-

import mysql.connector
from mysql.connector import errorcode

import sys
import os
from subprocess import Popen, PIPE

import time
startTime = time.time()


access_key = 'AKIAJPIDXTUN6JJOU7KA'
secret_key = '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'

import boto.sns

sns_conn = boto.sns.connect_to_region(aws_access_key_id=access_key,
                                      aws_secret_access_key=secret_key,
                                      region_name='us-east-1')

def getSingleData(cursor, sql):
    cursor.execute(sql, ())
    results = cursor.fetchall()
    return results[0][0]


def getVectorData(cursor, sql, index):
    cursor.execute(sql, ())
    results = cursor.fetchall()
    return [r[index] for r in results]

def getPointData(cursor, days):
    pointsEver = getVectorData(cursor,'SELECT `ptbl`.courseraUserID, SUM(`ptbl`.points) AS total FROM (SELECT `submission`.`courseraUserID`, `submission`.`partID`, MAX(`submission`.`grade`) AS points FROM `dopt_results`.`submission` WHERE DATEDIFF(NOW(),`submission`.`timestamp`) > '+str(days)+' GROUP BY `submission`.`courseraUserID`, `submission`.`partID`) AS ptbl GROUP BY `ptbl`.`courseraUserID` HAVING total > 1 ORDER BY total DESC;',1)
    return pointsEver

#WHERE .`submission`.`courseraUserID` = '++'

#user = 'coursera'
#password = 'optimization is fun'
#host = 'dopt-results.cwf0g50wotli.us-east-1.rds.amazonaws.com'
#database = 'dopt_results'

user = 'coursera'
password = 'optimization is fun'

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


#DATEDIFF(NOW(), `timestamp`) < 7

timePoints = [-1,7,14,21]

#pointsEver =getVectorData(cursor, 
#                            'SELECT `ptbl`.courseraUserID, SUM(`ptbl`.points) AS Total FROM' + 
#                                '(SELECT courseraUserID, partID, MAX(`submission`.`grade`) AS points FROM `'+database+'`.submission GROUP BY `submission`.`courseraUserID`,`submission`.`partID`)' +
#                                'AS ptbl GROUP BY `ptbl`.`courseraUserID` HAVING total > 1 ORDER BY total DESC;',1)

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


topicarn = 'arn:aws:sns:us-east-1:998334448481:leader'
subject = 'Points Plot Built'
message = 'time: '+str(endTime-startTime)+'\n';

print 'subject:',subject
print 'body:',message
publication = sns_conn.publish(topicarn, message, subject=subject)

