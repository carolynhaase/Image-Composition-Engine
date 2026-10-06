import yaml
from pprint import pprint

# function to read config file 
def main():
    with open("conf.yml") as f:
        config = yaml.load(f, yaml.CFullloader)
    pprint(config)
    print("***********")
    for layer in config["layers"]:
        print(layer["image"])
        print(layer["filters"])
        print("---------")
        #load image
        #apply the filter
        #save log


main()