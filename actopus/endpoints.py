"""Modeling Octopus endpoints."""

from collections import namedtuple

class Endpoints():
    """Octopus endpoints."""

    def __init__(self, space_id=None, proj_id=None, release_version=None):
        """Initialize the class."""
        self.space_id = space_id
        self.proj_id = proj_id
        self.release_version = release_version
        self.Releases = namedtuple('Releases', ['list', 'get', 'create'])
        self.Projects = namedtuple('Projects', ['list'])
        self.Endpoints = namedtuple('Endpoints', ['desc',
                                                  'endpoint_url',
                                                  'body',
                                                  'method'])

    @property
    def projects(self):
        """Return projects endpoint data.
        
        Returns namedtuple.
        """
        list_desc = 'list all projects'
        list = self.Endpoints(list_desc, '/projects/all', '', 'GET')

        projects = self.Projects(list)

        return projects

    @property
    def releases(self):
        """Return releases endpoint data.
        
        Returns namedtuple.
        """
        list_url = '/projects/{}/releases'.format(self.proj_id)
        list_desc = 'list all projects'
        list = self.Endpoints(list_desc, list_url, '', 'GET')

        get_url = '/projects/{}/releases/{}'.format(
                self.proj_id, self.release_version)
        get_desc = 'get a release'
        get = self.Endpoints(get_desc, get_url, '', 'GET')

        create_url = '/releases'
        create_desc = 'create a release'
        create_body = {
            "ChannelId" : "channelid",
            "ProjectId" : "projectid",
            "SelectedPackages" : [],
            "Version" : "release_version"
            }
        create = self.Endpoints(create_desc,
                                create_url,
                                create_body,
                                'POST')

        return self.Releases(list, get, create)

