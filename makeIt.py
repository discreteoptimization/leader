#!/usr/bin/python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
import time

startTime = time.time()

access_key = 'AKIAJPIDXTUN6JJOU7KA'
secret_key = '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'

import boto.sns

sns_conn = boto.sns.connect_to_region(aws_access_key_id=access_key,
                                      aws_secret_access_key=secret_key,
                                      region_name='us-east-1')

import boto.s3.connection
from boto.s3.bucket import Bucket
from boto.s3.key import Key

conn = boto.connect_s3(aws_access_key_id=access_key,
                       aws_secret_access_key=secret_key,
                       calling_format=boto.s3.connection.OrdinaryCallingFormat())


import mysql.connector
from mysql.connector import errorcode

from mako.template import Template
from mako.lookup import TemplateLookup

mylookup = TemplateLookup(directories=['.'])

assignmentsTmpl = Template(filename='assignments.tmpl', lookup=mylookup)
assignmentPartTableTmpl = Template(filename='assignmentPartTable.tmpl',lookup=mylookup)
assignmentAllTableTmpl = Template(filename='assignmentAllTable.tmpl',lookup=mylookup)
assignmentAllNoneTmpl = Template(filename='assignmentAllNone.tmpl',lookup=mylookup)
assignmentAllSummaryTmpl = Template(filename='assignmentAllSummary.tmpl',lookup=mylookup)
assignmentAllNotEnoughTmpl = Template(filename='assignmentAllNotEnough.tmpl',lookup=mylookup)
assignmentStartTmpl = Template(filename='assignmentStart.tmpl',lookup=mylookup)
assignmentEndTmpl = Template(filename='assignmentEnd.tmpl',lookup=mylookup)

start = time.clock()

# assignmentTmpl = Template(filename='header.tmpl')
# FooterTmpl = Template(filename='footer.tmpl')

from lbsql import CourseraLeaderDB

db = CourseraLeaderDB()
db.open()

bud_results = db.maxBoardID()

# print bud_results

if bud_results == None or len(bud_results) < 1 or bud_results[0][0] == None:
    bid = 0
else:
    bid = bud_results[0][0] + 1
print 'board id:', bid

user = 'coursera'
password = 'optimization is fun'

# host='mysqldb.discreteoptimization.com'
# database='coursera_results'

host = 'dopt-results.cwf0g50wotli.us-east-1.rds.amazonaws.com'
database = 'dopt_results'

import zipfile
from datetime import datetime
lid = -1;

dopt = Bucket(conn, name='dopt-logs')

for key in dopt.list():
    name = key.name
    if name.endswith('.zip') and name.startswith('leader_'):
        num = int(name.split('.')[0].split('_')[1])
        lid = max(lid,num)

import os
for (dirpath, dnames, fnames) in os.walk('./'):
    for name in fnames:
        #print dirpath, dnames, f
        if name.endswith('.zip') and name.startswith('leader_'):
            #print f, f.split('.')[0], f.split('.')[0].split('_')[1]
            num = int(name.split('.')[0].split('_')[1])
            lid = max(lid,num)

lid += 1
logFileName = 'leader_'+str(lid).zfill(8)+'.csv'
zipFileName = 'leader_'+str(lid).zfill(8)+'.zip'
print 'log:', lid, logFileName, zipFileName


cnx = None
cursor = None

try:
    cnx = mysql.connector.connect(user=user, password=password,host=host, database=database)
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

lookup_assignments_query = 'SELECT * FROM ' + database + '.`assignment` '
query_data = ()
cursor.execute(lookup_assignments_query, query_data)
assignments = cursor.fetchall()

fileName = 'index.html'
output = open(fileName, 'w')
output.write(assignmentsTmpl.render(assignmentList=assignments))
output.close()

lookup_users_query = 'SELECT * FROM ' + database + '.`user` '
query_data = ()
cursor.execute(lookup_users_query, query_data)
users = cursor.fetchall()



