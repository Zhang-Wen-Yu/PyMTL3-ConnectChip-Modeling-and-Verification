
import json
def read_config():
    """"读取配置"""
    with open("../Config/sdramconfig.json") as json_file:
        config = json.load(json_file)
    return config


def update_config(config):
    """"更新配置"""
    with open("../Config/sdramconfig.json", 'w') as json_file:
        json.dump(config, json_file, indent=4)
    return None
read_config()