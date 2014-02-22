#!/usr/bin/python
# -*- coding: utf-8 -*-

from leader import *

config = load_config()

#print config

from subprocess import Popen, PIPE
import time
from datetime import datetime
import boto.sns

startTime = time.time()

sns_conn = boto.sns.connect_to_region(aws_access_key_id=config.access_key,
                                      aws_secret_access_key=config.secret_key,
                                      region_name='us-east-1')

import mysql.connector
from mysql.connector import errorcode

from mako.template import Template
from mako.lookup import TemplateLookup

mylookup = TemplateLookup(directories=['.'])

assignmentsTmpl = Template(filename='tmpls/assignments.tmpl', lookup=mylookup)
assignmentPartTableTmpl = Template(filename='tmpls/assignmentPartTable.tmpl',lookup=mylookup)
assignmentAllTableTmpl = Template(filename='tmpls/assignmentAllTable.tmpl',lookup=mylookup)
assignmentAllNoneTmpl = Template(filename='tmpls/assignmentAllNone.tmpl',lookup=mylookup)
assignmentAllSummaryTmpl = Template(filename='tmpls/assignmentAllSummary.tmpl',lookup=mylookup)
assignmentAllNotEnoughTmpl = Template(filename='tmpls/assignmentAllNotEnough.tmpl',lookup=mylookup)
assignmentStartTmpl = Template(filename='tmpls/assignmentStart.tmpl',lookup=mylookup)
assignmentEndTmpl = Template(filename='tmpls/assignmentEnd.tmpl',lookup=mylookup)


cnx = None
cursor = None

try:
    cnx = mysql.connector.connect(user=config.user_name, password=config.password, host=config.host, database=config.database)
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

lookup_assignments_query = 'SELECT * FROM ' + config.database + '.`assignment` '
query_data = ()
cursor.execute(lookup_assignments_query, query_data)
assignments = cursor.fetchall()

fileName = 'index.html'
output = open(fileName, 'w')
output.write(assignmentsTmpl.render(assignmentList=assignments))
output.close()

lookup_users_query = 'SELECT * FROM ' + config.database + '.`user` '
query_data = ()
cursor.execute(lookup_users_query, query_data)
users = cursor.fetchall()

#print 'users', len(users)
#print users


#assignments = assignments[2:3]
#assignments = assignments[0:2]
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
                                     'FROM '+config.database+'.`problem` INNER JOIN (SELECT `partID` FROM '+config.database+'.`result` '\
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
    userScore = {}
    userResult = {}
    for user in users:
        userRank[user[1]] = 0
        userScore[user[1]] = 0
        userName[user[1]] = user[2]
        userResults = {}
        for part in parts:
            userResults[part[0]] = None
        userResult[user[1]] = userResults
    
    maxScore = {}
    #userRank = {}
    #userScore = {}
    #for user in users:
    #    userRank[user[1]] = 0
    #    userScore[user[1]] = 0
        
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

        lookup_results_query = \
            'SELECT `ID`, `courseraUserID`, `quality`, `proof`, `time` '\
            'FROM '+config.database+'.`result` WHERE `result`.`assignmentID`=%s AND `result`.`partID`=%s '\
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

            #print userId, userRank[userId], userResult[userId]
            try:
                userRank[userId] = userRank[userId] + i
                userResult[userId][partId] = r
                #print ('NULL',str(bid),str(userId),str(assignmentID),str(partId),str(r[2]),str(r[3]),str(r[4]),str(i),)
                rows.append(('NULL',0,str(userId),str(assignmentID),str(partId),str(r[2]),str(r[3]),str(r[4]),str(i),))  
            except:
                print 'WARNING: user id', userId, 'is missing from the userRank or userResult maps'
            val = int(r[2])
            bestVal = (max(bestVal, val) if sense == 1 else min(bestVal, val))

            # print i, " - ", r
            # print userId, " - ", userRank[userId]

        bestVals[partId] = bestVal
        #for r in rows:
            #log.write(','.join(r)+'\n')
            #logStr +=  ', '.join(r)+','+str(datetime.utcnow())+'\n'
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
        
        
        #print assignmentID
        #print partNameLong
        #print userName
        #print results 
        #print bestVal 
        #print ranks 
        #print assignmentDistPrefix
        #print len(rows)
        
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


endTime = time.time()

subject = 'Leader Board Built'
message = 'time: '+str(endTime-startTime)+'\n'
#          'bid: '+str(bid)+'\n'+\
#          'log: '+zipFileName+'\n';

print 'subject:',subject
print 'body:',message
publication = sns_conn.publish(config.topicarn, message, subject=subject)