logStr = ''

#assignments = assignments[2:3]
for assignment in assignments:
    assignmentID = int(assignment[0])
    assignmentName = assignment[1]
    sense = int(assignment[2])  # 1 - maximize, 0 - minimize
    print 'Working on assignment: ' + assignmentName

    sortDirection = 'ASC'
    bestValueSQLOp = 'MIN'
    if sense == 1:
        sortDirection = 'DESC'
        bestValueSQLOp = 'MAX'

    lookup_assignments_parts_query = 'SELECT `problem`.`partID`,`problem`.`partNumber`,`problem`.`problemName`,`problem`.`problemNameLong`,`problem`.`grade1`,`problem`.`grade2` '\
                                     'FROM '+database+'.`problem` INNER JOIN (SELECT `partID` FROM '+database+'.`result` '\
                                     'WHERE `result`.`assignmentID` = %s GROUP BY `result`.`partID`) AS Parts ON `problem`.`partID`=`Parts`.`partID` '\
                                     'ORDER BY `partNumber`'
    query_data = (assignmentID,)
    cursor.execute(lookup_assignments_parts_query, query_data)
    partsAll = cursor.fetchall()
    

    
    parts = []
    for part in partsAll:
        if (part[0])[-4:] == '-dev':
            print '   Removing part: ', part
            continue
        parts.append(part)

    partDistResults = {}
    bestVals = {}

    userName = {}
    userRank = {}
    userResult = {}
    for user in users:
        userRank[user[1]] = 0
        userName[user[1]] = user[2]
        userResults = {}
        for part in parts:
            userResults[part[0]] = None
        userResult[user[1]] = userResults
    
    maxScore = {}
    userRank = {}
    userScore = {}
    for user in users:
        userRank[user[1]] = 0
        userScore[user[1]] = 0
        
    for part in parts:
        namePrefix = str(assignmentID) + '_' + str(part[1])
        fileName = namePrefix + '.html'
        dataQualityFileName = namePrefix + '_quality.data'

        print '   Working on part: ' + part[2]
        partId = part[0]
        partName = part[2]
        partNameLong = part[3]
        partThreshold1 = int(part[4])
        partThreshold2 = int(part[5])
        bestVal = (-1234567890 if sense == 1 else 1234567890)
        partDistResults[partId] = None
        maxScore[partId] = 0
        # lookup_results_query = (
        # "SELECT `ID`, `userID`, `courseraUserID`, `UserName`, `assignmentID`, `problemID`, `problem`.`PartID`, `partNumber`, `problemName`, `quality`, `proof`, `mtime` FROM "+database+".`problem` INNER JOIN  "
        # "  (SELECT * FROM "+database+".`user` INNER JOIN "
        # "    (SELECT `result`.`ID`, `result`.`courseraUserID` AS `courseraUserID2`, `result`.`assignmentID`, `result`.`partID`, `result`.`quality`, `result`.`proof`, MIN(`result`.`time`) AS `mtime`"
        # "       FROM "+database+".`result`"
        # "       INNER JOIN"
        # "         (SELECT partID AS partID2, courseraUserID AS courseraUserID2, "+bestValueSQLOp+"(`result`.`quality`) AS maxq "
        # "            FROM "+database+".`result` WHERE `result`.`assignmentID`=%s AND `result`.`partID`=%s "
        # "            GROUP BY `result`.`partID`, `result`.`courseraUserID`"
        # "         ) AS qMax ON `result`.`partID`=`qMax`.`partID2` AND `result`.`courseraUserID`=`qMax`.`courseraUserID2` AND `result`.`quality`=`qMax`.`maxq` "
        # "       GROUP BY `result`.`partID`, `result`.`courseraUserID`) "
        # "    AS tbl1 ON `tbl1`.`courseraUserID2` = `user`.`courseraUserID`)"
        # "  AS tbl2 ON `tbl2`.`partID` = `problem`.`partID`"
        # "  ORDER BY `quality` "+sortDirection+", proof DESC, ID DESC"
        # )

        lookup_results_query = \
            'SELECT `ID`, `courseraUserID`, `quality`, `proof`, `time` '\
            'FROM '+database+'.`result` WHERE `result`.`assignmentID`=%s AND `result`.`partID`=%s '\
            'ORDER BY `result`.`quality` '+sortDirection+', `result`.`proof` DESC, `result`.`timestamp` DESC'

        query_data = (assignmentID, partId)

        # print lookup_results_query % query_data

        cursor.execute(lookup_results_query, query_data)
        results = cursor.fetchall()
        
        #remove non-screen name users
        index = 0
        while index < len(results):
            userId = results[index][1]
            if not userId in userName:
                results.pop(index)
            else :
                index += 1
        
        rows = []
        usersSeen = set()
        for i in range(0, len(results)):
            r = results[i]

            # print r

            userId = r[1]
            if userId in usersSeen:
                print 'WARNING: user id', userId, \
                    'appears more than once in the results list for assignment', \
                    assignmentID, 'part', partId
            usersSeen.add(userId)

            # db.addRow(bid, userId, assignmentID, partId, r[2], r[3], r[4], i)
            # rows.append([bid, userId, assignmentID, partId, r[2], r[3], r[4], i])

            try:
                userRank[userId] = userRank[userId] + i
                userResult[userId][partId] = r
                rows.append(('NULL',str(bid),str(userId),str(assignmentID),str(partId),str(r[2]),str(r[3]),str(r[4]),str(i),))
            except:
                print 'WARNING: user id', userId, 'is missing from the userRank or userResult maps'
            val = int(r[2])
            bestVal = (max(bestVal, val) if sense == 1 else min(bestVal, val))

            # print i, " - ", r
            # print userId, " - ", userRank[userId]

        bestVals[partId] = bestVal
        db.addRows(rows)
        for r in rows:
            #log.write(','.join(r)+'\n')
            logStr +=  ', '.join(r)+','+str(datetime.utcnow())+'\n'
        # fileName = str(assignmentID)+".html"
        # print(assignmentTmpl.render(name=assignmentName, results = results))
        
        assignmentDistPrefix = None
        if len(rows) >= 100: #65
            assignmentDistPrefix = namePrefix+'_dist'
            qualityStrs = [str(r[5]) for r in rows]

            output = open(dataQualityFileName, 'w')
            output.write(', '.join(qualityStrs))
            output.close()

            cmd = ['R', 'CMD', 'BATCH', '--no-save', '--no-restore', '--args '+namePrefix+' '+dataQualityFileName+' '+str(sense)+' '+partNameLong.replace(' ','_')+' '+str(partThreshold1)+' '+str(partThreshold2), 'dist.r',]
            process = Popen(cmd, stdout=PIPE)
            (stdout, stderr) = process.communicate()
            #print 'R',stdout
            #print 'R',stderr
            
            cmd = ['convert', '-density', '200', assignmentDistPrefix+'.pdf', '-resize', '800', assignmentDistPrefix+'.png']
            process = Popen(cmd, stdout=PIPE)
            (stdout, stderr) = process.communicate()
            #print 'R',stdout
            #print 'R',stderr
            
            
            partDistResults[partId] = assignmentDistPrefix
        
        #for i in range(1,len(rows)):    
        #    uId = int(rows[i][2])
        #    #score.append(bestVal/float(rows[i][5]))
        #    userScore[uId] = userScore[uId] + 1.0*bestVal/float(rows[i][5])
        #print score
        
        ranks = [0]
        rank = 0
        for i in range(1,len(rows)):
            prev = rows[i-1]
            curr = rows[i]
            if bestVal == int(float(curr[5])) and bestVal == int(float(prev[5])) and (int(prev[6]) != 0) and (int(curr[6]) == 0):
                #print prev
                #print curr
                #print bestVal, prev[5], int(float(prev[5])), curr[5], int(float(curr[5])), int(prev[6]), int(curr[6])
                rank += 1
                
            if int(float(prev[5])) > int(float(curr[5])) if sense == 1 else int(float(prev[5])) < int(float(curr[5])):
                #print prev[5], int(float(prev[5])), curr[5], int(float(curr[5]))
                rank += 1
                
            userScore[int(curr[2])] = userScore[int(curr[2])]+rank
                    
            ranks.append(rank)
            
        maxScore[partId] = rank+1
        
        output = open(fileName, 'w')
        output.write(assignmentStartTmpl.render(name=assignmentName))
        output.write(assignmentPartTableTmpl.render(assignmentID=assignmentID, partName=partNameLong, userNames=userName, results=results, bestVal=bestVal, ranks=ranks, distPrefix=assignmentDistPrefix))
        output.write(assignmentEndTmpl.render(dateAndTime=str(datetime.utcnow())))
        output.close()
        
        
        
        
    # fileter users if they have not submitted on this
    # print userRank.keys()

    for userId in userResult:

        # print userId, "-", userRank[userId]

        solved = sum(map(lambda x: userResult[userId][x] != None, userResult[userId]))
        if solved == 0:
            del userRank[userId]

    # print userRank.keys()

    bigM = len(userRank)
    # update score if they skipped a problem

    for userId in userRank:
        for partId in userResult[userId]:
            if userResult[userId][partId] == None:
                userRank[userId] = userRank[userId] + bigM
                userScore[userId] = userScore[userId] + maxScore[partId]
    
    # print userRank

    usersSorted = userRank.keys()

    # print "before sort: ", usersSorted

    #usersSorted = sorted(usersSorted, key=userRank.__getitem__)
    usersSorted = sorted(usersSorted, key=userScore.__getitem__)

    #print "after sort: ", usersSorted
    #print [userScore[i] for i in usersSorted] 

    # print parts
    # print bestVals
    # print userResult

    fileName = str(assignmentID) + '.html'
    output = open(fileName, 'w')
    output.write(assignmentStartTmpl.render(name=assignmentName))
    if len(usersSorted) > 0:
        output.write(assignmentAllTableTmpl.render(assignmentID=assignmentID, userIds=usersSorted, userNames=userName, parts=parts, results=userResult, bestVals=bestVals))
    else:
        output.write(assignmentAllNoneTmpl.render(assignmentID=assignmentID))
    output.write(assignmentEndTmpl.render(dateAndTime=str(datetime.utcnow())))
    output.close()
    
    fileName = str(assignmentID) + '_s.html'
    output = open(fileName, 'w')
    output.write(assignmentStartTmpl.render(name=assignmentName))
    #print [distResult for distResult in partDistResults.values()]
    if len(usersSorted) > 0 and sum([distResult != None for distResult in partDistResults.values()]) > 0:
        output.write(assignmentAllSummaryTmpl.render(assignmentID=assignmentID, parts=parts, partDistResults=partDistResults))
    else:
        output.write(assignmentAllNotEnoughTmpl.render(assignmentID=assignmentID))
    output.write(assignmentEndTmpl.render(dateAndTime=str(datetime.utcnow())))
    output.close()

#log.close()
zlog = zipfile.ZipFile(zipFileName, mode='w', compression=zipfile.ZIP_DEFLATED)
zlog.writestr(logFileName, logStr)
zlog.close()

endTime = time.time()

topicarn = 'arn:aws:sns:us-east-1:998334448481:leader'
subject = 'Leader Board Built'
message = 'time: '+str(endTime-startTime)+'\n'+\
          'records: '+str(logStr.count('\n'))+'\n'+\
          'bid: '+str(bid)+'\n'+\
          'log: '+zipFileName+'\n';

print 'subject:',subject
print 'body:',message
publication = sns_conn.publish(topicarn, message, subject=subject)

