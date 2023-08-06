import os
from configparser import ConfigParser

from notedata.work import WorkApp

app = WorkApp('notecron', dir_app='/root/workspace/tmp/notecron')
app.create()


def configs(key=None):
    cp = ConfigParser()
    cp.read('conf.ini', encoding='utf-8')

    is_single = cp.get('default', 'is_single')
    redis_host = cp.get('default', 'redis_host')
    redis_pwd = cp.get('default', 'redis_pwd')
    redis_db = cp.get('default', 'redis_db')
    cron_db_url = 'sqlite:///'+app.db_file('cron.sqlite')
    #cron_db_url = 'sqlite:////root/workspace/notechats/notecron/notecron/temp/cron.sqlite'
    #cron_db_url = 'sqlite:///'+os.path.abspath(os.path.dirname(__file__))+'/cron.sqlite'
    cron_job_log_db_url = 'sqlite:///'+app.db_file('db.sqlite')
    #cron_job_log_db_url = 'sqlite:////root/workspace/notechats/notecron/notecron/temp/db.sqlite'
    #cron_job_log_db_url = 'sqlite:///'+os.path.abspath(os.path.dirname(__file__))+'/db.sqlite'

    redis_port = cp.get('default', 'redis_port')
    login_pwd = cp.get('default', 'login_pwd')
    error_notice_api_key = cp.get('default', 'error_notice_api_key')
    job_log_counts = cp.get('default', 'job_log_counts')
    api_access_token = cp.get('default', 'api_access_token')
    error_keyword = cp.get('default', "error_keyword")

    pz = {
        'is_single': is_single,
        'redis_host': redis_host,
        'redis_pwd': redis_pwd,
        'redis_db': redis_db,
        'cron_db_url': cron_db_url,
        'cron_job_log_db_url': cron_job_log_db_url,
        'redis_port': redis_port,
        'login_pwd': login_pwd,
        'error_notice_api_key': error_notice_api_key,
        'job_log_counts': job_log_counts,
        'api_access_token': api_access_token,
        'error_keyword': error_keyword
    }

    if key:
        return pz[key]
    return pz
