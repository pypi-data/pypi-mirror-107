"""
Type annotations for health service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_health import HealthClient
    from mypy_boto3_health.paginator import (
        DescribeAffectedAccountsForOrganizationPaginator,
        DescribeAffectedEntitiesPaginator,
        DescribeAffectedEntitiesForOrganizationPaginator,
        DescribeEventAggregatesPaginator,
        DescribeEventTypesPaginator,
        DescribeEventsPaginator,
        DescribeEventsForOrganizationPaginator,
    )

    client: HealthClient = boto3.client("health")

    describe_affected_accounts_for_organization_paginator: DescribeAffectedAccountsForOrganizationPaginator = client.get_paginator("describe_affected_accounts_for_organization")
    describe_affected_entities_paginator: DescribeAffectedEntitiesPaginator = client.get_paginator("describe_affected_entities")
    describe_affected_entities_for_organization_paginator: DescribeAffectedEntitiesForOrganizationPaginator = client.get_paginator("describe_affected_entities_for_organization")
    describe_event_aggregates_paginator: DescribeEventAggregatesPaginator = client.get_paginator("describe_event_aggregates")
    describe_event_types_paginator: DescribeEventTypesPaginator = client.get_paginator("describe_event_types")
    describe_events_paginator: DescribeEventsPaginator = client.get_paginator("describe_events")
    describe_events_for_organization_paginator: DescribeEventsForOrganizationPaginator = client.get_paginator("describe_events_for_organization")
    ```
"""
import sys
from typing import Iterator, List

from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    DescribeAffectedAccountsForOrganizationResponseTypeDef,
    DescribeAffectedEntitiesForOrganizationResponseTypeDef,
    DescribeAffectedEntitiesResponseTypeDef,
    DescribeEventAggregatesResponseTypeDef,
    DescribeEventsForOrganizationResponseTypeDef,
    DescribeEventsResponseTypeDef,
    DescribeEventTypesResponseTypeDef,
    EntityFilterTypeDef,
    EventAccountFilterTypeDef,
    EventFilterTypeDef,
    EventTypeFilterTypeDef,
    OrganizationEventFilterTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "DescribeAffectedAccountsForOrganizationPaginator",
    "DescribeAffectedEntitiesPaginator",
    "DescribeAffectedEntitiesForOrganizationPaginator",
    "DescribeEventAggregatesPaginator",
    "DescribeEventTypesPaginator",
    "DescribeEventsPaginator",
    "DescribeEventsForOrganizationPaginator",
)


class DescribeAffectedAccountsForOrganizationPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/health.html#Health.Paginator.DescribeAffectedAccountsForOrganization)[Show boto3-stubs documentation](./paginators.md#describeaffectedaccountsfororganizationpaginator)
    """

    def paginate(
        self, eventArn: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[DescribeAffectedAccountsForOrganizationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/health.html#Health.Paginator.DescribeAffectedAccountsForOrganization.paginate)
        [Show boto3-stubs documentation](./paginators.md#describeaffectedaccountsfororganizationpaginator)
        """


class DescribeAffectedEntitiesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/health.html#Health.Paginator.DescribeAffectedEntities)[Show boto3-stubs documentation](./paginators.md#describeaffectedentitiespaginator)
    """

    def paginate(
        self,
        filter: EntityFilterTypeDef,
        locale: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeAffectedEntitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/health.html#Health.Paginator.DescribeAffectedEntities.paginate)
        [Show boto3-stubs documentation](./paginators.md#describeaffectedentitiespaginator)
        """


class DescribeAffectedEntitiesForOrganizationPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/health.html#Health.Paginator.DescribeAffectedEntitiesForOrganization)[Show boto3-stubs documentation](./paginators.md#describeaffectedentitiesfororganizationpaginator)
    """

    def paginate(
        self,
        organizationEntityFilters: List[EventAccountFilterTypeDef],
        locale: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeAffectedEntitiesForOrganizationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/health.html#Health.Paginator.DescribeAffectedEntitiesForOrganization.paginate)
        [Show boto3-stubs documentation](./paginators.md#describeaffectedentitiesfororganizationpaginator)
        """


class DescribeEventAggregatesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/health.html#Health.Paginator.DescribeEventAggregates)[Show boto3-stubs documentation](./paginators.md#describeeventaggregatespaginator)
    """

    def paginate(
        self,
        aggregateField: Literal["eventTypeCategory"],
        filter: EventFilterTypeDef = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeEventAggregatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/health.html#Health.Paginator.DescribeEventAggregates.paginate)
        [Show boto3-stubs documentation](./paginators.md#describeeventaggregatespaginator)
        """


class DescribeEventTypesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/health.html#Health.Paginator.DescribeEventTypes)[Show boto3-stubs documentation](./paginators.md#describeeventtypespaginator)
    """

    def paginate(
        self,
        filter: EventTypeFilterTypeDef = None,
        locale: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeEventTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/health.html#Health.Paginator.DescribeEventTypes.paginate)
        [Show boto3-stubs documentation](./paginators.md#describeeventtypespaginator)
        """


class DescribeEventsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/health.html#Health.Paginator.DescribeEvents)[Show boto3-stubs documentation](./paginators.md#describeeventspaginator)
    """

    def paginate(
        self,
        filter: EventFilterTypeDef = None,
        locale: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/health.html#Health.Paginator.DescribeEvents.paginate)
        [Show boto3-stubs documentation](./paginators.md#describeeventspaginator)
        """


class DescribeEventsForOrganizationPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/health.html#Health.Paginator.DescribeEventsForOrganization)[Show boto3-stubs documentation](./paginators.md#describeeventsfororganizationpaginator)
    """

    def paginate(
        self,
        filter: OrganizationEventFilterTypeDef = None,
        locale: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeEventsForOrganizationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/health.html#Health.Paginator.DescribeEventsForOrganization.paginate)
        [Show boto3-stubs documentation](./paginators.md#describeeventsfororganizationpaginator)
        """
