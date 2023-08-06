"""
Type annotations for iotsecuretunneling service literal definitions.

[Open documentation](./literals.md)

Usage::

    ```python
    from mypy_boto3_iotsecuretunneling.literals import ConnectionStatusType

    data: ConnectionStatusType = "CONNECTED"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ConnectionStatusType", "TunnelStatusType")


ConnectionStatusType = Literal["CONNECTED", "DISCONNECTED"]
TunnelStatusType = Literal["CLOSED", "OPEN"]
