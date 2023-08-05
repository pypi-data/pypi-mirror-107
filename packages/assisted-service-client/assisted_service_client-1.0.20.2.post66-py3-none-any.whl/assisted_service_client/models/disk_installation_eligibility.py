# coding: utf-8

"""
    AssistedInstall

    Assisted installation  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class DiskInstallationEligibility(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'eligible': 'bool',
        'not_eligible_reasons': 'list[str]'
    }

    attribute_map = {
        'eligible': 'eligible',
        'not_eligible_reasons': 'not_eligible_reasons'
    }

    def __init__(self, eligible=None, not_eligible_reasons=None):  # noqa: E501
        """DiskInstallationEligibility - a model defined in Swagger"""  # noqa: E501

        self._eligible = None
        self._not_eligible_reasons = None
        self.discriminator = None

        if eligible is not None:
            self.eligible = eligible
        if not_eligible_reasons is not None:
            self.not_eligible_reasons = not_eligible_reasons

    @property
    def eligible(self):
        """Gets the eligible of this DiskInstallationEligibility.  # noqa: E501

        Whether the disk is eligible for installation or not.  # noqa: E501

        :return: The eligible of this DiskInstallationEligibility.  # noqa: E501
        :rtype: bool
        """
        return self._eligible

    @eligible.setter
    def eligible(self, eligible):
        """Sets the eligible of this DiskInstallationEligibility.

        Whether the disk is eligible for installation or not.  # noqa: E501

        :param eligible: The eligible of this DiskInstallationEligibility.  # noqa: E501
        :type: bool
        """

        self._eligible = eligible

    @property
    def not_eligible_reasons(self):
        """Gets the not_eligible_reasons of this DiskInstallationEligibility.  # noqa: E501

        Reasons for why this disk is not eligible for installation.  # noqa: E501

        :return: The not_eligible_reasons of this DiskInstallationEligibility.  # noqa: E501
        :rtype: list[str]
        """
        return self._not_eligible_reasons

    @not_eligible_reasons.setter
    def not_eligible_reasons(self, not_eligible_reasons):
        """Sets the not_eligible_reasons of this DiskInstallationEligibility.

        Reasons for why this disk is not eligible for installation.  # noqa: E501

        :param not_eligible_reasons: The not_eligible_reasons of this DiskInstallationEligibility.  # noqa: E501
        :type: list[str]
        """

        self._not_eligible_reasons = not_eligible_reasons

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(DiskInstallationEligibility, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, DiskInstallationEligibility):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
