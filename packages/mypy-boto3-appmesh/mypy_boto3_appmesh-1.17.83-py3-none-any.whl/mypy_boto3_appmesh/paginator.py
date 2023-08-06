"""
Type annotations for appmesh service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_appmesh import AppMeshClient
    from mypy_boto3_appmesh.paginator import (
        ListGatewayRoutesPaginator,
        ListMeshesPaginator,
        ListRoutesPaginator,
        ListTagsForResourcePaginator,
        ListVirtualGatewaysPaginator,
        ListVirtualNodesPaginator,
        ListVirtualRoutersPaginator,
        ListVirtualServicesPaginator,
    )

    client: AppMeshClient = boto3.client("appmesh")

    list_gateway_routes_paginator: ListGatewayRoutesPaginator = client.get_paginator("list_gateway_routes")
    list_meshes_paginator: ListMeshesPaginator = client.get_paginator("list_meshes")
    list_routes_paginator: ListRoutesPaginator = client.get_paginator("list_routes")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    list_virtual_gateways_paginator: ListVirtualGatewaysPaginator = client.get_paginator("list_virtual_gateways")
    list_virtual_nodes_paginator: ListVirtualNodesPaginator = client.get_paginator("list_virtual_nodes")
    list_virtual_routers_paginator: ListVirtualRoutersPaginator = client.get_paginator("list_virtual_routers")
    list_virtual_services_paginator: ListVirtualServicesPaginator = client.get_paginator("list_virtual_services")
    ```
"""
from typing import Iterator

from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ListGatewayRoutesOutputTypeDef,
    ListMeshesOutputTypeDef,
    ListRoutesOutputTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListVirtualGatewaysOutputTypeDef,
    ListVirtualNodesOutputTypeDef,
    ListVirtualRoutersOutputTypeDef,
    ListVirtualServicesOutputTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListGatewayRoutesPaginator",
    "ListMeshesPaginator",
    "ListRoutesPaginator",
    "ListTagsForResourcePaginator",
    "ListVirtualGatewaysPaginator",
    "ListVirtualNodesPaginator",
    "ListVirtualRoutersPaginator",
    "ListVirtualServicesPaginator",
)


class ListGatewayRoutesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/appmesh.html#AppMesh.Paginator.ListGatewayRoutes)[Show boto3-stubs documentation](./paginators.md#listgatewayroutespaginator)
    """

    def paginate(
        self,
        meshName: str,
        virtualGatewayName: str,
        meshOwner: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListGatewayRoutesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/appmesh.html#AppMesh.Paginator.ListGatewayRoutes.paginate)
        [Show boto3-stubs documentation](./paginators.md#listgatewayroutespaginator)
        """


class ListMeshesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/appmesh.html#AppMesh.Paginator.ListMeshes)[Show boto3-stubs documentation](./paginators.md#listmeshespaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListMeshesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/appmesh.html#AppMesh.Paginator.ListMeshes.paginate)
        [Show boto3-stubs documentation](./paginators.md#listmeshespaginator)
        """


class ListRoutesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/appmesh.html#AppMesh.Paginator.ListRoutes)[Show boto3-stubs documentation](./paginators.md#listroutespaginator)
    """

    def paginate(
        self,
        meshName: str,
        virtualRouterName: str,
        meshOwner: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListRoutesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/appmesh.html#AppMesh.Paginator.ListRoutes.paginate)
        [Show boto3-stubs documentation](./paginators.md#listroutespaginator)
        """


class ListTagsForResourcePaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/appmesh.html#AppMesh.Paginator.ListTagsForResource)[Show boto3-stubs documentation](./paginators.md#listtagsforresourcepaginator)
    """

    def paginate(
        self, resourceArn: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListTagsForResourceOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/appmesh.html#AppMesh.Paginator.ListTagsForResource.paginate)
        [Show boto3-stubs documentation](./paginators.md#listtagsforresourcepaginator)
        """


class ListVirtualGatewaysPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/appmesh.html#AppMesh.Paginator.ListVirtualGateways)[Show boto3-stubs documentation](./paginators.md#listvirtualgatewayspaginator)
    """

    def paginate(
        self, meshName: str, meshOwner: str = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListVirtualGatewaysOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/appmesh.html#AppMesh.Paginator.ListVirtualGateways.paginate)
        [Show boto3-stubs documentation](./paginators.md#listvirtualgatewayspaginator)
        """


class ListVirtualNodesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/appmesh.html#AppMesh.Paginator.ListVirtualNodes)[Show boto3-stubs documentation](./paginators.md#listvirtualnodespaginator)
    """

    def paginate(
        self, meshName: str, meshOwner: str = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListVirtualNodesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/appmesh.html#AppMesh.Paginator.ListVirtualNodes.paginate)
        [Show boto3-stubs documentation](./paginators.md#listvirtualnodespaginator)
        """


class ListVirtualRoutersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/appmesh.html#AppMesh.Paginator.ListVirtualRouters)[Show boto3-stubs documentation](./paginators.md#listvirtualrouterspaginator)
    """

    def paginate(
        self, meshName: str, meshOwner: str = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListVirtualRoutersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/appmesh.html#AppMesh.Paginator.ListVirtualRouters.paginate)
        [Show boto3-stubs documentation](./paginators.md#listvirtualrouterspaginator)
        """


class ListVirtualServicesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/appmesh.html#AppMesh.Paginator.ListVirtualServices)[Show boto3-stubs documentation](./paginators.md#listvirtualservicespaginator)
    """

    def paginate(
        self, meshName: str, meshOwner: str = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListVirtualServicesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/appmesh.html#AppMesh.Paginator.ListVirtualServices.paginate)
        [Show boto3-stubs documentation](./paginators.md#listvirtualservicespaginator)
        """
