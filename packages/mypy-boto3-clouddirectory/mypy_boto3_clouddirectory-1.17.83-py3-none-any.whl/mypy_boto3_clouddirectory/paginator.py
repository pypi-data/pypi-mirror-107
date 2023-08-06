"""
Type annotations for clouddirectory service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_clouddirectory import CloudDirectoryClient
    from mypy_boto3_clouddirectory.paginator import (
        ListAppliedSchemaArnsPaginator,
        ListAttachedIndicesPaginator,
        ListDevelopmentSchemaArnsPaginator,
        ListDirectoriesPaginator,
        ListFacetAttributesPaginator,
        ListFacetNamesPaginator,
        ListIncomingTypedLinksPaginator,
        ListIndexPaginator,
        ListManagedSchemaArnsPaginator,
        ListObjectAttributesPaginator,
        ListObjectParentPathsPaginator,
        ListObjectPoliciesPaginator,
        ListOutgoingTypedLinksPaginator,
        ListPolicyAttachmentsPaginator,
        ListPublishedSchemaArnsPaginator,
        ListTagsForResourcePaginator,
        ListTypedLinkFacetAttributesPaginator,
        ListTypedLinkFacetNamesPaginator,
        LookupPolicyPaginator,
    )

    client: CloudDirectoryClient = boto3.client("clouddirectory")

    list_applied_schema_arns_paginator: ListAppliedSchemaArnsPaginator = client.get_paginator("list_applied_schema_arns")
    list_attached_indices_paginator: ListAttachedIndicesPaginator = client.get_paginator("list_attached_indices")
    list_development_schema_arns_paginator: ListDevelopmentSchemaArnsPaginator = client.get_paginator("list_development_schema_arns")
    list_directories_paginator: ListDirectoriesPaginator = client.get_paginator("list_directories")
    list_facet_attributes_paginator: ListFacetAttributesPaginator = client.get_paginator("list_facet_attributes")
    list_facet_names_paginator: ListFacetNamesPaginator = client.get_paginator("list_facet_names")
    list_incoming_typed_links_paginator: ListIncomingTypedLinksPaginator = client.get_paginator("list_incoming_typed_links")
    list_index_paginator: ListIndexPaginator = client.get_paginator("list_index")
    list_managed_schema_arns_paginator: ListManagedSchemaArnsPaginator = client.get_paginator("list_managed_schema_arns")
    list_object_attributes_paginator: ListObjectAttributesPaginator = client.get_paginator("list_object_attributes")
    list_object_parent_paths_paginator: ListObjectParentPathsPaginator = client.get_paginator("list_object_parent_paths")
    list_object_policies_paginator: ListObjectPoliciesPaginator = client.get_paginator("list_object_policies")
    list_outgoing_typed_links_paginator: ListOutgoingTypedLinksPaginator = client.get_paginator("list_outgoing_typed_links")
    list_policy_attachments_paginator: ListPolicyAttachmentsPaginator = client.get_paginator("list_policy_attachments")
    list_published_schema_arns_paginator: ListPublishedSchemaArnsPaginator = client.get_paginator("list_published_schema_arns")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    list_typed_link_facet_attributes_paginator: ListTypedLinkFacetAttributesPaginator = client.get_paginator("list_typed_link_facet_attributes")
    list_typed_link_facet_names_paginator: ListTypedLinkFacetNamesPaginator = client.get_paginator("list_typed_link_facet_names")
    lookup_policy_paginator: LookupPolicyPaginator = client.get_paginator("lookup_policy")
    ```
"""
from typing import Iterator, List

from botocore.paginate import Paginator as Boto3Paginator

from .literals import ConsistencyLevelType, DirectoryStateType
from .type_defs import (
    ListAppliedSchemaArnsResponseTypeDef,
    ListAttachedIndicesResponseTypeDef,
    ListDevelopmentSchemaArnsResponseTypeDef,
    ListDirectoriesResponseTypeDef,
    ListFacetAttributesResponseTypeDef,
    ListFacetNamesResponseTypeDef,
    ListIncomingTypedLinksResponseTypeDef,
    ListIndexResponseTypeDef,
    ListManagedSchemaArnsResponseTypeDef,
    ListObjectAttributesResponseTypeDef,
    ListObjectParentPathsResponseTypeDef,
    ListObjectPoliciesResponseTypeDef,
    ListOutgoingTypedLinksResponseTypeDef,
    ListPolicyAttachmentsResponseTypeDef,
    ListPublishedSchemaArnsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTypedLinkFacetAttributesResponseTypeDef,
    ListTypedLinkFacetNamesResponseTypeDef,
    LookupPolicyResponseTypeDef,
    ObjectAttributeRangeTypeDef,
    ObjectReferenceTypeDef,
    PaginatorConfigTypeDef,
    SchemaFacetTypeDef,
    TypedLinkAttributeRangeTypeDef,
    TypedLinkSchemaAndFacetNameTypeDef,
)

