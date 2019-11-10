"""Unittests for actopus module."""


import unittest
import requests
from unittest import mock
from unittest.mock import MagicMock
from http import HTTPStatus
from actopus.actopus import (Actopus, ResourceCreationError, ResourceNotFoundError,
                             ResourceAlreadyExistsError, EndpointDataError)
from .mocks import all_projects, created_success
from requests.exceptions import ConnectionError


class TestActopus(unittest.TestCase):
    """Tests for actopus.py"""

    def setUp(self):
        pass

    def tearUp(self):
        pass

    def test_get_endpoint_def_returns_endpoint_defs(self):
        """get_endpoint_def should return endpoint details."""
        ap = Actopus('myserver.mycomp.com', 'anapikey')
        epdef = ap.get_endpoint_def('projects', 'list')
        expected = {'action': 'list', 'endpoint': '/projects/all', 'method': 'GET'}
        self.assertEqual(epdef, expected)

    def test_get_endpoint_def_nonexisting_type(self):
        """get_endpoint_def should raise exception for nonexisting type."""
        ap = Actopus('myserver.mycomp.com', 'anapikey')
        with self.assertRaises(EndpointDataError) as cx:
            epdef = ap.get_endpoint_def('notatype', 'notanaction')

    def test_get_endpoint_def_nonexisting_action(self):
        """get_endpoint_def should raise exception for nonexisting action."""
        ap = Actopus('myserver.mycomp.com', 'anapikey')
        with self.assertRaises(EndpointDataError) as cx:
            epdef = ap.get_endpoint_def('projects', 'notanaction')

    @mock.patch('actopus.actopus.Actopus.send_request')
    @mock.patch('actopus.actopus.Actopus.find_projectid_byname')
    def test_release_exists_true(self, mock_find_by_name, mock_send_request):
        """test_release should return True if release exists already."""
        ap = Actopus('myserver.mycomp.com', 'anapikey')
        mock_find_by_name.return_value = 'Project-161'
        expected = requests.Response()
        expected.status_code = HTTPStatus.OK
        mock_send_request.return_value = expected
        self.assertTrue(ap.release_exists('myproject', 'B100'))

    @mock.patch('actopus.actopus.Actopus.send_request')
    @mock.patch('actopus.actopus.Actopus.find_projectid_byname')
    def test_release_exists_false(self, mock_find_by_name, mock_send_request):
        """test_release should return False if release does not exist."""
        ap = Actopus('myserver.mycomp.com', 'anapikey')
        mock_find_by_name.return_value = 'Project-161'
        expected = requests.Response()
        expected.status_code = HTTPStatus.NOT_FOUND
        mock_send_request.return_value = expected
        self.assertFalse(ap.release_exists('myproject', 'B100'))

    @mock.patch('actopus.actopus.Actopus.send_request')
    def test_find_project_byname_with_existing_project_name(self, mock_send_request):
        """find_projectid_byname should return projectid."""
        ap = Actopus('myserver.mycomp.com', 'anapikey')
        ret_json = all_projects
        expected = MagicMock()
        expected.json = MagicMock(return_value=ret_json)
        mock_send_request.return_value = expected
        ret = ap.find_projectid_byname('test-proj')
        self.assertEqual(ret, 'Projects-1')

    @mock.patch('actopus.actopus.Actopus.send_request')
    def test_find_project_byname_with_not_found_project_name(self, mock_send_request):
        """find_projectid_byname should return None if project name is not found."""
        ap = Actopus('myserver.mycomp.com', 'anapikey')
        ret_json = all_projects
        expected = MagicMock()
        expected.json = MagicMock(return_value=ret_json)
        mock_send_request.return_value = expected
        ret = ap.find_projectid_byname('notaproject')
        self.assertEqual(ret, None)

    @mock.patch('actopus.actopus.Actopus.send_request')
    @mock.patch('actopus.actopus.Actopus.find_projectid_byname')
    @mock.patch('actopus.actopus.Actopus.release_exists')
    def test_create_release(self, mock_release_exists, mock_find_by_name, mock_send_request):
        """create_release should create a release given valid params."""
        ap = Actopus('myserver.mycomp.com', 'anapikey')
        mock_find_by_name.return_value = 'Project-161'
        fbn_expected = requests.Response()
        fbn_expected.status_code = HTTPStatus.CREATED
        fbn_expected.json = MagicMock(return_value=created_success)
        mock_send_request.return_value = fbn_expected
        mock_release_exists.return_value = False
        resp = ap.create_release('my_project', '1.2.3')
        self.assertEqual(resp, fbn_expected.json())

    @mock.patch('actopus.actopus.Actopus.send_request')
    @mock.patch('actopus.actopus.Actopus.find_projectid_byname')
    @mock.patch('actopus.actopus.Actopus.release_exists')
    def test_create_release_version_exists(self, mock_release_exists, mock_find_by_name, mock_send_request):
        """create_release should throw an exception if release exists."""
        ap = Actopus('myserver.mycomp.com', 'anapikey')
        mock_find_by_name.return_value = 'Project-161'
        fbn_expected = requests.Response()
        fbn_expected.status_code = HTTPStatus.CREATED
        fbn_expected.json = MagicMock(return_value=created_success)
        mock_send_request.return_value = fbn_expected
        mock_release_exists.return_value = True
        with self.assertRaises(ResourceAlreadyExistsError) as cx:
            ap.create_release('my_project', '1.2.3')
    
    @mock.patch('actopus.actopus.Actopus.send_request')
    @mock.patch('actopus.actopus.Actopus.find_projectid_byname')
    @mock.patch('actopus.actopus.Actopus.release_exists')
    def test_create_release_project_not_found(self, mock_release_exists, mock_find_by_name, mock_send_request):
        """create_release should throw an exception if project name is not found."""
        ap = Actopus('myserver.mycomp.com', 'anapikey')
        mock_find_by_name.return_value = None
        fbn_expected = requests.Response()
        fbn_expected.status_code = HTTPStatus.CREATED
        fbn_expected.json = MagicMock(return_value=created_success)
        mock_send_request.return_value = fbn_expected
        mock_release_exists.return_value = False
        with self.assertRaises(ResourceNotFoundError) as cx:
            ap.create_release('myproject', '1.2.3')

    @mock.patch('actopus.actopus.Actopus.send_request')
    @mock.patch('actopus.actopus.Actopus.find_projectid_byname')
    @mock.patch('actopus.actopus.Actopus.release_exists')
    def test_create_release_bad_return_code(self, mock_release_exists, mock_find_by_name, mock_send_request):
        """create_release should throw an exception if octopus gives a bad return code."""
        ap = Actopus('myserver.mycomp.com', 'anapikey')
        mock_find_by_name.return_value = 'Project-161'
        fbn_expected = requests.Response()
        fbn_expected.status_code = HTTPStatus.UNAUTHORIZED
        fbn_expected.json = MagicMock(return_value=created_success)
        mock_send_request.return_value = fbn_expected
        mock_release_exists.return_value = False
        with self.assertRaises(ResourceCreationError) as cx:
            ap.create_release('myproject', '1.2.3')
