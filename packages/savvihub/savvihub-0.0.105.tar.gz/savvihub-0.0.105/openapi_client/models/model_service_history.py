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


class ModelServiceHistory(object):
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
        'edges': 'ModelServiceHistoryEdges',
        'id': 'int',
        'immutable_slug': 'str',
        'message': 'str',
        'service_history_service': 'int',
        'status': 'str',
        'updated_dt': 'datetime'
    }

    attribute_map = {
        'created_dt': 'created_dt',
        'edges': 'edges',
        'id': 'id',
        'immutable_slug': 'immutable_slug',
        'message': 'message',
        'service_history_service': 'service_history_service',
        'status': 'status',
        'updated_dt': 'updated_dt'
    }

    def __init__(self, created_dt=None, edges=None, id=None, immutable_slug=None, message=None, service_history_service=None, status=None, updated_dt=None, local_vars_configuration=None):  # noqa: E501
        """ModelServiceHistory - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._created_dt = None
        self._edges = None
        self._id = None
        self._immutable_slug = None
        self._message = None
        self._service_history_service = None
        self._status = None
        self._updated_dt = None
        self.discriminator = None

        self.created_dt = created_dt
        if edges is not None:
            self.edges = edges
        if id is not None:
            self.id = id
        if immutable_slug is not None:
            self.immutable_slug = immutable_slug
        if message is not None:
            self.message = message
        if service_history_service is not None:
            self.service_history_service = service_history_service
        if status is not None:
            self.status = status
        self.updated_dt = updated_dt

    @property
    def created_dt(self):
        """Gets the created_dt of this ModelServiceHistory.  # noqa: E501


        :return: The created_dt of this ModelServiceHistory.  # noqa: E501
        :rtype: datetime
        """
        return self._created_dt

    @created_dt.setter
    def created_dt(self, created_dt):
        """Sets the created_dt of this ModelServiceHistory.


        :param created_dt: The created_dt of this ModelServiceHistory.  # noqa: E501
        :type created_dt: datetime
        """

        self._created_dt = created_dt

    @property
    def edges(self):
        """Gets the edges of this ModelServiceHistory.  # noqa: E501


        :return: The edges of this ModelServiceHistory.  # noqa: E501
        :rtype: ModelServiceHistoryEdges
        """
        return self._edges

    @edges.setter
    def edges(self, edges):
        """Sets the edges of this ModelServiceHistory.


        :param edges: The edges of this ModelServiceHistory.  # noqa: E501
        :type edges: ModelServiceHistoryEdges
        """

        self._edges = edges

    @property
    def id(self):
        """Gets the id of this ModelServiceHistory.  # noqa: E501


        :return: The id of this ModelServiceHistory.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ModelServiceHistory.


        :param id: The id of this ModelServiceHistory.  # noqa: E501
        :type id: int
        """

        self._id = id

    @property
    def immutable_slug(self):
        """Gets the immutable_slug of this ModelServiceHistory.  # noqa: E501


        :return: The immutable_slug of this ModelServiceHistory.  # noqa: E501
        :rtype: str
        """
        return self._immutable_slug

    @immutable_slug.setter
    def immutable_slug(self, immutable_slug):
        """Sets the immutable_slug of this ModelServiceHistory.


        :param immutable_slug: The immutable_slug of this ModelServiceHistory.  # noqa: E501
        :type immutable_slug: str
        """

        self._immutable_slug = immutable_slug

    @property
    def message(self):
        """Gets the message of this ModelServiceHistory.  # noqa: E501


        :return: The message of this ModelServiceHistory.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this ModelServiceHistory.


        :param message: The message of this ModelServiceHistory.  # noqa: E501
        :type message: str
        """

        self._message = message

    @property
    def service_history_service(self):
        """Gets the service_history_service of this ModelServiceHistory.  # noqa: E501


        :return: The service_history_service of this ModelServiceHistory.  # noqa: E501
        :rtype: int
        """
        return self._service_history_service

    @service_history_service.setter
    def service_history_service(self, service_history_service):
        """Sets the service_history_service of this ModelServiceHistory.


        :param service_history_service: The service_history_service of this ModelServiceHistory.  # noqa: E501
        :type service_history_service: int
        """

        self._service_history_service = service_history_service

    @property
    def status(self):
        """Gets the status of this ModelServiceHistory.  # noqa: E501


        :return: The status of this ModelServiceHistory.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this ModelServiceHistory.


        :param status: The status of this ModelServiceHistory.  # noqa: E501
        :type status: str
        """

        self._status = status

    @property
    def updated_dt(self):
        """Gets the updated_dt of this ModelServiceHistory.  # noqa: E501


        :return: The updated_dt of this ModelServiceHistory.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_dt

    @updated_dt.setter
    def updated_dt(self, updated_dt):
        """Sets the updated_dt of this ModelServiceHistory.


        :param updated_dt: The updated_dt of this ModelServiceHistory.  # noqa: E501
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
        if not isinstance(other, ModelServiceHistory):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ModelServiceHistory):
            return True

        return self.to_dict() != other.to_dict()
