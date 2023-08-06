""" Core module with cli """
import click
import json
import os
import requests
import requests
from termcolor import cprint
from pprint import pprint
from urllib3.exceptions import InsecureRequestWarning
# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
# Set `verify=False` on `requests.post`.
# requests.post(url='https://example.com', data={'bar':'baz'}, verify=False)



@click.group()
def main():
    """
    Pypus is a cli tool for making changes to Octopus Deploy\n
    Set the following environment variables\n
    OCTOPUS_API_KEY = 'API-YOURAPIKEY'\n
    OCTOPUS_SERVER_URI = 'https://my-octopus-server.com/api'

    Example Usage: pypus get-projects Default
    """

@main.command('check-env', short_help='Check required environment variables')
def check_env():
    """ Prints out the current necessary environment variables """
    octopus_api_key = os.getenv('OCTOPUS_API_KEY')
    octopus_server_uri = os.getenv('OCTOPUS_SERVER_URI')
    print(f"Your environment has {octopus_api_key} for the variable OCTOPUS_API_KEY")
    print(f"Your environment has {octopus_server_uri} for the variable OCTOPUS_SERVER_URI")


@main.command('get-projects', short_help='Get a list of projects for space')
@click.argument("space")
def get_projects(space):
    """ Get a list of Projects for the defined URI

    Arguments:
        space: The name of the Octopus Deploy Space
    """
    octopus_api_key = os.getenv('OCTOPUS_API_KEY')
    octopus_server_uri = os.getenv('OCTOPUS_SERVER_URI')
    headers = {'X-Octopus-ApiKey': octopus_api_key}
    def get_octopus_resource(uri):
        """ Gets a resource from the API

        Arguments:
            uri: The base url of the Octopus Deploy API
        """
        response = requests.get(uri, headers=headers, verify=False)
        response.raise_for_status()
        return json.loads(response.content.decode('utf-8'))

    def get_by_name(uri, name):
        """ Gets a resource from the API by name

        Arguments:
            uri: The base url of the Octopus Deploy API
            name: The name of the resource
        """
        resources = get_octopus_resource(uri)
        return next((x for x in resources if x['Name'] == name), None)
    space_name = space
    space = get_by_name('{0}/spaces/all'.format(octopus_server_uri), space_name)
    projects = get_octopus_resource('{0}/{1}/projects/all'.format(octopus_server_uri, space['Id']))
    print(f"The space {space_name} has these Projects in it")
    for i in projects:
        print(f"Project {i['Name']} has an ID of {i['Id']}")
    return projects


@main.command('get-runbooks', short_help='Get a list of Runbooks for space')
@click.argument("space")
def get_runbooks(space):
    """ get a list of Runbooks for the defined URI """
    octopus_api_key = os.getenv('OCTOPUS_API_KEY')
    octopus_server_uri = os.getenv('OCTOPUS_SERVER_URI')
    headers = {'X-Octopus-ApiKey': octopus_api_key}
    def get_octopus_resource(uri):
        """ Gets a resource from the API

        Arguments:
            uri: The base url of the Octopus Deploy API
        """
        response = requests.get(uri, headers=headers, verify=False)
        response.raise_for_status()
        return json.loads(response.content.decode('utf-8'))

    def get_by_name(uri, name):
        """ Gets a resource from the API by name

        Arguments:
            uri: The base url of the Octopus Deploy API
            name: The name of the resource
        """
        resources = get_octopus_resource(uri)
        return next((x for x in resources if x['Name'] == name), None)
    space_name = space
    space = get_by_name('{0}/spaces/all'.format(octopus_server_uri), space_name)
    projects = get_octopus_resource('{0}/{1}/projects/all'.format(octopus_server_uri, space['Id']))
    print(f"The space {space_name} has these Projects in it")
    for i in projects:
        print("++++++++++++++++++++++++++++++++++++++")
        print(f"Project {i['Name']} has an ID of {i['Id']}")
        projname = i['Name']
        projectid = i['Id']
        projbooks = get_octopus_resource('{0}/{1}/projects/{2}/runbooks'.format(octopus_server_uri, space['Id'], projectid))
        print(f"The Project {projname} has {len(projbooks['Items'])} Runbooks")
        runbooks = projbooks['Items']
        for i in runbooks:
            print(f"Runbook {i['Name']} has an ID of {i['Id']}")
            runbookid = i['Id']


