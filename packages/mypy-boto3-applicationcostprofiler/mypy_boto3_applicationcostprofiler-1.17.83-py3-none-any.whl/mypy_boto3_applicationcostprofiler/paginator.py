"""
Type annotations for applicationcostprofiler service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_applicationcostprofiler import ApplicationCostProfilerClient
    from mypy_boto3_applicationcostprofiler.paginator import (
        ListReportDefinitionsPaginator,
    )

    client: ApplicationCostProfilerClient = boto3.client("applicationcostprofiler")

    list_report_definitions_paginator: ListReportDefinitionsPaginator = client.get_paginator("list_report_definitions")
    ```
"""
from typing import Iterator

from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import ListReportDefinitionsResultTypeDef, PaginatorConfigTypeDef

__all__ = ("ListReportDefinitionsPaginator",)


class ListReportDefinitionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/applicationcostprofiler.html#ApplicationCostProfiler.Paginator.ListReportDefinitions)[Show boto3-stubs documentation](./paginators.md#listreportdefinitionspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListReportDefinitionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/applicationcostprofiler.html#ApplicationCostProfiler.Paginator.ListReportDefinitions.paginate)
        [Show boto3-stubs documentation](./paginators.md#listreportdefinitionspaginator)
        """
