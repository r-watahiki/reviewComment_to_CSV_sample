import json
import requests
import os
import pandas as pd
import requests.packages.urllib3
import re

requests.packages.urllib3.disable_warnings()
    
def main():
    os.environ['no_proxy'] = 'localhost'
    token = os.environ['token']
    repo = os.environ['repo']
    urldomain = 'https://api.github.com/repos/' + repo
    rv_df = pd.DataFrame(columns=["プルリクエストID","指摘箇所","指摘者","指摘内容","指摘観点","対応内容","更新日","URL","親コメントID"]) #レビュー記録表フォーマットに合わせた内容
       
    issuecm_url = urldomain +'/issues/comments?access_token=' + token # PRConversationで残したコメント 
    issuecm_response = requests.get(issuecm_url, verify=False)
    issuecm_dict = json.loads(issuecm_response.text)
               
    for issuecm in issuecm_dict:
        issue_url = issuecm.get('issue_url',None)
        issuecm_prid = re.search(r'\d+$',issue_url).group()
        
        issuecm_se = pd.Series([issuecm_prid,"",issuecm['user']['login'],issuecm['body'],"","",issuecm['updated_at'],issuecm['html_url'],0], index=rv_df.columns)
        rv_df = rv_df.append( issuecm_se, ignore_index=True)
          
    cm_url = urldomain + '/pulls/comments?access_token=' + token # PRのFileChangedでAddsinglecomment/Startareviewで残したコメント
    cm_response = requests.get(cm_url, verify=False)
    cm_dict = json.loads(cm_response.text)
       
    for cm in cm_dict:
        cm_parentid = cm.get('in_reply_to_id',None)
        cm_prid = cm.get('pull_request_review_id',None)
              
        cm_se = pd.Series([cm_prid,cm['path'],cm['user']['login'],cm['body'],"","",cm['updated_at'],cm['html_url'],cm_parentid], index=rv_df.columns)

        rv_df = rv_df.append( cm_se, ignore_index=True)
    
    output_df = rv_df.sort_values(by="親コメントID", ascending=True).head().drop("親コメントID", axis=1)
    print(output_df)
    output_df.to_csv("output_reviewRecord.csv", index=False)   

if __name__ == '__main__':
    main()
