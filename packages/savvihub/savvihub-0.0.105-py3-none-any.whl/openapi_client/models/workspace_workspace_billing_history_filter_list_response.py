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


class WorkspaceWorkspaceBillingHistoryFilterListResponse(object):
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
        'projects': 'list[ResponseSimpleProject]',
        'statuses': 'list[str]',
        'types': 'list[str]',
        'users': 'list[ResponseSimpleUser]'
    }

    attribute_map = {
        'projects': 'projects',
        'statuses': 'statuses',
        'types': 'types',
        'users': 'users'
    }

    def __init__(self, projects=None, statuses=None, types=None, users=None, local_vars_configuration=None):  # noqa: E501
        """WorkspaceWorkspaceBillingHistoryFilterListResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._projects = None
        self._statuses = None
        self._types = None
        self._users = None
        self.discriminator = None

        if projects is not None:
            self.projects = projects
        if statuses is not None:
            self.statuses = statuses
        if types is not None:
            self.types = types
        if users is not None:
            self.users = users

    @property
    def projects(self):
        """Gets the projects of this WorkspaceWorkspaceBillingHistoryFilterListResponse.  # noqa: E501


        :return: The projects of this WorkspaceWorkspaceBillingHistoryFilterListResponse.  # noqa: E501
        :rtype: list[ResponseSimpleProject]
        """
        return self._projects

    @projects.setter
    def projects(self, projects):
        """Sets the projects of this WorkspaceWorkspaceBillingHistoryFilterListResponse.


        :param projects: The projects of this WorkspaceWorkspaceBillingHistoryFilterListResponse.  # noqa: E501
        :type projects: list[ResponseSimpleProject]
        """

        self._projects = projects

    @property
    def statuses(self):
        """Gets the statuses of this WorkspaceWorkspaceBillingHistoryFilterListResponse.  # noqa: E501


        :return: The statuses of this WorkspaceWorkspaceBillingHistoryFilterListResponse.  # noqa: E501
        :rtype: list[str]
        """
        return self._statuses

    @statuses.setter
    def statuses(self, statuses):
        """Sets the statuses of this WorkspaceWorkspaceBillingHistoryFilterListResponse.


        :param statuses: The statuses of this WorkspaceWorkspaceBillingHistoryFilterListResponse.  # noqa: E501
        :type statuses: list[str]
        """

        self._statuses = statuses

    @property
    def types(self):
        """Gets the types of this WorkspaceWorkspaceBillingHistoryFilterListResponse.  # noqa: E501


        :return: The types of this WorkspaceWorkspaceBillingHistoryFilterListResponse.  # noqa: E501
        :rtype: list[str]
        """
        return self._types

    @types.setter
    def types(self, types):
        """Sets the types of this WorkspaceWorkspaceBillingHistoryFilterListResponse.


        :param types: The types of this WorkspaceWorkspaceBillingHistoryFilterListResponse.  # noqa: E501
        :type types: list[str]
        """

        self._types = types

    @property
    def users(self):
        """Gets the users of this WorkspaceWorkspaceBillingHistoryFilterListResponse.  # noqa: E501


        :return: The users of this WorkspaceWorkspaceBillingHistoryFilterListResponse.  # noqa: E501
        :rtype: list[ResponseSimpleUser]
        """
        return self._users

    @users.setter
    def users(self, users):
        """Sets the users of this WorkspaceWorkspaceBillingHistoryFilterListResponse.


        :param users: The users of this WorkspaceWorkspaceBillingHistoryFilterListResponse.  # noqa: E501
        :type users: list[ResponseSimpleUser]
        """

        self._users = users

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
        if not isinstance(other, WorkspaceWorkspaceBillingHistoryFilterListResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, WorkspaceWorkspaceBillingHistoryFilterListResponse):
            return True

        return self.to_dict() != other.to_dict()
