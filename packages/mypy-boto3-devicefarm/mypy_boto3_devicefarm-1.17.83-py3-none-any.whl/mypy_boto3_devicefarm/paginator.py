"""
Type annotations for devicefarm service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_devicefarm import DeviceFarmClient
    from mypy_boto3_devicefarm.paginator import (
        GetOfferingStatusPaginator,
        ListArtifactsPaginator,
        ListDeviceInstancesPaginator,
        ListDevicePoolsPaginator,
        ListDevicesPaginator,
        ListInstanceProfilesPaginator,
        ListJobsPaginator,
        ListNetworkProfilesPaginator,
        ListOfferingPromotionsPaginator,
        ListOfferingTransactionsPaginator,
        ListOfferingsPaginator,
        ListProjectsPaginator,
        ListRemoteAccessSessionsPaginator,
        ListRunsPaginator,
        ListSamplesPaginator,
        ListSuitesPaginator,
        ListTestsPaginator,
        ListUniqueProblemsPaginator,
        ListUploadsPaginator,
        ListVPCEConfigurationsPaginator,
    )

    client: DeviceFarmClient = boto3.client("devicefarm")

    get_offering_status_paginator: GetOfferingStatusPaginator = client.get_paginator("get_offering_status")
    list_artifacts_paginator: ListArtifactsPaginator = client.get_paginator("list_artifacts")
    list_device_instances_paginator: ListDeviceInstancesPaginator = client.get_paginator("list_device_instances")
    list_device_pools_paginator: ListDevicePoolsPaginator = client.get_paginator("list_device_pools")
    list_devices_paginator: ListDevicesPaginator = client.get_paginator("list_devices")
    list_instance_profiles_paginator: ListInstanceProfilesPaginator = client.get_paginator("list_instance_profiles")
    list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    list_network_profiles_paginator: ListNetworkProfilesPaginator = client.get_paginator("list_network_profiles")
    list_offering_promotions_paginator: ListOfferingPromotionsPaginator = client.get_paginator("list_offering_promotions")
    list_offering_transactions_paginator: ListOfferingTransactionsPaginator = client.get_paginator("list_offering_transactions")
    list_offerings_paginator: ListOfferingsPaginator = client.get_paginator("list_offerings")
    list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
    list_remote_access_sessions_paginator: ListRemoteAccessSessionsPaginator = client.get_paginator("list_remote_access_sessions")
    list_runs_paginator: ListRunsPaginator = client.get_paginator("list_runs")
    list_samples_paginator: ListSamplesPaginator = client.get_paginator("list_samples")
    list_suites_paginator: ListSuitesPaginator = client.get_paginator("list_suites")
    list_tests_paginator: ListTestsPaginator = client.get_paginator("list_tests")
    list_unique_problems_paginator: ListUniqueProblemsPaginator = client.get_paginator("list_unique_problems")
    list_uploads_paginator: ListUploadsPaginator = client.get_paginator("list_uploads")
    list_vpce_configurations_paginator: ListVPCEConfigurationsPaginator = client.get_paginator("list_vpce_configurations")
    ```
"""
from typing import Iterator, List

from botocore.paginate import Paginator as Boto3Paginator

from .literals import (
    ArtifactCategoryType,
    DevicePoolTypeType,
    NetworkProfileTypeType,
    UploadTypeType,
)
from .type_defs import (
    DeviceFilterTypeDef,
    GetOfferingStatusResultTypeDef,
    ListArtifactsResultTypeDef,
    ListDeviceInstancesResultTypeDef,
    ListDevicePoolsResultTypeDef,
    ListDevicesResultTypeDef,
    ListInstanceProfilesResultTypeDef,
    ListJobsResultTypeDef,
    ListNetworkProfilesResultTypeDef,
    ListOfferingPromotionsResultTypeDef,
    ListOfferingsResultTypeDef,
    ListOfferingTransactionsResultTypeDef,
    ListProjectsResultTypeDef,
    ListRemoteAccessSessionsResultTypeDef,
    ListRunsResultTypeDef,
    ListSamplesResultTypeDef,
    ListSuitesResultTypeDef,
    ListTestsResultTypeDef,
    ListUniqueProblemsResultTypeDef,
    ListUploadsResultTypeDef,
    ListVPCEConfigurationsResultTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "GetOfferingStatusPaginator",
    "ListArtifactsPaginator",
    "ListDeviceInstancesPaginator",
    "ListDevicePoolsPaginator",
    "ListDevicesPaginator",
    "ListInstanceProfilesPaginator",
    "ListJobsPaginator",
    "ListNetworkProfilesPaginator",
    "ListOfferingPromotionsPaginator",
    "ListOfferingTransactionsPaginator",
    "ListOfferingsPaginator",
    "ListProjectsPaginator",
    "ListRemoteAccessSessionsPaginator",
    "ListRunsPaginator",
    "ListSamplesPaginator",
    "ListSuitesPaginator",
    "ListTestsPaginator",
    "ListUniqueProblemsPaginator",
    "ListUploadsPaginator",
    "ListVPCEConfigurationsPaginator",
)


class GetOfferingStatusPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.GetOfferingStatus)[Show boto3-stubs documentation](./paginators.md#getofferingstatuspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[GetOfferingStatusResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.GetOfferingStatus.paginate)
        [Show boto3-stubs documentation](./paginators.md#getofferingstatuspaginator)
        """


class ListArtifactsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListArtifacts)[Show boto3-stubs documentation](./paginators.md#listartifactspaginator)
    """

    def paginate(
        self, arn: str, type: ArtifactCategoryType, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListArtifactsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListArtifacts.paginate)
        [Show boto3-stubs documentation](./paginators.md#listartifactspaginator)
        """


class ListDeviceInstancesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListDeviceInstances)[Show boto3-stubs documentation](./paginators.md#listdeviceinstancespaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListDeviceInstancesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListDeviceInstances.paginate)
        [Show boto3-stubs documentation](./paginators.md#listdeviceinstancespaginator)
        """


class ListDevicePoolsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListDevicePools)[Show boto3-stubs documentation](./paginators.md#listdevicepoolspaginator)
    """

    def paginate(
        self,
        arn: str,
        type: DevicePoolTypeType = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListDevicePoolsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListDevicePools.paginate)
        [Show boto3-stubs documentation](./paginators.md#listdevicepoolspaginator)
        """


class ListDevicesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListDevices)[Show boto3-stubs documentation](./paginators.md#listdevicespaginator)
    """

    def paginate(
        self,
        arn: str = None,
        filters: List["DeviceFilterTypeDef"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListDevicesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListDevices.paginate)
        [Show boto3-stubs documentation](./paginators.md#listdevicespaginator)
        """


class ListInstanceProfilesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListInstanceProfiles)[Show boto3-stubs documentation](./paginators.md#listinstanceprofilespaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListInstanceProfilesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListInstanceProfiles.paginate)
        [Show boto3-stubs documentation](./paginators.md#listinstanceprofilespaginator)
        """


class ListJobsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListJobs)[Show boto3-stubs documentation](./paginators.md#listjobspaginator)
    """

    def paginate(
        self, arn: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListJobsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListJobs.paginate)
        [Show boto3-stubs documentation](./paginators.md#listjobspaginator)
        """


class ListNetworkProfilesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListNetworkProfiles)[Show boto3-stubs documentation](./paginators.md#listnetworkprofilespaginator)
    """

    def paginate(
        self,
        arn: str,
        type: NetworkProfileTypeType = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListNetworkProfilesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListNetworkProfiles.paginate)
        [Show boto3-stubs documentation](./paginators.md#listnetworkprofilespaginator)
        """


class ListOfferingPromotionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListOfferingPromotions)[Show boto3-stubs documentation](./paginators.md#listofferingpromotionspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListOfferingPromotionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListOfferingPromotions.paginate)
        [Show boto3-stubs documentation](./paginators.md#listofferingpromotionspaginator)
        """


class ListOfferingTransactionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListOfferingTransactions)[Show boto3-stubs documentation](./paginators.md#listofferingtransactionspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListOfferingTransactionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListOfferingTransactions.paginate)
        [Show boto3-stubs documentation](./paginators.md#listofferingtransactionspaginator)
        """


class ListOfferingsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListOfferings)[Show boto3-stubs documentation](./paginators.md#listofferingspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListOfferingsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListOfferings.paginate)
        [Show boto3-stubs documentation](./paginators.md#listofferingspaginator)
        """


class ListProjectsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListProjects)[Show boto3-stubs documentation](./paginators.md#listprojectspaginator)
    """

    def paginate(
        self, arn: str = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListProjectsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListProjects.paginate)
        [Show boto3-stubs documentation](./paginators.md#listprojectspaginator)
        """


class ListRemoteAccessSessionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListRemoteAccessSessions)[Show boto3-stubs documentation](./paginators.md#listremoteaccesssessionspaginator)
    """

    def paginate(
        self, arn: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListRemoteAccessSessionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListRemoteAccessSessions.paginate)
        [Show boto3-stubs documentation](./paginators.md#listremoteaccesssessionspaginator)
        """


class ListRunsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListRuns)[Show boto3-stubs documentation](./paginators.md#listrunspaginator)
    """

    def paginate(
        self, arn: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListRunsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListRuns.paginate)
        [Show boto3-stubs documentation](./paginators.md#listrunspaginator)
        """


class ListSamplesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListSamples)[Show boto3-stubs documentation](./paginators.md#listsamplespaginator)
    """

    def paginate(
        self, arn: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListSamplesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListSamples.paginate)
        [Show boto3-stubs documentation](./paginators.md#listsamplespaginator)
        """


class ListSuitesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListSuites)[Show boto3-stubs documentation](./paginators.md#listsuitespaginator)
    """

    def paginate(
        self, arn: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListSuitesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListSuites.paginate)
        [Show boto3-stubs documentation](./paginators.md#listsuitespaginator)
        """


class ListTestsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListTests)[Show boto3-stubs documentation](./paginators.md#listtestspaginator)
    """

    def paginate(
        self, arn: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListTestsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListTests.paginate)
        [Show boto3-stubs documentation](./paginators.md#listtestspaginator)
        """


class ListUniqueProblemsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListUniqueProblems)[Show boto3-stubs documentation](./paginators.md#listuniqueproblemspaginator)
    """

    def paginate(
        self, arn: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListUniqueProblemsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListUniqueProblems.paginate)
        [Show boto3-stubs documentation](./paginators.md#listuniqueproblemspaginator)
        """


class ListUploadsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListUploads)[Show boto3-stubs documentation](./paginators.md#listuploadspaginator)
    """

    def paginate(
        self, arn: str, type: UploadTypeType = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListUploadsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListUploads.paginate)
        [Show boto3-stubs documentation](./paginators.md#listuploadspaginator)
        """


class ListVPCEConfigurationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListVPCEConfigurations)[Show boto3-stubs documentation](./paginators.md#listvpceconfigurationspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListVPCEConfigurationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/devicefarm.html#DeviceFarm.Paginator.ListVPCEConfigurations.paginate)
        [Show boto3-stubs documentation](./paginators.md#listvpceconfigurationspaginator)
        """
