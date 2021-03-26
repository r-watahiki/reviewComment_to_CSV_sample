import json
import requests
import os
import pandas as pd
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()


    
def main():
    os.environ['no_proxy'] = 'localhost'
    token = os.environ['token']
    repo = os.environ['repo']
    url = 'https://api.github.com/repos/' + repo + '/pulls?&state=all'
    print(url)
    response = requests.get(url, verify=False)
    json_dict = json.loads(response.text)
    

if __name__ == '__main__':
    main()
