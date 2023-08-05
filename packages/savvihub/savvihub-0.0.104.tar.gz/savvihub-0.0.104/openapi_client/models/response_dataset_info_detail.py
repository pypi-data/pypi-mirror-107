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


class ResponseDatasetInfoDetail(object):
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
        'description': 'str',
        'file_count': 'int',
        'id': 'int',
        'immutable_slug': 'str',
        'is_public': 'bool',
        'is_read_only': 'bool',
        'is_support_snapshot': 'bool',
        'name': 'str',
        'size': 'int',
        'source': 'ResponseDatasetSource',
        'status': 'str',
        'summary': 'ResponseDatasetSummary',
        'updated_dt': 'datetime',
        'volume_id': 'int',
        'workspace': 'ResponseWorkspace',
        'workspace_id': 'int'
    }

    attribute_map = {
        'created_dt': 'created_dt',
        'description': 'description',
        'file_count': 'file_count',
        'id': 'id',
        'immutable_slug': 'immutable_slug',
        'is_public': 'is_public',
        'is_read_only': 'is_read_only',
        'is_support_snapshot': 'is_support_snapshot',
        'name': 'name',
        'size': 'size',
        'source': 'source',
        'status': 'status',
        'summary': 'summary',
        'updated_dt': 'updated_dt',
        'volume_id': 'volume_id',
        'workspace': 'workspace',
        'workspace_id': 'workspace_id'
    }

    def __init__(self, created_dt=None, description=None, file_count=None, id=None, immutable_slug=None, is_public=None, is_read_only=None, is_support_snapshot=None, name=None, size=None, source=None, status=None, summary=None, updated_dt=None, volume_id=None, workspace=None, workspace_id=None, local_vars_configuration=None):  # noqa: E501
        """ResponseDatasetInfoDetail - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._created_dt = None
        self._description = None
        self._file_count = None
        self._id = None
        self._immutable_slug = None
        self._is_public = None
        self._is_read_only = None
        self._is_support_snapshot = None
        self._name = None
        self._size = None
        self._source = None
        self._status = None
        self._summary = None
        self._updated_dt = None
        self._volume_id = None
        self._workspace = None
        self._workspace_id = None
        self.discriminator = None

        self.created_dt = created_dt
        self.description = description
        self.file_count = file_count
        self.id = id
        self.immutable_slug = immutable_slug
        self.is_public = is_public
        self.is_read_only = is_read_only
        self.is_support_snapshot = is_support_snapshot
        self.name = name
        self.size = size
        self.source = source
        self.status = status
        if summary is not None:
            self.summary = summary
        self.updated_dt = updated_dt
        self.volume_id = volume_id
        self.workspace = workspace
        self.workspace_id = workspace_id

    @property
    def created_dt(self):
        """Gets the created_dt of this ResponseDatasetInfoDetail.  # noqa: E501


        :return: The created_dt of this ResponseDatasetInfoDetail.  # noqa: E501
        :rtype: datetime
        """
        return self._created_dt

    @created_dt.setter
    def created_dt(self, created_dt):
        """Sets the created_dt of this ResponseDatasetInfoDetail.


        :param created_dt: The created_dt of this ResponseDatasetInfoDetail.  # noqa: E501
        :type created_dt: datetime
        """

        self._created_dt = created_dt

    @property
    def description(self):
        """Gets the description of this ResponseDatasetInfoDetail.  # noqa: E501


        :return: The description of this ResponseDatasetInfoDetail.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ResponseDatasetInfoDetail.


        :param description: The description of this ResponseDatasetInfoDetail.  # noqa: E501
        :type description: str
        """

        self._description = description

    @property
    def file_count(self):
        """Gets the file_count of this ResponseDatasetInfoDetail.  # noqa: E501


        :return: The file_count of this ResponseDatasetInfoDetail.  # noqa: E501
        :rtype: int
        """
        return self._file_count

    @file_count.setter
    def file_count(self, file_count):
        """Sets the file_count of this ResponseDatasetInfoDetail.


        :param file_count: The file_count of this ResponseDatasetInfoDetail.  # noqa: E501
        :type file_count: int
        """
        if self.local_vars_configuration.client_side_validation and file_count is None:  # noqa: E501
            raise ValueError("Invalid value for `file_count`, must not be `None`")  # noqa: E501

        self._file_count = file_count

    @property
    def id(self):
        """Gets the id of this ResponseDatasetInfoDetail.  # noqa: E501


        :return: The id of this ResponseDatasetInfoDetail.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ResponseDatasetInfoDetail.


        :param id: The id of this ResponseDatasetInfoDetail.  # noqa: E501
        :type id: int
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def immutable_slug(self):
        """Gets the immutable_slug of this ResponseDatasetInfoDetail.  # noqa: E501


        :return: The immutable_slug of this ResponseDatasetInfoDetail.  # noqa: E501
        :rtype: str
        """
        return self._immutable_slug

    @immutable_slug.setter
    def immutable_slug(self, immutable_slug):
        """Sets the immutable_slug of this ResponseDatasetInfoDetail.


        :param immutable_slug: The immutable_slug of this ResponseDatasetInfoDetail.  # noqa: E501
        :type immutable_slug: str
        """
        if self.local_vars_configuration.client_side_validation and immutable_slug is None:  # noqa: E501
            raise ValueError("Invalid value for `immutable_slug`, must not be `None`")  # noqa: E501

        self._immutable_slug = immutable_slug

    @property
    def is_public(self):
        """Gets the is_public of this ResponseDatasetInfoDetail.  # noqa: E501


        :return: The is_public of this ResponseDatasetInfoDetail.  # noqa: E501
        :rtype: bool
        """
        return self._is_public

    @is_public.setter
    def is_public(self, is_public):
        """Sets the is_public of this ResponseDatasetInfoDetail.


        :param is_public: The is_public of this ResponseDatasetInfoDetail.  # noqa: E501
        :type is_public: bool
        """
        if self.local_vars_configuration.client_side_validation and is_public is None:  # noqa: E501
            raise ValueError("Invalid value for `is_public`, must not be `None`")  # noqa: E501

        self._is_public = is_public

    @property
    def is_read_only(self):
        """Gets the is_read_only of this ResponseDatasetInfoDetail.  # noqa: E501


        :return: The is_read_only of this ResponseDatasetInfoDetail.  # noqa: E501
        :rtype: bool
        """
        return self._is_read_only

    @is_read_only.setter
    def is_read_only(self, is_read_only):
        """Sets the is_read_only of this ResponseDatasetInfoDetail.


        :param is_read_only: The is_read_only of this ResponseDatasetInfoDetail.  # noqa: E501
        :type is_read_only: bool
        """
        if self.local_vars_configuration.client_side_validation and is_read_only is None:  # noqa: E501
            raise ValueError("Invalid value for `is_read_only`, must not be `None`")  # noqa: E501

        self._is_read_only = is_read_only

    @property
    def is_support_snapshot(self):
        """Gets the is_support_snapshot of this ResponseDatasetInfoDetail.  # noqa: E501


        :return: The is_support_snapshot of this ResponseDatasetInfoDetail.  # noqa: E501
        :rtype: bool
        """
        return self._is_support_snapshot

    @is_support_snapshot.setter
    def is_support_snapshot(self, is_support_snapshot):
        """Sets the is_support_snapshot of this ResponseDatasetInfoDetail.


        :param is_support_snapshot: The is_support_snapshot of this ResponseDatasetInfoDetail.  # noqa: E501
        :type is_support_snapshot: bool
        """
        if self.local_vars_configuration.client_side_validation and is_support_snapshot is None:  # noqa: E501
            raise ValueError("Invalid value for `is_support_snapshot`, must not be `None`")  # noqa: E501

        self._is_support_snapshot = is_support_snapshot

    @property
    def name(self):
        """Gets the name of this ResponseDatasetInfoDetail.  # noqa: E501


        :return: The name of this ResponseDatasetInfoDetail.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ResponseDatasetInfoDetail.


        :param name: The name of this ResponseDatasetInfoDetail.  # noqa: E501
        :type name: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def size(self):
        """Gets the size of this ResponseDatasetInfoDetail.  # noqa: E501


        :return: The size of this ResponseDatasetInfoDetail.  # noqa: E501
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """Sets the size of this ResponseDatasetInfoDetail.


        :param size: The size of this ResponseDatasetInfoDetail.  # noqa: E501
        :type size: int
        """
        if self.local_vars_configuration.client_side_validation and size is None:  # noqa: E501
            raise ValueError("Invalid value for `size`, must not be `None`")  # noqa: E501

        self._size = size

    @property
    def source(self):
        """Gets the source of this ResponseDatasetInfoDetail.  # noqa: E501


        :return: The source of this ResponseDatasetInfoDetail.  # noqa: E501
        :rtype: ResponseDatasetSource
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this ResponseDatasetInfoDetail.


        :param source: The source of this ResponseDatasetInfoDetail.  # noqa: E501
        :type source: ResponseDatasetSource
        """
        if self.local_vars_configuration.client_side_validation and source is None:  # noqa: E501
            raise ValueError("Invalid value for `source`, must not be `None`")  # noqa: E501

        self._source = source

    @property
    def status(self):
        """Gets the status of this ResponseDatasetInfoDetail.  # noqa: E501


        :return: The status of this ResponseDatasetInfoDetail.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this ResponseDatasetInfoDetail.


        :param status: The status of this ResponseDatasetInfoDetail.  # noqa: E501
        :type status: str
        """
        if self.local_vars_configuration.client_side_validation and status is None:  # noqa: E501
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def summary(self):
        """Gets the summary of this ResponseDatasetInfoDetail.  # noqa: E501


        :return: The summary of this ResponseDatasetInfoDetail.  # noqa: E501
        :rtype: ResponseDatasetSummary
        """
        return self._summary

    @summary.setter
    def summary(self, summary):
        """Sets the summary of this ResponseDatasetInfoDetail.


        :param summary: The summary of this ResponseDatasetInfoDetail.  # noqa: E501
        :type summary: ResponseDatasetSummary
        """

        self._summary = summary

    @property
    def updated_dt(self):
        """Gets the updated_dt of this ResponseDatasetInfoDetail.  # noqa: E501


        :return: The updated_dt of this ResponseDatasetInfoDetail.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_dt

    @updated_dt.setter
    def updated_dt(self, updated_dt):
        """Sets the updated_dt of this ResponseDatasetInfoDetail.


        :param updated_dt: The updated_dt of this ResponseDatasetInfoDetail.  # noqa: E501
        :type updated_dt: datetime
        """

        self._updated_dt = updated_dt

    @property
    def volume_id(self):
        """Gets the volume_id of this ResponseDatasetInfoDetail.  # noqa: E501


        :return: The volume_id of this ResponseDatasetInfoDetail.  # noqa: E501
        :rtype: int
        """
        return self._volume_id

    @volume_id.setter
    def volume_id(self, volume_id):
        """Sets the volume_id of this ResponseDatasetInfoDetail.


        :param volume_id: The volume_id of this ResponseDatasetInfoDetail.  # noqa: E501
        :type volume_id: int
        """
        if self.local_vars_configuration.client_side_validation and volume_id is None:  # noqa: E501
            raise ValueError("Invalid value for `volume_id`, must not be `None`")  # noqa: E501

        self._volume_id = volume_id

    @property
    def workspace(self):
        """Gets the workspace of this ResponseDatasetInfoDetail.  # noqa: E501


        :return: The workspace of this ResponseDatasetInfoDetail.  # noqa: E501
        :rtype: ResponseWorkspace
        """
        return self._workspace

    @workspace.setter
    def workspace(self, workspace):
        """Sets the workspace of this ResponseDatasetInfoDetail.


        :param workspace: The workspace of this ResponseDatasetInfoDetail.  # noqa: E501
        :type workspace: ResponseWorkspace
        """
        if self.local_vars_configuration.client_side_validation and workspace is None:  # noqa: E501
            raise ValueError("Invalid value for `workspace`, must not be `None`")  # noqa: E501

        self._workspace = workspace

    @property
    def workspace_id(self):
        """Gets the workspace_id of this ResponseDatasetInfoDetail.  # noqa: E501


        :return: The workspace_id of this ResponseDatasetInfoDetail.  # noqa: E501
        :rtype: int
        """
        return self._workspace_id

    @workspace_id.setter
    def workspace_id(self, workspace_id):
        """Sets the workspace_id of this ResponseDatasetInfoDetail.


        :param workspace_id: The workspace_id of this ResponseDatasetInfoDetail.  # noqa: E501
        :type workspace_id: int
        """
        if self.local_vars_configuration.client_side_validation and workspace_id is None:  # noqa: E501
            raise ValueError("Invalid value for `workspace_id`, must not be `None`")  # noqa: E501

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
        if not isinstance(other, ResponseDatasetInfoDetail):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ResponseDatasetInfoDetail):
            return True

        return self.to_dict() != other.to_dict()
