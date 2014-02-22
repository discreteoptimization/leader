from collections import namedtuple

Config = namedtuple("Configuration", ['session_id', 'host', 'database', 'user_name', 'password', 'access_key', 'secret_key', 'topicarn'])

def load_config():
    try:
        metadata_file = open('_config', 'r')
        
        session_id = metadata_file.readline().strip()
        host = metadata_file.readline().strip()
        database = metadata_file.readline().strip()
        user_name = metadata_file.readline().strip()
        password = metadata_file.readline().strip()
        access_key = metadata_file.readline().strip()
        secret_key = metadata_file.readline().strip()
        topicarn = metadata_file.readline().strip()
        
        metadata_file.close()
    except Exception, e:
        print 'problem parsing assignment metadata file'
        print 'exception message:'
        print e
        quit()
    
    return Config(session_id, host, database, user_name, password, access_key, secret_key, topicarn)


