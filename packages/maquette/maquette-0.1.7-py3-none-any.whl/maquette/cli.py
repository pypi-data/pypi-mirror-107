import chevron
import click
import fnmatch
import json
import os
import pandas as pd
import pipes
import shutil
import yaml

from git import Repo
from typing import Optional

import maquette
from maquette_lib.__client import Client
from maquette_lib.__user_config import EnvironmentConfiguration


config = EnvironmentConfiguration()
client = Client.from_config(config)


@click.group()
def mq():
    """
    Maquette CLI main routine.
    """
    pass


@mq.group()
def projects():
    """
    Commands for managing projects
    """
    pass


@projects.command("create")
@click.argument('name')
@click.argument('title')
@click.argument('summary')
def projects_init(name, title, summary):
    """
    Initialize a project with it's NAME, a TITLE and a SUMMARY.
    """
    maquette.project(name,title,summary).create()
    print('# Heureka! You created a project called ' + name + '(‘-’)人(ﾟ_ﾟ)\n'
            '# \n'                                                 
            '# To activate the project type: mq project activate ' + name)


@projects.command("ls")
def projects_list():
    """
    Print a list of projects.
    """
    result = client.command(cmd='projects list', headers={ 'Accept': 'text/plain' })
    print(result[1])


@projects.command("activate")
@click.argument('name')
def projects_activate(name):
    """
    Activate a previously created project by referencing its NAME
    """
    project = maquette.project(name).activate()
    config.activate_project(project_name=project.name, project_id=project.project_id)

    status, env_variables = client.command(cmd='projects environment', args={'name': name})
    print(type(env_variables))
    if status == 200:
        for (env_key, env_value) in env_variables.items():
            config.add_process_env(env_key, env_value)
        
        if os.name == 'posix':
            print('# You are on a Unix based  system, so you are not done yet c[○┬●]כ \n'
                  '# Please copy and run the command: \n'
                  'eval $(mq projects env)')
        else:
            for (env_key, env_value) in config.mq_yaml_list['environment'].items():
                os.system("SETX {0} {1}".format(env_key, env_value))
            print('# Congrats you are on a Windows machine \n'
                  '# I activated your project \t\t~~\n'
                  '# Now relax and enjoy a hot cup of coffee \t C|__|')

    else:
        raise RuntimeError('# Ups! Something went wrong (ⓧ_ⓧ)\n'
                           '# status code: ' + str(status) + ', content:\n' + response)

@projects.command("env")
def projects_env():
    """
    ATTENTION USEAGE: eval $(mq projects env)
        This command is needed on unix based systems after activating the project to updated the environment variables
    """
    envs = config.get_process_env()
    if envs:
        for (key, value) in envs:
            print('export ' + key + '=' + pipes.quote(value))
    else:
        print('# We could not find an activate project \n'
              '# Please run: mq projects activate <my_awesome_project> \n'
              '# Or create one if you do not have one yet with: mq projects create <my_awesome_project>')


@projects.command("deactivate")
def projects_deactivate():
    """
    Currently only removes the currently activate environment variables from the config, no default env needed or
    available
    """
    config.remove_process_envs()
    print('Removed Environment from Config')


@projects.command("rm")
@click.argument('name')
def projects_remove(name):
    """
    Remove a project referenced by NAME

    """
    maquette.project(name).delete()
    print("# You successfully killed the project " + name + " and removed all evidences (╯°□°)--︻╦╤─ ")

@projects.command("report-cq")
@click.argument("pytest_log")
@click.argument("files", nargs=-1)
def projects_report_cq(files):
    """
    You can report the code quality for the FILES in this project. This can be a list of individual .py files,
    packages or a mix of both.
    It is generated using pylint and send to the Maquette Hub.

    If you have generated a pytest log file with the following command, the test coverage is reported as well:
    $ mq projects report-cq [packge_names, script.py, ...]

    """
    name = config.get_project_name()
    project = maquette.project(name)
    project.report_code_quality(files)

@projects.group("sandboxes")
def projects_sandboxes():
    """
    Work with sandboxes.
    """


