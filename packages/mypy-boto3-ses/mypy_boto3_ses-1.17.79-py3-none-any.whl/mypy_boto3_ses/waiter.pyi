"""
Type annotations for ses service client waiters.

[Open documentation](./waiters.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_ses import SESClient
    from mypy_boto3_ses.waiter import (
        IdentityExistsWaiter,
    )

    client: SESClient = boto3.client("ses")

    identity_exists_waiter: IdentityExistsWaiter = client.get_waiter("identity_exists")
    ```
"""
from typing import List

from botocore.waiter import Waiter as Boto3Waiter

from .type_defs import WaiterConfigTypeDef

__all__ = ("IdentityExistsWaiter",)

class IdentityExistsWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/ses.html#SES.Waiter.identity_exists)[Show boto3-stubs documentation](./waiters.md#identityexistswaiter)
    """

    def wait(self, Identities: List[str], WaiterConfig: WaiterConfigTypeDef = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/ses.html#SES.Waiter.IdentityExistsWaiter)
        [Show boto3-stubs documentation](./waiters.md#identityexists)
        """