@main.command('view-runbooks-publish-status', short_help='View which Runbooks have unpublished changes')
@click.argument("space")
def view_runbooks_publish_status(space):
    """ get a list of Runbooks for the defined URI
    and display the variable/snapshot publish status

    Arguments:
        space: The name of the Octopus Deploy Space
    """
    octopus_api_key = os.getenv('OCTOPUS_API_KEY')
    octopus_server_uri = os.getenv('OCTOPUS_SERVER_URI')
    headers = {'X-Octopus-ApiKey': octopus_api_key}


    def get_octopus_resource(uri):
        """ Gets a resource from the API

        Arguments:
            uri: The base url for the Octopus Deploy API
        """
        try:
            response = requests.get(uri, headers=headers, verify=False)
            response.raise_for_status()
        except requests.HTTPError as exception:
            print(exception)
        return json.loads(response.content.decode('utf-8'))


    def post_octopus_resource(uri, body):
        """ Posts a request to API

        Arguments:
            uri: The base url of the Octopus Deploy API
            body: The body of the HTTP POST request
        """
        response = requests.post(url = uri, json = body, headers=headers, verify=False)
        return response

    def get_by_name(uri, name):
        """ Gets a resource from the API by name

        Arguments:
            uri: The base url of the Octopus Deploy API
            name: The name of the resource
        """
        resources = get_octopus_resource(uri)
        return next((x for x in resources if x['Name'] == name), None)

    def get_item_by_name(uri, name):
        """ Gets a particular resource item by name

        Arguments:
            uri: The base url of the Octopus Deploy API
            name: The name of the resource
        """
        resources = get_octopus_resource(uri)
        return next((x for x in resources['Items'] if x['Name'] == name), None)

    def get_publishing_info(octopus_server_uri, space_id, runbook_id, runbook_pid, publish_id):
        """ Get the necessary info to determine if publishing is requred

        Arguments:
            octopus_server_uri: The base url of the Octopus Deploy API
            space_id: The ID of the Octopus Deploy Space
            runbook_id: The ID of the Octopus Deploy Runbook
            runbook_pid: The Process ID of the Octopus Deploy Runbook
            publish_id: The Publish ID of the Octopus Deploy Snapshot
        """
        snaptemp = get_octopus_resource('{0}/{1}/runbookProcesses/{2}/runbookSnapshotTemplate'.format(octopus_server_uri, space_id, runbook_pid))
        id_info = get_octopus_resource('{0}/{1}/runbookSnapshots/{2}/runbookRuns/template'.format(octopus_server_uri, space_id, publish_id))
        pub_info = { 'next_name': ((snaptemp['NextNameIncrement']).split()).pop(), 'packages': len(snaptemp['Packages']),
                'lib_set_modified': id_info['IsLibraryVariableSetModified'], 'run_proc_modified': id_info['IsRunbookProcessModified']}
        return pub_info

    def needs_publish(pub_info):
        """ Returns boolean based on whether the Runbook requires publishing

        Arguments:
            pub_info: A dictionary containing the necessary information for evaluation
        """
        if ((pub_info['lib_set_modified']) or (pub_info['run_proc_modified'])) and pub_info['packages'] == 0:
            return True
        else:
            return False

    space_name = space
    space = get_by_name('{0}/spaces/all'.format(octopus_server_uri), space_name)
    projects = get_octopus_resource('{0}/{1}/projects/all'.format(octopus_server_uri, space['Id']))
    print(f"The space {space_name} has these Projects in it")
    for i in projects:
        print("++++++++++++++++++++++++++++++++++++++")
        print(f"Project {i['Name']} has an ID of {i['Id']}")
        projname = i['Name']
        projectid = i['Id']
        projbooks = get_octopus_resource('{0}/{1}/projects/{2}/runbooks'.format(octopus_server_uri, space['Id'], projectid))
        print(f"The Project {projname} has {len(projbooks['Items'])} Runbooks")
        runbooks = projbooks['Items']
        for i in runbooks:
            print(f"Runbook {i['Name']} has an ID of {i['Id']}")
            runbook_id = i['Id']
            runbook_pid = i['RunbookProcessId']
            publish_id = i['PublishedRunbookSnapshotId']
            info = get_publishing_info(octopus_server_uri, space['Id'], runbook_id, runbook_pid, publish_id)
            cprint(info, 'yellow')
            if((info['packages']) > 0):
                cprint('Packages are not supported in this revision of Pypus!!!', 'red')
                cprint('Publish this Runbook manually!!!', 'red')
            if(needs_publish(info)):
                cprint('Runbook needs publishing', 'red')
            else:
                cprint('No publishing needed', 'green')


