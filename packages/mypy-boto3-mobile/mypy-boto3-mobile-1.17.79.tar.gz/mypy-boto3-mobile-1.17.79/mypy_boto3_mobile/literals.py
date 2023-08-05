"""
Type annotations for mobile service literal definitions.

[Open documentation](./literals.md)

Usage::

    ```python
    from mypy_boto3_mobile.literals import ListBundlesPaginatorName

    data: ListBundlesPaginatorName = "list_bundles"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "ListBundlesPaginatorName",
    "ListProjectsPaginatorName",
    "PlatformType",
    "ProjectStateType",
)


ListBundlesPaginatorName = Literal["list_bundles"]
ListProjectsPaginatorName = Literal["list_projects"]
PlatformType = Literal["ANDROID", "JAVASCRIPT", "LINUX", "OBJC", "OSX", "SWIFT", "WINDOWS"]
ProjectStateType = Literal["IMPORTING", "NORMAL", "SYNCING"]
