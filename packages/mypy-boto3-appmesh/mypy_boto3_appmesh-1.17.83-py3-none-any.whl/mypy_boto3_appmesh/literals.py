"""
Type annotations for appmesh service literal definitions.

[Open documentation](./literals.md)

Usage::

    ```python
    from mypy_boto3_appmesh.literals import DurationUnitType

    data: DurationUnitType = "ms"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "DurationUnitType",
    "EgressFilterTypeType",
    "GatewayRouteStatusCodeType",
    "GrpcRetryPolicyEventType",
    "HttpMethodType",
    "HttpSchemeType",
    "ListGatewayRoutesPaginatorName",
    "ListMeshesPaginatorName",
    "ListRoutesPaginatorName",
    "ListTagsForResourcePaginatorName",
    "ListVirtualGatewaysPaginatorName",
    "ListVirtualNodesPaginatorName",
    "ListVirtualRoutersPaginatorName",
    "ListVirtualServicesPaginatorName",
    "ListenerTlsModeType",
    "MeshStatusCodeType",
    "PortProtocolType",
    "RouteStatusCodeType",
    "TcpRetryPolicyEventType",
    "VirtualGatewayListenerTlsModeType",
    "VirtualGatewayPortProtocolType",
    "VirtualGatewayStatusCodeType",
    "VirtualNodeStatusCodeType",
    "VirtualRouterStatusCodeType",
    "VirtualServiceStatusCodeType",
)


DurationUnitType = Literal["ms", "s"]
EgressFilterTypeType = Literal["ALLOW_ALL", "DROP_ALL"]
GatewayRouteStatusCodeType = Literal["ACTIVE", "DELETED", "INACTIVE"]
GrpcRetryPolicyEventType = Literal[
    "cancelled", "deadline-exceeded", "internal", "resource-exhausted", "unavailable"
]
HttpMethodType = Literal[
    "CONNECT", "DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT", "TRACE"
]
HttpSchemeType = Literal["http", "https"]
ListGatewayRoutesPaginatorName = Literal["list_gateway_routes"]
ListMeshesPaginatorName = Literal["list_meshes"]
ListRoutesPaginatorName = Literal["list_routes"]
ListTagsForResourcePaginatorName = Literal["list_tags_for_resource"]
ListVirtualGatewaysPaginatorName = Literal["list_virtual_gateways"]
ListVirtualNodesPaginatorName = Literal["list_virtual_nodes"]
ListVirtualRoutersPaginatorName = Literal["list_virtual_routers"]
ListVirtualServicesPaginatorName = Literal["list_virtual_services"]
ListenerTlsModeType = Literal["DISABLED", "PERMISSIVE", "STRICT"]
MeshStatusCodeType = Literal["ACTIVE", "DELETED", "INACTIVE"]
PortProtocolType = Literal["grpc", "http", "http2", "tcp"]
RouteStatusCodeType = Literal["ACTIVE", "DELETED", "INACTIVE"]
TcpRetryPolicyEventType = Literal["connection-error"]
VirtualGatewayListenerTlsModeType = Literal["DISABLED", "PERMISSIVE", "STRICT"]
VirtualGatewayPortProtocolType = Literal["grpc", "http", "http2"]
VirtualGatewayStatusCodeType = Literal["ACTIVE", "DELETED", "INACTIVE"]
VirtualNodeStatusCodeType = Literal["ACTIVE", "DELETED", "INACTIVE"]
VirtualRouterStatusCodeType = Literal["ACTIVE", "DELETED", "INACTIVE"]
VirtualServiceStatusCodeType = Literal["ACTIVE", "DELETED", "INACTIVE"]
