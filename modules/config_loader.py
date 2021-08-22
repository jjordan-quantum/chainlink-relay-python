import json


def get_env(config_file):

    with open(config_file) as read_file:
        config = json.load(read_file)

    return (
        config["CHAINLINK_ACCESS_KEY"],
        config["CHAINLINK_ACCESS_SECRET"],
        config["CHAINLINK_IP"]
    )