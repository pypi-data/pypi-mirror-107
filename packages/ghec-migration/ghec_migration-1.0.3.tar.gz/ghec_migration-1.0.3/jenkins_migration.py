import requests
from requests.auth import HTTPBasicAuth

import jenkins
import json
from PyInquirer import style_from_dict, Token, prompt
import os
import re

style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',
})


def get_jobs(jenkins_answers):
    jenkins_url = jenkins_answers.get("jenkins_url")
    username = jenkins_answers.get("jenkins_username")
    token = jenkins_answers.get("jenkins_token")

    team_prefix = jenkins_answers.get("team_prefix")
    old_org = jenkins_answers.get("old_org")
    new_org = jenkins_answers.get("new_org")


    api_uri = "<apiUri>https://github.nike.com/api/v3<apiUri>"

    server = jenkins.Jenkins(jenkins_url, username=username, password=token)

    credentialsId = jenkins_answers.get("new_credentials_id")
    jobs = server.get_jobs(folder_depth=0)
    is_prompt_user = True
    for job in jobs:
        if job.get("_class") in ("org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject",
                                 "org.jenkinsci.plugins.workflow.job.WorkflowJob"):
            config = server.get_job_config(job.get("name"))
            config = config.replace(old_org + "/", f"{new_org}/{team_prefix}.").replace(api_uri,
                                                                                        "<apiUri>https://api.github.com<apiUri>")
            config = config.replace("github.nike.com","github.com")
            for org in old_org.split(","):
                config = config.replace(org, new_org)
            if credentialsId.strip()!="":
                config = re.sub("<credentialsId>.*</credentialsId>",f"<credentialsId>{credentialsId}</credentialsId>", config)
            print(config)
            with open(job.get("name"), "w") as outfile:
                outfile.write(config)
                job_name = job.get("name")
                server.reconfig_job(job.get("name"), config_xml=config)
                os.remove(job.get("name"))
                if is_prompt_user:
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
                        if answers.get("is_ok") == "don't ask me again!":
                            is_prompt_user=False





