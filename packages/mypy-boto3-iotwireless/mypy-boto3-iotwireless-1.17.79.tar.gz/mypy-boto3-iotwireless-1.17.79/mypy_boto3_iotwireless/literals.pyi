"""
Type annotations for iotwireless service literal definitions.

[Open documentation](./literals.md)

Usage::

    ```python
    from mypy_boto3_iotwireless.literals import BatteryLevelType

    data: BatteryLevelType = "critical"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "BatteryLevelType",
    "ConnectionStatusType",
    "DeviceStateType",
    "EventType",
    "ExpressionTypeType",
    "MessageTypeType",
    "PartnerTypeType",
    "SigningAlgType",
    "WirelessDeviceIdTypeType",
    "WirelessDeviceTypeType",
    "WirelessGatewayIdTypeType",
    "WirelessGatewayServiceTypeType",
    "WirelessGatewayTaskDefinitionTypeType",
    "WirelessGatewayTaskStatusType",
)

BatteryLevelType = Literal["critical", "low", "normal"]
ConnectionStatusType = Literal["Connected", "Disconnected"]
DeviceStateType = Literal[
    "Provisioned", "RegisteredNotSeen", "RegisteredReachable", "RegisteredUnreachable"
]
EventType = Literal["ack", "discovered", "lost", "nack", "passthrough"]
ExpressionTypeType = Literal["MqttTopic", "RuleName"]
MessageTypeType = Literal[
    "CUSTOM_COMMAND_ID_GET",
    "CUSTOM_COMMAND_ID_NOTIFY",
    "CUSTOM_COMMAND_ID_RESP",
    "CUSTOM_COMMAND_ID_SET",
]
PartnerTypeType = Literal["Sidewalk"]
SigningAlgType = Literal["Ed25519", "P256r1"]
WirelessDeviceIdTypeType = Literal["DevEui", "ThingName", "WirelessDeviceId"]
WirelessDeviceTypeType = Literal["LoRaWAN", "Sidewalk"]
WirelessGatewayIdTypeType = Literal["GatewayEui", "ThingName", "WirelessGatewayId"]
WirelessGatewayServiceTypeType = Literal["CUPS", "LNS"]
WirelessGatewayTaskDefinitionTypeType = Literal["UPDATE"]
WirelessGatewayTaskStatusType = Literal[
    "COMPLETED", "FAILED", "FIRST_RETRY", "IN_PROGRESS", "PENDING", "SECOND_RETRY"
]
