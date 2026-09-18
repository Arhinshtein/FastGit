#!/usr/bin/env python3

import argparse
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser(description="Команды и их примеры использования")
subparser = parser.add_subparsers(dest = "command", help = "Команды для созданий репозиториев или веток", required = True)

def is_function(string : str): return callable(globals().get(string))

# new_command("create-repository", "create_rep").add_arg("-")
class new_command():

    global parser
    global subparser

    def __init__ (self, name_command, command, help = ""):
        self.name_command = name_command
        self.command = command
        self.help = help
        self.registered_command = self.creating_command()

    def add_arg(self, **dictonary_arg_param): # {"-n" : type}

        for key, command in dictonary_arg_param.items():
            if key.count("-") < 1 or key.count('-') > 2: print("В иммени аргумента может быть либо -, либо --"); continue

            if command == "store_true": self.registered_command.add_argument(key, actions = command)
            else: self.registered_command.add_argument(key, type = command)


    def creating_command(self):
        return subparser.add_parser(self.name_command, help = self.help)



def push(): subprocess.run(["git", "push", "origin", "main"])

def auth():
    path = Path(__file__).resolve().parent
    print(path)

def main():
    global parser
    global subparser

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

    #Push

    #parse_push = subparser.add_parser("push", help = "Запушить проект")
    #parse_push.add_argument("--commit", "-c", nargs='*', help = "Автоматический коммит перед пушем, через пробел можно перечислить файлы для коммита")

    new_command("push", push)

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


        #case "push":
        #    if isinstance(argument.commit, list):
        #        if len(argument.commit) == 0:
        #            subprocess.run(["git", "commit", "-m", argument.name])
        #        else:
        #            subprocess.run(["git", "add"] + argument.commit)
        #
        #    subprocess.run(["git", "push", "origin", "main"])

if __name__ == '__main__':
    auth()
    main()
