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


class ResponseKernelResourceSpec(object):
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
        'available': 'bool',
        'cpu_limit': 'float',
        'cpu_type': 'str',
        'created_dt': 'datetime',
        'description': 'str',
        'gpu_labels': 'ModelKernelResourceSpecGpuLabels',
        'gpu_limit': 'int',
        'gpu_type': 'str',
        'id': 'int',
        'immutable_slug': 'str',
        'memory_limit': 'str',
        'name': 'str',
        'processor_type': 'str',
        'spot': 'bool',
        'updated_dt': 'datetime'
    }

    attribute_map = {
        'available': 'available',
        'cpu_limit': 'cpu_limit',
        'cpu_type': 'cpu_type',
        'created_dt': 'created_dt',
        'description': 'description',
        'gpu_labels': 'gpu_labels',
        'gpu_limit': 'gpu_limit',
        'gpu_type': 'gpu_type',
        'id': 'id',
        'immutable_slug': 'immutable_slug',
        'memory_limit': 'memory_limit',
        'name': 'name',
        'processor_type': 'processor_type',
        'spot': 'spot',
        'updated_dt': 'updated_dt'
    }

    def __init__(self, available=None, cpu_limit=None, cpu_type=None, created_dt=None, description=None, gpu_labels=None, gpu_limit=None, gpu_type=None, id=None, immutable_slug=None, memory_limit=None, name=None, processor_type=None, spot=None, updated_dt=None, local_vars_configuration=None):  # noqa: E501
        """ResponseKernelResourceSpec - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._available = None
        self._cpu_limit = None
        self._cpu_type = None
        self._created_dt = None
        self._description = None
        self._gpu_labels = None
        self._gpu_limit = None
        self._gpu_type = None
        self._id = None
        self._immutable_slug = None
        self._memory_limit = None
        self._name = None
        self._processor_type = None
        self._spot = None
        self._updated_dt = None
        self.discriminator = None

        self.available = available
        self.cpu_limit = cpu_limit
        self.cpu_type = cpu_type
        self.created_dt = created_dt
        self.description = description
        if gpu_labels is not None:
            self.gpu_labels = gpu_labels
        self.gpu_limit = gpu_limit
        self.gpu_type = gpu_type
        self.id = id
        self.immutable_slug = immutable_slug
        self.memory_limit = memory_limit
        self.name = name
        self.processor_type = processor_type
        self.spot = spot
        self.updated_dt = updated_dt

    @property
    def available(self):
        """Gets the available of this ResponseKernelResourceSpec.  # noqa: E501


        :return: The available of this ResponseKernelResourceSpec.  # noqa: E501
        :rtype: bool
        """
        return self._available

    @available.setter
    def available(self, available):
        """Sets the available of this ResponseKernelResourceSpec.


        :param available: The available of this ResponseKernelResourceSpec.  # noqa: E501
        :type available: bool
        """
        if self.local_vars_configuration.client_side_validation and available is None:  # noqa: E501
            raise ValueError("Invalid value for `available`, must not be `None`")  # noqa: E501

        self._available = available

    @property
    def cpu_limit(self):
        """Gets the cpu_limit of this ResponseKernelResourceSpec.  # noqa: E501


        :return: The cpu_limit of this ResponseKernelResourceSpec.  # noqa: E501
        :rtype: float
        """
        return self._cpu_limit

    @cpu_limit.setter
    def cpu_limit(self, cpu_limit):
        """Sets the cpu_limit of this ResponseKernelResourceSpec.


        :param cpu_limit: The cpu_limit of this ResponseKernelResourceSpec.  # noqa: E501
        :type cpu_limit: float
        """
        if self.local_vars_configuration.client_side_validation and cpu_limit is None:  # noqa: E501
            raise ValueError("Invalid value for `cpu_limit`, must not be `None`")  # noqa: E501

        self._cpu_limit = cpu_limit

    @property
    def cpu_type(self):
        """Gets the cpu_type of this ResponseKernelResourceSpec.  # noqa: E501


        :return: The cpu_type of this ResponseKernelResourceSpec.  # noqa: E501
        :rtype: str
        """
        return self._cpu_type

    @cpu_type.setter
    def cpu_type(self, cpu_type):
        """Sets the cpu_type of this ResponseKernelResourceSpec.


        :param cpu_type: The cpu_type of this ResponseKernelResourceSpec.  # noqa: E501
        :type cpu_type: str
        """
        if self.local_vars_configuration.client_side_validation and cpu_type is None:  # noqa: E501
            raise ValueError("Invalid value for `cpu_type`, must not be `None`")  # noqa: E501

        self._cpu_type = cpu_type

    @property
    def created_dt(self):
        """Gets the created_dt of this ResponseKernelResourceSpec.  # noqa: E501


        :return: The created_dt of this ResponseKernelResourceSpec.  # noqa: E501
        :rtype: datetime
        """
        return self._created_dt

    @created_dt.setter
    def created_dt(self, created_dt):
        """Sets the created_dt of this ResponseKernelResourceSpec.


        :param created_dt: The created_dt of this ResponseKernelResourceSpec.  # noqa: E501
        :type created_dt: datetime
        """

        self._created_dt = created_dt

    @property
    def description(self):
        """Gets the description of this ResponseKernelResourceSpec.  # noqa: E501


        :return: The description of this ResponseKernelResourceSpec.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ResponseKernelResourceSpec.


        :param description: The description of this ResponseKernelResourceSpec.  # noqa: E501
        :type description: str
        """

        self._description = description

    @property
    def gpu_labels(self):
        """Gets the gpu_labels of this ResponseKernelResourceSpec.  # noqa: E501


        :return: The gpu_labels of this ResponseKernelResourceSpec.  # noqa: E501
        :rtype: ModelKernelResourceSpecGpuLabels
        """
        return self._gpu_labels

    @gpu_labels.setter
    def gpu_labels(self, gpu_labels):
        """Sets the gpu_labels of this ResponseKernelResourceSpec.


        :param gpu_labels: The gpu_labels of this ResponseKernelResourceSpec.  # noqa: E501
        :type gpu_labels: ModelKernelResourceSpecGpuLabels
        """

        self._gpu_labels = gpu_labels

    @property
    def gpu_limit(self):
        """Gets the gpu_limit of this ResponseKernelResourceSpec.  # noqa: E501


        :return: The gpu_limit of this ResponseKernelResourceSpec.  # noqa: E501
        :rtype: int
        """
        return self._gpu_limit

    @gpu_limit.setter
    def gpu_limit(self, gpu_limit):
        """Sets the gpu_limit of this ResponseKernelResourceSpec.


        :param gpu_limit: The gpu_limit of this ResponseKernelResourceSpec.  # noqa: E501
        :type gpu_limit: int
        """
        if self.local_vars_configuration.client_side_validation and gpu_limit is None:  # noqa: E501
            raise ValueError("Invalid value for `gpu_limit`, must not be `None`")  # noqa: E501

        self._gpu_limit = gpu_limit

    @property
    def gpu_type(self):
        """Gets the gpu_type of this ResponseKernelResourceSpec.  # noqa: E501


        :return: The gpu_type of this ResponseKernelResourceSpec.  # noqa: E501
        :rtype: str
        """
        return self._gpu_type

    @gpu_type.setter
    def gpu_type(self, gpu_type):
        """Sets the gpu_type of this ResponseKernelResourceSpec.


        :param gpu_type: The gpu_type of this ResponseKernelResourceSpec.  # noqa: E501
        :type gpu_type: str
        """
        if self.local_vars_configuration.client_side_validation and gpu_type is None:  # noqa: E501
            raise ValueError("Invalid value for `gpu_type`, must not be `None`")  # noqa: E501

        self._gpu_type = gpu_type

    @property
    def id(self):
        """Gets the id of this ResponseKernelResourceSpec.  # noqa: E501


        :return: The id of this ResponseKernelResourceSpec.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ResponseKernelResourceSpec.


        :param id: The id of this ResponseKernelResourceSpec.  # noqa: E501
        :type id: int
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def immutable_slug(self):
        """Gets the immutable_slug of this ResponseKernelResourceSpec.  # noqa: E501


        :return: The immutable_slug of this ResponseKernelResourceSpec.  # noqa: E501
        :rtype: str
        """
        return self._immutable_slug

    @immutable_slug.setter
    def immutable_slug(self, immutable_slug):
        """Sets the immutable_slug of this ResponseKernelResourceSpec.


        :param immutable_slug: The immutable_slug of this ResponseKernelResourceSpec.  # noqa: E501
        :type immutable_slug: str
        """
        if self.local_vars_configuration.client_side_validation and immutable_slug is None:  # noqa: E501
            raise ValueError("Invalid value for `immutable_slug`, must not be `None`")  # noqa: E501

        self._immutable_slug = immutable_slug

    @property
    def memory_limit(self):
        """Gets the memory_limit of this ResponseKernelResourceSpec.  # noqa: E501


        :return: The memory_limit of this ResponseKernelResourceSpec.  # noqa: E501
        :rtype: str
        """
        return self._memory_limit

    @memory_limit.setter
    def memory_limit(self, memory_limit):
        """Sets the memory_limit of this ResponseKernelResourceSpec.


        :param memory_limit: The memory_limit of this ResponseKernelResourceSpec.  # noqa: E501
        :type memory_limit: str
        """
        if self.local_vars_configuration.client_side_validation and memory_limit is None:  # noqa: E501
            raise ValueError("Invalid value for `memory_limit`, must not be `None`")  # noqa: E501

        self._memory_limit = memory_limit

    @property
    def name(self):
        """Gets the name of this ResponseKernelResourceSpec.  # noqa: E501


        :return: The name of this ResponseKernelResourceSpec.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ResponseKernelResourceSpec.


        :param name: The name of this ResponseKernelResourceSpec.  # noqa: E501
        :type name: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def processor_type(self):
        """Gets the processor_type of this ResponseKernelResourceSpec.  # noqa: E501


        :return: The processor_type of this ResponseKernelResourceSpec.  # noqa: E501
        :rtype: str
        """
        return self._processor_type

    @processor_type.setter
    def processor_type(self, processor_type):
        """Sets the processor_type of this ResponseKernelResourceSpec.


        :param processor_type: The processor_type of this ResponseKernelResourceSpec.  # noqa: E501
        :type processor_type: str
        """
        if self.local_vars_configuration.client_side_validation and processor_type is None:  # noqa: E501
            raise ValueError("Invalid value for `processor_type`, must not be `None`")  # noqa: E501

        self._processor_type = processor_type

    @property
    def spot(self):
        """Gets the spot of this ResponseKernelResourceSpec.  # noqa: E501


        :return: The spot of this ResponseKernelResourceSpec.  # noqa: E501
        :rtype: bool
        """
        return self._spot

    @spot.setter
    def spot(self, spot):
        """Sets the spot of this ResponseKernelResourceSpec.


        :param spot: The spot of this ResponseKernelResourceSpec.  # noqa: E501
        :type spot: bool
        """
        if self.local_vars_configuration.client_side_validation and spot is None:  # noqa: E501
            raise ValueError("Invalid value for `spot`, must not be `None`")  # noqa: E501

        self._spot = spot

    @property
    def updated_dt(self):
        """Gets the updated_dt of this ResponseKernelResourceSpec.  # noqa: E501


        :return: The updated_dt of this ResponseKernelResourceSpec.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_dt

    @updated_dt.setter
    def updated_dt(self, updated_dt):
        """Sets the updated_dt of this ResponseKernelResourceSpec.


        :param updated_dt: The updated_dt of this ResponseKernelResourceSpec.  # noqa: E501
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
        if not isinstance(other, ResponseKernelResourceSpec):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ResponseKernelResourceSpec):
            return True

        return self.to_dict() != other.to_dict()
