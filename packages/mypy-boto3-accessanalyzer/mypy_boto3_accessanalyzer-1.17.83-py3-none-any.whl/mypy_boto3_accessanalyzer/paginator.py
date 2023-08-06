"""
Type annotations for accessanalyzer service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_accessanalyzer import AccessAnalyzerClient
    from mypy_boto3_accessanalyzer.paginator import (
        ListAccessPreviewFindingsPaginator,
        ListAccessPreviewsPaginator,
        ListAnalyzedResourcesPaginator,
        ListAnalyzersPaginator,
        ListArchiveRulesPaginator,
        ListFindingsPaginator,
        ListPolicyGenerationsPaginator,
        ValidatePolicyPaginator,
    )

    client: AccessAnalyzerClient = boto3.client("accessanalyzer")

    list_access_preview_findings_paginator: ListAccessPreviewFindingsPaginator = client.get_paginator("list_access_preview_findings")
    list_access_previews_paginator: ListAccessPreviewsPaginator = client.get_paginator("list_access_previews")
    list_analyzed_resources_paginator: ListAnalyzedResourcesPaginator = client.get_paginator("list_analyzed_resources")
    list_analyzers_paginator: ListAnalyzersPaginator = client.get_paginator("list_analyzers")
    list_archive_rules_paginator: ListArchiveRulesPaginator = client.get_paginator("list_archive_rules")
    list_findings_paginator: ListFindingsPaginator = client.get_paginator("list_findings")
    list_policy_generations_paginator: ListPolicyGenerationsPaginator = client.get_paginator("list_policy_generations")
    validate_policy_paginator: ValidatePolicyPaginator = client.get_paginator("validate_policy")
    ```
"""
from typing import Dict, Iterator

from botocore.paginate import Paginator as Boto3Paginator

from .literals import LocaleType, PolicyTypeType, ResourceTypeType, TypeType
from .type_defs import (
    CriterionTypeDef,
    ListAccessPreviewFindingsResponseTypeDef,
    ListAccessPreviewsResponseTypeDef,
    ListAnalyzedResourcesResponseTypeDef,
    ListAnalyzersResponseTypeDef,
    ListArchiveRulesResponseTypeDef,
    ListFindingsResponseTypeDef,
    ListPolicyGenerationsResponseTypeDef,
    PaginatorConfigTypeDef,
    SortCriteriaTypeDef,
    ValidatePolicyResponseTypeDef,
)

__all__ = (
    "ListAccessPreviewFindingsPaginator",
    "ListAccessPreviewsPaginator",
    "ListAnalyzedResourcesPaginator",
    "ListAnalyzersPaginator",
    "ListArchiveRulesPaginator",
    "ListFindingsPaginator",
    "ListPolicyGenerationsPaginator",
    "ValidatePolicyPaginator",
)


class ListAccessPreviewFindingsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAccessPreviewFindings)[Show boto3-stubs documentation](./paginators.md#listaccesspreviewfindingspaginator)
    """

    def paginate(
        self,
        accessPreviewId: str,
        analyzerArn: str,
        filter: Dict[str, "CriterionTypeDef"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListAccessPreviewFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAccessPreviewFindings.paginate)
        [Show boto3-stubs documentation](./paginators.md#listaccesspreviewfindingspaginator)
        """


class ListAccessPreviewsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAccessPreviews)[Show boto3-stubs documentation](./paginators.md#listaccesspreviewspaginator)
    """

    def paginate(
        self, analyzerArn: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListAccessPreviewsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAccessPreviews.paginate)
        [Show boto3-stubs documentation](./paginators.md#listaccesspreviewspaginator)
        """


class ListAnalyzedResourcesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAnalyzedResources)[Show boto3-stubs documentation](./paginators.md#listanalyzedresourcespaginator)
    """

    def paginate(
        self,
        analyzerArn: str,
        resourceType: ResourceTypeType = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListAnalyzedResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAnalyzedResources.paginate)
        [Show boto3-stubs documentation](./paginators.md#listanalyzedresourcespaginator)
        """


class ListAnalyzersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAnalyzers)[Show boto3-stubs documentation](./paginators.md#listanalyzerspaginator)
    """

    def paginate(
        self, type: TypeType = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListAnalyzersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAnalyzers.paginate)
        [Show boto3-stubs documentation](./paginators.md#listanalyzerspaginator)
        """


class ListArchiveRulesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListArchiveRules)[Show boto3-stubs documentation](./paginators.md#listarchiverulespaginator)
    """

    def paginate(
        self, analyzerName: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListArchiveRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListArchiveRules.paginate)
        [Show boto3-stubs documentation](./paginators.md#listarchiverulespaginator)
        """


class ListFindingsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListFindings)[Show boto3-stubs documentation](./paginators.md#listfindingspaginator)
    """

    def paginate(
        self,
        analyzerArn: str,
        filter: Dict[str, "CriterionTypeDef"] = None,
        sort: SortCriteriaTypeDef = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListFindings.paginate)
        [Show boto3-stubs documentation](./paginators.md#listfindingspaginator)
        """


class ListPolicyGenerationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListPolicyGenerations)[Show boto3-stubs documentation](./paginators.md#listpolicygenerationspaginator)
    """

    def paginate(
        self, principalArn: str = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListPolicyGenerationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListPolicyGenerations.paginate)
        [Show boto3-stubs documentation](./paginators.md#listpolicygenerationspaginator)
        """


class ValidatePolicyPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ValidatePolicy)[Show boto3-stubs documentation](./paginators.md#validatepolicypaginator)
    """

    def paginate(
        self,
        policyDocument: str,
        policyType: PolicyTypeType,
        locale: LocaleType = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ValidatePolicyResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ValidatePolicy.paginate)
        [Show boto3-stubs documentation](./paginators.md#validatepolicypaginator)
        """
