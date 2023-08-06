"""
Type annotations for greengrassv2 service client.

[Open documentation](./client.md)

Usage::

    ```python
    import boto3
    from mypy_boto3_greengrassv2 import GreengrassV2Client

    client: GreengrassV2Client = boto3.client("greengrassv2")
    ```
"""
import sys
from typing import IO, Any, Dict, List, Type, Union, overload

from botocore.client import ClientMeta

from .literals import (
    ComponentVisibilityScopeType,
    CoreDeviceStatusType,
    DeploymentHistoryFilterType,
    RecipeOutputFormatType,
)
from .paginator import (
    ListComponentsPaginator,
    ListComponentVersionsPaginator,
    ListCoreDevicesPaginator,
    ListDeploymentsPaginator,
    ListEffectiveDeploymentsPaginator,
    ListInstalledComponentsPaginator,
)
from .type_defs import (
    CancelDeploymentResponseTypeDef,
    ComponentCandidateTypeDef,
    ComponentDeploymentSpecificationTypeDef,
    ComponentPlatformTypeDef,
    CreateComponentVersionResponseTypeDef,
    CreateDeploymentResponseTypeDef,
    DeploymentIoTJobConfigurationTypeDef,
    DeploymentPoliciesTypeDef,
    DescribeComponentResponseTypeDef,
    GetComponentResponseTypeDef,
    GetComponentVersionArtifactResponseTypeDef,
    GetCoreDeviceResponseTypeDef,
    GetDeploymentResponseTypeDef,
    LambdaFunctionRecipeSourceTypeDef,
    ListComponentsResponseTypeDef,
    ListComponentVersionsResponseTypeDef,
    ListCoreDevicesResponseTypeDef,
    ListDeploymentsResponseTypeDef,
    ListEffectiveDeploymentsResponseTypeDef,
    ListInstalledComponentsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ResolveComponentCandidatesResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("GreengrassV2Client",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class GreengrassV2Client:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/greengrassv2.html#GreengrassV2.Client)
    [Show boto3-stubs documentation](./client.md)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/greengrassv2.html#GreengrassV2.Client.can_paginate)
        [Show boto3-stubs documentation](./client.md#can_paginate)
        """

    def cancel_deployment(self, deploymentId: str) -> CancelDeploymentResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/greengrassv2.html#GreengrassV2.Client.cancel_deployment)
        [Show boto3-stubs documentation](./client.md#cancel_deployment)
        """

    def create_component_version(
        self,
        inlineRecipe: Union[bytes, IO[bytes]] = None,
        lambdaFunction: LambdaFunctionRecipeSourceTypeDef = None,
        tags: Dict[str, str] = None,
    ) -> CreateComponentVersionResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/greengrassv2.html#GreengrassV2.Client.create_component_version)
        [Show boto3-stubs documentation](./client.md#create_component_version)
        """

    def create_deployment(
        self,
        targetArn: str,
        deploymentName: str = None,
        components: Dict[str, "ComponentDeploymentSpecificationTypeDef"] = None,
        iotJobConfiguration: "DeploymentIoTJobConfigurationTypeDef" = None,
        deploymentPolicies: "DeploymentPoliciesTypeDef" = None,
        tags: Dict[str, str] = None,
    ) -> CreateDeploymentResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/greengrassv2.html#GreengrassV2.Client.create_deployment)
        [Show boto3-stubs documentation](./client.md#create_deployment)
        """

    def delete_component(self, arn: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/greengrassv2.html#GreengrassV2.Client.delete_component)
        [Show boto3-stubs documentation](./client.md#delete_component)
        """

    def delete_core_device(self, coreDeviceThingName: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/greengrassv2.html#GreengrassV2.Client.delete_core_device)
        [Show boto3-stubs documentation](./client.md#delete_core_device)
        """

    def describe_component(self, arn: str) -> DescribeComponentResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/greengrassv2.html#GreengrassV2.Client.describe_component)
        [Show boto3-stubs documentation](./client.md#describe_component)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/greengrassv2.html#GreengrassV2.Client.generate_presigned_url)
        [Show boto3-stubs documentation](./client.md#generate_presigned_url)
        """

    def get_component(
        self, arn: str, recipeOutputFormat: RecipeOutputFormatType = None
    ) -> GetComponentResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/greengrassv2.html#GreengrassV2.Client.get_component)
        [Show boto3-stubs documentation](./client.md#get_component)
        """

    def get_component_version_artifact(
        self, arn: str, artifactName: str
    ) -> GetComponentVersionArtifactResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/greengrassv2.html#GreengrassV2.Client.get_component_version_artifact)
        [Show boto3-stubs documentation](./client.md#get_component_version_artifact)
        """

    def get_core_device(self, coreDeviceThingName: str) -> GetCoreDeviceResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/greengrassv2.html#GreengrassV2.Client.get_core_device)
        [Show boto3-stubs documentation](./client.md#get_core_device)
        """

    def get_deployment(self, deploymentId: str) -> GetDeploymentResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/greengrassv2.html#GreengrassV2.Client.get_deployment)
        [Show boto3-stubs documentation](./client.md#get_deployment)
        """

    def list_component_versions(
        self, arn: str, maxResults: int = None, nextToken: str = None
    ) -> ListComponentVersionsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/greengrassv2.html#GreengrassV2.Client.list_component_versions)
        [Show boto3-stubs documentation](./client.md#list_component_versions)
        """

    def list_components(
        self,
        scope: ComponentVisibilityScopeType = None,
        maxResults: int = None,
        nextToken: str = None,
    ) -> ListComponentsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/greengrassv2.html#GreengrassV2.Client.list_components)
        [Show boto3-stubs documentation](./client.md#list_components)
        """

    def list_core_devices(
        self,
        thingGroupArn: str = None,
        status: CoreDeviceStatusType = None,
        maxResults: int = None,
        nextToken: str = None,
    ) -> ListCoreDevicesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/greengrassv2.html#GreengrassV2.Client.list_core_devices)
        [Show boto3-stubs documentation](./client.md#list_core_devices)
        """

    def list_deployments(
        self,
        targetArn: str = None,
        historyFilter: DeploymentHistoryFilterType = None,
        maxResults: int = None,
        nextToken: str = None,
    ) -> ListDeploymentsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/greengrassv2.html#GreengrassV2.Client.list_deployments)
        [Show boto3-stubs documentation](./client.md#list_deployments)
        """

    def list_effective_deployments(
        self, coreDeviceThingName: str, maxResults: int = None, nextToken: str = None
    ) -> ListEffectiveDeploymentsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/greengrassv2.html#GreengrassV2.Client.list_effective_deployments)
        [Show boto3-stubs documentation](./client.md#list_effective_deployments)
        """

    def list_installed_components(
        self, coreDeviceThingName: str, maxResults: int = None, nextToken: str = None
    ) -> ListInstalledComponentsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/greengrassv2.html#GreengrassV2.Client.list_installed_components)
        [Show boto3-stubs documentation](./client.md#list_installed_components)
        """

    def list_tags_for_resource(self, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/greengrassv2.html#GreengrassV2.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](./client.md#list_tags_for_resource)
        """

    def resolve_component_candidates(
        self,
        platform: "ComponentPlatformTypeDef",
        componentCandidates: List[ComponentCandidateTypeDef],
    ) -> ResolveComponentCandidatesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/greengrassv2.html#GreengrassV2.Client.resolve_component_candidates)
        [Show boto3-stubs documentation](./client.md#resolve_component_candidates)
        """

    def tag_resource(self, resourceArn: str, tags: Dict[str, str]) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/greengrassv2.html#GreengrassV2.Client.tag_resource)
        [Show boto3-stubs documentation](./client.md#tag_resource)
        """

    def untag_resource(self, resourceArn: str, tagKeys: List[str]) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/greengrassv2.html#GreengrassV2.Client.untag_resource)
        [Show boto3-stubs documentation](./client.md#untag_resource)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_component_versions"]
    ) -> ListComponentVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListComponentVersions)[Show boto3-stubs documentation](./paginators.md#listcomponentversionspaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_components"]) -> ListComponentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListComponents)[Show boto3-stubs documentation](./paginators.md#listcomponentspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_core_devices"]
    ) -> ListCoreDevicesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListCoreDevices)[Show boto3-stubs documentation](./paginators.md#listcoredevicespaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_deployments"]
    ) -> ListDeploymentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListDeployments)[Show boto3-stubs documentation](./paginators.md#listdeploymentspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_effective_deployments"]
    ) -> ListEffectiveDeploymentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListEffectiveDeployments)[Show boto3-stubs documentation](./paginators.md#listeffectivedeploymentspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_installed_components"]
    ) -> ListInstalledComponentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListInstalledComponents)[Show boto3-stubs documentation](./paginators.md#listinstalledcomponentspaginator)
        """
