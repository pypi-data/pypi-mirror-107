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


class ModelKernelClusterEdges(object):
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
        'global_kernel_cluster': 'ModelGlobalKernelCluster',
        'kernel_cluster_nodes': 'list[ModelKernelClusterNode]',
        'kernel_cluster_storages': 'list[ModelKernelClusterStorage]',
        'workspace': 'ModelWorkspace'
    }

    attribute_map = {
        'global_kernel_cluster': 'global_kernel_cluster',
        'kernel_cluster_nodes': 'kernel_cluster_nodes',
        'kernel_cluster_storages': 'kernel_cluster_storages',
        'workspace': 'workspace'
    }

    def __init__(self, global_kernel_cluster=None, kernel_cluster_nodes=None, kernel_cluster_storages=None, workspace=None, local_vars_configuration=None):  # noqa: E501
        """ModelKernelClusterEdges - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._global_kernel_cluster = None
        self._kernel_cluster_nodes = None
        self._kernel_cluster_storages = None
        self._workspace = None
        self.discriminator = None

        if global_kernel_cluster is not None:
            self.global_kernel_cluster = global_kernel_cluster
        if kernel_cluster_nodes is not None:
            self.kernel_cluster_nodes = kernel_cluster_nodes
        if kernel_cluster_storages is not None:
            self.kernel_cluster_storages = kernel_cluster_storages
        if workspace is not None:
            self.workspace = workspace

    @property
    def global_kernel_cluster(self):
        """Gets the global_kernel_cluster of this ModelKernelClusterEdges.  # noqa: E501


        :return: The global_kernel_cluster of this ModelKernelClusterEdges.  # noqa: E501
        :rtype: ModelGlobalKernelCluster
        """
        return self._global_kernel_cluster

    @global_kernel_cluster.setter
    def global_kernel_cluster(self, global_kernel_cluster):
        """Sets the global_kernel_cluster of this ModelKernelClusterEdges.


        :param global_kernel_cluster: The global_kernel_cluster of this ModelKernelClusterEdges.  # noqa: E501
        :type global_kernel_cluster: ModelGlobalKernelCluster
        """

        self._global_kernel_cluster = global_kernel_cluster

    @property
    def kernel_cluster_nodes(self):
        """Gets the kernel_cluster_nodes of this ModelKernelClusterEdges.  # noqa: E501


        :return: The kernel_cluster_nodes of this ModelKernelClusterEdges.  # noqa: E501
        :rtype: list[ModelKernelClusterNode]
        """
        return self._kernel_cluster_nodes

    @kernel_cluster_nodes.setter
    def kernel_cluster_nodes(self, kernel_cluster_nodes):
        """Sets the kernel_cluster_nodes of this ModelKernelClusterEdges.


        :param kernel_cluster_nodes: The kernel_cluster_nodes of this ModelKernelClusterEdges.  # noqa: E501
        :type kernel_cluster_nodes: list[ModelKernelClusterNode]
        """

        self._kernel_cluster_nodes = kernel_cluster_nodes

    @property
    def kernel_cluster_storages(self):
        """Gets the kernel_cluster_storages of this ModelKernelClusterEdges.  # noqa: E501


        :return: The kernel_cluster_storages of this ModelKernelClusterEdges.  # noqa: E501
        :rtype: list[ModelKernelClusterStorage]
        """
        return self._kernel_cluster_storages

    @kernel_cluster_storages.setter
    def kernel_cluster_storages(self, kernel_cluster_storages):
        """Sets the kernel_cluster_storages of this ModelKernelClusterEdges.


        :param kernel_cluster_storages: The kernel_cluster_storages of this ModelKernelClusterEdges.  # noqa: E501
        :type kernel_cluster_storages: list[ModelKernelClusterStorage]
        """

        self._kernel_cluster_storages = kernel_cluster_storages

    @property
    def workspace(self):
        """Gets the workspace of this ModelKernelClusterEdges.  # noqa: E501


        :return: The workspace of this ModelKernelClusterEdges.  # noqa: E501
        :rtype: ModelWorkspace
        """
        return self._workspace

    @workspace.setter
    def workspace(self, workspace):
        """Sets the workspace of this ModelKernelClusterEdges.


        :param workspace: The workspace of this ModelKernelClusterEdges.  # noqa: E501
        :type workspace: ModelWorkspace
        """

        self._workspace = workspace

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
        if not isinstance(other, ModelKernelClusterEdges):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ModelKernelClusterEdges):
            return True

        return self.to_dict() != other.to_dict()
