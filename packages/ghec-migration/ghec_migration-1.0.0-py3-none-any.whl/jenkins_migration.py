import requests
from requests.auth import HTTPBasicAuth

import jenkins
import json
from PyInquirer import style_from_dict, Token, prompt
import os


style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',
})

# from jenkinsapi.jenkins import Jenkins
#
#
# def get_jobs(jenkins_answers):
#     jenkins_url = jenkins_answers.get("jenkins_url")
#     append_api = "api/json?pretty=true"
#     json_api = f"{jenkins_url}/{append_api}"
#     username = jenkins_answers.get("jenkins_username")
#     token = jenkins_answers.get("jenkins_token")
#
#     response = requests.request("GET", json_api, auth=HTTPBasicAuth(username, token))
#
#     print(response.content)
#
#     server = Jenkins(jenkins_url, username=username, password=token)
#     for job_name, job_instance in server.get_jobs():
#         print('Job Name:%s' % job_instance.name)
#         print('Job Description:%s' % (job_instance.get_description()))

def get_jobs(jenkins_answers):
    jenkins_url = jenkins_answers.get("jenkins_url")
    username = jenkins_answers.get("jenkins_username")
    token = jenkins_answers.get("jenkins_token")
    append_api = "api/json?pretty=true"
    team_prefix = jenkins_answers.get("team_prefix")
    old_org = jenkins_answers.get("old_org")
    new_org = jenkins_answers.get("new_org")
    json_api = f"{jenkins_url}/{append_api}"
    response = requests.request("GET", json_api, auth=HTTPBasicAuth(username, token))
    apiUri = "<apiUri>https://github.nike.com/api/v3<apiUri>"
    data = json.loads(response.content.decode())

    server = jenkins.Jenkins(jenkins_url, username=username, password=token)

    jobs = server.get_jobs(folder_depth=0)

    for job in jobs:
        if job.get("_class") in ("org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject",
                                 "org.jenkinsci.plugins.workflow.job.WorkflowJob"):
            config = server.get_job_config(job.get("name"))
            config = config.replace(old_org + "/", f"{new_org}/{team_prefix}.").replace(apiUri,
                                                                                        "<apiUri>https://api.github.com<apiUri>")
            with open(job.get("name"), "w") as outfile:
                outfile.write(config)
                job_name = job.get("name")
                server.reconfig_job(job.get("name"), config_xml=config)
                os.remove(job.get("name"))
                is_okay_to_proceed = [
                    {
                        'type': 'list',
                        'name': 'is_ok',
                        'message': f"Check the job {job_name} in jenkins. Is it ok to proceed?",
                        'choices': [
                            'yes',
                            'no',
                            "don't ask me again!"
                        ]
                    }
                ]
                answers = prompt(is_okay_to_proceed, style=style)
                if answers.get("is_ok") == "no":
                    break
                else:
                    continue


