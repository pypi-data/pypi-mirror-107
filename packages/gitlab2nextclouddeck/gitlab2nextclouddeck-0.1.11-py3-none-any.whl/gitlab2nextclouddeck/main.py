# -*- coding: utf-8 -*-
# filename             : gitlab2nextclouddeck_import.py
# description         : Imports Issues from gitlab to Nextcloud Deck
# author              : Ferit Cubukcuoglu
# email                : info@yazcub.com
# date                : 2021/05/20
# version              : 1.0
# usage               : $ python gitlab2nextclouddeck_import.py
# notes               :
# license             : GPL-3.0 or any later version
# python_version      : 3.8.5
# ==============================================================================

from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt
from progress.bar import ShadyBar
import os
from dotenv import load_dotenv
from os import system, name
from os.path import expanduser
from gitlab2nextclouddeck.NextCloudDeckAPI import NextCloudDeckAPI
from gitlab2nextclouddeck.GitlabAPI import GitlabAPI

home = expanduser("~") + "/"
dotenvfolder = ".gitlab2nextcloud/"

load_dotenv(dotenv_path=home + dotenvfolder + ".env", verbose=True)

nextcloud_url = ""
nextcloud_auth = ("", "")
gitlab_url = ""
gitlab_private_token = ""


def clear():
    # for windows
    if name == "nt":
        _ = system("cls")

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system("clear")


def input_creds():
    style = style_from_dict(
        {
            Token.QuestionMark: "#E91E63 bold",
            Token.Selected: "#673AB7 bold",
            Token.Instruction: "",  # default
            Token.Answer: "#2196f3 bold",
            Token.Question: "",
        }
    )

    clear()

    print("Please put the credentials")

    questions = [
        {
            "type": "input",
            "name": "nextcloud_url",
            "message": "Nextcloud Deck URL:",
        },
        {
            "type": "input",
            "name": "nextcloud_username",
            "message": "Nextcloud Deck USERNAME:",
        },
        {
            "type": "input",
            "name": "nextcloud_token",
            "message": "Nextcloud Deck TOKEN:",
        },
        {
            "type": "input",
            "name": "gitlab_url",
            "message": "Gitlab URL:",
        },
        {
            "type": "input",
            "name": "gitlab_token",
            "message": "Gitlab PRIVATE TOKEN:",
        },
    ]

    answers = prompt(questions, style=style)

    try:
        os.mkdir(home + dotenvfolder)
    except FileExistsError:
        pass

    with open(home + dotenvfolder + ".env", "w") as out:
        out.write(
            f"NEXTCLOUD_URL='{answers['nextcloud_url']}'\n"
            f"NEXTCLOUD_USERNAME='{answers['nextcloud_username']}'\n"
            f"NEXTCLOUD_TOKEN='{answers['nextcloud_token']}'\n"
            f"GITLAB_URL='{answers['gitlab_url']}'\n"
            f"GITLAB_PRIVATE_TOKEN='{answers['gitlab_token']}'\n"
        )


def check_environament():
    global nextcloud_url, nextcloud_auth, gitlab_url, gitlab_private_token
    nextcloud_url = os.getenv("NEXTCLOUD_URL")
    nextcloud_auth = (os.getenv("NEXTCLOUD_USERNAME"), os.getenv("NEXTCLOUD_TOKEN"))

    gitlab_url = os.getenv("GITLAB_URL")
    gitlab_private_token = os.getenv("GITLAB_PRIVATE_TOKEN")

    if (
        nextcloud_url is None
        or nextcloud_auth is None
        or gitlab_url is None
        or gitlab_private_token is None
    ):
        input_creds()
        load_dotenv(dotenv_path=home + dotenvfolder + ".env", verbose=True)
        nextcloud_url = os.getenv("NEXTCLOUD_URL")
        nextcloud_auth = (os.getenv("NEXTCLOUD_USERNAME"), os.getenv("NEXTCLOUD_TOKEN"))

        gitlab_url = os.getenv("GITLAB_URL")
        gitlab_private_token = os.getenv("GITLAB_PRIVATE_TOKEN")

    return True


def main():
    check_environament()

    clear()

    style = style_from_dict(
        {
            Token.QuestionMark: "#E91E63 bold",
            Token.Selected: "#673AB7 bold",
            Token.Instruction: "",  # default
            Token.Answer: "#2196f3 bold",
            Token.Question: "",
        }
    )

    glb = GitlabAPI(gitlab_url, gitlab_private_token)
    ncd = NextCloudDeckAPI(nextcloud_url, nextcloud_auth)
    print("Gitlab2Nextcloud Sync")

    questions = [
        {
            "type": "list",
            "name": "projects",
            "message": "Welches Projekt soll gesynced werden?",
            "choices": glb.getProjects(),
        },
        {
            "type": "list",
            "name": "board",
            "message": "In welches Board soll reingesyced werden?",
            "choices": ncd.getBoards(),
        },
    ]

    answers_first_sec = prompt(questions, style=style)

    board_id = answers_first_sec["board"].split("::")[1]

    questions = [
        {
            "type": "list",
            "name": "stack",
            "message": "In welches Stack soll reingesyced werden?",
            "choices": ncd.getStacks(answers_first_sec["board"].split("::")[1]),
        },
    ]

    answers_second_sec = prompt(questions, style=style)

    questions = [
        {
            "type": "confirm",
            "name": "lastentry",
            "message": "Sollen die Stack Einträge entfernt werden?",
            "default": True,
        },
    ]

    last_stack_entries = prompt(questions, style=style)

    stack_title = " " + answers_second_sec["stack"].split("::")[0]
    stack_id = answers_second_sec["stack"].split("::")[1]

    project = glb.getProject(answers_first_sec["projects"].split("::")[1])
    gitlab_issues = glb.getIssues(project)

    # Wenn User moechte das die Stack Eintraege geloescht werden
    if last_stack_entries["lastentry"]:
        ncd.deleteAllCardsStack(board_id, stack_id)

    bar = ShadyBar("Import data ", max=len(gitlab_issues))
    for git_issue in gitlab_issues:
        if "In Warteschleife" in git_issue.labels or "In Review" in git_issue.labels:
            bar.next()
            continue
        gitdesc = "" if git_issue.description is None else git_issue.description
        desc = f"""### [#{git_issue.iid}]({git_issue.web_url}) {git_issue.title}\n\n----\n\n{gitdesc}"""
        title = f"""#{git_issue.iid} {git_issue.title}"""
        new_card = ncd.createCard(
            title, "plain", 999, desc, git_issue.due_date, board_id, stack_id
        )

        filtered_label = glb.filter_labels(git_issue.labels)
        filtered_label.insert(0, stack_title)
        ncd.create_non_exists_label(filtered_label, int(board_id))
        ncd.assignAllLabels(filtered_label, new_card["id"], board_id, stack_id)

        if "__EPIC__" in filtered_label:
            linked_issues = glb.getLinkedIssues(git_issue)
            ncd.assignLinkedIssues(
                new_card["title"],
                new_card["duedate"],
                desc,
                board_id,
                stack_id,
                new_card["id"],
                linked_issues,
                desc,
            )
        bar.next()
    bar.finish()

    return


app = main()
# if __name__ == "__main__":
#     main()
