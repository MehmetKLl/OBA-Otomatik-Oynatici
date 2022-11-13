from . import login
from . import tools
import bs4
import lxml.etree
import selenium.webdriver

class Repository:
    def __init__(self, github_account, repo):
        if not isinstance(github_account, login.GitHubAccount):
            raise ValueError(f"GitHubAccount instance expected, not {type(github_account).__name__}")

        self.repo = repo
        self.account = github_account

    def list_all_branches(self):
        main_branch_page = self.account.session.get(f"{self.repo['repo-link']}/branches/all")
        parser = bs4.BeautifulSoup(main_branch_page.text,"html.parser")
        branches_list = [i.text for i in parser.find_all("a",{"class":"branch-name css-truncate-target v-align-baseline width-fit mr-2 Details-content--shown"})]

        return branches_list

    def check_branch_exists(self,branch):
        return branch in self.list_all_branches()

    def delete_file(self, file, branch, message, description):
        if not self.check_branch_exists(branch):
            raise ValueError(f"Branch \"{branch}\" couldn't found.")
        
        delete_page = self.account.session.get(f"{self.repo['repo-link']}/delete/{branch}/{file}")
        xpath_handler = lxml.etree.HTML(delete_page.text)

        guidance_task_value = dict(xpath_handler.xpath("//*[@id='new_blob']/div/div[@class='d-flex flex-column d-md-block col-md-11 offset-md-1 pr-lg-3 js-file-commit-form']/input[@name='guidance_task']")[0].items())["value"]
        commit_value = dict(xpath_handler.xpath("//*[@id='new_blob']/div/div[@class='d-flex flex-column d-md-block col-md-11 offset-md-1 pr-lg-3 js-file-commit-form']/input[@name='commit']")[0].items())["value"]
        same_repo = dict(xpath_handler.xpath("//*[@id='new_blob']/div/div[@class='d-flex flex-column d-md-block col-md-11 offset-md-1 pr-lg-3 js-file-commit-form']/input[@name='same_repo']")[0].items())["value"]
        pr_value = dict(xpath_handler.xpath("//*[@id='new_blob']/div/div[@class='d-flex flex-column d-md-block col-md-11 offset-md-1 pr-lg-3 js-file-commit-form']/input[@name='pr']")[0].items())["value"]
        commit_event_text = dict(xpath_handler.xpath("//*[@id='new_blob']/div/div[@class='d-flex flex-column d-md-block col-md-11 offset-md-1 pr-lg-3 js-file-commit-form']/div/input[@name='placeholder_message']")[0].items())["value"]
        authenticity_token = dict(xpath_handler.xpath("//*[@id='new_blob']/input[@name='authenticity_token']")[0].items())["value"]
        method_name = dict(xpath_handler.xpath("//*[@id='new_blob']/input[@name='_method']")[0].items())["value"]

        delete_post_payload = {"_method":method_name,
                               "authenticity_token":authenticity_token,
                               "message":message,
                               "placeholder_message":commit_event_text,
                               "description":description,
                               "commit-choice":"direct",
                               "target_branch":branch,
                               "quick_pull":"",
                               "guidance_task":guidance_task_value,
                               "commit":commit_value,
                               "same_repo":same_repo,
                               "pr":pr_value}
        delete_post_headers = {"User-Agent":"Mozilla/5.0",
                               "Content-Type":"application/x-www-form-urlencoded"}

        delete_post_request = self.account.session.post(f"{self.repo['repo-link']}/blob/{branch}/{file}",data=delete_post_payload,cookies=self.account.get_cookies(),headers=delete_post_headers)

    def upload_file(self, file, branch, message, description):
        if not self.check_branch_exists(branch):
            raise ValueError(f"Branch \"{branch}\" couldn't found.")
        
        handled_path = tools.arg_handler.FileArgument(file)

        browser_options = selenium.webdriver.ChromeOptions()
        browser_options.add_argument("--headless")
        browser = selenium.webdriver.Chrome(executable_path="webdriver",options=browser_options)
        browser.get("https://github.com")
        
        for e,v in self.account.get_cookies().items():
            browser.add_cookie({"name":e,"value":v})

        for files, sub_dir, abs_path in handled_path.get(method="yield"):
            
            browser.get(f"{self.repo['repo-link']}/upload/{branch}{'/'+sub_dir}")

            for file in files:
                upload_element = browser.find_element(selenium.webdriver.common.by.By.XPATH,"//*[@id='upload-manifest-files-input']")
                print(abs_path+"\\"+file)
                upload_element.send_keys(abs_path+"\\"+file)

                while True:
                    loaded_file_list = [i.text for i in browser.find_elements(selenium.webdriver.common.by.By.XPATH,"//*[@id='repo-content-pjax-container']/div/div[4]/div[@class='js-manifest-file-list-root']/div[@class='js-manifest-file-entry Box-row d-flex']/div[@class='js-filename flex-auto min-width-0 css-truncate css-truncate-target width-fit mr-3']")]
                    if len(loaded_file_list) != 0:
                        if file == loaded_file_list[-1]:
                            break

            message_element = browser.find_element(selenium.webdriver.common.by.By.XPATH,"//*[@name='message']")
            message_element.send_keys(message)

            description_element = browser.find_element(selenium.webdriver.common.by.By.XPATH, "//*[@id='commit-description-textarea']")
            description_element.send_keys(description)
            
            commit_button = browser.find_element(selenium.webdriver.common.by.By.XPATH, "//*[@id='repo-content-pjax-container']/div/form/button")
            commit_button.click()

        browser.close()

        ##        upload_page = self.account.session.get(f"{self.repo['repo-link']}/upload/{branch}")
        ##        parser = bs4.BeautifulSoup(upload_page.text,"html.parser")
        ##        xpath_handler = lxml.etree.HTML(upload_page.text)
        ##        repository_id = dict(xpath_handler.xpath("/html/head/meta[@name='octolytics-dimension-repository_id']")[0].items())["content"]
        ##
        ##        for file in file_list:
        ##            file_size = os.stat(file)[6]
        ##            file_type = mimetypes.guess_type(file)[0]
        ##            with open(file,"rb") as file_io:
        ##                file_content = file_io.read()
        ##
        ##            manifest_authenticity_token = dict(xpath_handler.xpath("//*[@id='repo-content-pjax-container']/div/div[2]/form[@action='/upload/manifests']/input[@name='authenticity_token']")[0].items())["value"]
        ##            manifest_directory_binary = dict(xpath_handler.xpath("//*[@id='repo-content-pjax-container']/div/div[2]/form[@action='/upload/manifests']/input[@name='directory_binary']")[0].items())["value"]
        ##
        ##            manifest_payload = {"authenticity_token":manifest_authenticity_token,
        ##                                "repository_id":repository_id,
        ##                                "directory_binary":manifest_directory_binary}
        ##
        ##            manifest_multipart = tools.request_tools.create_multipart_data(field=manifest_payload)
        ##
        ##            manifest_headers = {"Accept":"application/json",
        ##                                "Content-Type":manifest_multipart.content_type}
        ##
        ##            manifest_request = self.account.session.post("https://github.com/upload/manifests",data=manifest_multipart.body,cookies=self.account.get_cookies(),headers=manifest_headers)
        ##            manifest_request_return_dict = manifest_request.json()
        ##
        ##
        ##            upload_manifest_files_authenticity_token = dict(xpath_handler.xpath("//*[@id='repo-content-pjax-container']/div/div[2]/form[@action='/upload/upload-manifest-files']/file-attachment/input[@class='js-data-upload-policy-url-csrf']")[0].items())["value"]
        ##            upload_manifest_files_id = str(manifest_request.json()["upload_manifest"]["id"])
        ##
        ##            upload_manifest_files_payload = {"name":file,
        ##                                             "size":str(file_size),
        ##                                             "authenticity_token":upload_manifest_files_authenticity_token,
        ##                                             "repository_id":repository_id,
        ##                                             "upload_manifest_id":str(upload_manifest_files_id),
        ##                                             "content_type":file_type}
        ##            
        ##            upload_manifest_files_multipart = tools.create_multipart_data(field=upload_manifest_files_payload)
        ##            
        ##            upload_manifest_files_headers = {"Accept":"application/json",
        ##                                             "X-Requested-With":"XMLHttpRequest",
        ##                                             "Content-Type":upload_manifest_files_multipart.content_type}
        ##
        ##            upload_manifest_files_request = self.account.session.post("https://github.com/upload/policies/upload-manifest-files",data=upload_manifest_files_multipart.body,cookies=self.account.get_cookies(),headers=upload_manifest_files_headers)
        ##            upload_manifest_files_return_dict = upload_manifest_files_request.json()
        ##
        ##            aws_service_upload_url = upload_manifest_files_return_dict["upload_url"]
        ##
        ##            aws_service_upload_payload = upload_manifest_files_return_dict["form"] | {"file":(file,file_content,file_type)}
        ##
        ##            aws_service_upload_multipart = tools.request_tools.create_multipart_data(field=aws_service_upload_payload)
        ##
        ##            aws_service_upload_headers = {"Accept":"*/*",
        ##                                          "Content-Type":aws_service_upload_multipart.content_type}
        ##
        ##            aws_service_upload_request = self.account.session.post(aws_service_upload_url,data=aws_service_upload_multipart.body,cookies=None,headers=aws_service_upload_headers)
        ##            print(aws_service_upload_request)
        ##
        ##            upload_manifest_files_put_url = upload_manifest_files_return_dict["asset_upload_url"]
        ##            
        ##            upload_manifest_files_put_authenticity_token = upload_manifest_files_return_dict["asset_upload_authenticity_token"]
        ##
        ##            upload_manifest_files_put_payload = {"authenticity_token":upload_manifest_files_put_authenticity_token}
        ##
        ##            upload_manifest_files_put_multipart = tools.request_tools.create_multipart_data(field=upload_manifest_files_put_payload)
        ##
        ##            upload_manifest_files_put_headers = {"Accept":"application/json",
        ##                                                 "Content-Type":upload_manifest_files_put_multipart.content_type}
        ##
        ##            upload_manifest_files_put_request = self.account.session.put("https://github.com"+upload_manifest_files_put_url,data=upload_manifest_files_put_multipart.body,cookies=self.account.get_cookies(),headers=upload_manifest_files_put_headers)
        ##            print(upload_manifest_files_put_request)
        ##
        ##            api_stats_payload = {"stats":[{"uploadTiming":{"duration":tools.request_tools.get_request_ms(aws_service_upload_request),
        ##                                                           "size":file_size,
        ##                                                           "fileType":file_type,
        ##                                                           "success":True},
        ##                                           "timestamp":tools.request_tools.get_timestamp(),
        ##                                           "loggedIn":True,
        ##                                           "staff":False}]}
        ##
        ##            api_stats_body = json.dumps(api_stats_payload)
        ##
        ##            api_stats_headers = {"Accept":"*/*",
        ##                                 "Content-Type":"text/plain"}
        ##
        ##            api_stats_request = self.account.session.post("https://api.github.com/_private/browser/stats",data=api_stats_body,cookies=self.account.get_cookies(),headers=api_stats_headers)
        ##            print(api_stats_request)
        ##
        ##            commit_upload_authenticity_token = dict(xpath_handler.xpath(f"//*[@id='repo-content-pjax-container']/div/form[@action='/{self.account.username}/{self.repo['repo-name']}/upload']/input[@name='authenticity_token']")[0].items())["value"]
        ##            commit_upload_manifest_id = upload_manifest_files_return_dict["asset"]["id"]
        ##            commit_upload_target_branch = dict(xpath_handler.xpath(f"//*[@id='repo-content-pjax-container']/div/form[@action='/{self.account.username}/{self.repo['repo-name']}/upload']/div/input[@name='target_branch']")[0].items())["value"]
        ##            commit_upload_quick_pull = dict(xpath_handler.xpath(f"//*[@id='repo-content-pjax-container']/div/form[@action='/{self.account.username}/{self.repo['repo-name']}/upload']/div/input[@name='quick_pull']")[0].items())["value"]
        ##
        ##
        ##            commit_upload_payload = {"authenticity_token":commit_upload_authenticity_token,
        ##                                     "message":message,
        ##                                     "description":description,
        ##                                     "commit-choice":"direct",
        ##                                     "target_branch":branch,
        ##                                     "quick_pull":commit_upload_quick_pull,
        ##                                     "manifest_id":str(commit_upload_manifest_id)}
        ##
        ##            commit_upload_headers = {"Content-Type":"application/x-www-form-urlencoded"}
        ##
        ##            commit_upload_request = requests.Request("POST",f"{self.repo['repo-link']}/upload",data=commit_upload_payload,cookies=self.account.get_cookies(),headers=commit_upload_payload)
        ##            print(commit_upload_request.prepare().headers)
        ##
        ##            #commit_upload_request = self.account.session.post(f"{self.repo['repo-link']}/upload",data=commit_upload_payload,cookies=self.account.get_cookies(),headers=commit_upload_headers,allow_redirects=True)
        ##            #commit_upload_request.html.render()
        ##            #open("result.html","wb").write(commit_upload_request.content)
        ##
        ##            #a = self.account.session.get("https://github.com/Alihakan001/deneme")
        ##            #a.html.render()

                

            
            

