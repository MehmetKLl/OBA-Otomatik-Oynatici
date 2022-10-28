import requests, requests_toolbelt
import bs4
import os
import string, random
from lxml import etree
from pprint import pprint
import tools
import mimetypes
import time
import json
import datetime
import calendar

class GithubAccount:
    def __init__(self,mail,password):
        self.session = requests.Session()
        self.session.headers = {"User-Agent":"Mozilla/5.0"}
        self.session.cookies.clear()

        login_page = self.session.get("https://github.com/login")
        parser = bs4.BeautifulSoup(login_page.text,"html.parser")
        auth_token = parser.find("input",{"name":"authenticity_token"}).get("value")

        login_post = self.session.post("https://github.com/session",data={"authenticity_token":auth_token,"login":mail,"password":password})
        login_post_contents = login_post.content
        self.login_cookies = dict(self.session.cookies)

     
        if b"Incorrect username or password." in login_post.content:
            raise ValueError("Password or e-mail is incorrect.")

        self.mail = mail
        self.password = password
        self.username = self.get_username()

    def get_cookies(self):
        return {"tz":"Europe/London","tz":"Europe/London","preferred_color_mode": "dark"} | dict(self.session.cookies)

    def get_username(self):
        user_page = self.session.get("https://github.com/")
        parser = bs4.BeautifulSoup(user_page.text,"html.parser")
        return parser.find("meta",{"name":"user-login"}).get("content")

    def list_all_repos(self):
        repo_page = self.session.get("https://github.com/dashboard/my_top_repositories")
        parser = bs4.BeautifulSoup(repo_page.text,"html.parser")
        raw_elements = parser.find_all("a",{"data-hovercard-type":"repository"})
        repo_names = [i.text.replace("\n","").strip().split("/")[1] for i in parser.find_all("a",{"data-hovercard-type":"repository"}) if i.text.replace("\n","")]
        repo_links = [f'https://github.com{i.get("href")}' for i in raw_elements if i.text.replace("\n","")]
        return [{"repo-name":repo_name, "repo-link":repo_link} for repo_name, repo_link in zip(repo_names,repo_links)]

    def find_repository(self,repo_name):
        for repo in self.list_all_repos():
            if repo_name == repo["repo-name"]:
                return repo

    def select_repository(self,repo_name):
        repo = self.find_repository(repo_name)
        if not repo:
            raise ValueError("Repository couldn't found.")

        return Repository(self,repo)
        
    def close(self):
        self.session.close()

    def __del__(self):
        self.close()

    def __exit__(self):
        self.close()

