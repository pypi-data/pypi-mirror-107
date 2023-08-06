"""
Type annotations for worklink service client.

[Open documentation](./client.md)

Usage::

    ```python
    import boto3
    from mypy_boto3_worklink import WorkLinkClient

    client: WorkLinkClient = boto3.client("worklink")
    ```
"""
import sys
from typing import Any, Dict, List, Type

from botocore.client import ClientMeta

from .type_defs import (
    AssociateWebsiteAuthorizationProviderResponseTypeDef,
    AssociateWebsiteCertificateAuthorityResponseTypeDef,
    CreateFleetResponseTypeDef,
    DescribeAuditStreamConfigurationResponseTypeDef,
    DescribeCompanyNetworkConfigurationResponseTypeDef,
    DescribeDevicePolicyConfigurationResponseTypeDef,
    DescribeDeviceResponseTypeDef,
    DescribeDomainResponseTypeDef,
    DescribeFleetMetadataResponseTypeDef,
    DescribeIdentityProviderConfigurationResponseTypeDef,
    DescribeWebsiteCertificateAuthorityResponseTypeDef,
    ListDevicesResponseTypeDef,
    ListDomainsResponseTypeDef,
    ListFleetsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWebsiteAuthorizationProvidersResponseTypeDef,
    ListWebsiteCertificateAuthoritiesResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("WorkLinkClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]


class WorkLinkClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client)
    [Show boto3-stubs documentation](./client.md)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def associate_domain(
        self, FleetArn: str, DomainName: str, AcmCertificateArn: str, DisplayName: str = None
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.associate_domain)
        [Show boto3-stubs documentation](./client.md#associate_domain)
        """

    def associate_website_authorization_provider(
        self, FleetArn: str, AuthorizationProviderType: Literal["SAML"], DomainName: str = None
    ) -> AssociateWebsiteAuthorizationProviderResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.associate_website_authorization_provider)
        [Show boto3-stubs documentation](./client.md#associate_website_authorization_provider)
        """

    def associate_website_certificate_authority(
        self, FleetArn: str, Certificate: str, DisplayName: str = None
    ) -> AssociateWebsiteCertificateAuthorityResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.associate_website_certificate_authority)
        [Show boto3-stubs documentation](./client.md#associate_website_certificate_authority)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.can_paginate)
        [Show boto3-stubs documentation](./client.md#can_paginate)
        """

    def create_fleet(
        self,
        FleetName: str,
        DisplayName: str = None,
        OptimizeForEndUserLocation: bool = None,
        Tags: Dict[str, str] = None,
    ) -> CreateFleetResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.create_fleet)
        [Show boto3-stubs documentation](./client.md#create_fleet)
        """

    def delete_fleet(self, FleetArn: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.delete_fleet)
        [Show boto3-stubs documentation](./client.md#delete_fleet)
        """

    def describe_audit_stream_configuration(
        self, FleetArn: str
    ) -> DescribeAuditStreamConfigurationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.describe_audit_stream_configuration)
        [Show boto3-stubs documentation](./client.md#describe_audit_stream_configuration)
        """

    def describe_company_network_configuration(
        self, FleetArn: str
    ) -> DescribeCompanyNetworkConfigurationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.describe_company_network_configuration)
        [Show boto3-stubs documentation](./client.md#describe_company_network_configuration)
        """

    def describe_device(self, FleetArn: str, DeviceId: str) -> DescribeDeviceResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.describe_device)
        [Show boto3-stubs documentation](./client.md#describe_device)
        """

    def describe_device_policy_configuration(
        self, FleetArn: str
    ) -> DescribeDevicePolicyConfigurationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.describe_device_policy_configuration)
        [Show boto3-stubs documentation](./client.md#describe_device_policy_configuration)
        """

    def describe_domain(self, FleetArn: str, DomainName: str) -> DescribeDomainResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.describe_domain)
        [Show boto3-stubs documentation](./client.md#describe_domain)
        """

    def describe_fleet_metadata(self, FleetArn: str) -> DescribeFleetMetadataResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.describe_fleet_metadata)
        [Show boto3-stubs documentation](./client.md#describe_fleet_metadata)
        """

    def describe_identity_provider_configuration(
        self, FleetArn: str
    ) -> DescribeIdentityProviderConfigurationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.describe_identity_provider_configuration)
        [Show boto3-stubs documentation](./client.md#describe_identity_provider_configuration)
        """

    def describe_website_certificate_authority(
        self, FleetArn: str, WebsiteCaId: str
    ) -> DescribeWebsiteCertificateAuthorityResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.describe_website_certificate_authority)
        [Show boto3-stubs documentation](./client.md#describe_website_certificate_authority)
        """

    def disassociate_domain(self, FleetArn: str, DomainName: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.disassociate_domain)
        [Show boto3-stubs documentation](./client.md#disassociate_domain)
        """

    def disassociate_website_authorization_provider(
        self, FleetArn: str, AuthorizationProviderId: str
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.disassociate_website_authorization_provider)
        [Show boto3-stubs documentation](./client.md#disassociate_website_authorization_provider)
        """

    def disassociate_website_certificate_authority(
        self, FleetArn: str, WebsiteCaId: str
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.disassociate_website_certificate_authority)
        [Show boto3-stubs documentation](./client.md#disassociate_website_certificate_authority)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.generate_presigned_url)
        [Show boto3-stubs documentation](./client.md#generate_presigned_url)
        """

    def list_devices(
        self, FleetArn: str, NextToken: str = None, MaxResults: int = None
    ) -> ListDevicesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.list_devices)
        [Show boto3-stubs documentation](./client.md#list_devices)
        """

    def list_domains(
        self, FleetArn: str, NextToken: str = None, MaxResults: int = None
    ) -> ListDomainsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.list_domains)
        [Show boto3-stubs documentation](./client.md#list_domains)
        """

    def list_fleets(
        self, NextToken: str = None, MaxResults: int = None
    ) -> ListFleetsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.list_fleets)
        [Show boto3-stubs documentation](./client.md#list_fleets)
        """

    def list_tags_for_resource(self, ResourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](./client.md#list_tags_for_resource)
        """

    def list_website_authorization_providers(
        self, FleetArn: str, NextToken: str = None, MaxResults: int = None
    ) -> ListWebsiteAuthorizationProvidersResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.list_website_authorization_providers)
        [Show boto3-stubs documentation](./client.md#list_website_authorization_providers)
        """

    def list_website_certificate_authorities(
        self, FleetArn: str, MaxResults: int = None, NextToken: str = None
    ) -> ListWebsiteCertificateAuthoritiesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.list_website_certificate_authorities)
        [Show boto3-stubs documentation](./client.md#list_website_certificate_authorities)
        """

    def restore_domain_access(self, FleetArn: str, DomainName: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.restore_domain_access)
        [Show boto3-stubs documentation](./client.md#restore_domain_access)
        """

    def revoke_domain_access(self, FleetArn: str, DomainName: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.revoke_domain_access)
        [Show boto3-stubs documentation](./client.md#revoke_domain_access)
        """

    def sign_out_user(self, FleetArn: str, Username: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.sign_out_user)
        [Show boto3-stubs documentation](./client.md#sign_out_user)
        """

    def tag_resource(self, ResourceArn: str, Tags: Dict[str, str]) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.tag_resource)
        [Show boto3-stubs documentation](./client.md#tag_resource)
        """

    def untag_resource(self, ResourceArn: str, TagKeys: List[str]) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.untag_resource)
        [Show boto3-stubs documentation](./client.md#untag_resource)
        """

    def update_audit_stream_configuration(
        self, FleetArn: str, AuditStreamArn: str = None
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.update_audit_stream_configuration)
        [Show boto3-stubs documentation](./client.md#update_audit_stream_configuration)
        """

    def update_company_network_configuration(
        self, FleetArn: str, VpcId: str, SubnetIds: List[str], SecurityGroupIds: List[str]
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.update_company_network_configuration)
        [Show boto3-stubs documentation](./client.md#update_company_network_configuration)
        """

    def update_device_policy_configuration(
        self, FleetArn: str, DeviceCaCertificate: str = None
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.update_device_policy_configuration)
        [Show boto3-stubs documentation](./client.md#update_device_policy_configuration)
        """

    def update_domain_metadata(
        self, FleetArn: str, DomainName: str, DisplayName: str = None
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.update_domain_metadata)
        [Show boto3-stubs documentation](./client.md#update_domain_metadata)
        """

    def update_fleet_metadata(
        self, FleetArn: str, DisplayName: str = None, OptimizeForEndUserLocation: bool = None
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.update_fleet_metadata)
        [Show boto3-stubs documentation](./client.md#update_fleet_metadata)
        """

    def update_identity_provider_configuration(
        self,
        FleetArn: str,
        IdentityProviderType: Literal["SAML"],
        IdentityProviderSamlMetadata: str = None,
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/worklink.html#WorkLink.Client.update_identity_provider_configuration)
        [Show boto3-stubs documentation](./client.md#update_identity_provider_configuration)
        """
