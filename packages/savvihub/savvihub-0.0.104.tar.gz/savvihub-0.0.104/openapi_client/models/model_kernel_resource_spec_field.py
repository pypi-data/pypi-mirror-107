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


class ModelKernelResourceSpecField(object):
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
        'cpu_limit': 'float',
        'cpu_type': 'str',
        'gpu_labels': 'dict(str, object)',
        'gpu_limit': 'int',
        'gpu_type': 'str',
        'memory_limit': 'str',
        'processor_type': 'str'
    }

    attribute_map = {
        'cpu_limit': 'cpu_limit',
        'cpu_type': 'cpu_type',
        'gpu_labels': 'gpu_labels',
        'gpu_limit': 'gpu_limit',
        'gpu_type': 'gpu_type',
        'memory_limit': 'memory_limit',
        'processor_type': 'processor_type'
    }

    def __init__(self, cpu_limit=None, cpu_type=None, gpu_labels=None, gpu_limit=None, gpu_type=None, memory_limit=None, processor_type=None, local_vars_configuration=None):  # noqa: E501
        """ModelKernelResourceSpecField - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._cpu_limit = None
        self._cpu_type = None
        self._gpu_labels = None
        self._gpu_limit = None
        self._gpu_type = None
        self._memory_limit = None
        self._processor_type = None
        self.discriminator = None

        self.cpu_limit = cpu_limit
        self.cpu_type = cpu_type
        if gpu_labels is not None:
            self.gpu_labels = gpu_labels
        if gpu_limit is not None:
            self.gpu_limit = gpu_limit
        self.gpu_type = gpu_type
        self.memory_limit = memory_limit
        self.processor_type = processor_type

    @property
    def cpu_limit(self):
        """Gets the cpu_limit of this ModelKernelResourceSpecField.  # noqa: E501


        :return: The cpu_limit of this ModelKernelResourceSpecField.  # noqa: E501
        :rtype: float
        """
        return self._cpu_limit

    @cpu_limit.setter
    def cpu_limit(self, cpu_limit):
        """Sets the cpu_limit of this ModelKernelResourceSpecField.


        :param cpu_limit: The cpu_limit of this ModelKernelResourceSpecField.  # noqa: E501
        :type cpu_limit: float
        """
        if self.local_vars_configuration.client_side_validation and cpu_limit is None:  # noqa: E501
            raise ValueError("Invalid value for `cpu_limit`, must not be `None`")  # noqa: E501

        self._cpu_limit = cpu_limit

    @property
    def cpu_type(self):
        """Gets the cpu_type of this ModelKernelResourceSpecField.  # noqa: E501


        :return: The cpu_type of this ModelKernelResourceSpecField.  # noqa: E501
        :rtype: str
        """
        return self._cpu_type

    @cpu_type.setter
    def cpu_type(self, cpu_type):
        """Sets the cpu_type of this ModelKernelResourceSpecField.


        :param cpu_type: The cpu_type of this ModelKernelResourceSpecField.  # noqa: E501
        :type cpu_type: str
        """
        if self.local_vars_configuration.client_side_validation and cpu_type is None:  # noqa: E501
            raise ValueError("Invalid value for `cpu_type`, must not be `None`")  # noqa: E501

        self._cpu_type = cpu_type

    @property
    def gpu_labels(self):
        """Gets the gpu_labels of this ModelKernelResourceSpecField.  # noqa: E501


        :return: The gpu_labels of this ModelKernelResourceSpecField.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._gpu_labels

    @gpu_labels.setter
    def gpu_labels(self, gpu_labels):
        """Sets the gpu_labels of this ModelKernelResourceSpecField.


        :param gpu_labels: The gpu_labels of this ModelKernelResourceSpecField.  # noqa: E501
        :type gpu_labels: dict(str, object)
        """

        self._gpu_labels = gpu_labels

    @property
    def gpu_limit(self):
        """Gets the gpu_limit of this ModelKernelResourceSpecField.  # noqa: E501


        :return: The gpu_limit of this ModelKernelResourceSpecField.  # noqa: E501
        :rtype: int
        """
        return self._gpu_limit

    @gpu_limit.setter
    def gpu_limit(self, gpu_limit):
        """Sets the gpu_limit of this ModelKernelResourceSpecField.


        :param gpu_limit: The gpu_limit of this ModelKernelResourceSpecField.  # noqa: E501
        :type gpu_limit: int
        """

        self._gpu_limit = gpu_limit

    @property
    def gpu_type(self):
        """Gets the gpu_type of this ModelKernelResourceSpecField.  # noqa: E501


        :return: The gpu_type of this ModelKernelResourceSpecField.  # noqa: E501
        :rtype: str
        """
        return self._gpu_type

    @gpu_type.setter
    def gpu_type(self, gpu_type):
        """Sets the gpu_type of this ModelKernelResourceSpecField.


        :param gpu_type: The gpu_type of this ModelKernelResourceSpecField.  # noqa: E501
        :type gpu_type: str
        """
        if self.local_vars_configuration.client_side_validation and gpu_type is None:  # noqa: E501
            raise ValueError("Invalid value for `gpu_type`, must not be `None`")  # noqa: E501

        self._gpu_type = gpu_type

    @property
    def memory_limit(self):
        """Gets the memory_limit of this ModelKernelResourceSpecField.  # noqa: E501


        :return: The memory_limit of this ModelKernelResourceSpecField.  # noqa: E501
        :rtype: str
        """
        return self._memory_limit

    @memory_limit.setter
    def memory_limit(self, memory_limit):
        """Sets the memory_limit of this ModelKernelResourceSpecField.


        :param memory_limit: The memory_limit of this ModelKernelResourceSpecField.  # noqa: E501
        :type memory_limit: str
        """
        if self.local_vars_configuration.client_side_validation and memory_limit is None:  # noqa: E501
            raise ValueError("Invalid value for `memory_limit`, must not be `None`")  # noqa: E501

        self._memory_limit = memory_limit

    @property
    def processor_type(self):
        """Gets the processor_type of this ModelKernelResourceSpecField.  # noqa: E501


        :return: The processor_type of this ModelKernelResourceSpecField.  # noqa: E501
        :rtype: str
        """
        return self._processor_type

    @processor_type.setter
    def processor_type(self, processor_type):
        """Sets the processor_type of this ModelKernelResourceSpecField.


        :param processor_type: The processor_type of this ModelKernelResourceSpecField.  # noqa: E501
        :type processor_type: str
        """
        if self.local_vars_configuration.client_side_validation and processor_type is None:  # noqa: E501
            raise ValueError("Invalid value for `processor_type`, must not be `None`")  # noqa: E501

        self._processor_type = processor_type

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
        if not isinstance(other, ModelKernelResourceSpecField):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ModelKernelResourceSpecField):
            return True

        return self.to_dict() != other.to_dict()
