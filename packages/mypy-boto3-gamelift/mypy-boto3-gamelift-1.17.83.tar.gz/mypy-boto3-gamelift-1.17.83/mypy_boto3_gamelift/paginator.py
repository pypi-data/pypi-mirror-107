"""
Type annotations for gamelift service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_gamelift import GameLiftClient
    from mypy_boto3_gamelift.paginator import (
        DescribeFleetAttributesPaginator,
        DescribeFleetCapacityPaginator,
        DescribeFleetEventsPaginator,
        DescribeFleetUtilizationPaginator,
        DescribeGameServerInstancesPaginator,
        DescribeGameSessionDetailsPaginator,
        DescribeGameSessionQueuesPaginator,
        DescribeGameSessionsPaginator,
        DescribeInstancesPaginator,
        DescribeMatchmakingConfigurationsPaginator,
        DescribeMatchmakingRuleSetsPaginator,
        DescribePlayerSessionsPaginator,
        DescribeScalingPoliciesPaginator,
        ListAliasesPaginator,
        ListBuildsPaginator,
        ListFleetsPaginator,
        ListGameServerGroupsPaginator,
        ListGameServersPaginator,
        ListScriptsPaginator,
        SearchGameSessionsPaginator,
    )

    client: GameLiftClient = boto3.client("gamelift")

    describe_fleet_attributes_paginator: DescribeFleetAttributesPaginator = client.get_paginator("describe_fleet_attributes")
    describe_fleet_capacity_paginator: DescribeFleetCapacityPaginator = client.get_paginator("describe_fleet_capacity")
    describe_fleet_events_paginator: DescribeFleetEventsPaginator = client.get_paginator("describe_fleet_events")
    describe_fleet_utilization_paginator: DescribeFleetUtilizationPaginator = client.get_paginator("describe_fleet_utilization")
    describe_game_server_instances_paginator: DescribeGameServerInstancesPaginator = client.get_paginator("describe_game_server_instances")
    describe_game_session_details_paginator: DescribeGameSessionDetailsPaginator = client.get_paginator("describe_game_session_details")
    describe_game_session_queues_paginator: DescribeGameSessionQueuesPaginator = client.get_paginator("describe_game_session_queues")
    describe_game_sessions_paginator: DescribeGameSessionsPaginator = client.get_paginator("describe_game_sessions")
    describe_instances_paginator: DescribeInstancesPaginator = client.get_paginator("describe_instances")
    describe_matchmaking_configurations_paginator: DescribeMatchmakingConfigurationsPaginator = client.get_paginator("describe_matchmaking_configurations")
    describe_matchmaking_rule_sets_paginator: DescribeMatchmakingRuleSetsPaginator = client.get_paginator("describe_matchmaking_rule_sets")
    describe_player_sessions_paginator: DescribePlayerSessionsPaginator = client.get_paginator("describe_player_sessions")
    describe_scaling_policies_paginator: DescribeScalingPoliciesPaginator = client.get_paginator("describe_scaling_policies")
    list_aliases_paginator: ListAliasesPaginator = client.get_paginator("list_aliases")
    list_builds_paginator: ListBuildsPaginator = client.get_paginator("list_builds")
    list_fleets_paginator: ListFleetsPaginator = client.get_paginator("list_fleets")
    list_game_server_groups_paginator: ListGameServerGroupsPaginator = client.get_paginator("list_game_server_groups")
    list_game_servers_paginator: ListGameServersPaginator = client.get_paginator("list_game_servers")
    list_scripts_paginator: ListScriptsPaginator = client.get_paginator("list_scripts")
    search_game_sessions_paginator: SearchGameSessionsPaginator = client.get_paginator("search_game_sessions")
    ```
"""
from datetime import datetime
from typing import Iterator, List

from botocore.paginate import Paginator as Boto3Paginator

from .literals import BuildStatusType, RoutingStrategyTypeType, ScalingStatusTypeType, SortOrderType
from .type_defs import (
    DescribeFleetAttributesOutputTypeDef,
    DescribeFleetCapacityOutputTypeDef,
    DescribeFleetEventsOutputTypeDef,
    DescribeFleetUtilizationOutputTypeDef,
    DescribeGameServerInstancesOutputTypeDef,
    DescribeGameSessionDetailsOutputTypeDef,
    DescribeGameSessionQueuesOutputTypeDef,
    DescribeGameSessionsOutputTypeDef,
    DescribeInstancesOutputTypeDef,
    DescribeMatchmakingConfigurationsOutputTypeDef,
    DescribeMatchmakingRuleSetsOutputTypeDef,
    DescribePlayerSessionsOutputTypeDef,
    DescribeScalingPoliciesOutputTypeDef,
    ListAliasesOutputTypeDef,
    ListBuildsOutputTypeDef,
    ListFleetsOutputTypeDef,
    ListGameServerGroupsOutputTypeDef,
    ListGameServersOutputTypeDef,
    ListScriptsOutputTypeDef,
    PaginatorConfigTypeDef,
    SearchGameSessionsOutputTypeDef,
)

