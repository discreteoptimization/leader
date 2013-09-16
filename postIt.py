#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
def percent_cb(complete, total): 
    sys.stdout.write('.')
    sys.stdout.flush()

import time
startTime = time.time()

sessionID = '001_dev'

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
    # host = 'objects.dreamhost.com',
    # host = 's3.amazonaws.com' default
    # is_secure=False,  # uncommmnt if you are not using ssl

uploadedHTML = 0
uploadedHTMLSize = 0
uploadedZIP = 0
uploadedZIPSize = 0

print 'All Buckets'
for bucket in conn.get_all_buckets():
    print '{name}\t{created}'.format(name=bucket.name,created=bucket.creation_date)

dopt = Bucket(conn, name='dopt')
k = Key(dopt)

#print 'Files in HTML Bucket'
#for key in dopt.list():
#    print '{name}\t{size}\t{modified}'.format(name=key.name, size=key.size, modified=key.last_modified)
#print ''

print 'Starting Upload to HTML Bucket'
import os
for (dirpath, dnames, fnames) in os.walk('./'):
    for f in fnames:
        # print dirpath, dnames, f
        if f.endswith('.html') or f.endswith('.css') or f.endswith('.ico') or f.endswith('.png') or f.endswith('.pdf'):
            fileName = os.path.join(dirpath, f)
            remoteLocation = sessionID+'/'+f
            print 'Uploading %s to Amazon S3 bucket %s at %s' % (f, dopt, remoteLocation)
            k.key = remoteLocation
            k.set_contents_from_filename(fileName, cb=percent_cb, num_cb=10)
            #print ''
            uploadedHTML += 1
            uploadedHTMLSize += os.path.getsize(fileName)


#dopt_logs = Bucket(conn, name='dopt-logs')
#k = Key(dopt_logs)

#for (dirpath, dnames, fnames) in os.walk('./'):
#    for f in fnames:
#        #print dirpath, dnames, f
#        if f.endswith('.zip') and f.startswith('leader_'):
#            fileName = os.path.join(dirpath, f)
#            remoteLocation = sessionID+'/'+f
#            print 'Uploading %s to Amazon S3 bucket %s at %s' % (f, dopt_logs, remoteLocation)
#            k.key = remoteLocation
#            k.set_contents_from_filename(fileName, cb=percent_cb, num_cb=10)
#            print ''
#            uploadedZIP += 1
#            uploadedZIPSize += os.path.getsize(fileName)
#            print 'deleting local copy:', fileName
#            os.remove(fileName)
            

endTime = time.time()

topicarn = 'arn:aws:sns:us-east-1:998334448481:leader'
subject = 'Leader Board Posted'
message = 'time: '+str(endTime-startTime)+'\n'+\
          'uploaded html: '+str(uploadedHTML)+' - '+str(uploadedHTMLSize)+'\n'+\
          'uploaded zip:  '+str(uploadedZIP)+' - '+str(uploadedZIPSize)+'\n'

print 'subject:',subject
print 'body:',message
publication = sns_conn.publish(topicarn, message, subject=subject)

