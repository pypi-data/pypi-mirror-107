# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from opera.api.openapi.models.base_model_ import Model
from opera.api.openapi import util


class DeploymentInput(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, inputs=None, service_template=None, clean_state=None):  # noqa: E501
        """DeploymentInput - a model defined in OpenAPI

        :param inputs: The inputs of this DeploymentInput.  # noqa: E501
        :type inputs: object
        :param service_template: The service_template of this DeploymentInput.  # noqa: E501
        :type service_template: str
        :param clean_state: The clean_state of this DeploymentInput.  # noqa: E501
        :type clean_state: bool
        """
        self.openapi_types = {
            'inputs': object,
            'service_template': str,
            'clean_state': bool
        }

        self.attribute_map = {
            'inputs': 'inputs',
            'service_template': 'service_template',
            'clean_state': 'clean_state'
        }

        self._inputs = inputs
        self._service_template = service_template
        self._clean_state = clean_state

    @classmethod
    def from_dict(cls, dikt) -> 'DeploymentInput':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The DeploymentInput of this DeploymentInput.  # noqa: E501
        :rtype: DeploymentInput
        """
        return util.deserialize_model(dikt, cls)

    @property
    def inputs(self):
        """Gets the inputs of this DeploymentInput.


        :return: The inputs of this DeploymentInput.
        :rtype: object
        """
        return self._inputs

    @inputs.setter
    def inputs(self, inputs):
        """Sets the inputs of this DeploymentInput.


        :param inputs: The inputs of this DeploymentInput.
        :type inputs: object
        """

        self._inputs = inputs

    @property
    def service_template(self):
        """Gets the service_template of this DeploymentInput.


        :return: The service_template of this DeploymentInput.
        :rtype: str
        """
        return self._service_template

    @service_template.setter
    def service_template(self, service_template):
        """Sets the service_template of this DeploymentInput.


        :param service_template: The service_template of this DeploymentInput.
        :type service_template: str
        """
        if service_template is None:
            raise ValueError("Invalid value for `service_template`, must not be `None`")  # noqa: E501

        self._service_template = service_template

    @property
    def clean_state(self):
        """Gets the clean_state of this DeploymentInput.


        :return: The clean_state of this DeploymentInput.
        :rtype: bool
        """
        return self._clean_state

    @clean_state.setter
    def clean_state(self, clean_state):
        """Sets the clean_state of this DeploymentInput.


        :param clean_state: The clean_state of this DeploymentInput.
        :type clean_state: bool
        """

        self._clean_state = clean_state
