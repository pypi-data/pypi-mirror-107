"""
Type annotations for dynamodb service client waiters.

[Open documentation](./waiters.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_dynamodb import DynamoDBClient
    from mypy_boto3_dynamodb.waiter import (
        TableExistsWaiter,
        TableNotExistsWaiter,
    )

    client: DynamoDBClient = boto3.client("dynamodb")

    table_exists_waiter: TableExistsWaiter = client.get_waiter("table_exists")
    table_not_exists_waiter: TableNotExistsWaiter = client.get_waiter("table_not_exists")
    ```
"""
from botocore.waiter import Waiter as Boto3Waiter

from .type_defs import WaiterConfigTypeDef

__all__ = ("TableExistsWaiter", "TableNotExistsWaiter")


class TableExistsWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/dynamodb.html#DynamoDB.Waiter.table_exists)[Show boto3-stubs documentation](./waiters.md#tableexistswaiter)
    """

    def wait(self, TableName: str, WaiterConfig: WaiterConfigTypeDef = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/dynamodb.html#DynamoDB.Waiter.TableExistsWaiter)
        [Show boto3-stubs documentation](./waiters.md#tableexists)
        """


class TableNotExistsWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/dynamodb.html#DynamoDB.Waiter.table_not_exists)[Show boto3-stubs documentation](./waiters.md#tablenotexistswaiter)
    """

    def wait(self, TableName: str, WaiterConfig: WaiterConfigTypeDef = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/dynamodb.html#DynamoDB.Waiter.TableNotExistsWaiter)
        [Show boto3-stubs documentation](./waiters.md#tablenotexists)
        """
