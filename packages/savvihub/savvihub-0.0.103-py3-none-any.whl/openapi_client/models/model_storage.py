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


class ModelStorage(object):
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
        'base_path': 'str',
        'bucket_name': 'str',
        'capacity_limit': 'str',
        'created_dt': 'datetime',
        'credentials': 'dict(str, object)',
        'edges': 'ModelStorageEdges',
        'id': 'int',
        'immutable_slug': 'str',
        'minio_endpoint': 'str',
        'name': 'str',
        'nfs_host': 'str',
        'region': 'str',
        'source_type': 'str',
        'storage_workspace': 'int',
        'updated_dt': 'datetime'
    }

    attribute_map = {
        'base_path': 'base_path',
        'bucket_name': 'bucket_name',
        'capacity_limit': 'capacity_limit',
        'created_dt': 'created_dt',
        'credentials': 'credentials',
        'edges': 'edges',
        'id': 'id',
        'immutable_slug': 'immutable_slug',
        'minio_endpoint': 'minio_endpoint',
        'name': 'name',
        'nfs_host': 'nfs_host',
        'region': 'region',
        'source_type': 'source_type',
        'storage_workspace': 'storage_workspace',
        'updated_dt': 'updated_dt'
    }

    def __init__(self, base_path=None, bucket_name=None, capacity_limit=None, created_dt=None, credentials=None, edges=None, id=None, immutable_slug=None, minio_endpoint=None, name=None, nfs_host=None, region=None, source_type=None, storage_workspace=None, updated_dt=None, local_vars_configuration=None):  # noqa: E501
        """ModelStorage - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._base_path = None
        self._bucket_name = None
        self._capacity_limit = None
        self._created_dt = None
        self._credentials = None
        self._edges = None
        self._id = None
        self._immutable_slug = None
        self._minio_endpoint = None
        self._name = None
        self._nfs_host = None
        self._region = None
        self._source_type = None
        self._storage_workspace = None
        self._updated_dt = None
        self.discriminator = None

        if base_path is not None:
            self.base_path = base_path
        if bucket_name is not None:
            self.bucket_name = bucket_name
        self.capacity_limit = capacity_limit
        self.created_dt = created_dt
        if credentials is not None:
            self.credentials = credentials
        if edges is not None:
            self.edges = edges
        if id is not None:
            self.id = id
        if immutable_slug is not None:
            self.immutable_slug = immutable_slug
        self.minio_endpoint = minio_endpoint
        if name is not None:
            self.name = name
        self.nfs_host = nfs_host
        if region is not None:
            self.region = region
        if source_type is not None:
            self.source_type = source_type
        self.storage_workspace = storage_workspace
        self.updated_dt = updated_dt

    @property
    def base_path(self):
        """Gets the base_path of this ModelStorage.  # noqa: E501


        :return: The base_path of this ModelStorage.  # noqa: E501
        :rtype: str
        """
        return self._base_path

    @base_path.setter
    def base_path(self, base_path):
        """Sets the base_path of this ModelStorage.


        :param base_path: The base_path of this ModelStorage.  # noqa: E501
        :type base_path: str
        """

        self._base_path = base_path

    @property
    def bucket_name(self):
        """Gets the bucket_name of this ModelStorage.  # noqa: E501


        :return: The bucket_name of this ModelStorage.  # noqa: E501
        :rtype: str
        """
        return self._bucket_name

    @bucket_name.setter
    def bucket_name(self, bucket_name):
        """Sets the bucket_name of this ModelStorage.


        :param bucket_name: The bucket_name of this ModelStorage.  # noqa: E501
        :type bucket_name: str
        """

        self._bucket_name = bucket_name

    @property
    def capacity_limit(self):
        """Gets the capacity_limit of this ModelStorage.  # noqa: E501


        :return: The capacity_limit of this ModelStorage.  # noqa: E501
        :rtype: str
        """
        return self._capacity_limit

    @capacity_limit.setter
    def capacity_limit(self, capacity_limit):
        """Sets the capacity_limit of this ModelStorage.


        :param capacity_limit: The capacity_limit of this ModelStorage.  # noqa: E501
        :type capacity_limit: str
        """

        self._capacity_limit = capacity_limit

    @property
    def created_dt(self):
        """Gets the created_dt of this ModelStorage.  # noqa: E501


        :return: The created_dt of this ModelStorage.  # noqa: E501
        :rtype: datetime
        """
        return self._created_dt

    @created_dt.setter
    def created_dt(self, created_dt):
        """Sets the created_dt of this ModelStorage.


        :param created_dt: The created_dt of this ModelStorage.  # noqa: E501
        :type created_dt: datetime
        """

        self._created_dt = created_dt

    @property
    def credentials(self):
        """Gets the credentials of this ModelStorage.  # noqa: E501


        :return: The credentials of this ModelStorage.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._credentials

    @credentials.setter
    def credentials(self, credentials):
        """Sets the credentials of this ModelStorage.


        :param credentials: The credentials of this ModelStorage.  # noqa: E501
        :type credentials: dict(str, object)
        """

        self._credentials = credentials

    @property
    def edges(self):
        """Gets the edges of this ModelStorage.  # noqa: E501


        :return: The edges of this ModelStorage.  # noqa: E501
        :rtype: ModelStorageEdges
        """
        return self._edges

    @edges.setter
    def edges(self, edges):
        """Sets the edges of this ModelStorage.


        :param edges: The edges of this ModelStorage.  # noqa: E501
        :type edges: ModelStorageEdges
        """

        self._edges = edges

    @property
    def id(self):
        """Gets the id of this ModelStorage.  # noqa: E501


        :return: The id of this ModelStorage.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ModelStorage.


        :param id: The id of this ModelStorage.  # noqa: E501
        :type id: int
        """

        self._id = id

    @property
    def immutable_slug(self):
        """Gets the immutable_slug of this ModelStorage.  # noqa: E501


        :return: The immutable_slug of this ModelStorage.  # noqa: E501
        :rtype: str
        """
        return self._immutable_slug

    @immutable_slug.setter
    def immutable_slug(self, immutable_slug):
        """Sets the immutable_slug of this ModelStorage.


        :param immutable_slug: The immutable_slug of this ModelStorage.  # noqa: E501
        :type immutable_slug: str
        """

        self._immutable_slug = immutable_slug

    @property
    def minio_endpoint(self):
        """Gets the minio_endpoint of this ModelStorage.  # noqa: E501


        :return: The minio_endpoint of this ModelStorage.  # noqa: E501
        :rtype: str
        """
        return self._minio_endpoint

    @minio_endpoint.setter
    def minio_endpoint(self, minio_endpoint):
        """Sets the minio_endpoint of this ModelStorage.


        :param minio_endpoint: The minio_endpoint of this ModelStorage.  # noqa: E501
        :type minio_endpoint: str
        """

        self._minio_endpoint = minio_endpoint

    @property
    def name(self):
        """Gets the name of this ModelStorage.  # noqa: E501


        :return: The name of this ModelStorage.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ModelStorage.


        :param name: The name of this ModelStorage.  # noqa: E501
        :type name: str
        """

        self._name = name

    @property
    def nfs_host(self):
        """Gets the nfs_host of this ModelStorage.  # noqa: E501


        :return: The nfs_host of this ModelStorage.  # noqa: E501
        :rtype: str
        """
        return self._nfs_host

    @nfs_host.setter
    def nfs_host(self, nfs_host):
        """Sets the nfs_host of this ModelStorage.


        :param nfs_host: The nfs_host of this ModelStorage.  # noqa: E501
        :type nfs_host: str
        """

        self._nfs_host = nfs_host

    @property
    def region(self):
        """Gets the region of this ModelStorage.  # noqa: E501


        :return: The region of this ModelStorage.  # noqa: E501
        :rtype: str
        """
        return self._region

    @region.setter
    def region(self, region):
        """Sets the region of this ModelStorage.


        :param region: The region of this ModelStorage.  # noqa: E501
        :type region: str
        """

        self._region = region

    @property
    def source_type(self):
        """Gets the source_type of this ModelStorage.  # noqa: E501


        :return: The source_type of this ModelStorage.  # noqa: E501
        :rtype: str
        """
        return self._source_type

    @source_type.setter
    def source_type(self, source_type):
        """Sets the source_type of this ModelStorage.


        :param source_type: The source_type of this ModelStorage.  # noqa: E501
        :type source_type: str
        """

        self._source_type = source_type

    @property
    def storage_workspace(self):
        """Gets the storage_workspace of this ModelStorage.  # noqa: E501


        :return: The storage_workspace of this ModelStorage.  # noqa: E501
        :rtype: int
        """
        return self._storage_workspace

    @storage_workspace.setter
    def storage_workspace(self, storage_workspace):
        """Sets the storage_workspace of this ModelStorage.


        :param storage_workspace: The storage_workspace of this ModelStorage.  # noqa: E501
        :type storage_workspace: int
        """

        self._storage_workspace = storage_workspace

    @property
    def updated_dt(self):
        """Gets the updated_dt of this ModelStorage.  # noqa: E501


        :return: The updated_dt of this ModelStorage.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_dt

    @updated_dt.setter
    def updated_dt(self, updated_dt):
        """Sets the updated_dt of this ModelStorage.


        :param updated_dt: The updated_dt of this ModelStorage.  # noqa: E501
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
        if not isinstance(other, ModelStorage):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ModelStorage):
            return True

        return self.to_dict() != other.to_dict()
