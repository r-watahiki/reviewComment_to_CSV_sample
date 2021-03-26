import json
import requests
import os
import pandas as pd
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()
    
def main():
    os.environ['no_proxy'] = 'localhost'
    token = os.environ['token']
    url = 'https://api.github.com/repos/r-watahiki/reviewComment_to_CSV_sample/pulls?access_token='+ token +'&state=all'
    response = requests.get(url, verify=False)
    json_dict = json.loads(response.text)
    
    pr_df = pd.DataFrame(columns=["プルリクエストID", "タイトル", "内容","プルリクエストした人","更新日時","URL"])
    cm_df = pd.DataFrame(columns=["プルリクエストID","コメントID","対象","コメント","コメントした人","更新日時","URL","親コメントID"])
    
    for i,pr in enumerate(json_dict):
       cnt=str(i+1)
       pr_response = pd.Series([cnt,pr['title'],pr['body'],pr['user']['login'],pr['updated_at'],pr['html_url']], index=pr_df.columns)
       pr_df = pr_df.append( pr_response,ignore_index=True)
        
       rv_url = 'https://api.github.com/repos/r-watahiki/reviewComment_to_CSV_sample/issues/' + cnt + '/comments'
       rv_response = requests.get(rv_url, verify=False)
       rv_dict = json.loads(rv_response.text)
               
       for review in rv_dict:
          rv_se = pd.Series([cnt,review['id'],"",review['body'],review['user']['login'],review['updated_at'],review['html_url'],""], index=cm_df.columns)
          cm_df = cm_df.append( rv_se, ignore_index=True)
          
       cm_url = 'https://api.github.com/repos/r-watahiki/reviewComment_to_CSV_sample/pulls/' + cnt + '/comments'
       cm_response = requests.get(cm_url, verify=False)
       cm_dict = json.loads(cm_response.text)
       
       for cm in cm_dict:
          cm_parentid = cm.get('in_reply_to_id',None)
              
          cm_se = pd.Series([cnt,cm['id'],cm['path'],cm['body'],cm['user']['login'],cm['updated_at'],cm['html_url'],cm_parentid], index=cm_df.columns)
          cm_df = cm_df.append( cm_se, ignore_index=True)
              
    print(pr_df)
    print(cm_df)
    pr_df.to_csv("output_pr.csv", index=False)
    cm_df.to_csv("output_cm.csv", index=False)       

if __name__ == '__main__':
    main()
