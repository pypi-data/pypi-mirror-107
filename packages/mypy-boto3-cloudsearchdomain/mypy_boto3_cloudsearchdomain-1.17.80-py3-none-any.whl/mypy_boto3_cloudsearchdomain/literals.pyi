"""
Type annotations for cloudsearchdomain service literal definitions.

[Open documentation](./literals.md)

Usage::

    ```python
    from mypy_boto3_cloudsearchdomain.literals import ContentTypeType

    data: ContentTypeType = "application/json"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("ContentTypeType", "QueryParserType")

ContentTypeType = Literal["application/json", "application/xml"]
QueryParserType = Literal["dismax", "lucene", "simple", "structured"]
