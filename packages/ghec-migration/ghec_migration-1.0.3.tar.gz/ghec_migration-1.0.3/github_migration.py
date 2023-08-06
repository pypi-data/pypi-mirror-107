import json
import traceback

import time
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import logging
import http.client
import ssl

from PyInquirer import style_from_dict, Token, prompt

logging.basicConfig(level=logging.DEBUG)

style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',
})

accept_header = "application/vnd.github.mercy-preview+json"

errors = []

s = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[404])
s.mount('https://', HTTPAdapter(max_retries=retries))


def prompt_questions(repo, proceed_with_prompt):
    if proceed_with_prompt:
        proceed = [
            {
                'type': 'list',
                'name': 'is_ok',
                'message': f"Check the  {repo} in target repo. Is it ok to proceed To next repo?",
                'choices': [
                    'yes',
                    'no',
                    "don't ask me again!"
                ]
            }
        ]

        proceed_answers_ok = prompt(questions=proceed, style=style)

        return proceed_answers_ok
    else:
        proceed_answers_ok = {}
        proceed_answers_ok["is_ok"] == "don't ask me again!"
        return proceed_answers_ok

def get_team(answers_github):
    target_team_name = answers_github.get("target_team_name")
    source_org = answers_github.get("source_github_org")
    target_org = answers_github.get("target_github_org")
    team_url = f"https://api.github.com/orgs/{target_org}/teams/{target_team_name}"
    password = answers_github.get("github_password")
    team_resp = s.get(team_url,
                      headers={"Authorization": "token " + password,
                               "Accept": accept_header})
    team_ids = []
    if team_resp.status_code == 200:
        team_id = json.loads(team_resp.content.decode()).get("id")
        team_ids.append(team_id)
        if "parent" in json.loads(team_resp.content.decode()) and json.loads(team_resp.content.decode())[
            "parent"] is not None:
            parent_id = json.loads(team_resp.content.decode())["parent"]["id"]
            team_ids.append(parent_id)

    else:
        print("Team not found")
        exit(1)

    return team_ids


def search_by_topic(topic, source_org, password, answers_github):
    results = []

    print("Searching by topic...")

    topics = topic.split(",")

    topics = topic.split(",")
    list_of_topics = [f"topic:{single_topic}" for single_topic in topics]

    separator = "+"
    search_string = separator.join(list_of_topics)


    url = f"https://api.github.com/search/repositories?q=org:{source_org} {search_string}"

    team_ids = get_team(answers_github)

    headers = {"Authorization": "token " + password,
               "Accept": "application/vnd.github.mercy-preview+json"}

    repo_response = s.get(
        url,
        headers=headers)

    repos_contents = repo_response.content.decode("utf-8")

    if repo_response.status_code == 200:
        content = json.loads(repos_contents)
        count = json.loads(repos_contents).get("total_count")

        results.extend(content.get("items"))

        while "next" in repo_response.links:
            url = repo_response.links["next"]["url"]
            repo_response = s.get(url, headers=headers)
            data = repo_response.json()
            results.extend(data.get("items"))

        print("\n Found " + str(len(results)) + " repos with topic " + topic + " in the org " + source_org)
        questions = [
            {
                'type': 'confirm',
                'name': 'listRepos',
                'message': 'List repos found?',
                'default': False
            }, ]
        answers = prompt(questions, style=style)

        if answers.get('listRepos'):
            for item in results:
                print(item.get("full_name"))

                questions = [
                    {
                        'type': 'confirm',
                        'name': 'proceedToTransfer',
                        'message': 'If the list of repos are correct, can we proceed to transfer the repos? ',
                        'default': False
                    }, ]
            proceed_answers = prompt(questions, style=style)
        else:
            proceed_answers = {"proceedToTransfer": True}

        if proceed_answers.get("proceedToTransfer"):
            proceed_with_prompt = True
            for item in content.get("items"):
                try:
                    repo = item.get("name")
                    transfer_repo(item.get("name"), answers_github, team_ids)
                    print(f"Completed transfer for " + item.get("name"))
                    proceed_answers_ok = prompt_questions(repo, proceed_with_prompt)

                    if proceed_answers_ok.get("is_ok") == "yes":
                        continue
                    elif proceed_answers_ok.get("is_ok") == "no":
                        break
                    elif proceed_answers_ok.get("is_ok") == "don't ask me again!":
                        proceed_with_prompt = False

                except Exception as ex:
                    print("Failed to transfer due to " + str(ex))
                    traceback.print_exc()

                    proceed_answers_ok = prompt_questions(repo, proceed_with_prompt)

                    if proceed_answers_ok.get("is_ok") == "yes":
                        continue
                    elif proceed_answers_ok.get("is_ok") == "no":
                        break
                    elif proceed_answers_ok.get("is_ok") == "don't ask me again!":
                        proceed_with_prompt = False
        else:
            print("Re-run the tool with correct search criteria!!")
            exit(1)
    else:
        print("No Repos found! Try running the tool again with correct topic ")


