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


class ModelAccessToken(object):
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
        'access_token_user': 'int',
        'created_dt': 'datetime',
        'edges': 'ModelAccessTokenEdges',
        'expire_at': 'datetime',
        'id': 'int',
        'immutable_slug': 'str',
        'permissions': 'dict(str, object)',
        'title': 'str',
        'type': 'str',
        'updated_dt': 'datetime'
    }

    attribute_map = {
        'access_token_user': 'access_token_user',
        'created_dt': 'created_dt',
        'edges': 'edges',
        'expire_at': 'expire_at',
        'id': 'id',
        'immutable_slug': 'immutable_slug',
        'permissions': 'permissions',
        'title': 'title',
        'type': 'type',
        'updated_dt': 'updated_dt'
    }

    def __init__(self, access_token_user=None, created_dt=None, edges=None, expire_at=None, id=None, immutable_slug=None, permissions=None, title=None, type=None, updated_dt=None, local_vars_configuration=None):  # noqa: E501
        """ModelAccessToken - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._access_token_user = None
        self._created_dt = None
        self._edges = None
        self._expire_at = None
        self._id = None
        self._immutable_slug = None
        self._permissions = None
        self._title = None
        self._type = None
        self._updated_dt = None
        self.discriminator = None

        if access_token_user is not None:
            self.access_token_user = access_token_user
        self.created_dt = created_dt
        if edges is not None:
            self.edges = edges
        self.expire_at = expire_at
        if id is not None:
            self.id = id
        if immutable_slug is not None:
            self.immutable_slug = immutable_slug
        if permissions is not None:
            self.permissions = permissions
        self.title = title
        if type is not None:
            self.type = type
        self.updated_dt = updated_dt

    @property
    def access_token_user(self):
        """Gets the access_token_user of this ModelAccessToken.  # noqa: E501


        :return: The access_token_user of this ModelAccessToken.  # noqa: E501
        :rtype: int
        """
        return self._access_token_user

    @access_token_user.setter
    def access_token_user(self, access_token_user):
        """Sets the access_token_user of this ModelAccessToken.


        :param access_token_user: The access_token_user of this ModelAccessToken.  # noqa: E501
        :type access_token_user: int
        """

        self._access_token_user = access_token_user

    @property
    def created_dt(self):
        """Gets the created_dt of this ModelAccessToken.  # noqa: E501


        :return: The created_dt of this ModelAccessToken.  # noqa: E501
        :rtype: datetime
        """
        return self._created_dt

    @created_dt.setter
    def created_dt(self, created_dt):
        """Sets the created_dt of this ModelAccessToken.


        :param created_dt: The created_dt of this ModelAccessToken.  # noqa: E501
        :type created_dt: datetime
        """

        self._created_dt = created_dt

    @property
    def edges(self):
        """Gets the edges of this ModelAccessToken.  # noqa: E501


        :return: The edges of this ModelAccessToken.  # noqa: E501
        :rtype: ModelAccessTokenEdges
        """
        return self._edges

    @edges.setter
    def edges(self, edges):
        """Sets the edges of this ModelAccessToken.


        :param edges: The edges of this ModelAccessToken.  # noqa: E501
        :type edges: ModelAccessTokenEdges
        """

        self._edges = edges

    @property
    def expire_at(self):
        """Gets the expire_at of this ModelAccessToken.  # noqa: E501


        :return: The expire_at of this ModelAccessToken.  # noqa: E501
        :rtype: datetime
        """
        return self._expire_at

    @expire_at.setter
    def expire_at(self, expire_at):
        """Sets the expire_at of this ModelAccessToken.


        :param expire_at: The expire_at of this ModelAccessToken.  # noqa: E501
        :type expire_at: datetime
        """

        self._expire_at = expire_at

    @property
    def id(self):
        """Gets the id of this ModelAccessToken.  # noqa: E501


        :return: The id of this ModelAccessToken.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ModelAccessToken.


        :param id: The id of this ModelAccessToken.  # noqa: E501
        :type id: int
        """

        self._id = id

    @property
    def immutable_slug(self):
        """Gets the immutable_slug of this ModelAccessToken.  # noqa: E501


        :return: The immutable_slug of this ModelAccessToken.  # noqa: E501
        :rtype: str
        """
        return self._immutable_slug

    @immutable_slug.setter
    def immutable_slug(self, immutable_slug):
        """Sets the immutable_slug of this ModelAccessToken.


        :param immutable_slug: The immutable_slug of this ModelAccessToken.  # noqa: E501
        :type immutable_slug: str
        """

        self._immutable_slug = immutable_slug

    @property
    def permissions(self):
        """Gets the permissions of this ModelAccessToken.  # noqa: E501


        :return: The permissions of this ModelAccessToken.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._permissions

    @permissions.setter
    def permissions(self, permissions):
        """Sets the permissions of this ModelAccessToken.


        :param permissions: The permissions of this ModelAccessToken.  # noqa: E501
        :type permissions: dict(str, object)
        """

        self._permissions = permissions

    @property
    def title(self):
        """Gets the title of this ModelAccessToken.  # noqa: E501


        :return: The title of this ModelAccessToken.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this ModelAccessToken.


        :param title: The title of this ModelAccessToken.  # noqa: E501
        :type title: str
        """

        self._title = title

    @property
    def type(self):
        """Gets the type of this ModelAccessToken.  # noqa: E501


        :return: The type of this ModelAccessToken.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this ModelAccessToken.


        :param type: The type of this ModelAccessToken.  # noqa: E501
        :type type: str
        """

        self._type = type

    @property
    def updated_dt(self):
        """Gets the updated_dt of this ModelAccessToken.  # noqa: E501


        :return: The updated_dt of this ModelAccessToken.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_dt

    @updated_dt.setter
    def updated_dt(self, updated_dt):
        """Sets the updated_dt of this ModelAccessToken.


        :param updated_dt: The updated_dt of this ModelAccessToken.  # noqa: E501
        :type updated_dt: datetime
        """

        self._updated_dt = updated_dt

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
        if not isinstance(other, ModelAccessToken):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ModelAccessToken):
            return True

        return self.to_dict() != other.to_dict()
