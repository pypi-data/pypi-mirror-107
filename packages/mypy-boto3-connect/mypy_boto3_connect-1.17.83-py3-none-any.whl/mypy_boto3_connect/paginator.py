"""
Type annotations for connect service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_connect import ConnectClient
    from mypy_boto3_connect.paginator import (
        GetMetricDataPaginator,
        ListApprovedOriginsPaginator,
        ListContactFlowsPaginator,
        ListHoursOfOperationsPaginator,
        ListInstanceAttributesPaginator,
        ListInstanceStorageConfigsPaginator,
        ListInstancesPaginator,
        ListIntegrationAssociationsPaginator,
        ListLambdaFunctionsPaginator,
        ListLexBotsPaginator,
        ListPhoneNumbersPaginator,
        ListPromptsPaginator,
        ListQueueQuickConnectsPaginator,
        ListQueuesPaginator,
        ListQuickConnectsPaginator,
        ListRoutingProfileQueuesPaginator,
        ListRoutingProfilesPaginator,
        ListSecurityKeysPaginator,
        ListSecurityProfilesPaginator,
        ListUseCasesPaginator,
        ListUserHierarchyGroupsPaginator,
        ListUsersPaginator,
    )

    client: ConnectClient = boto3.client("connect")

    get_metric_data_paginator: GetMetricDataPaginator = client.get_paginator("get_metric_data")
    list_approved_origins_paginator: ListApprovedOriginsPaginator = client.get_paginator("list_approved_origins")
    list_contact_flows_paginator: ListContactFlowsPaginator = client.get_paginator("list_contact_flows")
    list_hours_of_operations_paginator: ListHoursOfOperationsPaginator = client.get_paginator("list_hours_of_operations")
    list_instance_attributes_paginator: ListInstanceAttributesPaginator = client.get_paginator("list_instance_attributes")
    list_instance_storage_configs_paginator: ListInstanceStorageConfigsPaginator = client.get_paginator("list_instance_storage_configs")
    list_instances_paginator: ListInstancesPaginator = client.get_paginator("list_instances")
    list_integration_associations_paginator: ListIntegrationAssociationsPaginator = client.get_paginator("list_integration_associations")
    list_lambda_functions_paginator: ListLambdaFunctionsPaginator = client.get_paginator("list_lambda_functions")
    list_lex_bots_paginator: ListLexBotsPaginator = client.get_paginator("list_lex_bots")
    list_phone_numbers_paginator: ListPhoneNumbersPaginator = client.get_paginator("list_phone_numbers")
    list_prompts_paginator: ListPromptsPaginator = client.get_paginator("list_prompts")
    list_queue_quick_connects_paginator: ListQueueQuickConnectsPaginator = client.get_paginator("list_queue_quick_connects")
    list_queues_paginator: ListQueuesPaginator = client.get_paginator("list_queues")
    list_quick_connects_paginator: ListQuickConnectsPaginator = client.get_paginator("list_quick_connects")
    list_routing_profile_queues_paginator: ListRoutingProfileQueuesPaginator = client.get_paginator("list_routing_profile_queues")
    list_routing_profiles_paginator: ListRoutingProfilesPaginator = client.get_paginator("list_routing_profiles")
    list_security_keys_paginator: ListSecurityKeysPaginator = client.get_paginator("list_security_keys")
    list_security_profiles_paginator: ListSecurityProfilesPaginator = client.get_paginator("list_security_profiles")
    list_use_cases_paginator: ListUseCasesPaginator = client.get_paginator("list_use_cases")
    list_user_hierarchy_groups_paginator: ListUserHierarchyGroupsPaginator = client.get_paginator("list_user_hierarchy_groups")
    list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
    ```
"""
from datetime import datetime
from typing import Iterator, List

from botocore.paginate import Paginator as Boto3Paginator