def rename_repo(repo, org, answers, headers):
    team_prefix = answers.get("prefix")
    print(f"Renaming {repo} to {team_prefix}.{repo}")
    url = f"https://api.github.com/repos/{org}/{repo}"

    data = {"name": team_prefix + "." + repo}
    rename_response = s.patch(url=url, headers=headers,
                              data=json.dumps(data))

    if rename_response.status_code == 200:
        print("Renamed successfully")
        return True

    else:
        print(f"Renaming {repo} failed due to error {str(rename_response.status_code)}")
        errors.append(repo + "| Renaming failed")
        return False


def rename_master_to_main(repo, org, answers, headers):
    print("Renaming master to main")
    team_prefix = answers.get("prefix")

    branch_url = f"https://api.github.com/repos/{org}/{team_prefix}.{repo}/branches/master/rename"
    data = {"new_name": "main"}

    rename_response = s.post(url=branch_url, headers=headers,
                             data=json.dumps(data))
    if rename_response.status_code == 201:
        print("Renamed master to main")
        return True
    else:
        print(f"Renaming to master failed for repo {repo}")
        errors.append(repo + "| Renaming master failed")
        return False


def update_webhooks(repo, org, answers, headers):
    print("Updating Web Hooks .... ")

    team_prefix = answers.get("prefix")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode=ssl.CERT_NONE
    headers["User-Agent"] = "python"
    conn = http.client.HTTPSConnection("api.github.com", context=ctx)

    url = f"/repos/{org}/{team_prefix}.{repo}/hooks"

    payload = ''
    conn.request("GET", url,payload,headers)

    hooks_response = conn.getresponse()
    data = hooks_response.read()

    print(data.decode("utf-8"))

    if hooks_response.status == 200:
        response_json = json.loads(data.decode("utf-8"))

        for config in response_json:
            hook_url = config.get("config").get("url")
            hook_id = config.get("id")
            if "bmx" in hook_url:
                new_hook_url = f"https://github-webhooks.baat-tools-prod.nikecloud.com/v1/{hook_url}"
                url = f"https://api.github.com/repos/{org}/{team_prefix}.{repo}/hooks/{hook_id}"
                data = {"config": {"url": new_hook_url}}
                response = s.patch(url, data=json.dumps(data),
                                   headers=headers)
                if response.status_code == 200:
                    print("Updated Web Hooks ")

            else:
                print("no bmx repo wehbooks found")
        return True
    else:
        print("no webhooks found")
        return True


def transfer_repo_to_targetorg(repo, answers, headers):
    source_org = answers.get("source_github_org")
    target_org = answers.get("target_github_org")
    team_prefix = answers.get("prefix")
    team_ids = get_team(answers)

    print(f"Transferring repo {repo} to {target_org}")
    url = f"https://api.github.com/repos/{source_org}/{team_prefix}.{repo}/transfer"

    data = {"new_owner": target_org, "team_ids": team_ids}
    time.sleep(0.2)
    response = s.post(url=url, headers=headers,
                      data=json.dumps(data))
    if response.status_code == 202:
        return True
    else:
        errors.append(repo + "| Failed to transfer")
        return False


def transfer_repo(repo, answers, team_ids):
    print("\nTransferring " + repo + " to target organization")
    source_org = answers.get("source_github_org")
    target_org = answers.get("target_github_org")

    headers = {"Authorization": "token " + answers.get('github_password'),
               "Accept": "application/vnd.github.mercy-preview+json"}

    # Rename Repo
    is_rename_success = rename_repo(repo, source_org, answers, headers)

    if is_rename_success:
        is_branch_rename_success = rename_master_to_main(repo, source_org, answers, headers)
        if is_branch_rename_success:
            is_update_webhook_success = update_webhooks(repo, source_org, answers, headers)
            if is_update_webhook_success:
                is_transfer_success = transfer_repo_to_targetorg(repo, answers, headers)
                if is_transfer_success:
                    print(f"Transfer completed for repo {repo}")
                else:
                    print(f"Transfer failed for repo {repo}")
            else:
                print(f"updating webhooks failed for repo {repo}")
        else:
            print(f"Renaming master failed for repo {repo}")
    else:
        print(f"Renaming failed for {repo} proceeding to other")


def migrate_github(answers, topic_answers):
    if "topic_name" in topic_answers:
        topic = topic_answers.get("topic_name")
        print("searching for repos with topic name " + topic)
        search_by_topic(
            topic, answers.get('source_github_org'), answers.get('github_password'),
            answers
        )
    else:
        filepath = topic_answers.get("filepath")
        proceed_with_prompt = True
        print("Reading repos from " + filepath)
        team_ids = get_team(answers)
        with open(filepath, 'r') as inputFile:
            for line in inputFile.readlines():
                repo_name = line.replace("\n", "")
                transfer_repo(repo_name, answers, team_ids)
                print(f"Completed transfer for {repo_name}")

                if proceed_with_prompt:
                    proceed = [
                        {
                            'type': 'list',
                            'name': 'is_ok',
                            'message': f"Check the  {repo_name} in target repo. Is it ok to proceed To next repo?",
                            'choices': [
                                'yes',
                                'no',
                                "don't ask me again!"
                            ]
                        }
                    ]

                    proceed_answers_ok = prompt(questions=proceed, style=style)

                    if proceed_answers_ok.get("is_ok") == "yes":
                        continue
                    elif proceed_answers_ok.get("is_ok") == "no":
                        break
                    elif proceed_answers_ok.get("is_ok") == "don't ask me again!":
                        proceed_with_prompt = False
