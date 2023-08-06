"""
Type annotations for budgets service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_budgets import BudgetsClient
    from mypy_boto3_budgets.paginator import (
        DescribeBudgetActionHistoriesPaginator,
        DescribeBudgetActionsForAccountPaginator,
        DescribeBudgetActionsForBudgetPaginator,
        DescribeBudgetPerformanceHistoryPaginator,
        DescribeBudgetsPaginator,
        DescribeNotificationsForBudgetPaginator,
        DescribeSubscribersForNotificationPaginator,
    )

    client: BudgetsClient = boto3.client("budgets")

    describe_budget_action_histories_paginator: DescribeBudgetActionHistoriesPaginator = client.get_paginator("describe_budget_action_histories")
    describe_budget_actions_for_account_paginator: DescribeBudgetActionsForAccountPaginator = client.get_paginator("describe_budget_actions_for_account")
    describe_budget_actions_for_budget_paginator: DescribeBudgetActionsForBudgetPaginator = client.get_paginator("describe_budget_actions_for_budget")
    describe_budget_performance_history_paginator: DescribeBudgetPerformanceHistoryPaginator = client.get_paginator("describe_budget_performance_history")
    describe_budgets_paginator: DescribeBudgetsPaginator = client.get_paginator("describe_budgets")
    describe_notifications_for_budget_paginator: DescribeNotificationsForBudgetPaginator = client.get_paginator("describe_notifications_for_budget")
    describe_subscribers_for_notification_paginator: DescribeSubscribersForNotificationPaginator = client.get_paginator("describe_subscribers_for_notification")
    ```
"""
from typing import Iterator

from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    DescribeBudgetActionHistoriesResponseTypeDef,
    DescribeBudgetActionsForAccountResponseTypeDef,
    DescribeBudgetActionsForBudgetResponseTypeDef,
    DescribeBudgetPerformanceHistoryResponseTypeDef,
    DescribeBudgetsResponseTypeDef,
    DescribeNotificationsForBudgetResponseTypeDef,
    DescribeSubscribersForNotificationResponseTypeDef,
    NotificationTypeDef,
    PaginatorConfigTypeDef,
    TimePeriodTypeDef,
)

__all__ = (
    "DescribeBudgetActionHistoriesPaginator",
    "DescribeBudgetActionsForAccountPaginator",
    "DescribeBudgetActionsForBudgetPaginator",
    "DescribeBudgetPerformanceHistoryPaginator",
    "DescribeBudgetsPaginator",
    "DescribeNotificationsForBudgetPaginator",
    "DescribeSubscribersForNotificationPaginator",
)


class DescribeBudgetActionHistoriesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/budgets.html#Budgets.Paginator.DescribeBudgetActionHistories)[Show boto3-stubs documentation](./paginators.md#describebudgetactionhistoriespaginator)
    """

    def paginate(
        self,
        AccountId: str,
        BudgetName: str,
        ActionId: str,
        TimePeriod: "TimePeriodTypeDef" = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeBudgetActionHistoriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/budgets.html#Budgets.Paginator.DescribeBudgetActionHistories.paginate)
        [Show boto3-stubs documentation](./paginators.md#describebudgetactionhistoriespaginator)
        """


class DescribeBudgetActionsForAccountPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/budgets.html#Budgets.Paginator.DescribeBudgetActionsForAccount)[Show boto3-stubs documentation](./paginators.md#describebudgetactionsforaccountpaginator)
    """

    def paginate(
        self, AccountId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[DescribeBudgetActionsForAccountResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/budgets.html#Budgets.Paginator.DescribeBudgetActionsForAccount.paginate)
        [Show boto3-stubs documentation](./paginators.md#describebudgetactionsforaccountpaginator)
        """


class DescribeBudgetActionsForBudgetPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/budgets.html#Budgets.Paginator.DescribeBudgetActionsForBudget)[Show boto3-stubs documentation](./paginators.md#describebudgetactionsforbudgetpaginator)
    """

    def paginate(
        self, AccountId: str, BudgetName: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[DescribeBudgetActionsForBudgetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/budgets.html#Budgets.Paginator.DescribeBudgetActionsForBudget.paginate)
        [Show boto3-stubs documentation](./paginators.md#describebudgetactionsforbudgetpaginator)
        """


class DescribeBudgetPerformanceHistoryPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/budgets.html#Budgets.Paginator.DescribeBudgetPerformanceHistory)[Show boto3-stubs documentation](./paginators.md#describebudgetperformancehistorypaginator)
    """

    def paginate(
        self,
        AccountId: str,
        BudgetName: str,
        TimePeriod: "TimePeriodTypeDef" = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeBudgetPerformanceHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/budgets.html#Budgets.Paginator.DescribeBudgetPerformanceHistory.paginate)
        [Show boto3-stubs documentation](./paginators.md#describebudgetperformancehistorypaginator)
        """


class DescribeBudgetsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/budgets.html#Budgets.Paginator.DescribeBudgets)[Show boto3-stubs documentation](./paginators.md#describebudgetspaginator)
    """

    def paginate(
        self, AccountId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[DescribeBudgetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/budgets.html#Budgets.Paginator.DescribeBudgets.paginate)
        [Show boto3-stubs documentation](./paginators.md#describebudgetspaginator)
        """


class DescribeNotificationsForBudgetPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/budgets.html#Budgets.Paginator.DescribeNotificationsForBudget)[Show boto3-stubs documentation](./paginators.md#describenotificationsforbudgetpaginator)
    """

    def paginate(
        self, AccountId: str, BudgetName: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[DescribeNotificationsForBudgetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/budgets.html#Budgets.Paginator.DescribeNotificationsForBudget.paginate)
        [Show boto3-stubs documentation](./paginators.md#describenotificationsforbudgetpaginator)
        """


class DescribeSubscribersForNotificationPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/budgets.html#Budgets.Paginator.DescribeSubscribersForNotification)[Show boto3-stubs documentation](./paginators.md#describesubscribersfornotificationpaginator)
    """

    def paginate(
        self,
        AccountId: str,
        BudgetName: str,
        Notification: "NotificationTypeDef",
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeSubscribersForNotificationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/budgets.html#Budgets.Paginator.DescribeSubscribersForNotification.paginate)
        [Show boto3-stubs documentation](./paginators.md#describesubscribersfornotificationpaginator)
        """
