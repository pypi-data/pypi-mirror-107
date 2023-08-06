import json
import time
import requests
from PyInquirer import style_from_dict, Token, prompt

style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',
})

accept_header = "application/vnd.github.mercy-preview+json"


def get_team(answers_github):
    target_team_name = answers_github.get("target_team_name")
    team_url = f"https://api.github.com/orgs/nike-internal/teams/{target_team_name}"
    password = answers_github.get("github_password")
    team_resp = requests.get(team_url,
                             headers={"Authorization": "token " + password,
                                      "Accept": accept_header})
    team_ids = []
    if team_resp.status_code == 200:
        team_id = json.loads(team_resp.content.decode()).get("id")
        team_ids.append(team_id)
        if "parent" in json.loads(team_resp.content.decode()):
            parent_id = json.loads(team_resp.content.decode())["parent"]["id"]
            team_ids.append(parent_id)

    else:
        print("Team not found")
        exit(1)

    return team_ids


def search_by_topic(topic, source_org, password, answers_github):
    page = 1
    count = 0


    url = f"https://api.github.com/search/repositories?q=org:{source_org} topic:{topic}"

    team_ids = get_team(answers_github)

    repo_response = requests.get(
        url,
        headers={"Authorization": "token " + password,
                 "Accept": "application/vnd.github.mercy-preview+json"})

    repos_contents = repo_response.content.decode("utf-8")

    if repo_response.status_code == 200:
        content = json.loads(repos_contents)
        count = json.loads(repos_contents).get("total_count")

        print("\n Found " + str(count) + " repos with topic " + topic + " in the org " + source_org)
        questions = [
            {
                'type': 'confirm',
                'name': 'listRepos',
                'message': 'List repos found?',
                'default': False
            }, ]
        answers = prompt(questions, style=style)

        if answers.get('listRepos'):
            for item in content.get("items"):
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
            for item in content.get("items"):
                try:
                    transfer_repo(item.get("name"), answers_github, team_ids)
                    print(f"Completed transfer for " + item.get("name"))
                except Exception as ex:
                    print("Failed to transfer due to " + ex)
        else:
            print("Re-run the tool with correct search criteria!!")
            exit(1)
    else:
        print("No Repos found! Try running the tool again with correct topic ")


def transfer_repo(repo, answers, team_ids):
    print("\nTransferring " + repo + " to target organization")
    source_org = answers.get("source_github_org")
    target_org = answers.get("target_github_org")

    headers = {"Authorization": "token " + answers.get('github_password'),
               "Accept": "application/vnd.github.mercy-preview+json"}

    url = f"https://api.github.com/repos/{source_org}/{repo}/transfer"

    data = {"new_owner": target_org, "team_ids": team_ids}

    response = requests.post(url=url, headers=headers,
                             data=json.dumps(data))

    if response.status_code == 202:
        team_prefix = answers.get("prefix")
        print(f"Renaming {repo} to {team_prefix}.{repo}")
        url = f"https://api.github.com/repos/{target_org}/{repo}"

        data = {"name": team_prefix + "." + repo}
        rename_response = requests.patch(url=url, headers=headers,
                                         data=json.dumps(data))
        if rename_response.status_code == 200:
            hook_repo_url = json.loads(response.content.decode()).get("hooks_url").replace("\n", "")
            print("Updating Web Hooks .... ")
            time.sleep(1)
            hooks_response = requests.request("GET", url=hook_repo_url, headers=headers)

            if hooks_response.status_code == 200:
                response_json = json.loads(hooks_response.content.decode())

                for config in response_json:
                    hook_url = config.get("config").get("url")
                    hook_id = config.get("id")
                    if "bmx" in hook_url:
                        new_hook_url = f"https://github-webhooks.baat-tools-prod.nikecloud.com/v1/{hook_url}"
                        url = f"https://api.github.com/repos/{target_org}/{team_prefix}.{repo}/hooks/{hook_id}"
                        data = {"config": {"url": new_hook_url}}
                        response = requests.patch(url, data=json.dumps(data),
                                                  headers=headers)
                        if response.status_code == 200:
                            print("Updated Web Hooks ")
            else:
                print("no webhooks found")

        time.sleep(0.5)

        print("Renaming master to main")

        branch_url = f"https://api.github.com/repos/{target_org}/{team_prefix}.{repo}/branches/master/rename"
        data = {"new_name": "main"}

        time.sleep(0.25)
        rename_response = requests.post(url=branch_url, headers=headers,
                                         data=json.dumps(data))
        if rename_response.status_code == 201:
            print("Renamed master to main")


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

        print("Reading repos from " + filepath)
        team_ids = get_team(answers)
        with open(filepath, 'r') as inputFile:
            for line in inputFile.readlines():
                transfer_repo(line.replace("\n", ""), answers, team_ids)
