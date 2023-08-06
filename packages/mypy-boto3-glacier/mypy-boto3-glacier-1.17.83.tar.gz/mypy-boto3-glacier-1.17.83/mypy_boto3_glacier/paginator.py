"""
Type annotations for glacier service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_glacier import GlacierClient
    from mypy_boto3_glacier.paginator import (
        ListJobsPaginator,
        ListMultipartUploadsPaginator,
        ListPartsPaginator,
        ListVaultsPaginator,
    )

    client: GlacierClient = boto3.client("glacier")

    list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    list_multipart_uploads_paginator: ListMultipartUploadsPaginator = client.get_paginator("list_multipart_uploads")
    list_parts_paginator: ListPartsPaginator = client.get_paginator("list_parts")
    list_vaults_paginator: ListVaultsPaginator = client.get_paginator("list_vaults")
    ```
"""
from typing import Iterator

from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ListJobsOutputTypeDef,
    ListMultipartUploadsOutputTypeDef,
    ListPartsOutputTypeDef,
    ListVaultsOutputTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListJobsPaginator",
    "ListMultipartUploadsPaginator",
    "ListPartsPaginator",
    "ListVaultsPaginator",
)


class ListJobsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/glacier.html#Glacier.Paginator.ListJobs)[Show boto3-stubs documentation](./paginators.md#listjobspaginator)
    """

    def paginate(
        self,
        accountId: str,
        vaultName: str,
        statuscode: str = None,
        completed: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/glacier.html#Glacier.Paginator.ListJobs.paginate)
        [Show boto3-stubs documentation](./paginators.md#listjobspaginator)
        """


class ListMultipartUploadsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/glacier.html#Glacier.Paginator.ListMultipartUploads)[Show boto3-stubs documentation](./paginators.md#listmultipartuploadspaginator)
    """

    def paginate(
        self, accountId: str, vaultName: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListMultipartUploadsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/glacier.html#Glacier.Paginator.ListMultipartUploads.paginate)
        [Show boto3-stubs documentation](./paginators.md#listmultipartuploadspaginator)
        """


class ListPartsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/glacier.html#Glacier.Paginator.ListParts)[Show boto3-stubs documentation](./paginators.md#listpartspaginator)
    """

    def paginate(
        self,
        accountId: str,
        vaultName: str,
        uploadId: str,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListPartsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/glacier.html#Glacier.Paginator.ListParts.paginate)
        [Show boto3-stubs documentation](./paginators.md#listpartspaginator)
        """


class ListVaultsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/glacier.html#Glacier.Paginator.ListVaults)[Show boto3-stubs documentation](./paginators.md#listvaultspaginator)
    """

    def paginate(
        self, accountId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListVaultsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/glacier.html#Glacier.Paginator.ListVaults.paginate)
        [Show boto3-stubs documentation](./paginators.md#listvaultspaginator)
        """
