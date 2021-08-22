import requests


def call_chainlink_node(job_id, chainlink_access_key, chainlink_access_secret, chainlink_ip, data=None):

    url = chainlink_ip + '/v2/specs/' + job_id + '/runs'
    headers = {
        "content-type": "application/json",
        "X-Chainlink-EA-AccessKey": chainlink_access_key,
        "X-Chainlink-EA-Secret": chainlink_access_secret
    }
    if data:
        return requests.post(url, headers=headers, data=data)
    else:
        return requests.post(url, headers=headers)