class Repository:
    def __init__(self,github_account: GithubAccount, repo):
        if not isinstance(github_account, GithubAccount):
            raise ValueError(f"GithubAccount instance expected, not {type(github_account).__name__}")

        self.repo = repo
        self.account = github_account

    def list_all_branches(self):
        main_branch_page = self.account.session.get(f"{self.repo['repo-link']}/branches/all")
        parser = bs4.BeautifulSoup(main_branch_page.text,"html.parser")
        branches_list = [i.text for i in parser.find_all("a",{"class":"branch-name css-truncate-target v-align-baseline width-fit mr-2 Details-content--shown"})]

        return branches_list

    def upload_file(self,file_list: list, branch, message, description):
        branches_list = self.list_all_branches()
        if branch not in branches_list:
            raise ValueError("Branch couldn't found.")
        
        upload_page = self.account.session.get(f"{self.repo['repo-link']}/upload/{branch}")
        parser = bs4.BeautifulSoup(upload_page.text,"html.parser")
        xpath_handler = etree.HTML(upload_page.text)
        repo_id = parser.find("input",{"name":"repository_id"}).get("value")

        for file in file_list:
            file_size = str(os.stat(file)[6])
            file_type = mimetypes.guess_type(file)[0]

            
            manifest_auth_token = dict(xpath_handler.xpath("//*[@id='repo-content-pjax-container']/div/div[2]/form[@action='/upload/manifests']/input[@name='authenticity_token']")[0].items())["value"]
            manifest_file_auth_token = dict(xpath_handler.xpath("//*[@id='repo-content-pjax-container']/div/div[2]/form[@action='/upload/upload-manifest-files']/file-attachment/input[@class='js-data-upload-policy-url-csrf']")[0].items())["value"]
            commit_auth_token = dict(xpath_handler.xpath("//*[@id='repo-content-pjax-container']/div/form[@class='file-commit-form manifest-commit-form js-file-commit-form js-manifest-commit-form']/input[@name='authenticity_token']")[0].items())["value"]

            
            manifest_payload = {"authenticity_token":manifest_auth_token,
                                "directory_binary":"",
                                "repository_id":repo_id}
            manifest_body = tools.create_multipart_data(field=manifest_payload)
            manifest_headers = {"Accept":"application/json",
                                "User-Agent":"Mozilla/5.0",
                                "Content-Type":manifest_body.content_type}
            
            manifest_request = self.account.session.post("https://github.com/upload/manifests",data=manifest_body.body,cookies=self.account.get_cookies(),headers=manifest_headers)
            print(f"Upload manifest (1): {manifest_request.status_code}")
            upload_id = str(manifest_request.json()["upload_manifest"]["id"])

            manifest_file_payload = {"name":file,
                                     "size":file_size,
                                     "authenticity_token":manifest_file_auth_token,
                                     "repository_id":repo_id,
                                     "upload_manifest_id":upload_id,
                                     "content_type":file_type}
            manifest_file_body = tools.create_multipart_data(field=manifest_file_payload)
            manifest_file_headers = {"Accept":"application/json",
                                     "X-Requested-With":"XMLHttpRequest",
                                     "User-Agent":"Mozilla/5.0",
                                     "Content-Type":manifest_file_body.content_type}

            manifest_file_request = self.account.session.post("https://github.com/upload/policies/upload-manifest-files",data=manifest_file_body.body,cookies=self.account.get_cookies(),headers=manifest_file_headers)
            print(f"Upload manifest (2): {manifest_file_request.status_code}")
            upload_manifest_data = manifest_file_request.json() # Buradaki tüm json verirlerini gelecek istekte post body olarak göndermen lazım.
            

            amazon_aws_upload_manifest_payload = upload_manifest_data["form"] | {"file":(file,open(file,"rb").read(),upload_manifest_data["asset"]["content_type"])}
            amazon_aws_upload_manifest_body = tools.create_multipart_data(field=amazon_aws_upload_manifest_payload)
            amazon_aws_upload_manifest_headers ={"Accept":"*/*",
                                                 "User-Agent":"Mozilla/5.0",
                                                 "Content-Type":amazon_aws_upload_manifest_body.content_type}
            
            amazon_aws_upload_manifest_request = self.account.session.post(upload_manifest_data["upload_url"],cookies=None,data=amazon_aws_upload_manifest_body.body,headers=amazon_aws_upload_manifest_headers)
            print(f"AWS Upload: {amazon_aws_upload_manifest_request.status_code} // Duration: {amazon_aws_upload_manifest_request.elapsed.total_seconds()}")
            
            asset_manifest_upload_payload = {"authenticity_token":upload_manifest_data["asset_upload_authenticity_token"]}
            asset_manifest_upload_multipart = tools.create_multipart_data(field=asset_manifest_upload_payload)
            asset_manifest_upload_headers = {
                'accept': 'application/json',
                'content-type': asset_manifest_upload_multipart.content_type,
                'user-agent': 'Mozilla/5.0',
                'x-requested-with': 'XMLHttpRequest'}

            asset_manifest_upload_request = self.account.session.put(f"https://github.com{upload_manifest_data['asset_upload_url']}", cookies=self.account.get_cookies(),headers=asset_manifest_upload_headers, data=asset_manifest_upload_multipart.body)
            print(f"Github Manifest Upload: {asset_manifest_upload_request.status_code}")

            print(asset_manifest_upload_request.content)

            api_annotation_payload = {"stats":[{"uploadTiming":
                                                {"duration":int(amazon_aws_upload_manifest_request.elapsed.total_seconds()*1000),
                                                 "size":os.stat(file)[6],
                                                 "fileType":file_type,
                                                 "success":True
                                                 },
                                                "timestamp":calendar.timegm(datetime.datetime.utcnow().utctimetuple()),
                                                "loggedIn":True,
                                                "staff":False}
                                               ]
                                      }


            api_annotation_headers = {
                'Accept': '*/*',
                'Content-Type': 'text/plain;charset=UTF-8',            
                'Origin': 'https://github.com',
                'Referer': f"{self.repo['repo-link']}/upload/{branch}",
                'User-Agent': 'Mozilla/5.0',
            }


            response = requests.post('https://api.github.com/_private/browser/stats', cookies=self.account.get_cookies(), headers=api_annotation_headers, data=json.dumps(api_annotation_payload))
            print("???",response.content,response)



            commit_upload_file_payload = {"authenticity_token":commit_auth_token,
                                          "message":message,
                                          "description":description,
                                          "commit-choice":"direct",
                                          "target_branch":branch,
                                          "quick_pull":branch,
                                          "manifest_id":upload_manifest_data["asset"]["id"]}

            commit_upload_file_request = self.account.session.post(f"{self.repo['repo-link']}/upload",data=commit_upload_file_payload,cookies=self.account.get_cookies())

            api_annotation_2_payload = {"stats":
                                        [{"longTasks":
                                          [{"name":"unknown",
                                            "duration":int(amazon_aws_upload_manifest_request.elapsed.total_seconds()*1000),
                                            "url":f"{self.repo['repo-link']}/upload/{branch}"}],
                                          "timestamp":calendar.timegm(datetime.datetime.utcnow().utctimetuple()),
                                          "loggedIn":True,
                                          "staff":False}]}

            api_annotation_2_headers = {
                'Accept': '*/*',
                'Content-Type': 'text/plain;charset=UTF-8',            
                'Origin': 'https://github.com',
                'Referer': f"{self.repo['repo-link']}/upload/{branch}",
                'User-Agent': 'Mozilla/5.0',
            }


            response = requests.post('https://api.github.com/_private/browser/stats', cookies=self.account.get_cookies(), headers=api_annotation_2_headers, data=json.dumps(api_annotation_2_payload))
            print("??? 2",response.content,response)

            last_req_headers = {"Referer":f"{self.repo['repo-link']}/upload",
                                "User-Agent":"Mozilla/5.0"}
            last_req = self.account.session.get(self.repo['repo-link'],cookies=self.account.get_cookies(),headers=last_req_headers)

            open("result.html","wb").write(last_req.content)
            


            

            
            
            


    



account = GithubAccount("tudkhahq@gmail.com","u67Ww?!52")
repo = account.select_repository("OBA-Otomatik-Oynatici")
repo.upload_file(["deneme.py"],"main",message="",description="")
account.close()
            
