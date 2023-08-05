# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from opera.api.openapi.models.base_model_ import Model
from opera.api.openapi import util


class InvocationState(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    """
    allowed enum values
    """
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"
    def __init__(self):  # noqa: E501
        """InvocationState - a model defined in OpenAPI

        """
        self.openapi_types = {
        }

        self.attribute_map = {
        }

    @classmethod
    def from_dict(cls, dikt) -> 'InvocationState':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The InvocationState of this InvocationState.  # noqa: E501
        :rtype: InvocationState
        """
        return util.deserialize_model(dikt, cls)
