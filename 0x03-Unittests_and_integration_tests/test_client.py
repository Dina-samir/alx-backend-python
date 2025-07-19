#!/usr/bin/env python3

import unittest
from unittest.mock import patch, Mock,PropertyMock
from parameterized import parameterized, parameterized_class
from fixtures import TEST_PAYLOAD
from client import GithubOrgClient
import requests


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct data and calls get_json once"""
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, test_payload)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns expected URL from mocked org"""
        with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/google/repos"}
            client = GithubOrgClient("google")
            result = client._public_repos_url
            self.assertEqual(result, "https://api.github.com/orgs/google/repos")


    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected list and mocks are called once"""
        # Mock get_json response (repos payload)
        test_repos = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        mock_get_json.return_value = test_repos

        # Patch _public_repos_url to avoid using .org
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "http://fake-url.com"

            client = GithubOrgClient("google")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("http://fake-url.com")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct boolean"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)

##################################################################################################################



@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],          
        "repos_payload": TEST_PAYLOAD[0][1],        # list of repos
        "expected_repos": TEST_PAYLOAD[0][2],        
        "apache2_repos": TEST_PAYLOAD[0][3],        
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get with predefined payloads"""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()


        cls.mock_get.side_effect = [
            Mock(json=Mock(return_value=cls.org_payload)),      # test 1: org
            Mock(json=Mock(return_value=cls.repos_payload)),    # test 1: repos
            Mock(json=Mock(return_value=cls.org_payload)),      # test 2: org
            Mock(json=Mock(return_value=cls.repos_payload)),    # test 2: repos
        ]


    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repo names"""
        client = GithubOrgClient("google")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filters repos by apache-2.0 license"""
        client = GithubOrgClient("google")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)
