import json
import datetime

import requests
import time
import random
import snowflake.connector
from decimal import Decimal

END_POINT_URL = 'https://api.arctica.ai'

WAIT_A_SEC = random.randint(0, 50)


def serialize_obj(item):

    if isinstance(item, dict):
        return {str(k): serialize_obj(v) for k, v in item.items()}
    elif isinstance(item, Decimal):
        return float(item)
    elif isinstance(item, datetime.datetime):
        return item.strftime('%Y-%m-%d %H:%M:%S.%f')
    elif callable(item):
        return item.__name__
    else:
        return item


def show(token='', config={}, alert_id=None):
    accounts = config.get('accounts', [])
    alerts_result = []

    if config.get('env') == 'stage':
        END_POINT_URL = 'https://api-stage.arctica.ai'
    elif config.get('env') == 'local':
        END_POINT_URL = 'http://localhost:9000'

    payload = {}
    headers = {
        'Authorization': f'Bearer {token}'
    }

    if alert_id:
        alerts_res = requests.get(url=f"{END_POINT_URL}/digests/{alert_id}", headers=headers,
                                  data=payload)  # GET ALERTS
        res_obj = json.loads(alerts_res._content)
        alerts = {"digests": [res_obj], "status": res_obj.get("status")}
    else:
        alerts_res = requests.get(url=f"{END_POINT_URL}/digests", headers=headers, data=payload)  # GET ALERTS
        alerts = json.loads(alerts_res._content)

    return alerts


def run_locally(token='', config={}, alert_id=None):

    accounts = config.get('accounts',[])
    alerts_result=[]

    if not config.get('debug'):
        time.sleep(WAIT_A_SEC)

    if  config.get('env')=='stage':
        END_POINT_URL = 'https://api-stage.arctica.ai'
    elif  config.get('env') == 'local':
        END_POINT_URL = 'http://localhost:9000'



    payload = {}
    headers = {
        'Authorization': f'Bearer {token}'
    }


    if alert_id:
        alerts_res = requests.get(url=f"{END_POINT_URL}/digests/{alert_id}", headers=headers, data=payload)  # GET ALERTS
        res_obj = json.loads(alerts_res._content)
        alerts = {"digests":[res_obj], "status":res_obj.get("status")}
    else:
        alerts_res = requests.get(url=f"{END_POINT_URL}/digests", headers=headers, data = payload) #GET ALERTS
        alerts = json.loads(alerts_res._content)


    if alerts.get("status")!=200:
        print("CALL EMERGENCY!!!")


    for alert_obj in alerts['digests']:

        send_obj={}
        # for command in alert_obj['sqls']:
        for account in accounts:

            # Connecting to Snowflake using the default authenticator
            cnx = snowflake.connector.connect(
                account=account['host'],
                user=account['user'],
                password=account['password']
            )

            #Get Queries & Execute
            sql = alert_obj['sql']
            cur_res = cnx.cursor().execute(sql)

            #Results Wrapper
            header = [col[0] for col in cur_res._description]
            rows = [{col: serialize_obj(row[idx]) for idx,col in enumerate(header)}
                    for row in cur_res]

            # send_obj[command] = rows


        res = requests.post(f"{END_POINT_URL}/digests/{alert_id}", headers=headers,
                            data=json.dumps({"data":rows, "mail_to":config.get('mail_to')}))
        alerts_result.append(json.loads(res._content))

    return alerts_result



def execute_one(token='', config={}, alert_id=None):

    alerts_result=[]

    assert alert_id

    if not config.get('debug'):
        time.sleep(WAIT_A_SEC)

    if  config.get('env')=='stage':
        END_POINT_URL = 'https://api-stage.arctica.ai'
    elif  config.get('env') == 'local':
        END_POINT_URL = 'http://localhost:9000'



    payload = {}
    headers = {
        'Authorization': f'Bearer {token}'
    }

    res = requests.post(f"{END_POINT_URL}/digests/run/{alert_id}", headers=headers)
    alerts_result.append(json.loads(res._content))

    return alerts_result


if __name__ == '__main__':

    accounts = [{"host": "account.region", "display_name": "info", "user": "john", "password": "**"}]

    run_locally('<YOUR_API_TOKEN>', accounts, mail_to = 'ilan@snowly.io')
