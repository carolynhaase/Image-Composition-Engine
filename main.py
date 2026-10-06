import yaml
import json
from pprint import pprint

# function to read config file and 
def main():
    with open("conf.yml") as f:
        config = yaml.load(f, yaml.CFullLoader)
    pprint(config)
    print("***********")
    for layer in config["layers"]:
        print(layer["image"])
        print(layer["filters"])
        print("---------")
        #load image
        #apply the filter
        #save log
#read the .yml file
with open("conf.yml","r") as f:
    data = yaml.safe_load(f)
#write the .json file
with open("config.json", "w") as f:
    json.dump(data, f, indent=3)