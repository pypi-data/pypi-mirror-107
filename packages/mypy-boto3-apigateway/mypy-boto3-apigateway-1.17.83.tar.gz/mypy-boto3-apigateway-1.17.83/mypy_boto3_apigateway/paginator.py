"""
Type annotations for apigateway service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_apigateway import APIGatewayClient
    from mypy_boto3_apigateway.paginator import (
        GetApiKeysPaginator,
        GetAuthorizersPaginator,
        GetBasePathMappingsPaginator,
        GetClientCertificatesPaginator,
        GetDeploymentsPaginator,
        GetDocumentationPartsPaginator,
        GetDocumentationVersionsPaginator,
        GetDomainNamesPaginator,
        GetGatewayResponsesPaginator,
        GetModelsPaginator,
        GetRequestValidatorsPaginator,
        GetResourcesPaginator,
        GetRestApisPaginator,
        GetSdkTypesPaginator,
        GetUsagePaginator,
        GetUsagePlanKeysPaginator,
        GetUsagePlansPaginator,
        GetVpcLinksPaginator,
    )

    client: APIGatewayClient = boto3.client("apigateway")

    get_api_keys_paginator: GetApiKeysPaginator = client.get_paginator("get_api_keys")
    get_authorizers_paginator: GetAuthorizersPaginator = client.get_paginator("get_authorizers")
    get_base_path_mappings_paginator: GetBasePathMappingsPaginator = client.get_paginator("get_base_path_mappings")
    get_client_certificates_paginator: GetClientCertificatesPaginator = client.get_paginator("get_client_certificates")
    get_deployments_paginator: GetDeploymentsPaginator = client.get_paginator("get_deployments")
    get_documentation_parts_paginator: GetDocumentationPartsPaginator = client.get_paginator("get_documentation_parts")
    get_documentation_versions_paginator: GetDocumentationVersionsPaginator = client.get_paginator("get_documentation_versions")
    get_domain_names_paginator: GetDomainNamesPaginator = client.get_paginator("get_domain_names")
    get_gateway_responses_paginator: GetGatewayResponsesPaginator = client.get_paginator("get_gateway_responses")
    get_models_paginator: GetModelsPaginator = client.get_paginator("get_models")
    get_request_validators_paginator: GetRequestValidatorsPaginator = client.get_paginator("get_request_validators")
    get_resources_paginator: GetResourcesPaginator = client.get_paginator("get_resources")
    get_rest_apis_paginator: GetRestApisPaginator = client.get_paginator("get_rest_apis")
    get_sdk_types_paginator: GetSdkTypesPaginator = client.get_paginator("get_sdk_types")
    get_usage_paginator: GetUsagePaginator = client.get_paginator("get_usage")
    get_usage_plan_keys_paginator: GetUsagePlanKeysPaginator = client.get_paginator("get_usage_plan_keys")
    get_usage_plans_paginator: GetUsagePlansPaginator = client.get_paginator("get_usage_plans")
    get_vpc_links_paginator: GetVpcLinksPaginator = client.get_paginator("get_vpc_links")
    ```
"""
from typing import Iterator, List

from botocore.paginate import Paginator as Boto3Paginator

from .literals import DocumentationPartTypeType, LocationStatusTypeType
from .type_defs import (
    ApiKeysTypeDef,
    AuthorizersTypeDef,
    BasePathMappingsTypeDef,
    ClientCertificatesTypeDef,
    DeploymentsTypeDef,
    DocumentationPartsTypeDef,
    DocumentationVersionsTypeDef,
    DomainNamesTypeDef,
    GatewayResponsesTypeDef,
    ModelsTypeDef,
    PaginatorConfigTypeDef,
    RequestValidatorsTypeDef,
    ResourcesTypeDef,
    RestApisTypeDef,
    SdkTypesTypeDef,
    UsagePlanKeysTypeDef,
    UsagePlansTypeDef,
    UsageTypeDef,
    VpcLinksTypeDef,
)

__all__ = (
    "GetApiKeysPaginator",
    "GetAuthorizersPaginator",
    "GetBasePathMappingsPaginator",
    "GetClientCertificatesPaginator",
    "GetDeploymentsPaginator",
    "GetDocumentationPartsPaginator",
    "GetDocumentationVersionsPaginator",
    "GetDomainNamesPaginator",
    "GetGatewayResponsesPaginator",
    "GetModelsPaginator",
    "GetRequestValidatorsPaginator",
    "GetResourcesPaginator",
    "GetRestApisPaginator",
    "GetSdkTypesPaginator",
    "GetUsagePaginator",
    "GetUsagePlanKeysPaginator",
    "GetUsagePlansPaginator",
    "GetVpcLinksPaginator",
)


class GetApiKeysPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetApiKeys)[Show boto3-stubs documentation](./paginators.md#getapikeyspaginator)
    """

    def paginate(
        self,
        nameQuery: str = None,
        customerId: str = None,
        includeValues: bool = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ApiKeysTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetApiKeys.paginate)
        [Show boto3-stubs documentation](./paginators.md#getapikeyspaginator)
        """


class GetAuthorizersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetAuthorizers)[Show boto3-stubs documentation](./paginators.md#getauthorizerspaginator)
    """

    def paginate(
        self, restApiId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[AuthorizersTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetAuthorizers.paginate)
        [Show boto3-stubs documentation](./paginators.md#getauthorizerspaginator)
        """


class GetBasePathMappingsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetBasePathMappings)[Show boto3-stubs documentation](./paginators.md#getbasepathmappingspaginator)
    """

    def paginate(
        self, domainName: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[BasePathMappingsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetBasePathMappings.paginate)
        [Show boto3-stubs documentation](./paginators.md#getbasepathmappingspaginator)
        """


class GetClientCertificatesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetClientCertificates)[Show boto3-stubs documentation](./paginators.md#getclientcertificatespaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ClientCertificatesTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetClientCertificates.paginate)
        [Show boto3-stubs documentation](./paginators.md#getclientcertificatespaginator)
        """


class GetDeploymentsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetDeployments)[Show boto3-stubs documentation](./paginators.md#getdeploymentspaginator)
    """

    def paginate(
        self, restApiId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[DeploymentsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetDeployments.paginate)
        [Show boto3-stubs documentation](./paginators.md#getdeploymentspaginator)
        """


class GetDocumentationPartsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetDocumentationParts)[Show boto3-stubs documentation](./paginators.md#getdocumentationpartspaginator)
    """

    def paginate(
        self,
        restApiId: str,
        type: DocumentationPartTypeType = None,
        nameQuery: str = None,
        path: str = None,
        locationStatus: LocationStatusTypeType = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DocumentationPartsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetDocumentationParts.paginate)
        [Show boto3-stubs documentation](./paginators.md#getdocumentationpartspaginator)
        """


class GetDocumentationVersionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetDocumentationVersions)[Show boto3-stubs documentation](./paginators.md#getdocumentationversionspaginator)
    """

    def paginate(
        self, restApiId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[DocumentationVersionsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetDocumentationVersions.paginate)
        [Show boto3-stubs documentation](./paginators.md#getdocumentationversionspaginator)
        """


class GetDomainNamesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetDomainNames)[Show boto3-stubs documentation](./paginators.md#getdomainnamespaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[DomainNamesTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetDomainNames.paginate)
        [Show boto3-stubs documentation](./paginators.md#getdomainnamespaginator)
        """


class GetGatewayResponsesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetGatewayResponses)[Show boto3-stubs documentation](./paginators.md#getgatewayresponsespaginator)
    """

    def paginate(
        self, restApiId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[GatewayResponsesTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetGatewayResponses.paginate)
        [Show boto3-stubs documentation](./paginators.md#getgatewayresponsespaginator)
        """


class GetModelsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetModels)[Show boto3-stubs documentation](./paginators.md#getmodelspaginator)
    """

    def paginate(
        self, restApiId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ModelsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetModels.paginate)
        [Show boto3-stubs documentation](./paginators.md#getmodelspaginator)
        """


class GetRequestValidatorsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetRequestValidators)[Show boto3-stubs documentation](./paginators.md#getrequestvalidatorspaginator)
    """

    def paginate(
        self, restApiId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[RequestValidatorsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetRequestValidators.paginate)
        [Show boto3-stubs documentation](./paginators.md#getrequestvalidatorspaginator)
        """


class GetResourcesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetResources)[Show boto3-stubs documentation](./paginators.md#getresourcespaginator)
    """

    def paginate(
        self,
        restApiId: str,
        embed: List[str] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ResourcesTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetResources.paginate)
        [Show boto3-stubs documentation](./paginators.md#getresourcespaginator)
        """


class GetRestApisPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetRestApis)[Show boto3-stubs documentation](./paginators.md#getrestapispaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[RestApisTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetRestApis.paginate)
        [Show boto3-stubs documentation](./paginators.md#getrestapispaginator)
        """


class GetSdkTypesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetSdkTypes)[Show boto3-stubs documentation](./paginators.md#getsdktypespaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[SdkTypesTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetSdkTypes.paginate)
        [Show boto3-stubs documentation](./paginators.md#getsdktypespaginator)
        """


class GetUsagePaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetUsage)[Show boto3-stubs documentation](./paginators.md#getusagepaginator)
    """

    def paginate(
        self,
        usagePlanId: str,
        startDate: str,
        endDate: str,
        keyId: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[UsageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetUsage.paginate)
        [Show boto3-stubs documentation](./paginators.md#getusagepaginator)
        """


class GetUsagePlanKeysPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetUsagePlanKeys)[Show boto3-stubs documentation](./paginators.md#getusageplankeyspaginator)
    """

    def paginate(
        self,
        usagePlanId: str,
        nameQuery: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[UsagePlanKeysTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetUsagePlanKeys.paginate)
        [Show boto3-stubs documentation](./paginators.md#getusageplankeyspaginator)
        """


class GetUsagePlansPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetUsagePlans)[Show boto3-stubs documentation](./paginators.md#getusageplanspaginator)
    """

    def paginate(
        self, keyId: str = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[UsagePlansTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetUsagePlans.paginate)
        [Show boto3-stubs documentation](./paginators.md#getusageplanspaginator)
        """


class GetVpcLinksPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetVpcLinks)[Show boto3-stubs documentation](./paginators.md#getvpclinkspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[VpcLinksTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/apigateway.html#APIGateway.Paginator.GetVpcLinks.paginate)
        [Show boto3-stubs documentation](./paginators.md#getvpclinkspaginator)
        """
