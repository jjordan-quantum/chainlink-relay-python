import requests


def call_chainlink_node(job_id, chainlink_access_key, chainlink_access_secret, chainlink_ip, body={}):

    url = chainlink_ip + '/v2/specs/' + job_id + '/runs'
    headers = {
        "content-type": "application/json",
        "X-Chainlink-EA-AccessKey": chainlink_access_key,
        "X-Chainlink-EA-Secret": chainlink_access_secret
    }
    response = requests.post(url, headers=headers, json=body)
