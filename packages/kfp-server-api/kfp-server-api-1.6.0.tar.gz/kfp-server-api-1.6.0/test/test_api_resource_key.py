# coding: utf-8

"""
    Kubeflow Pipelines API

    This file contains REST API specification for Kubeflow Pipelines. The file is autogenerated from the swagger definition.

    Contact: kubeflow-pipelines@google.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import kfp_server_api
from kfp_server_api.models.api_resource_key import ApiResourceKey  # noqa: E501
from kfp_server_api.rest import ApiException

class TestApiResourceKey(unittest.TestCase):
    """ApiResourceKey unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ApiResourceKey
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = kfp_server_api.models.api_resource_key.ApiResourceKey()  # noqa: E501
        if include_optional :
            return ApiResourceKey(
                type = 'UNKNOWN_RESOURCE_TYPE', 
                id = '0'
            )
        else :
            return ApiResourceKey(
        )

    def testApiResourceKey(self):
        """Test ApiResourceKey"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
