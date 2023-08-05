# coding: utf-8

"""
    Aron API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


import inspect
import pprint
import re  # noqa: F401
import six

from openapi_client.configuration import Configuration


class ProtoSystemMetricList(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'name': 'str',
        'system_metrics': 'list[ProtoSystemMetric]'
    }

    attribute_map = {
        'name': 'name',
        'system_metrics': 'system_metrics'
    }

    def __init__(self, name=None, system_metrics=None, local_vars_configuration=None):  # noqa: E501
        """ProtoSystemMetricList - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._system_metrics = None
        self.discriminator = None

        self.name = name
        self.system_metrics = system_metrics

    @property
    def name(self):
        """Gets the name of this ProtoSystemMetricList.  # noqa: E501


        :return: The name of this ProtoSystemMetricList.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ProtoSystemMetricList.


        :param name: The name of this ProtoSystemMetricList.  # noqa: E501
        :type name: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def system_metrics(self):
        """Gets the system_metrics of this ProtoSystemMetricList.  # noqa: E501


        :return: The system_metrics of this ProtoSystemMetricList.  # noqa: E501
        :rtype: list[ProtoSystemMetric]
        """
        return self._system_metrics

    @system_metrics.setter
    def system_metrics(self, system_metrics):
        """Sets the system_metrics of this ProtoSystemMetricList.


        :param system_metrics: The system_metrics of this ProtoSystemMetricList.  # noqa: E501
        :type system_metrics: list[ProtoSystemMetric]
        """
        if self.local_vars_configuration.client_side_validation and system_metrics is None:  # noqa: E501
            raise ValueError("Invalid value for `system_metrics`, must not be `None`")  # noqa: E501

        self._system_metrics = system_metrics

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = inspect.getargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ProtoSystemMetricList):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ProtoSystemMetricList):
            return True

        return self.to_dict() != other.to_dict()