@projects_sandboxes.command('ls')
@click.option('--project', '-p', default=None, help='The parent project. If none is provided the currently active project will be used.')
def projects_sandboxes_list(project: str = None):
    """
    List available sandboxes of a project.
    """
    if project is None:
        project = config.get_project_name()

    result = client.command(cmd='sandboxes list', args={ 'project': project }, headers={ 'Accept': 'text/plain' })
    print(result[1])


@projects_sandboxes.command('config')
@click.argument('sandbox')
@click.option('--project', '-p', default=None, help='The parent project. If none is provided the currently active project will be used.')
def projects_sandboxes_config(sandbox: str, project: str = None):
    """
    Get the sandbox configuration.
    """
    if project is None:
        project = config.get_project_name()

    result = client.command(cmd='sandboxes get-config', args={ 'project': project, 'sandbox': sandbox })
    print(json.dumps(result[1]['data']['stacks'], indent=2))

@projects_sandboxes.command('inspect')
@click.argument('sandbox')
@click.option('--project', '-p', default=None, help='The parent project. If none is provided the currently active project will be used.')
def projects_sandboxes_inspect(sandbox: str, project: str = None):
    """
    Get the sandbox details and status.
    """
    if project is None:
        project = config.get_project_name()

    result = client.command(cmd='sandboxes get', args={ 'project': project, 'sandbox': sandbox })
    print(json.dumps(result[1]['data'], indent=2))


@mq.group()
def workspaces():
    """
    Commands for managing workspaces
    """
    pass

@workspaces.command('generators')
def workspaces_generators() -> None:
    """
    List available generators
    """
    maquette.Workspaces.apply().generators()


@workspaces.command('create')
@click.argument('generator', required=False)
@click.argument('directory', required=False)
def workspaces_create(generator: Optional[str], directory: Optional[str]) -> None:
    """
    Creates a new workspace using a specified generator.
    """
    maquette.Workspaces.apply().create(generator, directory)


@mq.group()
def code():
    """
    Commands for managing code repositorys
    """
    pass

@code.command("ls")
def code_repositorys_list():
    """
    TODO: as soon as backend supplys list of code repository templates
    """
    maquette.Workspaces.create().templates()

@code.command("cl")
@click.argument('template')
@click.argument('target')
def code_repositorys_clone(template, target):
    """
    With this command, a coede repository is cloned from the Git location with the TEMPLATE as address. It is saved
    in the TARGET folder (which is generated in this process, no worries)
    """
    Repo.clone_from(template, target)
    print("# Repository cloned from git")
    shutil.rmtree(os.path.join(target,".git"))
    if os.path.exists(os.path.join(target, "code_repository.yaml")):

        # Get all file paths
        fnames = []
        for root, d_names, f_names in os.walk(target):
            for f in f_names:
                fnames.append(os.path.join(root, f))

        # access yaml
        with open(os.path.join(target, "code_repository.yaml")) as file:
            code_repo_yaml = yaml.load(file, Loader=yaml.FullLoader)
        print("code_repository.yaml loaded")


        if "templates" in code_repo_yaml:
            print("found template attribute")
            templates = code_repo_yaml["templates"]
            if "filter" in templates:
                filter_list = templates["filter"]
            else:
                print("Nothing to filter, you get the full mustache treatment ( °┏＿┓°) ")

            # reduce fname by filter list
            for file_filter in filter_list:
                fnames = [x for x in fnames if x not in fnmatch.filter(fnames, file_filter)]

            print("---------- List of files to be mustached ----------")
            print(fnames)
            print("-----------（°〜～°）-----------")

            if "values" in templates:
                print("")
                value_dict = {}
                for value_item in templates["values"]:
                    # go trough the values list and ask the questions
                    value = click.prompt(value_item["question"], default=value_item["default"])
                    value_dict[value_item["label"]] = value

                    # go through all files per value, very inefficient, thank you for nothing chevron
                    for file in fnames:
                        with open(file) as temp_file:
                            output = chevron.render(temp_file, value_dict)
                        with open(file, "w") as out_file:
                            out_file.write(output)
                        print(file + "has been mustached (•┏∞┓•) ")
            else:
                print("nothing to mustache (￣┏Д┓￣ )")
    else:
        print("No code_repository.yaml found in " + template)


if __name__ == '__main__':
    mq()
