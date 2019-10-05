#!/usr/bin/env python
"""Pythonic library to wrap Octopus Deploy REST API."""

from docopt import docopt
import requests
from sys import exit
from http import HTTPStatus
from .endpoints import Endpoints


class ResourceNotFoundError(Exception):
    """Exception raised when resource cannot be found."""

    def __init__(self, message):
        """Initialize class."""
        self.message = message

    def __str__(self):
        """String representation."""
        return repr(self.message)


class ResourceAlreadyExistsError(Exception):
    """Exception raised when resource being created already exists."""

    def __init__(self, message):
        """Initialize class."""
        self.message = message

    def __str__(self):
        """String representation."""
        return repr(self.message)


class ResourceCreationError(Exception):
    """Exception raised when resource creation errors."""

    def __init__(self, message):
        """Initialize class."""
        self.message = message

    def __str__(self):
        """String representation."""
        return repr(self.message)


class UnexpectedResponseError(Exception):
    """Exception raised when status code from Octopus is unexpected."""

    def __init__(self, message):
        """Initialize class."""
        self.message = message

    def __str__(self):
        """String representation."""
        return repr(self.message)


class Actopus():
    """
actopus.
Run actions against Octopus Deploy server instance.

Usage: 
  actopus release <project> <release> (--server=<server> --key=<key>)
  actopus -h | --help

Options:
  -h --help          Show this screen.
  --server=<server>  Octopus server fqdn.
  --key=<key>        API key for auth.
    """

    def __init__(self, octo_host, api_key):
        """Initialize the class.
        
        octo_host(str): hostname of Octopus host.
        api_key(str):   api key for auth.
        """
        self.octo_host = octo_host
        self.api_key = api_key
        self.base_url = "https://{}/api".format(self.octo_host)
        self.endpoints = Endpoints()

    def find_projectid_byname(self, proj_name):
        """Find a Project ID by project name.
        
        proj_name(str): name of project.

        Returns project id, or None if no project found.
        """
        method = self.endpoints.projects.list.method
        endpoint = self.endpoints.projects.list.endpoint_url
        projects = self.send_request(method, endpoint)
        all_projects = projects.json()

        for project in all_projects:
            if project['Name'] == proj_name:
                return project['Id']

        return None

    def release_exists(self, proj_name, release_version):
        """Find out if a release already exists.
        
        proj_name(str):       name of project.
        release_version(str): version number of release.
        
        Throws exceptions for unexpected response from Octopus.
        Otherwise returns boolean.
        """
        proj_id = self.find_projectid_byname(proj_name)
        if not proj_id:
            raise ResourceNotFoundError('no project id found for {}'.format(
                proj_name))

        self.endpoints.proj_id = proj_id
        self.endpoints.release_version = release_version
        method=self.endpoints.releases.get.method
        endpoint = self.endpoints.releases.get.endpoint_url
        response = self.send_request(method, endpoint)

        if response.status_code == HTTPStatus.NOT_FOUND:
            return False
        elif response.status_code == HTTPStatus.OK:
            return True
        else:
            raise UnexpectedResponseError('got bad response code {}: {}'.format(
                response.status_code, response.text))

    def create_release(self, proj_name, release_version):
        """Create a release.

        proj_name(str):       name of project.
        release_version(str): version number of release.

        If the release already exists, throws exception.
        If project name is not found, throws exception.
        Otherwise, returns json response from Octopus.
        """
        if self.release_exists(proj_name, release_version):
            raise ResourceAlreadyExistsError(
                'release already exists for version {}'.format(release_version))

        proj_id = self.find_projectid_byname(proj_name)
        if not proj_id:
            raise ResourceNotFoundError('no project id found for {}'.format(
                proj_name))

        self.endpoints.proj_id = proj_id
        self.endpoints.release_version = release_version
        method = self.endpoints.releases.create.method
        endpoint = self.endpoints.releases.create.endpoint_url
        selected_packages = {"ActionName": "deploy_package",
                             "Version": release_version}
        body = self.endpoints.releases.create.body
        body['ProjectId'] = proj_id
        body['ChannelId'] = 'Channels-{}'.format(proj_id.split('-')[1])
        body['Version'] = release_version
        body['SelectedPackages'].append(selected_packages)

        response = self.send_request(method, endpoint, body)

        if response.status_code == HTTPStatus.CREATED:
            return response.json()
        else:
            raise ResourceCreationError('got error code {}: {}'.format(
                response.status_code, response.text))

    def send_request(self, method, endpoint, body=None):
        """Send a request to Octopus.

        method(str):   HTTP verb.
        endpoint(str): HTTP endpoint excluding the hostname.
        body(str):     optional - body of request.

        In case of exception, returns None.
        Otherwise, returns requests response object.
        """
        headers = {
            'Accept': "application/json",
            'X-Octopus-ApiKey': self.api_key,
            'User-Agent': "actopus",
            'Host': self.octo_host
        }
        url = '{}{}'.format(self.base_url, endpoint)

        try:
            if body:
                response = requests.request(
                    method, url, headers=headers, json=body, verify=False)
            else:
                response = requests.request(
                    method, url, headers=headers, verify=False)
        except ConnectionError:
            return None

        return response

    if __name__ == '__main__':
        arguments = docopt(__doc__)
        print(arguments)

        octo_host = arguments['--server']
        api_key = arguments['--key']

        if arguments['release']:
            proj_name = arguments['<project>']
            release_version = arguments['<release>']

        from actopus import Actopus
        ap = Actopus(octo_host, api_key)

        try:
            ret = ap.create_release(proj_name, release_version)
        except ResourceAlreadyExistsError:
            print('Release version already found for {}'.format(
                release_version))
        except ResourceNotFoundError:
            print('Could not find the project {}'.format(proj_name))
        except ResourceCreationError:
            print('There was an error creating the release')
            exit(1)

        print(ret)

