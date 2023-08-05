# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from opera.api.openapi.models.base_model_ import Model
from opera.api.openapi import util


class CsarValidationInput(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, csar_path=None, inputs=None):  # noqa: E501
        """CsarValidationInput - a model defined in OpenAPI

        :param csar_path: The csar_path of this CsarValidationInput.  # noqa: E501
        :type csar_path: str
        :param inputs: The inputs of this CsarValidationInput.  # noqa: E501
        :type inputs: object
        """
        self.openapi_types = {
            'csar_path': str,
            'inputs': object
        }

        self.attribute_map = {
            'csar_path': 'csar_path',
            'inputs': 'inputs'
        }

        self._csar_path = csar_path
        self._inputs = inputs

    @classmethod
    def from_dict(cls, dikt) -> 'CsarValidationInput':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The CsarValidationInput of this CsarValidationInput.  # noqa: E501
        :rtype: CsarValidationInput
        """
        return util.deserialize_model(dikt, cls)

    @property
    def csar_path(self):
        """Gets the csar_path of this CsarValidationInput.


        :return: The csar_path of this CsarValidationInput.
        :rtype: str
        """
        return self._csar_path

    @csar_path.setter
    def csar_path(self, csar_path):
        """Sets the csar_path of this CsarValidationInput.


        :param csar_path: The csar_path of this CsarValidationInput.
        :type csar_path: str
        """

        self._csar_path = csar_path

    @property
    def inputs(self):
        """Gets the inputs of this CsarValidationInput.


        :return: The inputs of this CsarValidationInput.
        :rtype: object
        """
        return self._inputs

    @inputs.setter
    def inputs(self, inputs):
        """Sets the inputs of this CsarValidationInput.


        :param inputs: The inputs of this CsarValidationInput.
        :type inputs: object
        """

        self._inputs = inputs
