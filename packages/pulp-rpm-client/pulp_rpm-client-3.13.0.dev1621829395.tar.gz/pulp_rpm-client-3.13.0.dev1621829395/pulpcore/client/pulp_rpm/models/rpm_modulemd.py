# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from pulpcore.client.pulp_rpm.configuration import Configuration


class RpmModulemd(object):
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
        'artifact': 'str',
        'relative_path': 'str',
        'file': 'file',
        'repository': 'str',
        'name': 'str',
        'stream': 'str',
        'version': 'str',
        'static_context': 'bool',
        'context': 'str',
        'arch': 'str',
        'artifacts': 'object',
        'dependencies': 'object',
        'packages': 'list[str]'
    }

    attribute_map = {
        'artifact': 'artifact',
        'relative_path': 'relative_path',
        'file': 'file',
        'repository': 'repository',
        'name': 'name',
        'stream': 'stream',
        'version': 'version',
        'static_context': 'static_context',
        'context': 'context',
        'arch': 'arch',
        'artifacts': 'artifacts',
        'dependencies': 'dependencies',
        'packages': 'packages'
    }

    def __init__(self, artifact=None, relative_path=None, file=None, repository=None, name=None, stream=None, version=None, static_context=None, context=None, arch=None, artifacts=None, dependencies=None, packages=None, local_vars_configuration=None):  # noqa: E501
        """RpmModulemd - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._artifact = None
        self._relative_path = None
        self._file = None
        self._repository = None
        self._name = None
        self._stream = None
        self._version = None
        self._static_context = None
        self._context = None
        self._arch = None
        self._artifacts = None
        self._dependencies = None
        self._packages = None
        self.discriminator = None

        if artifact is not None:
            self.artifact = artifact
        self.relative_path = relative_path
        if file is not None:
            self.file = file
        if repository is not None:
            self.repository = repository
        self.name = name
        self.stream = stream
        self.version = version
        self.static_context = static_context
        self.context = context
        self.arch = arch
        self.artifacts = artifacts
        self.dependencies = dependencies
        if packages is not None:
            self.packages = packages

    @property
    def artifact(self):
        """Gets the artifact of this RpmModulemd.  # noqa: E501

        Artifact file representing the physical content  # noqa: E501

        :return: The artifact of this RpmModulemd.  # noqa: E501
        :rtype: str
        """
        return self._artifact

    @artifact.setter
    def artifact(self, artifact):
        """Sets the artifact of this RpmModulemd.

        Artifact file representing the physical content  # noqa: E501

        :param artifact: The artifact of this RpmModulemd.  # noqa: E501
        :type: str
        """

        self._artifact = artifact

    @property
    def relative_path(self):
        """Gets the relative_path of this RpmModulemd.  # noqa: E501

        Path where the artifact is located relative to distributions base_path  # noqa: E501

        :return: The relative_path of this RpmModulemd.  # noqa: E501
        :rtype: str
        """
        return self._relative_path

    @relative_path.setter
    def relative_path(self, relative_path):
        """Sets the relative_path of this RpmModulemd.

        Path where the artifact is located relative to distributions base_path  # noqa: E501

        :param relative_path: The relative_path of this RpmModulemd.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and relative_path is None:  # noqa: E501
            raise ValueError("Invalid value for `relative_path`, must not be `None`")  # noqa: E501

        self._relative_path = relative_path

    @property
    def file(self):
        """Gets the file of this RpmModulemd.  # noqa: E501

        An uploaded file that may be turned into the artifact of the content unit.  # noqa: E501

        :return: The file of this RpmModulemd.  # noqa: E501
        :rtype: file
        """
        return self._file

    @file.setter
    def file(self, file):
        """Sets the file of this RpmModulemd.

        An uploaded file that may be turned into the artifact of the content unit.  # noqa: E501

        :param file: The file of this RpmModulemd.  # noqa: E501
        :type: file
        """

        self._file = file

    @property
    def repository(self):
        """Gets the repository of this RpmModulemd.  # noqa: E501

        A URI of a repository the new content unit should be associated with.  # noqa: E501

        :return: The repository of this RpmModulemd.  # noqa: E501
        :rtype: str
        """
        return self._repository

    @repository.setter
    def repository(self, repository):
        """Sets the repository of this RpmModulemd.

        A URI of a repository the new content unit should be associated with.  # noqa: E501

        :param repository: The repository of this RpmModulemd.  # noqa: E501
        :type: str
        """

        self._repository = repository

    @property
    def name(self):
        """Gets the name of this RpmModulemd.  # noqa: E501

        Modulemd name.  # noqa: E501

        :return: The name of this RpmModulemd.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this RpmModulemd.

        Modulemd name.  # noqa: E501

        :param name: The name of this RpmModulemd.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def stream(self):
        """Gets the stream of this RpmModulemd.  # noqa: E501

        Stream name.  # noqa: E501

        :return: The stream of this RpmModulemd.  # noqa: E501
        :rtype: str
        """
        return self._stream

    @stream.setter
    def stream(self, stream):
        """Sets the stream of this RpmModulemd.

        Stream name.  # noqa: E501

        :param stream: The stream of this RpmModulemd.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and stream is None:  # noqa: E501
            raise ValueError("Invalid value for `stream`, must not be `None`")  # noqa: E501

        self._stream = stream

    @property
    def version(self):
        """Gets the version of this RpmModulemd.  # noqa: E501

        Modulemd version.  # noqa: E501

        :return: The version of this RpmModulemd.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this RpmModulemd.

        Modulemd version.  # noqa: E501

        :param version: The version of this RpmModulemd.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and version is None:  # noqa: E501
            raise ValueError("Invalid value for `version`, must not be `None`")  # noqa: E501

        self._version = version

    @property
    def static_context(self):
        """Gets the static_context of this RpmModulemd.  # noqa: E501

        Modulemd static-context flag.  # noqa: E501

        :return: The static_context of this RpmModulemd.  # noqa: E501
        :rtype: bool
        """
        return self._static_context

    @static_context.setter
    def static_context(self, static_context):
        """Sets the static_context of this RpmModulemd.

        Modulemd static-context flag.  # noqa: E501

        :param static_context: The static_context of this RpmModulemd.  # noqa: E501
        :type: bool
        """
        if self.local_vars_configuration.client_side_validation and static_context is None:  # noqa: E501
            raise ValueError("Invalid value for `static_context`, must not be `None`")  # noqa: E501

        self._static_context = static_context

    @property
    def context(self):
        """Gets the context of this RpmModulemd.  # noqa: E501

        Modulemd context.  # noqa: E501

        :return: The context of this RpmModulemd.  # noqa: E501
        :rtype: str
        """
        return self._context

    @context.setter
    def context(self, context):
        """Sets the context of this RpmModulemd.

        Modulemd context.  # noqa: E501

        :param context: The context of this RpmModulemd.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and context is None:  # noqa: E501
            raise ValueError("Invalid value for `context`, must not be `None`")  # noqa: E501

        self._context = context

    @property
    def arch(self):
        """Gets the arch of this RpmModulemd.  # noqa: E501

        Modulemd architecture.  # noqa: E501

        :return: The arch of this RpmModulemd.  # noqa: E501
        :rtype: str
        """
        return self._arch

    @arch.setter
    def arch(self, arch):
        """Sets the arch of this RpmModulemd.

        Modulemd architecture.  # noqa: E501

        :param arch: The arch of this RpmModulemd.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and arch is None:  # noqa: E501
            raise ValueError("Invalid value for `arch`, must not be `None`")  # noqa: E501

        self._arch = arch

    @property
    def artifacts(self):
        """Gets the artifacts of this RpmModulemd.  # noqa: E501

        Modulemd artifacts.  # noqa: E501

        :return: The artifacts of this RpmModulemd.  # noqa: E501
        :rtype: object
        """
        return self._artifacts

    @artifacts.setter
    def artifacts(self, artifacts):
        """Sets the artifacts of this RpmModulemd.

        Modulemd artifacts.  # noqa: E501

        :param artifacts: The artifacts of this RpmModulemd.  # noqa: E501
        :type: object
        """

        self._artifacts = artifacts

    @property
    def dependencies(self):
        """Gets the dependencies of this RpmModulemd.  # noqa: E501

        Modulemd dependencies.  # noqa: E501

        :return: The dependencies of this RpmModulemd.  # noqa: E501
        :rtype: object
        """
        return self._dependencies

    @dependencies.setter
    def dependencies(self, dependencies):
        """Sets the dependencies of this RpmModulemd.

        Modulemd dependencies.  # noqa: E501

        :param dependencies: The dependencies of this RpmModulemd.  # noqa: E501
        :type: object
        """

        self._dependencies = dependencies

    @property
    def packages(self):
        """Gets the packages of this RpmModulemd.  # noqa: E501

        Modulemd artifacts' packages.  # noqa: E501

        :return: The packages of this RpmModulemd.  # noqa: E501
        :rtype: list[str]
        """
        return self._packages

    @packages.setter
    def packages(self, packages):
        """Sets the packages of this RpmModulemd.

        Modulemd artifacts' packages.  # noqa: E501

        :param packages: The packages of this RpmModulemd.  # noqa: E501
        :type: list[str]
        """

        self._packages = packages

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, RpmModulemd):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RpmModulemd):
            return True

        return self.to_dict() != other.to_dict()