@main.command('publish-runbooks', short_help='Publish Runbooks with unpublished variables')
@click.argument("space")
def get_runbooks(space):
    """ get a list of Runbooks for the defined URI

    Arguments:
        space: The name of the Octopus Deploy Space
    """
    print('\n' * 3)
    print("This is going to publish ALL Runbooks for ALL Projects in the Space you provided")
    print("Try the view-runbook-publish-status first to see what will be affected.")
    input("CTRL+C to abort!!!   Press any key to continue.")
    print('\n' * 3)
    octopus_api_key = os.getenv('OCTOPUS_API_KEY')
    octopus_server_uri = os.getenv('OCTOPUS_SERVER_URI')
    headers = {'X-Octopus-ApiKey': octopus_api_key}

    def get_octopus_resource(uri):
        """ Gets a resource from the API

        Arguments:
            uri: The base url for the Octopus Deploy API
        """
        try:
            response = requests.get(uri, headers=headers, verify=False)
            response.raise_for_status()
        except requests.HTTPError as exception:
            print(exception)
        return json.loads(response.content.decode('utf-8'))

    def post_octopus_resource(uri, body):
        """ Posts a request to API

        Arguments:
            uri: The base url ofr the Octopus Deploy API
            body: The body of the HTTP POST
        """
        response = requests.post(url = uri, json = body, headers=headers, verify=False)
        return response

    def get_by_name(uri, name):
        """ Gets a resource from the API by name

        Arguments:
            uri: The base url for the Octopus Deploy API
            name: The name of the resource
        """
        resources = get_octopus_resource(uri)
        return next((x for x in resources if x['Name'] == name), None)

    def get_item_by_name(uri, name):
        """ Gets a particular resource item by name

        Arguments:
            uri: The base url for the Octopus Deploy API
            name: The name of the resource
        """
        resources = get_octopus_resource(uri)
        return next((x for x in resources['Items'] if x['Name'] == name), None)

    def get_publishing_info(octopus_server_uri, space_id, runbook_id, runbook_pid, publish_id):
        """ Get the necessary info to determine if publishing is requred

        Arguments:
            octopus_server_uri: The base url of the Octopus Deploy API
            space_id: The ID of the Octopus Deploy Space
            runbook_id: The ID of the Octopus Deploy Runbook
            runbook_pid: The Process ID of the Octopus Deploy Runbook
            publish_id: The Publish ID of the Octopus Deploy Snapshot
        """
        snaptemp = get_octopus_resource('{0}/{1}/runbookProcesses/{2}/runbookSnapshotTemplate'.format(octopus_server_uri, space_id, runbook_pid))
        id_info = get_octopus_resource('{0}/{1}/runbookSnapshots/{2}/runbookRuns/template'.format(octopus_server_uri, space_id, publish_id))
        pub_info = { 'next_name': snaptemp['NextNameIncrement'], 'packages': len(snaptemp['Packages']),
                'lib_set_modified': id_info['IsLibraryVariableSetModified'], 'run_proc_modified': id_info['IsRunbookProcessModified']}
        return pub_info

    def needs_publish(pub_info):
        """ Returns boolean based on whether the Runbook requires publishing

        Arguments:
            pub_info: A dictionary containing the necessary information for evaluation
        """
        if ((pub_info['lib_set_modified']) or (pub_info['run_proc_modified'])) and pub_info['packages'] == 0:
            return True
        else:
            return False

    def create_publish_object(project_id, runbook_id, snapshot_name):
        pub_object = {"ProjectId":project_id,"RunbookId":runbook_id,"Notes":'null',"Name":snapshot_name,"SelectedPackages":[]}
        return pub_object



    space_name = space
    space = get_by_name('{0}/spaces/all'.format(octopus_server_uri), space_name)
    projects = get_octopus_resource('{0}/{1}/projects/all'.format(octopus_server_uri, space['Id']))
    print(f"The space {space_name} has these Projects in it")
    for i in projects:
        print("++++++++++++++++++++++++++++++++++++++")
        print(f"Project {i['Name']} has an ID of {i['Id']}")
        project_name = i['Name']
        project_id = i['Id']
        project_runbooks = get_octopus_resource('{0}/{1}/projects/{2}/runbooks'.format(octopus_server_uri, space['Id'], project_id))
        print(f"The Project {project_name} has {len(project_runbooks['Items'])} Runbooks")
        runbooks = project_runbooks['Items']
        for i in runbooks:
            print(f"Runbook {i['Name']} has an ID of {i['Id']}")
            runbook_id = i['Id']
            runbook_pid = i['RunbookProcessId']
            publish_id = i['PublishedRunbookSnapshotId']
            info = get_publishing_info(octopus_server_uri, space['Id'], runbook_id, runbook_pid, publish_id)
            cprint(info, 'yellow')
            if((info['packages']) > 0):
                cprint('Packages are not supported in this revision of Pypus!!!', 'red')
                cprint('Publish this Runbook manually!!!', 'red')
                sys.exit()
            if(needs_publish(info)):
                cprint('Runbook needs publishing', 'red')
                publish_object = create_publish_object(project_id, runbook_id, info['next_name'])
                print(f" This is the publish_object {publish_object}")
                publish_result = post_octopus_resource('{0}/{1}/runbookSnapshots?publish=true'.format(octopus_server_uri, space['Id']), publish_object)
                print(publish_result)
            else:
                cprint('No publishing needed', 'green')

