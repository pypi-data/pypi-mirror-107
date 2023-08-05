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


class ResponseWorkspaceCredentialsInfo(object):
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
        'created_dt': 'datetime',
        'credentials_id': 'int',
        'credentials_key': 'str',
        'credentials_name': 'str',
        'credentials_type': 'str',
        'workspace_id': 'int'
    }

    attribute_map = {
        'created_dt': 'created_dt',
        'credentials_id': 'credentials_id',
        'credentials_key': 'credentials_key',
        'credentials_name': 'credentials_name',
        'credentials_type': 'credentials_type',
        'workspace_id': 'workspace_id'
    }

    def __init__(self, created_dt=None, credentials_id=None, credentials_key=None, credentials_name=None, credentials_type=None, workspace_id=None, local_vars_configuration=None):  # noqa: E501
        """ResponseWorkspaceCredentialsInfo - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._created_dt = None
        self._credentials_id = None
        self._credentials_key = None
        self._credentials_name = None
        self._credentials_type = None
        self._workspace_id = None
        self.discriminator = None

        self.created_dt = created_dt
        if credentials_id is not None:
            self.credentials_id = credentials_id
        if credentials_key is not None:
            self.credentials_key = credentials_key
        if credentials_name is not None:
            self.credentials_name = credentials_name
        if credentials_type is not None:
            self.credentials_type = credentials_type
        if workspace_id is not None:
            self.workspace_id = workspace_id

    @property
    def created_dt(self):
        """Gets the created_dt of this ResponseWorkspaceCredentialsInfo.  # noqa: E501


        :return: The created_dt of this ResponseWorkspaceCredentialsInfo.  # noqa: E501
        :rtype: datetime
        """
        return self._created_dt

    @created_dt.setter
    def created_dt(self, created_dt):
        """Sets the created_dt of this ResponseWorkspaceCredentialsInfo.


        :param created_dt: The created_dt of this ResponseWorkspaceCredentialsInfo.  # noqa: E501
        :type created_dt: datetime
        """

        self._created_dt = created_dt

    @property
    def credentials_id(self):
        """Gets the credentials_id of this ResponseWorkspaceCredentialsInfo.  # noqa: E501


        :return: The credentials_id of this ResponseWorkspaceCredentialsInfo.  # noqa: E501
        :rtype: int
        """
        return self._credentials_id

    @credentials_id.setter
    def credentials_id(self, credentials_id):
        """Sets the credentials_id of this ResponseWorkspaceCredentialsInfo.


        :param credentials_id: The credentials_id of this ResponseWorkspaceCredentialsInfo.  # noqa: E501
        :type credentials_id: int
        """

        self._credentials_id = credentials_id

    @property
    def credentials_key(self):
        """Gets the credentials_key of this ResponseWorkspaceCredentialsInfo.  # noqa: E501


        :return: The credentials_key of this ResponseWorkspaceCredentialsInfo.  # noqa: E501
        :rtype: str
        """
        return self._credentials_key

    @credentials_key.setter
    def credentials_key(self, credentials_key):
        """Sets the credentials_key of this ResponseWorkspaceCredentialsInfo.


        :param credentials_key: The credentials_key of this ResponseWorkspaceCredentialsInfo.  # noqa: E501
        :type credentials_key: str
        """

        self._credentials_key = credentials_key

    @property
    def credentials_name(self):
        """Gets the credentials_name of this ResponseWorkspaceCredentialsInfo.  # noqa: E501


        :return: The credentials_name of this ResponseWorkspaceCredentialsInfo.  # noqa: E501
        :rtype: str
        """
        return self._credentials_name

    @credentials_name.setter
    def credentials_name(self, credentials_name):
        """Sets the credentials_name of this ResponseWorkspaceCredentialsInfo.


        :param credentials_name: The credentials_name of this ResponseWorkspaceCredentialsInfo.  # noqa: E501
        :type credentials_name: str
        """

        self._credentials_name = credentials_name

    @property
    def credentials_type(self):
        """Gets the credentials_type of this ResponseWorkspaceCredentialsInfo.  # noqa: E501


        :return: The credentials_type of this ResponseWorkspaceCredentialsInfo.  # noqa: E501
        :rtype: str
        """
        return self._credentials_type

    @credentials_type.setter
    def credentials_type(self, credentials_type):
        """Sets the credentials_type of this ResponseWorkspaceCredentialsInfo.


        :param credentials_type: The credentials_type of this ResponseWorkspaceCredentialsInfo.  # noqa: E501
        :type credentials_type: str
        """

        self._credentials_type = credentials_type

    @property
    def workspace_id(self):
        """Gets the workspace_id of this ResponseWorkspaceCredentialsInfo.  # noqa: E501


        :return: The workspace_id of this ResponseWorkspaceCredentialsInfo.  # noqa: E501
        :rtype: int
        """
        return self._workspace_id

    @workspace_id.setter
    def workspace_id(self, workspace_id):
        """Sets the workspace_id of this ResponseWorkspaceCredentialsInfo.


        :param workspace_id: The workspace_id of this ResponseWorkspaceCredentialsInfo.  # noqa: E501
        :type workspace_id: int
        """

        self._workspace_id = workspace_id

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
        if not isinstance(other, ResponseWorkspaceCredentialsInfo):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ResponseWorkspaceCredentialsInfo):
            return True

        return self.to_dict() != other.to_dict()