from .literals import (
    ContactFlowTypeType,
    GroupingType,
    InstanceStorageResourceTypeType,
    PhoneNumberCountryCodeType,
    PhoneNumberTypeType,
    QueueTypeType,
    QuickConnectTypeType,
)
from .type_defs import (
    FiltersTypeDef,
    GetMetricDataResponseTypeDef,
    HistoricalMetricTypeDef,
    ListApprovedOriginsResponseTypeDef,
    ListContactFlowsResponseTypeDef,
    ListHoursOfOperationsResponseTypeDef,
    ListInstanceAttributesResponseTypeDef,
    ListInstancesResponseTypeDef,
    ListInstanceStorageConfigsResponseTypeDef,
    ListIntegrationAssociationsResponseTypeDef,
    ListLambdaFunctionsResponseTypeDef,
    ListLexBotsResponseTypeDef,
    ListPhoneNumbersResponseTypeDef,
    ListPromptsResponseTypeDef,
    ListQueueQuickConnectsResponseTypeDef,
    ListQueuesResponseTypeDef,
    ListQuickConnectsResponseTypeDef,
    ListRoutingProfileQueuesResponseTypeDef,
    ListRoutingProfilesResponseTypeDef,
    ListSecurityKeysResponseTypeDef,
    ListSecurityProfilesResponseTypeDef,
    ListUseCasesResponseTypeDef,
    ListUserHierarchyGroupsResponseTypeDef,
    ListUsersResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "GetMetricDataPaginator",
    "ListApprovedOriginsPaginator",
    "ListContactFlowsPaginator",
    "ListHoursOfOperationsPaginator",
    "ListInstanceAttributesPaginator",
    "ListInstanceStorageConfigsPaginator",
    "ListInstancesPaginator",
    "ListIntegrationAssociationsPaginator",
    "ListLambdaFunctionsPaginator",
    "ListLexBotsPaginator",
    "ListPhoneNumbersPaginator",
    "ListPromptsPaginator",
    "ListQueueQuickConnectsPaginator",
    "ListQueuesPaginator",
    "ListQuickConnectsPaginator",
    "ListRoutingProfileQueuesPaginator",
    "ListRoutingProfilesPaginator",
    "ListSecurityKeysPaginator",
    "ListSecurityProfilesPaginator",
    "ListUseCasesPaginator",
    "ListUserHierarchyGroupsPaginator",
    "ListUsersPaginator",
)


class GetMetricDataPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.GetMetricData)[Show boto3-stubs documentation](./paginators.md#getmetricdatapaginator)
    """

    def paginate(
        self,
        InstanceId: str,
        StartTime: datetime,
        EndTime: datetime,
        Filters: FiltersTypeDef,
        HistoricalMetrics: List["HistoricalMetricTypeDef"],
        Groupings: List[GroupingType] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[GetMetricDataResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.GetMetricData.paginate)
        [Show boto3-stubs documentation](./paginators.md#getmetricdatapaginator)
        """


class ListApprovedOriginsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListApprovedOrigins)[Show boto3-stubs documentation](./paginators.md#listapprovedoriginspaginator)
    """

    def paginate(
        self, InstanceId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListApprovedOriginsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListApprovedOrigins.paginate)
        [Show boto3-stubs documentation](./paginators.md#listapprovedoriginspaginator)
        """


class ListContactFlowsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListContactFlows)[Show boto3-stubs documentation](./paginators.md#listcontactflowspaginator)
    """

    def paginate(
        self,
        InstanceId: str,
        ContactFlowTypes: List[ContactFlowTypeType] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListContactFlowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListContactFlows.paginate)
        [Show boto3-stubs documentation](./paginators.md#listcontactflowspaginator)
        """


class ListHoursOfOperationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListHoursOfOperations)[Show boto3-stubs documentation](./paginators.md#listhoursofoperationspaginator)
    """

    def paginate(
        self, InstanceId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListHoursOfOperationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListHoursOfOperations.paginate)
        [Show boto3-stubs documentation](./paginators.md#listhoursofoperationspaginator)
        """


class ListInstanceAttributesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListInstanceAttributes)[Show boto3-stubs documentation](./paginators.md#listinstanceattributespaginator)
    """

    def paginate(
        self, InstanceId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListInstanceAttributesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListInstanceAttributes.paginate)
        [Show boto3-stubs documentation](./paginators.md#listinstanceattributespaginator)
        """


class ListInstanceStorageConfigsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListInstanceStorageConfigs)[Show boto3-stubs documentation](./paginators.md#listinstancestorageconfigspaginator)
    """

    def paginate(
        self,
        InstanceId: str,
        ResourceType: InstanceStorageResourceTypeType,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListInstanceStorageConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListInstanceStorageConfigs.paginate)
        [Show boto3-stubs documentation](./paginators.md#listinstancestorageconfigspaginator)
        """


class ListInstancesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListInstances)[Show boto3-stubs documentation](./paginators.md#listinstancespaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListInstances.paginate)
        [Show boto3-stubs documentation](./paginators.md#listinstancespaginator)
        """


class ListIntegrationAssociationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListIntegrationAssociations)[Show boto3-stubs documentation](./paginators.md#listintegrationassociationspaginator)
    """

    def paginate(
        self, InstanceId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListIntegrationAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListIntegrationAssociations.paginate)
        [Show boto3-stubs documentation](./paginators.md#listintegrationassociationspaginator)
        """


class ListLambdaFunctionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListLambdaFunctions)[Show boto3-stubs documentation](./paginators.md#listlambdafunctionspaginator)
    """

    def paginate(
        self, InstanceId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListLambdaFunctionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListLambdaFunctions.paginate)
        [Show boto3-stubs documentation](./paginators.md#listlambdafunctionspaginator)
        """


class ListLexBotsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListLexBots)[Show boto3-stubs documentation](./paginators.md#listlexbotspaginator)
    """

    def paginate(
        self, InstanceId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListLexBotsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListLexBots.paginate)
        [Show boto3-stubs documentation](./paginators.md#listlexbotspaginator)
        """


class ListPhoneNumbersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListPhoneNumbers)[Show boto3-stubs documentation](./paginators.md#listphonenumberspaginator)
    """

    def paginate(
        self,
        InstanceId: str,
        PhoneNumberTypes: List[PhoneNumberTypeType] = None,
        PhoneNumberCountryCodes: List[PhoneNumberCountryCodeType] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListPhoneNumbersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListPhoneNumbers.paginate)
        [Show boto3-stubs documentation](./paginators.md#listphonenumberspaginator)
        """


class ListPromptsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListPrompts)[Show boto3-stubs documentation](./paginators.md#listpromptspaginator)
    """

    def paginate(
        self, InstanceId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListPromptsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListPrompts.paginate)
        [Show boto3-stubs documentation](./paginators.md#listpromptspaginator)
        """


class ListQueueQuickConnectsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListQueueQuickConnects)[Show boto3-stubs documentation](./paginators.md#listqueuequickconnectspaginator)
    """

    def paginate(
        self, InstanceId: str, QueueId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListQueueQuickConnectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListQueueQuickConnects.paginate)
        [Show boto3-stubs documentation](./paginators.md#listqueuequickconnectspaginator)
        """


class ListQueuesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListQueues)[Show boto3-stubs documentation](./paginators.md#listqueuespaginator)
    """

    def paginate(
        self,
        InstanceId: str,
        QueueTypes: List[QueueTypeType] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListQueuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListQueues.paginate)
        [Show boto3-stubs documentation](./paginators.md#listqueuespaginator)
        """


class ListQuickConnectsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListQuickConnects)[Show boto3-stubs documentation](./paginators.md#listquickconnectspaginator)
    """

    def paginate(
        self,
        InstanceId: str,
        QuickConnectTypes: List[QuickConnectTypeType] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListQuickConnectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListQuickConnects.paginate)
        [Show boto3-stubs documentation](./paginators.md#listquickconnectspaginator)
        """


class ListRoutingProfileQueuesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListRoutingProfileQueues)[Show boto3-stubs documentation](./paginators.md#listroutingprofilequeuespaginator)
    """

    def paginate(
        self,
        InstanceId: str,
        RoutingProfileId: str,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListRoutingProfileQueuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListRoutingProfileQueues.paginate)
        [Show boto3-stubs documentation](./paginators.md#listroutingprofilequeuespaginator)
        """


class ListRoutingProfilesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListRoutingProfiles)[Show boto3-stubs documentation](./paginators.md#listroutingprofilespaginator)
    """

    def paginate(
        self, InstanceId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListRoutingProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListRoutingProfiles.paginate)
        [Show boto3-stubs documentation](./paginators.md#listroutingprofilespaginator)
        """


class ListSecurityKeysPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListSecurityKeys)[Show boto3-stubs documentation](./paginators.md#listsecuritykeyspaginator)
    """

    def paginate(
        self, InstanceId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListSecurityKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListSecurityKeys.paginate)
        [Show boto3-stubs documentation](./paginators.md#listsecuritykeyspaginator)
        """


class ListSecurityProfilesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListSecurityProfiles)[Show boto3-stubs documentation](./paginators.md#listsecurityprofilespaginator)
    """

    def paginate(
        self, InstanceId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListSecurityProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListSecurityProfiles.paginate)
        [Show boto3-stubs documentation](./paginators.md#listsecurityprofilespaginator)
        """


class ListUseCasesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListUseCases)[Show boto3-stubs documentation](./paginators.md#listusecasespaginator)
    """

    def paginate(
        self,
        InstanceId: str,
        IntegrationAssociationId: str,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListUseCasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListUseCases.paginate)
        [Show boto3-stubs documentation](./paginators.md#listusecasespaginator)
        """


class ListUserHierarchyGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListUserHierarchyGroups)[Show boto3-stubs documentation](./paginators.md#listuserhierarchygroupspaginator)
    """

    def paginate(
        self, InstanceId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListUserHierarchyGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListUserHierarchyGroups.paginate)
        [Show boto3-stubs documentation](./paginators.md#listuserhierarchygroupspaginator)
        """


class ListUsersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListUsers)[Show boto3-stubs documentation](./paginators.md#listuserspaginator)
    """

    def paginate(
        self, InstanceId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/connect.html#Connect.Paginator.ListUsers.paginate)
        [Show boto3-stubs documentation](./paginators.md#listuserspaginator)
        """
