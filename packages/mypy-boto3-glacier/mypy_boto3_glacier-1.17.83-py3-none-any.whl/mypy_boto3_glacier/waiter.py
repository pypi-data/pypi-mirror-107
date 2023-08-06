"""
Type annotations for glacier service client waiters.

[Open documentation](./waiters.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_glacier import GlacierClient
    from mypy_boto3_glacier.waiter import (
        VaultExistsWaiter,
        VaultNotExistsWaiter,
    )

    client: GlacierClient = boto3.client("glacier")

    vault_exists_waiter: VaultExistsWaiter = client.get_waiter("vault_exists")
    vault_not_exists_waiter: VaultNotExistsWaiter = client.get_waiter("vault_not_exists")
    ```
"""
from botocore.waiter import Waiter as Boto3Waiter

from .type_defs import WaiterConfigTypeDef

__all__ = ("VaultExistsWaiter", "VaultNotExistsWaiter")


class VaultExistsWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/glacier.html#Glacier.Waiter.vault_exists)[Show boto3-stubs documentation](./waiters.md#vaultexistswaiter)
    """

    def wait(
        self, accountId: str, vaultName: str, WaiterConfig: WaiterConfigTypeDef = None
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/glacier.html#Glacier.Waiter.VaultExistsWaiter)
        [Show boto3-stubs documentation](./waiters.md#vaultexists)
        """


class VaultNotExistsWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/glacier.html#Glacier.Waiter.vault_not_exists)[Show boto3-stubs documentation](./waiters.md#vaultnotexistswaiter)
    """

    def wait(
        self, accountId: str, vaultName: str, WaiterConfig: WaiterConfigTypeDef = None
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/glacier.html#Glacier.Waiter.VaultNotExistsWaiter)
        [Show boto3-stubs documentation](./waiters.md#vaultnotexists)
        """
