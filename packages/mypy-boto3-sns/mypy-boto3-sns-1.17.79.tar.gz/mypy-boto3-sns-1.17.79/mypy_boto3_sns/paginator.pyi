"""
Type annotations for sns service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_sns import SNSClient
    from mypy_boto3_sns.paginator import (
        ListEndpointsByPlatformApplicationPaginator,
        ListPhoneNumbersOptedOutPaginator,
        ListPlatformApplicationsPaginator,
        ListSubscriptionsPaginator,
        ListSubscriptionsByTopicPaginator,
        ListTopicsPaginator,
    )

    client: SNSClient = boto3.client("sns")

    list_endpoints_by_platform_application_paginator: ListEndpointsByPlatformApplicationPaginator = client.get_paginator("list_endpoints_by_platform_application")
    list_phone_numbers_opted_out_paginator: ListPhoneNumbersOptedOutPaginator = client.get_paginator("list_phone_numbers_opted_out")
    list_platform_applications_paginator: ListPlatformApplicationsPaginator = client.get_paginator("list_platform_applications")
    list_subscriptions_paginator: ListSubscriptionsPaginator = client.get_paginator("list_subscriptions")
    list_subscriptions_by_topic_paginator: ListSubscriptionsByTopicPaginator = client.get_paginator("list_subscriptions_by_topic")
    list_topics_paginator: ListTopicsPaginator = client.get_paginator("list_topics")
    ```
"""
from typing import Iterator

from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ListEndpointsByPlatformApplicationResponseTypeDef,
    ListPhoneNumbersOptedOutResponseTypeDef,
    ListPlatformApplicationsResponseTypeDef,
    ListSubscriptionsByTopicResponseTypeDef,
    ListSubscriptionsResponseTypeDef,
    ListTopicsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListEndpointsByPlatformApplicationPaginator",
    "ListPhoneNumbersOptedOutPaginator",
    "ListPlatformApplicationsPaginator",
    "ListSubscriptionsPaginator",
    "ListSubscriptionsByTopicPaginator",
    "ListTopicsPaginator",
)

class ListEndpointsByPlatformApplicationPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/sns.html#SNS.Paginator.ListEndpointsByPlatformApplication)[Show boto3-stubs documentation](./paginators.md#listendpointsbyplatformapplicationpaginator)
    """

    def paginate(
        self, PlatformApplicationArn: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListEndpointsByPlatformApplicationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/sns.html#SNS.Paginator.ListEndpointsByPlatformApplication.paginate)
        [Show boto3-stubs documentation](./paginators.md#listendpointsbyplatformapplicationpaginator)
        """

class ListPhoneNumbersOptedOutPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/sns.html#SNS.Paginator.ListPhoneNumbersOptedOut)[Show boto3-stubs documentation](./paginators.md#listphonenumbersoptedoutpaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListPhoneNumbersOptedOutResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/sns.html#SNS.Paginator.ListPhoneNumbersOptedOut.paginate)
        [Show boto3-stubs documentation](./paginators.md#listphonenumbersoptedoutpaginator)
        """

class ListPlatformApplicationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/sns.html#SNS.Paginator.ListPlatformApplications)[Show boto3-stubs documentation](./paginators.md#listplatformapplicationspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListPlatformApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/sns.html#SNS.Paginator.ListPlatformApplications.paginate)
        [Show boto3-stubs documentation](./paginators.md#listplatformapplicationspaginator)
        """

class ListSubscriptionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/sns.html#SNS.Paginator.ListSubscriptions)[Show boto3-stubs documentation](./paginators.md#listsubscriptionspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListSubscriptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/sns.html#SNS.Paginator.ListSubscriptions.paginate)
        [Show boto3-stubs documentation](./paginators.md#listsubscriptionspaginator)
        """

class ListSubscriptionsByTopicPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/sns.html#SNS.Paginator.ListSubscriptionsByTopic)[Show boto3-stubs documentation](./paginators.md#listsubscriptionsbytopicpaginator)
    """

    def paginate(
        self, TopicArn: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListSubscriptionsByTopicResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/sns.html#SNS.Paginator.ListSubscriptionsByTopic.paginate)
        [Show boto3-stubs documentation](./paginators.md#listsubscriptionsbytopicpaginator)
        """

class ListTopicsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/sns.html#SNS.Paginator.ListTopics)[Show boto3-stubs documentation](./paginators.md#listtopicspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListTopicsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/sns.html#SNS.Paginator.ListTopics.paginate)
        [Show boto3-stubs documentation](./paginators.md#listtopicspaginator)
        """
