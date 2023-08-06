"""
Type annotations for acm service client waiters.

[Open documentation](./waiters.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_acm import ACMClient
    from mypy_boto3_acm.waiter import (
        CertificateValidatedWaiter,
    )

    client: ACMClient = boto3.client("acm")

    certificate_validated_waiter: CertificateValidatedWaiter = client.get_waiter("certificate_validated")
    ```
"""
from botocore.waiter import Waiter as Boto3Waiter

from .type_defs import WaiterConfigTypeDef

__all__ = ("CertificateValidatedWaiter",)


class CertificateValidatedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/acm.html#ACM.Waiter.certificate_validated)[Show boto3-stubs documentation](./waiters.md#certificatevalidatedwaiter)
    """

    def wait(self, CertificateArn: str, WaiterConfig: WaiterConfigTypeDef = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/acm.html#ACM.Waiter.CertificateValidatedWaiter)
        [Show boto3-stubs documentation](./waiters.md#certificatevalidated)
        """
