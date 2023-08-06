"""
Type annotations for elastictranscoder service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_elastictranscoder import ElasticTranscoderClient
    from mypy_boto3_elastictranscoder.paginator import (
        ListJobsByPipelinePaginator,
        ListJobsByStatusPaginator,
        ListPipelinesPaginator,
        ListPresetsPaginator,
    )

    client: ElasticTranscoderClient = boto3.client("elastictranscoder")

    list_jobs_by_pipeline_paginator: ListJobsByPipelinePaginator = client.get_paginator("list_jobs_by_pipeline")
    list_jobs_by_status_paginator: ListJobsByStatusPaginator = client.get_paginator("list_jobs_by_status")
    list_pipelines_paginator: ListPipelinesPaginator = client.get_paginator("list_pipelines")
    list_presets_paginator: ListPresetsPaginator = client.get_paginator("list_presets")
    ```
"""
from typing import Iterator

from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ListJobsByPipelineResponseTypeDef,
    ListJobsByStatusResponseTypeDef,
    ListPipelinesResponseTypeDef,
    ListPresetsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListJobsByPipelinePaginator",
    "ListJobsByStatusPaginator",
    "ListPipelinesPaginator",
    "ListPresetsPaginator",
)


class ListJobsByPipelinePaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/elastictranscoder.html#ElasticTranscoder.Paginator.ListJobsByPipeline)[Show boto3-stubs documentation](./paginators.md#listjobsbypipelinepaginator)
    """

    def paginate(
        self,
        PipelineId: str,
        Ascending: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListJobsByPipelineResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/elastictranscoder.html#ElasticTranscoder.Paginator.ListJobsByPipeline.paginate)
        [Show boto3-stubs documentation](./paginators.md#listjobsbypipelinepaginator)
        """


class ListJobsByStatusPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/elastictranscoder.html#ElasticTranscoder.Paginator.ListJobsByStatus)[Show boto3-stubs documentation](./paginators.md#listjobsbystatuspaginator)
    """

    def paginate(
        self, Status: str, Ascending: str = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListJobsByStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/elastictranscoder.html#ElasticTranscoder.Paginator.ListJobsByStatus.paginate)
        [Show boto3-stubs documentation](./paginators.md#listjobsbystatuspaginator)
        """


class ListPipelinesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/elastictranscoder.html#ElasticTranscoder.Paginator.ListPipelines)[Show boto3-stubs documentation](./paginators.md#listpipelinespaginator)
    """

    def paginate(
        self, Ascending: str = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListPipelinesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/elastictranscoder.html#ElasticTranscoder.Paginator.ListPipelines.paginate)
        [Show boto3-stubs documentation](./paginators.md#listpipelinespaginator)
        """


class ListPresetsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/elastictranscoder.html#ElasticTranscoder.Paginator.ListPresets)[Show boto3-stubs documentation](./paginators.md#listpresetspaginator)
    """

    def paginate(
        self, Ascending: str = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListPresetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/elastictranscoder.html#ElasticTranscoder.Paginator.ListPresets.paginate)
        [Show boto3-stubs documentation](./paginators.md#listpresetspaginator)
        """