__all__ = (
    "DescribeFleetAttributesPaginator",
    "DescribeFleetCapacityPaginator",
    "DescribeFleetEventsPaginator",
    "DescribeFleetUtilizationPaginator",
    "DescribeGameServerInstancesPaginator",
    "DescribeGameSessionDetailsPaginator",
    "DescribeGameSessionQueuesPaginator",
    "DescribeGameSessionsPaginator",
    "DescribeInstancesPaginator",
    "DescribeMatchmakingConfigurationsPaginator",
    "DescribeMatchmakingRuleSetsPaginator",
    "DescribePlayerSessionsPaginator",
    "DescribeScalingPoliciesPaginator",
    "ListAliasesPaginator",
    "ListBuildsPaginator",
    "ListFleetsPaginator",
    "ListGameServerGroupsPaginator",
    "ListGameServersPaginator",
    "ListScriptsPaginator",
    "SearchGameSessionsPaginator",
)


class DescribeFleetAttributesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.DescribeFleetAttributes)[Show boto3-stubs documentation](./paginators.md#describefleetattributespaginator)
    """

    def paginate(
        self, FleetIds: List[str] = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[DescribeFleetAttributesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.DescribeFleetAttributes.paginate)
        [Show boto3-stubs documentation](./paginators.md#describefleetattributespaginator)
        """


class DescribeFleetCapacityPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.DescribeFleetCapacity)[Show boto3-stubs documentation](./paginators.md#describefleetcapacitypaginator)
    """

    def paginate(
        self, FleetIds: List[str] = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[DescribeFleetCapacityOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.DescribeFleetCapacity.paginate)
        [Show boto3-stubs documentation](./paginators.md#describefleetcapacitypaginator)
        """


class DescribeFleetEventsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.DescribeFleetEvents)[Show boto3-stubs documentation](./paginators.md#describefleeteventspaginator)
    """

    def paginate(
        self,
        FleetId: str,
        StartTime: datetime = None,
        EndTime: datetime = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeFleetEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.DescribeFleetEvents.paginate)
        [Show boto3-stubs documentation](./paginators.md#describefleeteventspaginator)
        """


class DescribeFleetUtilizationPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.DescribeFleetUtilization)[Show boto3-stubs documentation](./paginators.md#describefleetutilizationpaginator)
    """

    def paginate(
        self, FleetIds: List[str] = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[DescribeFleetUtilizationOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.DescribeFleetUtilization.paginate)
        [Show boto3-stubs documentation](./paginators.md#describefleetutilizationpaginator)
        """


class DescribeGameServerInstancesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.DescribeGameServerInstances)[Show boto3-stubs documentation](./paginators.md#describegameserverinstancespaginator)
    """

    def paginate(
        self,
        GameServerGroupName: str,
        InstanceIds: List[str] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeGameServerInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.DescribeGameServerInstances.paginate)
        [Show boto3-stubs documentation](./paginators.md#describegameserverinstancespaginator)
        """


class DescribeGameSessionDetailsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.DescribeGameSessionDetails)[Show boto3-stubs documentation](./paginators.md#describegamesessiondetailspaginator)
    """

    def paginate(
        self,
        FleetId: str = None,
        GameSessionId: str = None,
        AliasId: str = None,
        Location: str = None,
        StatusFilter: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeGameSessionDetailsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.DescribeGameSessionDetails.paginate)
        [Show boto3-stubs documentation](./paginators.md#describegamesessiondetailspaginator)
        """


class DescribeGameSessionQueuesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.DescribeGameSessionQueues)[Show boto3-stubs documentation](./paginators.md#describegamesessionqueuespaginator)
    """

    def paginate(
        self, Names: List[str] = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[DescribeGameSessionQueuesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.DescribeGameSessionQueues.paginate)
        [Show boto3-stubs documentation](./paginators.md#describegamesessionqueuespaginator)
        """


class DescribeGameSessionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.DescribeGameSessions)[Show boto3-stubs documentation](./paginators.md#describegamesessionspaginator)
    """

    def paginate(
        self,
        FleetId: str = None,
        GameSessionId: str = None,
        AliasId: str = None,
        Location: str = None,
        StatusFilter: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeGameSessionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.DescribeGameSessions.paginate)
        [Show boto3-stubs documentation](./paginators.md#describegamesessionspaginator)
        """


class DescribeInstancesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.DescribeInstances)[Show boto3-stubs documentation](./paginators.md#describeinstancespaginator)
    """

    def paginate(
        self,
        FleetId: str,
        InstanceId: str = None,
        Location: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.DescribeInstances.paginate)
        [Show boto3-stubs documentation](./paginators.md#describeinstancespaginator)
        """


class DescribeMatchmakingConfigurationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.DescribeMatchmakingConfigurations)[Show boto3-stubs documentation](./paginators.md#describematchmakingconfigurationspaginator)
    """

    def paginate(
        self,
        Names: List[str] = None,
        RuleSetName: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeMatchmakingConfigurationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.DescribeMatchmakingConfigurations.paginate)
        [Show boto3-stubs documentation](./paginators.md#describematchmakingconfigurationspaginator)
        """


class DescribeMatchmakingRuleSetsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.DescribeMatchmakingRuleSets)[Show boto3-stubs documentation](./paginators.md#describematchmakingrulesetspaginator)
    """

    def paginate(
        self, Names: List[str] = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[DescribeMatchmakingRuleSetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.DescribeMatchmakingRuleSets.paginate)
        [Show boto3-stubs documentation](./paginators.md#describematchmakingrulesetspaginator)
        """


class DescribePlayerSessionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.DescribePlayerSessions)[Show boto3-stubs documentation](./paginators.md#describeplayersessionspaginator)
    """

    def paginate(
        self,
        GameSessionId: str = None,
        PlayerId: str = None,
        PlayerSessionId: str = None,
        PlayerSessionStatusFilter: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribePlayerSessionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.DescribePlayerSessions.paginate)
        [Show boto3-stubs documentation](./paginators.md#describeplayersessionspaginator)
        """


class DescribeScalingPoliciesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.DescribeScalingPolicies)[Show boto3-stubs documentation](./paginators.md#describescalingpoliciespaginator)
    """

    def paginate(
        self,
        FleetId: str,
        StatusFilter: ScalingStatusTypeType = None,
        Location: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeScalingPoliciesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.DescribeScalingPolicies.paginate)
        [Show boto3-stubs documentation](./paginators.md#describescalingpoliciespaginator)
        """


class ListAliasesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.ListAliases)[Show boto3-stubs documentation](./paginators.md#listaliasespaginator)
    """

    def paginate(
        self,
        RoutingStrategyType: RoutingStrategyTypeType = None,
        Name: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListAliasesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.ListAliases.paginate)
        [Show boto3-stubs documentation](./paginators.md#listaliasespaginator)
        """


class ListBuildsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.ListBuilds)[Show boto3-stubs documentation](./paginators.md#listbuildspaginator)
    """

    def paginate(
        self, Status: BuildStatusType = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListBuildsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.ListBuilds.paginate)
        [Show boto3-stubs documentation](./paginators.md#listbuildspaginator)
        """


class ListFleetsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.ListFleets)[Show boto3-stubs documentation](./paginators.md#listfleetspaginator)
    """

    def paginate(
        self,
        BuildId: str = None,
        ScriptId: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListFleetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.ListFleets.paginate)
        [Show boto3-stubs documentation](./paginators.md#listfleetspaginator)
        """


class ListGameServerGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.ListGameServerGroups)[Show boto3-stubs documentation](./paginators.md#listgameservergroupspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListGameServerGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.ListGameServerGroups.paginate)
        [Show boto3-stubs documentation](./paginators.md#listgameservergroupspaginator)
        """


class ListGameServersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.ListGameServers)[Show boto3-stubs documentation](./paginators.md#listgameserverspaginator)
    """

    def paginate(
        self,
        GameServerGroupName: str,
        SortOrder: SortOrderType = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListGameServersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.ListGameServers.paginate)
        [Show boto3-stubs documentation](./paginators.md#listgameserverspaginator)
        """


class ListScriptsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.ListScripts)[Show boto3-stubs documentation](./paginators.md#listscriptspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListScriptsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.ListScripts.paginate)
        [Show boto3-stubs documentation](./paginators.md#listscriptspaginator)
        """


class SearchGameSessionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.SearchGameSessions)[Show boto3-stubs documentation](./paginators.md#searchgamesessionspaginator)
    """

    def paginate(
        self,
        FleetId: str = None,
        AliasId: str = None,
        Location: str = None,
        FilterExpression: str = None,
        SortExpression: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[SearchGameSessionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/gamelift.html#GameLift.Paginator.SearchGameSessions.paginate)
        [Show boto3-stubs documentation](./paginators.md#searchgamesessionspaginator)
        """