__all__ = (
    "ListAppliedSchemaArnsPaginator",
    "ListAttachedIndicesPaginator",
    "ListDevelopmentSchemaArnsPaginator",
    "ListDirectoriesPaginator",
    "ListFacetAttributesPaginator",
    "ListFacetNamesPaginator",
    "ListIncomingTypedLinksPaginator",
    "ListIndexPaginator",
    "ListManagedSchemaArnsPaginator",
    "ListObjectAttributesPaginator",
    "ListObjectParentPathsPaginator",
    "ListObjectPoliciesPaginator",
    "ListOutgoingTypedLinksPaginator",
    "ListPolicyAttachmentsPaginator",
    "ListPublishedSchemaArnsPaginator",
    "ListTagsForResourcePaginator",
    "ListTypedLinkFacetAttributesPaginator",
    "ListTypedLinkFacetNamesPaginator",
    "LookupPolicyPaginator",
)


class ListAppliedSchemaArnsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListAppliedSchemaArns)[Show boto3-stubs documentation](./paginators.md#listappliedschemaarnspaginator)
    """

    def paginate(
        self,
        DirectoryArn: str,
        SchemaArn: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListAppliedSchemaArnsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListAppliedSchemaArns.paginate)
        [Show boto3-stubs documentation](./paginators.md#listappliedschemaarnspaginator)
        """


class ListAttachedIndicesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListAttachedIndices)[Show boto3-stubs documentation](./paginators.md#listattachedindicespaginator)
    """

    def paginate(
        self,
        DirectoryArn: str,
        TargetReference: "ObjectReferenceTypeDef",
        ConsistencyLevel: ConsistencyLevelType = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListAttachedIndicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListAttachedIndices.paginate)
        [Show boto3-stubs documentation](./paginators.md#listattachedindicespaginator)
        """


class ListDevelopmentSchemaArnsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListDevelopmentSchemaArns)[Show boto3-stubs documentation](./paginators.md#listdevelopmentschemaarnspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListDevelopmentSchemaArnsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListDevelopmentSchemaArns.paginate)
        [Show boto3-stubs documentation](./paginators.md#listdevelopmentschemaarnspaginator)
        """


class ListDirectoriesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListDirectories)[Show boto3-stubs documentation](./paginators.md#listdirectoriespaginator)
    """

    def paginate(
        self, state: DirectoryStateType = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListDirectoriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListDirectories.paginate)
        [Show boto3-stubs documentation](./paginators.md#listdirectoriespaginator)
        """


class ListFacetAttributesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListFacetAttributes)[Show boto3-stubs documentation](./paginators.md#listfacetattributespaginator)
    """

    def paginate(
        self, SchemaArn: str, Name: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListFacetAttributesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListFacetAttributes.paginate)
        [Show boto3-stubs documentation](./paginators.md#listfacetattributespaginator)
        """


class ListFacetNamesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListFacetNames)[Show boto3-stubs documentation](./paginators.md#listfacetnamespaginator)
    """

    def paginate(
        self, SchemaArn: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListFacetNamesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListFacetNames.paginate)
        [Show boto3-stubs documentation](./paginators.md#listfacetnamespaginator)
        """


class ListIncomingTypedLinksPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListIncomingTypedLinks)[Show boto3-stubs documentation](./paginators.md#listincomingtypedlinkspaginator)
    """

    def paginate(
        self,
        DirectoryArn: str,
        ObjectReference: "ObjectReferenceTypeDef",
        FilterAttributeRanges: List["TypedLinkAttributeRangeTypeDef"] = None,
        FilterTypedLink: "TypedLinkSchemaAndFacetNameTypeDef" = None,
        ConsistencyLevel: ConsistencyLevelType = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListIncomingTypedLinksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListIncomingTypedLinks.paginate)
        [Show boto3-stubs documentation](./paginators.md#listincomingtypedlinkspaginator)
        """


class ListIndexPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListIndex)[Show boto3-stubs documentation](./paginators.md#listindexpaginator)
    """

    def paginate(
        self,
        DirectoryArn: str,
        IndexReference: "ObjectReferenceTypeDef",
        RangesOnIndexedValues: List["ObjectAttributeRangeTypeDef"] = None,
        ConsistencyLevel: ConsistencyLevelType = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListIndexResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListIndex.paginate)
        [Show boto3-stubs documentation](./paginators.md#listindexpaginator)
        """


class ListManagedSchemaArnsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListManagedSchemaArns)[Show boto3-stubs documentation](./paginators.md#listmanagedschemaarnspaginator)
    """

    def paginate(
        self, SchemaArn: str = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListManagedSchemaArnsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListManagedSchemaArns.paginate)
        [Show boto3-stubs documentation](./paginators.md#listmanagedschemaarnspaginator)
        """


class ListObjectAttributesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListObjectAttributes)[Show boto3-stubs documentation](./paginators.md#listobjectattributespaginator)
    """

    def paginate(
        self,
        DirectoryArn: str,
        ObjectReference: "ObjectReferenceTypeDef",
        ConsistencyLevel: ConsistencyLevelType = None,
        FacetFilter: "SchemaFacetTypeDef" = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListObjectAttributesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListObjectAttributes.paginate)
        [Show boto3-stubs documentation](./paginators.md#listobjectattributespaginator)
        """


class ListObjectParentPathsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListObjectParentPaths)[Show boto3-stubs documentation](./paginators.md#listobjectparentpathspaginator)
    """

    def paginate(
        self,
        DirectoryArn: str,
        ObjectReference: "ObjectReferenceTypeDef",
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListObjectParentPathsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListObjectParentPaths.paginate)
        [Show boto3-stubs documentation](./paginators.md#listobjectparentpathspaginator)
        """


class ListObjectPoliciesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListObjectPolicies)[Show boto3-stubs documentation](./paginators.md#listobjectpoliciespaginator)
    """

    def paginate(
        self,
        DirectoryArn: str,
        ObjectReference: "ObjectReferenceTypeDef",
        ConsistencyLevel: ConsistencyLevelType = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListObjectPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListObjectPolicies.paginate)
        [Show boto3-stubs documentation](./paginators.md#listobjectpoliciespaginator)
        """


class ListOutgoingTypedLinksPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListOutgoingTypedLinks)[Show boto3-stubs documentation](./paginators.md#listoutgoingtypedlinkspaginator)
    """

    def paginate(
        self,
        DirectoryArn: str,
        ObjectReference: "ObjectReferenceTypeDef",
        FilterAttributeRanges: List["TypedLinkAttributeRangeTypeDef"] = None,
        FilterTypedLink: "TypedLinkSchemaAndFacetNameTypeDef" = None,
        ConsistencyLevel: ConsistencyLevelType = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListOutgoingTypedLinksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListOutgoingTypedLinks.paginate)
        [Show boto3-stubs documentation](./paginators.md#listoutgoingtypedlinkspaginator)
        """


class ListPolicyAttachmentsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListPolicyAttachments)[Show boto3-stubs documentation](./paginators.md#listpolicyattachmentspaginator)
    """

    def paginate(
        self,
        DirectoryArn: str,
        PolicyReference: "ObjectReferenceTypeDef",
        ConsistencyLevel: ConsistencyLevelType = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListPolicyAttachmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListPolicyAttachments.paginate)
        [Show boto3-stubs documentation](./paginators.md#listpolicyattachmentspaginator)
        """


class ListPublishedSchemaArnsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListPublishedSchemaArns)[Show boto3-stubs documentation](./paginators.md#listpublishedschemaarnspaginator)
    """

    def paginate(
        self, SchemaArn: str = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListPublishedSchemaArnsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListPublishedSchemaArns.paginate)
        [Show boto3-stubs documentation](./paginators.md#listpublishedschemaarnspaginator)
        """


class ListTagsForResourcePaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListTagsForResource)[Show boto3-stubs documentation](./paginators.md#listtagsforresourcepaginator)
    """

    def paginate(
        self, ResourceArn: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListTagsForResource.paginate)
        [Show boto3-stubs documentation](./paginators.md#listtagsforresourcepaginator)
        """


class ListTypedLinkFacetAttributesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListTypedLinkFacetAttributes)[Show boto3-stubs documentation](./paginators.md#listtypedlinkfacetattributespaginator)
    """

    def paginate(
        self, SchemaArn: str, Name: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListTypedLinkFacetAttributesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListTypedLinkFacetAttributes.paginate)
        [Show boto3-stubs documentation](./paginators.md#listtypedlinkfacetattributespaginator)
        """


class ListTypedLinkFacetNamesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListTypedLinkFacetNames)[Show boto3-stubs documentation](./paginators.md#listtypedlinkfacetnamespaginator)
    """

    def paginate(
        self, SchemaArn: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListTypedLinkFacetNamesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListTypedLinkFacetNames.paginate)
        [Show boto3-stubs documentation](./paginators.md#listtypedlinkfacetnamespaginator)
        """


class LookupPolicyPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.LookupPolicy)[Show boto3-stubs documentation](./paginators.md#lookuppolicypaginator)
    """

    def paginate(
        self,
        DirectoryArn: str,
        ObjectReference: "ObjectReferenceTypeDef",
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[LookupPolicyResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/clouddirectory.html#CloudDirectory.Paginator.LookupPolicy.paginate)
        [Show boto3-stubs documentation](./paginators.md#lookuppolicypaginator)
        """
