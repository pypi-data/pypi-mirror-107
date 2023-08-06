"""
Type annotations for kinesis-video-signaling service literal definitions.

[Open documentation](./literals.md)

Usage::

    ```python
    from mypy_boto3_kinesis_video_signaling.literals import ServiceType

    data: ServiceType = "TURN"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("ServiceType",)

ServiceType = Literal["TURN"]
