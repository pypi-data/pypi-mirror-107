"""
Type annotations for lambda service client waiters.

[Open documentation](./waiters.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_lambda import LambdaClient
    from mypy_boto3_lambda.waiter import (
        FunctionActiveWaiter,
        FunctionExistsWaiter,
        FunctionUpdatedWaiter,
    )

    client: LambdaClient = boto3.client("lambda")

    function_active_waiter: FunctionActiveWaiter = client.get_waiter("function_active")
    function_exists_waiter: FunctionExistsWaiter = client.get_waiter("function_exists")
    function_updated_waiter: FunctionUpdatedWaiter = client.get_waiter("function_updated")
    ```
"""
from botocore.waiter import Waiter as Boto3Waiter

from .type_defs import WaiterConfigTypeDef

__all__ = ("FunctionActiveWaiter", "FunctionExistsWaiter", "FunctionUpdatedWaiter")


class FunctionActiveWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/lambda.html#Lambda.Waiter.function_active)[Show boto3-stubs documentation](./waiters.md#functionactivewaiter)
    """

    def wait(
        self, FunctionName: str, Qualifier: str = None, WaiterConfig: WaiterConfigTypeDef = None
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/lambda.html#Lambda.Waiter.FunctionActiveWaiter)
        [Show boto3-stubs documentation](./waiters.md#functionactive)
        """


class FunctionExistsWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/lambda.html#Lambda.Waiter.function_exists)[Show boto3-stubs documentation](./waiters.md#functionexistswaiter)
    """

    def wait(
        self, FunctionName: str, Qualifier: str = None, WaiterConfig: WaiterConfigTypeDef = None
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/lambda.html#Lambda.Waiter.FunctionExistsWaiter)
        [Show boto3-stubs documentation](./waiters.md#functionexists)
        """


class FunctionUpdatedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/lambda.html#Lambda.Waiter.function_updated)[Show boto3-stubs documentation](./waiters.md#functionupdatedwaiter)
    """

    def wait(
        self, FunctionName: str, Qualifier: str = None, WaiterConfig: WaiterConfigTypeDef = None
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/lambda.html#Lambda.Waiter.FunctionUpdatedWaiter)
        [Show boto3-stubs documentation](./waiters.md#functionupdated)
        """
