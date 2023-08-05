"""
Type annotations for sns service literal definitions.

[Open documentation](./literals.md)

Usage::

    ```python
    from mypy_boto3_sns.literals import ListEndpointsByPlatformApplicationPaginatorName

    data: ListEndpointsByPlatformApplicationPaginatorName = "list_endpoints_by_platform_application"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "ListEndpointsByPlatformApplicationPaginatorName",
    "ListPhoneNumbersOptedOutPaginatorName",
    "ListPlatformApplicationsPaginatorName",
    "ListSubscriptionsByTopicPaginatorName",
    "ListSubscriptionsPaginatorName",
    "ListTopicsPaginatorName",
)

ListEndpointsByPlatformApplicationPaginatorName = Literal["list_endpoints_by_platform_application"]
ListPhoneNumbersOptedOutPaginatorName = Literal["list_phone_numbers_opted_out"]
ListPlatformApplicationsPaginatorName = Literal["list_platform_applications"]
ListSubscriptionsByTopicPaginatorName = Literal["list_subscriptions_by_topic"]
ListSubscriptionsPaginatorName = Literal["list_subscriptions"]
ListTopicsPaginatorName = Literal["list_topics"]
