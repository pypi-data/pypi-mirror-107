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


class ModelWorkspace(object):
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
        'aws_external_id': 'str',
        'created_dt': 'datetime',
        'credit_balance': 'float',
        'default_region': 'str',
        'description': 'str',
        'display_name': 'str',
        'edges': 'ModelWorkspaceEdges',
        'id': 'int',
        'immutable_slug': 'str',
        'is_public': 'bool',
        'name': 'str',
        'updated_dt': 'datetime',
        'workspace_default_kernel_cluster': 'int',
        'workspace_default_storage': 'int',
        'workspace_default_volume': 'int',
        'workspace_primary_owner': 'int'
    }

    attribute_map = {
        'aws_external_id': 'aws_external_id',
        'created_dt': 'created_dt',
        'credit_balance': 'credit_balance',
        'default_region': 'default_region',
        'description': 'description',
        'display_name': 'display_name',
        'edges': 'edges',
        'id': 'id',
        'immutable_slug': 'immutable_slug',
        'is_public': 'is_public',
        'name': 'name',
        'updated_dt': 'updated_dt',
        'workspace_default_kernel_cluster': 'workspace_default_kernel_cluster',
        'workspace_default_storage': 'workspace_default_storage',
        'workspace_default_volume': 'workspace_default_volume',
        'workspace_primary_owner': 'workspace_primary_owner'
    }

    def __init__(self, aws_external_id=None, created_dt=None, credit_balance=None, default_region=None, description=None, display_name=None, edges=None, id=None, immutable_slug=None, is_public=None, name=None, updated_dt=None, workspace_default_kernel_cluster=None, workspace_default_storage=None, workspace_default_volume=None, workspace_primary_owner=None, local_vars_configuration=None):  # noqa: E501
        """ModelWorkspace - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._aws_external_id = None
        self._created_dt = None
        self._credit_balance = None
        self._default_region = None
        self._description = None
        self._display_name = None
        self._edges = None
        self._id = None
        self._immutable_slug = None
        self._is_public = None
        self._name = None
        self._updated_dt = None
        self._workspace_default_kernel_cluster = None
        self._workspace_default_storage = None
        self._workspace_default_volume = None
        self._workspace_primary_owner = None
        self.discriminator = None

        if aws_external_id is not None:
            self.aws_external_id = aws_external_id
        self.created_dt = created_dt
        if credit_balance is not None:
            self.credit_balance = credit_balance
        if default_region is not None:
            self.default_region = default_region
        self.description = description
        if display_name is not None:
            self.display_name = display_name
        if edges is not None:
            self.edges = edges
        if id is not None:
            self.id = id
        if immutable_slug is not None:
            self.immutable_slug = immutable_slug
        if is_public is not None:
            self.is_public = is_public
        if name is not None:
            self.name = name
        self.updated_dt = updated_dt
        self.workspace_default_kernel_cluster = workspace_default_kernel_cluster
        self.workspace_default_storage = workspace_default_storage
        self.workspace_default_volume = workspace_default_volume
        if workspace_primary_owner is not None:
            self.workspace_primary_owner = workspace_primary_owner

    @property
    def aws_external_id(self):
        """Gets the aws_external_id of this ModelWorkspace.  # noqa: E501


        :return: The aws_external_id of this ModelWorkspace.  # noqa: E501
        :rtype: str
        """
        return self._aws_external_id

    @aws_external_id.setter
    def aws_external_id(self, aws_external_id):
        """Sets the aws_external_id of this ModelWorkspace.


        :param aws_external_id: The aws_external_id of this ModelWorkspace.  # noqa: E501
        :type aws_external_id: str
        """

        self._aws_external_id = aws_external_id

    @property
    def created_dt(self):
        """Gets the created_dt of this ModelWorkspace.  # noqa: E501


        :return: The created_dt of this ModelWorkspace.  # noqa: E501
        :rtype: datetime
        """
        return self._created_dt

    @created_dt.setter
    def created_dt(self, created_dt):
        """Sets the created_dt of this ModelWorkspace.


        :param created_dt: The created_dt of this ModelWorkspace.  # noqa: E501
        :type created_dt: datetime
        """

        self._created_dt = created_dt

    @property
    def credit_balance(self):
        """Gets the credit_balance of this ModelWorkspace.  # noqa: E501


        :return: The credit_balance of this ModelWorkspace.  # noqa: E501
        :rtype: float
        """
        return self._credit_balance

    @credit_balance.setter
    def credit_balance(self, credit_balance):
        """Sets the credit_balance of this ModelWorkspace.


        :param credit_balance: The credit_balance of this ModelWorkspace.  # noqa: E501
        :type credit_balance: float
        """

        self._credit_balance = credit_balance

    @property
    def default_region(self):
        """Gets the default_region of this ModelWorkspace.  # noqa: E501


        :return: The default_region of this ModelWorkspace.  # noqa: E501
        :rtype: str
        """
        return self._default_region

    @default_region.setter
    def default_region(self, default_region):
        """Sets the default_region of this ModelWorkspace.


        :param default_region: The default_region of this ModelWorkspace.  # noqa: E501
        :type default_region: str
        """

        self._default_region = default_region

    @property
    def description(self):
        """Gets the description of this ModelWorkspace.  # noqa: E501


        :return: The description of this ModelWorkspace.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ModelWorkspace.


        :param description: The description of this ModelWorkspace.  # noqa: E501
        :type description: str
        """

        self._description = description

    @property
    def display_name(self):
        """Gets the display_name of this ModelWorkspace.  # noqa: E501


        :return: The display_name of this ModelWorkspace.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this ModelWorkspace.


        :param display_name: The display_name of this ModelWorkspace.  # noqa: E501
        :type display_name: str
        """

        self._display_name = display_name

    @property
    def edges(self):
        """Gets the edges of this ModelWorkspace.  # noqa: E501


        :return: The edges of this ModelWorkspace.  # noqa: E501
        :rtype: ModelWorkspaceEdges
        """
        return self._edges

    @edges.setter
    def edges(self, edges):
        """Sets the edges of this ModelWorkspace.


        :param edges: The edges of this ModelWorkspace.  # noqa: E501
        :type edges: ModelWorkspaceEdges
        """

        self._edges = edges

    @property
    def id(self):
        """Gets the id of this ModelWorkspace.  # noqa: E501


        :return: The id of this ModelWorkspace.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ModelWorkspace.


        :param id: The id of this ModelWorkspace.  # noqa: E501
        :type id: int
        """

        self._id = id

    @property
    def immutable_slug(self):
        """Gets the immutable_slug of this ModelWorkspace.  # noqa: E501


        :return: The immutable_slug of this ModelWorkspace.  # noqa: E501
        :rtype: str
        """
        return self._immutable_slug

    @immutable_slug.setter
    def immutable_slug(self, immutable_slug):
        """Sets the immutable_slug of this ModelWorkspace.


        :param immutable_slug: The immutable_slug of this ModelWorkspace.  # noqa: E501
        :type immutable_slug: str
        """

        self._immutable_slug = immutable_slug

    @property
    def is_public(self):
        """Gets the is_public of this ModelWorkspace.  # noqa: E501


        :return: The is_public of this ModelWorkspace.  # noqa: E501
        :rtype: bool
        """
        return self._is_public

    @is_public.setter
    def is_public(self, is_public):
        """Sets the is_public of this ModelWorkspace.


        :param is_public: The is_public of this ModelWorkspace.  # noqa: E501
        :type is_public: bool
        """

        self._is_public = is_public

    @property
    def name(self):
        """Gets the name of this ModelWorkspace.  # noqa: E501


        :return: The name of this ModelWorkspace.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ModelWorkspace.


        :param name: The name of this ModelWorkspace.  # noqa: E501
        :type name: str
        """

        self._name = name

    @property
    def updated_dt(self):
        """Gets the updated_dt of this ModelWorkspace.  # noqa: E501


        :return: The updated_dt of this ModelWorkspace.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_dt

    @updated_dt.setter
    def updated_dt(self, updated_dt):
        """Sets the updated_dt of this ModelWorkspace.


        :param updated_dt: The updated_dt of this ModelWorkspace.  # noqa: E501
        :type updated_dt: datetime
        """

        self._updated_dt = updated_dt

    @property
    def workspace_default_kernel_cluster(self):
        """Gets the workspace_default_kernel_cluster of this ModelWorkspace.  # noqa: E501


        :return: The workspace_default_kernel_cluster of this ModelWorkspace.  # noqa: E501
        :rtype: int
        """
        return self._workspace_default_kernel_cluster

    @workspace_default_kernel_cluster.setter
    def workspace_default_kernel_cluster(self, workspace_default_kernel_cluster):
        """Sets the workspace_default_kernel_cluster of this ModelWorkspace.


        :param workspace_default_kernel_cluster: The workspace_default_kernel_cluster of this ModelWorkspace.  # noqa: E501
        :type workspace_default_kernel_cluster: int
        """

        self._workspace_default_kernel_cluster = workspace_default_kernel_cluster

    @property
    def workspace_default_storage(self):
        """Gets the workspace_default_storage of this ModelWorkspace.  # noqa: E501


        :return: The workspace_default_storage of this ModelWorkspace.  # noqa: E501
        :rtype: int
        """
        return self._workspace_default_storage

    @workspace_default_storage.setter
    def workspace_default_storage(self, workspace_default_storage):
        """Sets the workspace_default_storage of this ModelWorkspace.


        :param workspace_default_storage: The workspace_default_storage of this ModelWorkspace.  # noqa: E501
        :type workspace_default_storage: int
        """

        self._workspace_default_storage = workspace_default_storage

    @property
    def workspace_default_volume(self):
        """Gets the workspace_default_volume of this ModelWorkspace.  # noqa: E501


        :return: The workspace_default_volume of this ModelWorkspace.  # noqa: E501
        :rtype: int
        """
        return self._workspace_default_volume

    @workspace_default_volume.setter
    def workspace_default_volume(self, workspace_default_volume):
        """Sets the workspace_default_volume of this ModelWorkspace.


        :param workspace_default_volume: The workspace_default_volume of this ModelWorkspace.  # noqa: E501
        :type workspace_default_volume: int
        """

        self._workspace_default_volume = workspace_default_volume

    @property
    def workspace_primary_owner(self):
        """Gets the workspace_primary_owner of this ModelWorkspace.  # noqa: E501


        :return: The workspace_primary_owner of this ModelWorkspace.  # noqa: E501
        :rtype: int
        """
        return self._workspace_primary_owner

    @workspace_primary_owner.setter
    def workspace_primary_owner(self, workspace_primary_owner):
        """Sets the workspace_primary_owner of this ModelWorkspace.


        :param workspace_primary_owner: The workspace_primary_owner of this ModelWorkspace.  # noqa: E501
        :type workspace_primary_owner: int
        """

        self._workspace_primary_owner = workspace_primary_owner

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
        if not isinstance(other, ModelWorkspace):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ModelWorkspace):
            return True

        return self.to_dict() != other.to_dict()
