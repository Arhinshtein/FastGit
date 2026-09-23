#!/usr/bin/env python3

import argparse
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser(description="Команды и их примеры использования")
subparser = parser.add_subparsers(dest = "command", help = "Команды для созданий репозиториев или веток", required = True)

def is_function(string : str): return callable(globals().get(string))

# new_command("create-repository", "create_rep").add_arg("-n", def, help)
class NewCommand():

    def __init__ (self, name_command, command, help = ""):
        self.name_command = name_command
        self.command = command
        self.help = help
        self.registered_command = self.creating_command
        self.registered_command.set_defaults(func=self.command)

    def add_arg(self, argument_name : str, command_name : str, command_type): # {"-n" : type}

        if not(argument_name.startswith("-") or argument_name.startswith("--")): print("В иммени аргумента может быть либо -, либо --"); return

        if command_type == "store_true":
            self.registered_command.add_argument(argument_name, dest = command_type, action = command_name)
        else:
            self.registered_command.add_argument(argument_name, type = command_name, dest = command_type, help = "help")

    @property
    def creating_command(self):
        return subparser.add_parser(self.name_command, help = self.help)


def push(string_value):
   if isinstance(string_value, argparse.Namespace):
       subprocess.run(["git", "commit", "-m", "test_func"])
       subprocess.run(["git", "push", "origin", "main"])
       print(f"ok, {string_value}, {type(string_value)}")

   else:
       subprocess.run(["git", "add", string_value])
       print("file")

def auth():
    path = Path(__file__).resolve().parent
    print(path)

def main():
    global parser
    global subparser

    #Create repository

    parser_create_rep = subparser.add_parser(
        "create-repository", help="Создание репозитория"
    )
    parser_create_rep.add_argument(
        "-n", "--name", type=str, default="project-test", help="Имя репозитория"
    )
    parser_create_rep.add_argument(
        "--public", action="store_true", help="Репозиторий будет публичным"
    )
    parser_create_rep.add_argument(
        "--private", action="store_true", help="Репозиторий будет приватным"
    )

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

    parse_push = subparser.add_parser("push", help = "Запушить проект")
    parse_push.add_argument("--commit", "-c", type=push, nargs='*', help = "Автоматический коммит перед пушем, через пробел можно перечислить файлы для коммита") #nargs='*'
    parse_push.set_defaults(func=push)

    #pu = NewCommand("push", push, "Запушить проект")
    #pu.add_arg("-c", "push", "store_true")

    argument = parser.parse_args()
    argument.func(argument)

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
