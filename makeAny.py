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

assignmentAllPartsTmpl = Template(filename='tmpls/assignmentAllParts.tmpl',lookup=mylookup)
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


assignmentName = "Set Cover"
assignmentID = 9
partId = 'HoAkIHSK'
sortDirection = 'ASC'
bestValueSQLOp = 'MIN'
sense = 0

lookup_users_query = 'SELECT * FROM ' + config.database + '.`user` '
query_data = ()
cursor.execute(lookup_users_query, query_data)
users = cursor.fetchall()

userName = {}
userRank = {}
for user in users:
    userName[user[1]] = user[2]
    userRank[user[1]] = 0



lookup_files_query = 'SELECT DISTINCT fileName FROM ' + config.database + '.`leader_2` WHERE `leader_2`.`partID` = \'HoAkIHSK\' ORDER BY `leader_2`.`fileName`'
query_data = ()
cursor.execute(lookup_files_query, query_data)
file_names = [x[0] for x in cursor.fetchall()]

#print file_names

output_file = 'set_cover.html'
output = open(output_file, 'w')

output.write(assignmentStartTmpl.render(name=assignmentName))

output.write('<h1> '+assignmentName+' - Any Problem </h1> \n');
output.write('<p> This is an experimental extension the leader board \
              to the "set cover - any problem" assignment. This collection \
              of tables show the 10 best solutions for any problem that has \
              been submitted for evaluation.</p>  \n');



for file_name in file_names:
    print '   Working on file: ' + file_name
    #userRank = {}
    #userScore = {}
    #userResult = {}
    #for user in users:
    #    userRank[user[1]] = 0
    #    userScore[user[1]] = 0
    #    userResults = {}
    #    for part in parts:
    #        userResults[part[0]] = None
    #    userResult[user[1]] = userResults
    
    
    bestVal = (-1234567890 if sense == 1 else 1234567890)
    partDistResults = None
    maxScore = 0
    
    lookup_results_query = \
        'SELECT `ID`, `courseraUserID`, `quality`, `proof`, `time` '\
        'FROM '+config.database+'.`leader_2` WHERE `leader_2`.`assignmentID`=%s AND `leader_2`.`partID`=%s AND `leader_2`.`fileName`=%s' \
        'ORDER BY `leader_2`.`quality` '+sortDirection+', `leader_2`.`proof` DESC, `leader_2`.`timestamp` DESC'

    query_data = (assignmentID, partId, file_name)

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
            #userResult[userId][partId] = r
            #print ('NULL',str(bid),str(userId),str(assignmentID),str(partId),str(r[2]),str(r[3]),str(r[4]),str(i),)
            rows.append(('NULL',0,str(userId),str(assignmentID),str(file_name),str(r[2]),str(r[3]),str(r[4]),str(i),))  
        except:
            print 'WARNING: user id', userId, 'is missing from the userRank or userResult maps'
            
        val = int(r[2])
        bestVal = (max(bestVal, val) if sense == 1 else min(bestVal, val))

        # print i, " - ", r
        # print userId, " - ", userRank[userId]

    #bestVals[partId] = bestVal
    
    #for r in rows:
        #log.write(','.join(r)+'\n')
        #logStr +=  ', '.join(r)+','+str(datetime.utcnow())+'\n'
    # fileName = str(assignmentID)+".html"
    # print(assignmentTmpl.render(name=assignmentName, results = results))
    
    
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
        
    maxScore = rank+1
    
    #print assignmentID, file_name
    #print userName
    #print results
    #print bestVal
    #print ranks
    #print assignmentDistPrefix
    output.write(assignmentAllPartsTmpl.render(assignmentID=assignmentID, assignmentName=assignmentName, partName=file_name, userNames=userName, results=results, bestVal=bestVal, ranks=ranks))


output.write(assignmentEndTmpl.render(dateAndTime=str(datetime.utcnow())))
output.close()


endTime = time.time()

subject = 'Any Problem Leader Board Built'
message = 'time: '+str(endTime-startTime)+'\n'
#          'bid: '+str(bid)+'\n'+\
#          'log: '+zipFileName+'\n';

print 'subject:',subject
print 'body:',message
publication = sns_conn.publish(config.topicarn, message, subject=subject)