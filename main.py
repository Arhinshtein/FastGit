#!/usr/bin/env python3

import argparse
import subprocess
from pathlib import Path


def auth():
    path = Path(__file__).resolve().parent
    print(path)

def main():

    parser = argparse.ArgumentParser(description="Команды и их примеры использования")

    subparser = parser.add_subparsers(dest = "command", help = "Команды для созданий репозиториев или веток", required = True)

    #Create repository

    parser_create_rep = subparser.add_parser("create-repository", help = "Создание репозиторий")
    parser_create_rep.add_argument("-n", "--name", type=str, default = "project-test", help = "Имя репозитория")
    parser_create_rep.add_argument("--public", action = "store_true", help = "Репозиторий будет публичным")
    parser_create_rep.add_argument("--private", action = "store_true", help = "Репозиторий будет приватным")

    #Delete repository
    parser_delete_rep = subparser.add_parser("delete-repository", help = "Удаление репозитория")
    parser_delete_rep.add_argument("-n", "--name", type=str, default = "project-test", help = "Имя репозитория")


    #Create branch

    parse_create_branch = subparser.add_parser("create-branch", help = "Создание ветки")
    parse_create_branch.add_argument("--name", "-n", type=str, default="main", help = "Имя ветки")

    #Commit

    parse_commit = subparser.add_parser("commit", help = "Закоммитить проект")
    parse_commit.add_argument("--name", "-n", type=str, default="New Commit", help = "Имя коммита")
    parse_commit.add_argument("--file", "-f", nargs="+", help = "Указать определённый список файлов для коммита")

    argument = parser.parse_args()

    match argument.command:
        case "create-repository":
            if argument.public + argument.private > 1 or argument.public + argument.private == 0: print("Нельзя использовать private и public одновременно или не использовать вовсе"); return -1

            #print(f"c-r {argument.name}, {argument.public}, {argument.private}")

            if argument.public: subprocess.run(["gh", "repo", "create", argument.name, "--public"])
            elif argument.private: subprocess.run(["gh", "repo", "create", argument.name, "--private"])

        case "delete-repository":
            subprocess.run(["gh", "repo", "delete", argument.name, "--yes"])

        case "create-branch":
            pass
            #print(f"c-b {argument.name}")

        case "commit":
            if argument.file:
                print(argument.file)
                subprocess.run(["git", "add"] + argument.file)

            subprocess.run(["git", "commit", "-m", argument.name])

if __name__ == '__main__':
    auth()
    main()
