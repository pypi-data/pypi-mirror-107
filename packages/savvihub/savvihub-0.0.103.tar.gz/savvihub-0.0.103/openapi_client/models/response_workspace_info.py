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


class ResponseWorkspaceInfo(object):
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
        'default_kernel_cluster': 'ModelKernelCluster',
        'default_kernel_cluster_id': 'int',
        'default_region': 'str',
        'default_storage_id': 'int',
        'default_volume_id': 'int',
        'description': 'str',
        'display_name': 'str',
        'id': 'int',
        'immutable_slug': 'str',
        'is_public': 'bool',
        'name': 'str',
        'primary_owner_id': 'int',
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
        'default_kernel_cluster': 'default_kernel_cluster',
        'default_kernel_cluster_id': 'default_kernel_cluster_id',
        'default_region': 'default_region',
        'default_storage_id': 'default_storage_id',
        'default_volume_id': 'default_volume_id',
        'description': 'description',
        'display_name': 'display_name',
        'id': 'id',
        'immutable_slug': 'immutable_slug',
        'is_public': 'is_public',
        'name': 'name',
        'primary_owner_id': 'primary_owner_id',
        'updated_dt': 'updated_dt',
        'workspace_default_kernel_cluster': 'workspace_default_kernel_cluster',
        'workspace_default_storage': 'workspace_default_storage',
        'workspace_default_volume': 'workspace_default_volume',
        'workspace_primary_owner': 'workspace_primary_owner'
    }

    def __init__(self, aws_external_id=None, created_dt=None, credit_balance=None, default_kernel_cluster=None, default_kernel_cluster_id=None, default_region=None, default_storage_id=None, default_volume_id=None, description=None, display_name=None, id=None, immutable_slug=None, is_public=None, name=None, primary_owner_id=None, updated_dt=None, workspace_default_kernel_cluster=None, workspace_default_storage=None, workspace_default_volume=None, workspace_primary_owner=None, local_vars_configuration=None):  # noqa: E501
        """ResponseWorkspaceInfo - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._aws_external_id = None
        self._created_dt = None
        self._credit_balance = None
        self._default_kernel_cluster = None
        self._default_kernel_cluster_id = None
        self._default_region = None
        self._default_storage_id = None
        self._default_volume_id = None
        self._description = None
        self._display_name = None
        self._id = None
        self._immutable_slug = None
        self._is_public = None
        self._name = None
        self._primary_owner_id = None
        self._updated_dt = None
        self._workspace_default_kernel_cluster = None
        self._workspace_default_storage = None
        self._workspace_default_volume = None
        self._workspace_primary_owner = None
        self.discriminator = None

        self.aws_external_id = aws_external_id
        self.created_dt = created_dt
        self.credit_balance = credit_balance
        if default_kernel_cluster is not None:
            self.default_kernel_cluster = default_kernel_cluster
        self.default_kernel_cluster_id = default_kernel_cluster_id
        self.default_region = default_region
        self.default_storage_id = default_storage_id
        self.default_volume_id = default_volume_id
        self.description = description
        self.display_name = display_name
        self.id = id
        self.immutable_slug = immutable_slug
        self.is_public = is_public
        self.name = name
        self.primary_owner_id = primary_owner_id
        self.updated_dt = updated_dt
        self.workspace_default_kernel_cluster = workspace_default_kernel_cluster
        self.workspace_default_storage = workspace_default_storage
        self.workspace_default_volume = workspace_default_volume
        self.workspace_primary_owner = workspace_primary_owner

    @property
    def aws_external_id(self):
        """Gets the aws_external_id of this ResponseWorkspaceInfo.  # noqa: E501


        :return: The aws_external_id of this ResponseWorkspaceInfo.  # noqa: E501
        :rtype: str
        """
        return self._aws_external_id

    @aws_external_id.setter
    def aws_external_id(self, aws_external_id):
        """Sets the aws_external_id of this ResponseWorkspaceInfo.


        :param aws_external_id: The aws_external_id of this ResponseWorkspaceInfo.  # noqa: E501
        :type aws_external_id: str
        """
        if self.local_vars_configuration.client_side_validation and aws_external_id is None:  # noqa: E501
            raise ValueError("Invalid value for `aws_external_id`, must not be `None`")  # noqa: E501

        self._aws_external_id = aws_external_id

    @property
    def created_dt(self):
        """Gets the created_dt of this ResponseWorkspaceInfo.  # noqa: E501


        :return: The created_dt of this ResponseWorkspaceInfo.  # noqa: E501
        :rtype: datetime
        """
        return self._created_dt

    @created_dt.setter
    def created_dt(self, created_dt):
        """Sets the created_dt of this ResponseWorkspaceInfo.


        :param created_dt: The created_dt of this ResponseWorkspaceInfo.  # noqa: E501
        :type created_dt: datetime
        """

        self._created_dt = created_dt

    @property
    def credit_balance(self):
        """Gets the credit_balance of this ResponseWorkspaceInfo.  # noqa: E501


        :return: The credit_balance of this ResponseWorkspaceInfo.  # noqa: E501
        :rtype: float
        """
        return self._credit_balance

    @credit_balance.setter
    def credit_balance(self, credit_balance):
        """Sets the credit_balance of this ResponseWorkspaceInfo.


        :param credit_balance: The credit_balance of this ResponseWorkspaceInfo.  # noqa: E501
        :type credit_balance: float
        """
        if self.local_vars_configuration.client_side_validation and credit_balance is None:  # noqa: E501
            raise ValueError("Invalid value for `credit_balance`, must not be `None`")  # noqa: E501

        self._credit_balance = credit_balance

    @property
    def default_kernel_cluster(self):
        """Gets the default_kernel_cluster of this ResponseWorkspaceInfo.  # noqa: E501


        :return: The default_kernel_cluster of this ResponseWorkspaceInfo.  # noqa: E501
        :rtype: ModelKernelCluster
        """
        return self._default_kernel_cluster

    @default_kernel_cluster.setter
    def default_kernel_cluster(self, default_kernel_cluster):
        """Sets the default_kernel_cluster of this ResponseWorkspaceInfo.


        :param default_kernel_cluster: The default_kernel_cluster of this ResponseWorkspaceInfo.  # noqa: E501
        :type default_kernel_cluster: ModelKernelCluster
        """

        self._default_kernel_cluster = default_kernel_cluster

    @property
    def default_kernel_cluster_id(self):
        """Gets the default_kernel_cluster_id of this ResponseWorkspaceInfo.  # noqa: E501


        :return: The default_kernel_cluster_id of this ResponseWorkspaceInfo.  # noqa: E501
        :rtype: int
        """
        return self._default_kernel_cluster_id

    @default_kernel_cluster_id.setter
    def default_kernel_cluster_id(self, default_kernel_cluster_id):
        """Sets the default_kernel_cluster_id of this ResponseWorkspaceInfo.


        :param default_kernel_cluster_id: The default_kernel_cluster_id of this ResponseWorkspaceInfo.  # noqa: E501
        :type default_kernel_cluster_id: int
        """

        self._default_kernel_cluster_id = default_kernel_cluster_id

    @property
    def default_region(self):
        """Gets the default_region of this ResponseWorkspaceInfo.  # noqa: E501


        :return: The default_region of this ResponseWorkspaceInfo.  # noqa: E501
        :rtype: str
        """
        return self._default_region

    @default_region.setter
    def default_region(self, default_region):
        """Sets the default_region of this ResponseWorkspaceInfo.


        :param default_region: The default_region of this ResponseWorkspaceInfo.  # noqa: E501
        :type default_region: str
        """
        if self.local_vars_configuration.client_side_validation and default_region is None:  # noqa: E501
            raise ValueError("Invalid value for `default_region`, must not be `None`")  # noqa: E501

        self._default_region = default_region

    @property
    def default_storage_id(self):
        """Gets the default_storage_id of this ResponseWorkspaceInfo.  # noqa: E501


        :return: The default_storage_id of this ResponseWorkspaceInfo.  # noqa: E501
        :rtype: int
        """
        return self._default_storage_id

    @default_storage_id.setter
    def default_storage_id(self, default_storage_id):
        """Sets the default_storage_id of this ResponseWorkspaceInfo.


        :param default_storage_id: The default_storage_id of this ResponseWorkspaceInfo.  # noqa: E501
        :type default_storage_id: int
        """

        self._default_storage_id = default_storage_id

    @property
    def default_volume_id(self):
        """Gets the default_volume_id of this ResponseWorkspaceInfo.  # noqa: E501


        :return: The default_volume_id of this ResponseWorkspaceInfo.  # noqa: E501
        :rtype: int
        """
        return self._default_volume_id

    @default_volume_id.setter
    def default_volume_id(self, default_volume_id):
        """Sets the default_volume_id of this ResponseWorkspaceInfo.


        :param default_volume_id: The default_volume_id of this ResponseWorkspaceInfo.  # noqa: E501
        :type default_volume_id: int
        """

        self._default_volume_id = default_volume_id

    @property
    def description(self):
        """Gets the description of this ResponseWorkspaceInfo.  # noqa: E501


        :return: The description of this ResponseWorkspaceInfo.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ResponseWorkspaceInfo.


        :param description: The description of this ResponseWorkspaceInfo.  # noqa: E501
        :type description: str
        """

        self._description = description

    @property
    def display_name(self):
        """Gets the display_name of this ResponseWorkspaceInfo.  # noqa: E501


        :return: The display_name of this ResponseWorkspaceInfo.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this ResponseWorkspaceInfo.


        :param display_name: The display_name of this ResponseWorkspaceInfo.  # noqa: E501
        :type display_name: str
        """
        if self.local_vars_configuration.client_side_validation and display_name is None:  # noqa: E501
            raise ValueError("Invalid value for `display_name`, must not be `None`")  # noqa: E501

        self._display_name = display_name

    @property
    def id(self):
        """Gets the id of this ResponseWorkspaceInfo.  # noqa: E501


        :return: The id of this ResponseWorkspaceInfo.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ResponseWorkspaceInfo.


        :param id: The id of this ResponseWorkspaceInfo.  # noqa: E501
        :type id: int
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def immutable_slug(self):
        """Gets the immutable_slug of this ResponseWorkspaceInfo.  # noqa: E501


        :return: The immutable_slug of this ResponseWorkspaceInfo.  # noqa: E501
        :rtype: str
        """
        return self._immutable_slug

    @immutable_slug.setter
    def immutable_slug(self, immutable_slug):
        """Sets the immutable_slug of this ResponseWorkspaceInfo.


        :param immutable_slug: The immutable_slug of this ResponseWorkspaceInfo.  # noqa: E501
        :type immutable_slug: str
        """
        if self.local_vars_configuration.client_side_validation and immutable_slug is None:  # noqa: E501
            raise ValueError("Invalid value for `immutable_slug`, must not be `None`")  # noqa: E501

        self._immutable_slug = immutable_slug

    @property
    def is_public(self):
        """Gets the is_public of this ResponseWorkspaceInfo.  # noqa: E501


        :return: The is_public of this ResponseWorkspaceInfo.  # noqa: E501
        :rtype: bool
        """
        return self._is_public

    @is_public.setter
    def is_public(self, is_public):
        """Sets the is_public of this ResponseWorkspaceInfo.


        :param is_public: The is_public of this ResponseWorkspaceInfo.  # noqa: E501
        :type is_public: bool
        """
        if self.local_vars_configuration.client_side_validation and is_public is None:  # noqa: E501
            raise ValueError("Invalid value for `is_public`, must not be `None`")  # noqa: E501

        self._is_public = is_public

    @property
    def name(self):
        """Gets the name of this ResponseWorkspaceInfo.  # noqa: E501


        :return: The name of this ResponseWorkspaceInfo.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ResponseWorkspaceInfo.


        :param name: The name of this ResponseWorkspaceInfo.  # noqa: E501
        :type name: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def primary_owner_id(self):
        """Gets the primary_owner_id of this ResponseWorkspaceInfo.  # noqa: E501


        :return: The primary_owner_id of this ResponseWorkspaceInfo.  # noqa: E501
        :rtype: int
        """
        return self._primary_owner_id

    @primary_owner_id.setter
    def primary_owner_id(self, primary_owner_id):
        """Sets the primary_owner_id of this ResponseWorkspaceInfo.


        :param primary_owner_id: The primary_owner_id of this ResponseWorkspaceInfo.  # noqa: E501
        :type primary_owner_id: int
        """
        if self.local_vars_configuration.client_side_validation and primary_owner_id is None:  # noqa: E501
            raise ValueError("Invalid value for `primary_owner_id`, must not be `None`")  # noqa: E501

        self._primary_owner_id = primary_owner_id

    @property
    def updated_dt(self):
        """Gets the updated_dt of this ResponseWorkspaceInfo.  # noqa: E501


        :return: The updated_dt of this ResponseWorkspaceInfo.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_dt

    @updated_dt.setter
    def updated_dt(self, updated_dt):
        """Sets the updated_dt of this ResponseWorkspaceInfo.


        :param updated_dt: The updated_dt of this ResponseWorkspaceInfo.  # noqa: E501
        :type updated_dt: datetime
        """

        self._updated_dt = updated_dt

    @property
    def workspace_default_kernel_cluster(self):
        """Gets the workspace_default_kernel_cluster of this ResponseWorkspaceInfo.  # noqa: E501


        :return: The workspace_default_kernel_cluster of this ResponseWorkspaceInfo.  # noqa: E501
        :rtype: int
        """
        return self._workspace_default_kernel_cluster

    @workspace_default_kernel_cluster.setter
    def workspace_default_kernel_cluster(self, workspace_default_kernel_cluster):
        """Sets the workspace_default_kernel_cluster of this ResponseWorkspaceInfo.


        :param workspace_default_kernel_cluster: The workspace_default_kernel_cluster of this ResponseWorkspaceInfo.  # noqa: E501
        :type workspace_default_kernel_cluster: int
        """

        self._workspace_default_kernel_cluster = workspace_default_kernel_cluster

    @property
    def workspace_default_storage(self):
        """Gets the workspace_default_storage of this ResponseWorkspaceInfo.  # noqa: E501


        :return: The workspace_default_storage of this ResponseWorkspaceInfo.  # noqa: E501
        :rtype: int
        """
        return self._workspace_default_storage

    @workspace_default_storage.setter
    def workspace_default_storage(self, workspace_default_storage):
        """Sets the workspace_default_storage of this ResponseWorkspaceInfo.


        :param workspace_default_storage: The workspace_default_storage of this ResponseWorkspaceInfo.  # noqa: E501
        :type workspace_default_storage: int
        """

        self._workspace_default_storage = workspace_default_storage

    @property
    def workspace_default_volume(self):
        """Gets the workspace_default_volume of this ResponseWorkspaceInfo.  # noqa: E501


        :return: The workspace_default_volume of this ResponseWorkspaceInfo.  # noqa: E501
        :rtype: int
        """
        return self._workspace_default_volume

    @workspace_default_volume.setter
    def workspace_default_volume(self, workspace_default_volume):
        """Sets the workspace_default_volume of this ResponseWorkspaceInfo.


        :param workspace_default_volume: The workspace_default_volume of this ResponseWorkspaceInfo.  # noqa: E501
        :type workspace_default_volume: int
        """

        self._workspace_default_volume = workspace_default_volume

    @property
    def workspace_primary_owner(self):
        """Gets the workspace_primary_owner of this ResponseWorkspaceInfo.  # noqa: E501


        :return: The workspace_primary_owner of this ResponseWorkspaceInfo.  # noqa: E501
        :rtype: int
        """
        return self._workspace_primary_owner

    @workspace_primary_owner.setter
    def workspace_primary_owner(self, workspace_primary_owner):
        """Sets the workspace_primary_owner of this ResponseWorkspaceInfo.


        :param workspace_primary_owner: The workspace_primary_owner of this ResponseWorkspaceInfo.  # noqa: E501
        :type workspace_primary_owner: int
        """
        if self.local_vars_configuration.client_side_validation and workspace_primary_owner is None:  # noqa: E501
            raise ValueError("Invalid value for `workspace_primary_owner`, must not be `None`")  # noqa: E501

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
        if not isinstance(other, ResponseWorkspaceInfo):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ResponseWorkspaceInfo):
            return True

        return self.to_dict() != other.to_dict()
