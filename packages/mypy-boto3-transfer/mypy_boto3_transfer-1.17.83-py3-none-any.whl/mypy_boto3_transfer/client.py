"""
Type annotations for transfer service client.

[Open documentation](./client.md)

Usage::

    ```python
    import boto3
    from mypy_boto3_transfer import TransferClient

    client: TransferClient = boto3.client("transfer")
    ```
"""
import sys
from typing import Any, Dict, List, Type

from botocore.client import ClientMeta

from .literals import (
    DomainType,
    EndpointTypeType,
    HomeDirectoryTypeType,
    IdentityProviderTypeType,
    ProtocolType,
)
from .paginator import ListServersPaginator
from .type_defs import (
    CreateAccessResponseTypeDef,
    CreateServerResponseTypeDef,
    CreateUserResponseTypeDef,
    DescribeAccessResponseTypeDef,
    DescribeSecurityPolicyResponseTypeDef,
    DescribeServerResponseTypeDef,
    DescribeUserResponseTypeDef,
    EndpointDetailsTypeDef,
    HomeDirectoryMapEntryTypeDef,
    IdentityProviderDetailsTypeDef,
    ImportSshPublicKeyResponseTypeDef,
    ListAccessesResponseTypeDef,
    ListSecurityPoliciesResponseTypeDef,
    ListServersResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListUsersResponseTypeDef,
    PosixProfileTypeDef,
    TagTypeDef,
    TestIdentityProviderResponseTypeDef,
    UpdateAccessResponseTypeDef,
    UpdateServerResponseTypeDef,
    UpdateUserResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("TransferClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServiceError: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    ResourceExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]


class TransferClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/transfer.html#Transfer.Client)
    [Show boto3-stubs documentation](./client.md)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/transfer.html#Transfer.Client.can_paginate)
        [Show boto3-stubs documentation](./client.md#can_paginate)
        """

    def create_access(
        self,
        Role: str,
        ServerId: str,
        ExternalId: str,
        HomeDirectory: str = None,
        HomeDirectoryType: HomeDirectoryTypeType = None,
        HomeDirectoryMappings: List["HomeDirectoryMapEntryTypeDef"] = None,
        Policy: str = None,
        PosixProfile: "PosixProfileTypeDef" = None,
    ) -> CreateAccessResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/transfer.html#Transfer.Client.create_access)
        [Show boto3-stubs documentation](./client.md#create_access)
        """

    def create_server(
        self,
        Certificate: str = None,
        Domain: DomainType = None,
        EndpointDetails: "EndpointDetailsTypeDef" = None,
        EndpointType: EndpointTypeType = None,
        HostKey: str = None,
        IdentityProviderDetails: "IdentityProviderDetailsTypeDef" = None,
        IdentityProviderType: IdentityProviderTypeType = None,
        LoggingRole: str = None,
        Protocols: List[ProtocolType] = None,
        SecurityPolicyName: str = None,
        Tags: List["TagTypeDef"] = None,
    ) -> CreateServerResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/transfer.html#Transfer.Client.create_server)
        [Show boto3-stubs documentation](./client.md#create_server)
        """

    def create_user(
        self,
        Role: str,
        ServerId: str,
        UserName: str,
        HomeDirectory: str = None,
        HomeDirectoryType: HomeDirectoryTypeType = None,
        HomeDirectoryMappings: List["HomeDirectoryMapEntryTypeDef"] = None,
        Policy: str = None,
        PosixProfile: "PosixProfileTypeDef" = None,
        SshPublicKeyBody: str = None,
        Tags: List["TagTypeDef"] = None,
    ) -> CreateUserResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/transfer.html#Transfer.Client.create_user)
        [Show boto3-stubs documentation](./client.md#create_user)
        """

    def delete_access(self, ServerId: str, ExternalId: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/transfer.html#Transfer.Client.delete_access)
        [Show boto3-stubs documentation](./client.md#delete_access)
        """

    def delete_server(self, ServerId: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/transfer.html#Transfer.Client.delete_server)
        [Show boto3-stubs documentation](./client.md#delete_server)
        """

    def delete_ssh_public_key(self, ServerId: str, SshPublicKeyId: str, UserName: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/transfer.html#Transfer.Client.delete_ssh_public_key)
        [Show boto3-stubs documentation](./client.md#delete_ssh_public_key)
        """

    def delete_user(self, ServerId: str, UserName: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/transfer.html#Transfer.Client.delete_user)
        [Show boto3-stubs documentation](./client.md#delete_user)
        """

    def describe_access(self, ServerId: str, ExternalId: str) -> DescribeAccessResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/transfer.html#Transfer.Client.describe_access)
        [Show boto3-stubs documentation](./client.md#describe_access)
        """

    def describe_security_policy(
        self, SecurityPolicyName: str
    ) -> DescribeSecurityPolicyResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/transfer.html#Transfer.Client.describe_security_policy)
        [Show boto3-stubs documentation](./client.md#describe_security_policy)
        """

    def describe_server(self, ServerId: str) -> DescribeServerResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/transfer.html#Transfer.Client.describe_server)
        [Show boto3-stubs documentation](./client.md#describe_server)
        """

    def describe_user(self, ServerId: str, UserName: str) -> DescribeUserResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/transfer.html#Transfer.Client.describe_user)
        [Show boto3-stubs documentation](./client.md#describe_user)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/transfer.html#Transfer.Client.generate_presigned_url)
        [Show boto3-stubs documentation](./client.md#generate_presigned_url)
        """

    def import_ssh_public_key(
        self, ServerId: str, SshPublicKeyBody: str, UserName: str
    ) -> ImportSshPublicKeyResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/transfer.html#Transfer.Client.import_ssh_public_key)
        [Show boto3-stubs documentation](./client.md#import_ssh_public_key)
        """

    def list_accesses(
        self, ServerId: str, MaxResults: int = None, NextToken: str = None
    ) -> ListAccessesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/transfer.html#Transfer.Client.list_accesses)
        [Show boto3-stubs documentation](./client.md#list_accesses)
        """

    def list_security_policies(
        self, MaxResults: int = None, NextToken: str = None
    ) -> ListSecurityPoliciesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/transfer.html#Transfer.Client.list_security_policies)
        [Show boto3-stubs documentation](./client.md#list_security_policies)
        """

    def list_servers(
        self, MaxResults: int = None, NextToken: str = None
    ) -> ListServersResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/transfer.html#Transfer.Client.list_servers)
        [Show boto3-stubs documentation](./client.md#list_servers)
        """

    def list_tags_for_resource(
        self, Arn: str, MaxResults: int = None, NextToken: str = None
    ) -> ListTagsForResourceResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/transfer.html#Transfer.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](./client.md#list_tags_for_resource)
        """

    def list_users(
        self, ServerId: str, MaxResults: int = None, NextToken: str = None
    ) -> ListUsersResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/transfer.html#Transfer.Client.list_users)
        [Show boto3-stubs documentation](./client.md#list_users)
        """

    def start_server(self, ServerId: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/transfer.html#Transfer.Client.start_server)
        [Show boto3-stubs documentation](./client.md#start_server)
        """

    def stop_server(self, ServerId: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/transfer.html#Transfer.Client.stop_server)
        [Show boto3-stubs documentation](./client.md#stop_server)
        """

    def tag_resource(self, Arn: str, Tags: List["TagTypeDef"]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/transfer.html#Transfer.Client.tag_resource)
        [Show boto3-stubs documentation](./client.md#tag_resource)
        """

    def test_identity_provider(
        self,
        ServerId: str,
        UserName: str,
        ServerProtocol: ProtocolType = None,
        SourceIp: str = None,
        UserPassword: str = None,
    ) -> TestIdentityProviderResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/transfer.html#Transfer.Client.test_identity_provider)
        [Show boto3-stubs documentation](./client.md#test_identity_provider)
        """

    def untag_resource(self, Arn: str, TagKeys: List[str]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/transfer.html#Transfer.Client.untag_resource)
        [Show boto3-stubs documentation](./client.md#untag_resource)
        """

    def update_access(
        self,
        ServerId: str,
        ExternalId: str,
        HomeDirectory: str = None,
        HomeDirectoryType: HomeDirectoryTypeType = None,
        HomeDirectoryMappings: List["HomeDirectoryMapEntryTypeDef"] = None,
        Policy: str = None,
        PosixProfile: "PosixProfileTypeDef" = None,
        Role: str = None,
    ) -> UpdateAccessResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/transfer.html#Transfer.Client.update_access)
        [Show boto3-stubs documentation](./client.md#update_access)
        """

    def update_server(
        self,
        ServerId: str,
        Certificate: str = None,
        EndpointDetails: "EndpointDetailsTypeDef" = None,
        EndpointType: EndpointTypeType = None,
        HostKey: str = None,
        IdentityProviderDetails: "IdentityProviderDetailsTypeDef" = None,
        LoggingRole: str = None,
        Protocols: List[ProtocolType] = None,
        SecurityPolicyName: str = None,
    ) -> UpdateServerResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/transfer.html#Transfer.Client.update_server)
        [Show boto3-stubs documentation](./client.md#update_server)
        """

    def update_user(
        self,
        ServerId: str,
        UserName: str,
        HomeDirectory: str = None,
        HomeDirectoryType: HomeDirectoryTypeType = None,
        HomeDirectoryMappings: List["HomeDirectoryMapEntryTypeDef"] = None,
        Policy: str = None,
        PosixProfile: "PosixProfileTypeDef" = None,
        Role: str = None,
    ) -> UpdateUserResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/transfer.html#Transfer.Client.update_user)
        [Show boto3-stubs documentation](./client.md#update_user)
        """

    def get_paginator(self, operation_name: Literal["list_servers"]) -> ListServersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/transfer.html#Transfer.Paginator.ListServers)[Show boto3-stubs documentation](./paginators.md#listserverspaginator)
        """
