"""
Type annotations for redshift-data service client.

[Open documentation](./client.md)

Usage::

    ```python
    import boto3
    from mypy_boto3_redshift_data import RedshiftDataAPIServiceClient

    client: RedshiftDataAPIServiceClient = boto3.client("redshift-data")
    ```
"""
import sys
from typing import Any, Dict, Type, overload

from botocore.client import ClientMeta

from .literals import StatusStringType
from .paginator import (
    DescribeTablePaginator,
    GetStatementResultPaginator,
    ListDatabasesPaginator,
    ListSchemasPaginator,
    ListStatementsPaginator,
    ListTablesPaginator,
)
from .type_defs import (
    CancelStatementResponseTypeDef,
    DescribeStatementResponseTypeDef,
    DescribeTableResponseTypeDef,
    ExecuteStatementOutputTypeDef,
    GetStatementResultResponseTypeDef,
    ListDatabasesResponseTypeDef,
    ListSchemasResponseTypeDef,
    ListStatementsResponseTypeDef,
    ListTablesResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("RedshiftDataAPIServiceClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ActiveStatementsExceededException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ExecuteStatementException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class RedshiftDataAPIServiceClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/redshift-data.html#RedshiftDataAPIService.Client)
    [Show boto3-stubs documentation](./client.md)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/redshift-data.html#RedshiftDataAPIService.Client.can_paginate)
        [Show boto3-stubs documentation](./client.md#can_paginate)
        """

    def cancel_statement(self, Id: str) -> CancelStatementResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/redshift-data.html#RedshiftDataAPIService.Client.cancel_statement)
        [Show boto3-stubs documentation](./client.md#cancel_statement)
        """

    def describe_statement(self, Id: str) -> DescribeStatementResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/redshift-data.html#RedshiftDataAPIService.Client.describe_statement)
        [Show boto3-stubs documentation](./client.md#describe_statement)
        """

    def describe_table(
        self,
        ClusterIdentifier: str,
        Database: str,
        ConnectedDatabase: str = None,
        DbUser: str = None,
        MaxResults: int = None,
        NextToken: str = None,
        Schema: str = None,
        SecretArn: str = None,
        Table: str = None,
    ) -> DescribeTableResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/redshift-data.html#RedshiftDataAPIService.Client.describe_table)
        [Show boto3-stubs documentation](./client.md#describe_table)
        """

    def execute_statement(
        self,
        ClusterIdentifier: str,
        Sql: str,
        Database: str = None,
        DbUser: str = None,
        SecretArn: str = None,
        StatementName: str = None,
        WithEvent: bool = None,
    ) -> ExecuteStatementOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/redshift-data.html#RedshiftDataAPIService.Client.execute_statement)
        [Show boto3-stubs documentation](./client.md#execute_statement)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/redshift-data.html#RedshiftDataAPIService.Client.generate_presigned_url)
        [Show boto3-stubs documentation](./client.md#generate_presigned_url)
        """

    def get_statement_result(
        self, Id: str, NextToken: str = None
    ) -> GetStatementResultResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/redshift-data.html#RedshiftDataAPIService.Client.get_statement_result)
        [Show boto3-stubs documentation](./client.md#get_statement_result)
        """

    def list_databases(
        self,
        ClusterIdentifier: str,
        Database: str = None,
        DbUser: str = None,
        MaxResults: int = None,
        NextToken: str = None,
        SecretArn: str = None,
    ) -> ListDatabasesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/redshift-data.html#RedshiftDataAPIService.Client.list_databases)
        [Show boto3-stubs documentation](./client.md#list_databases)
        """

    def list_schemas(
        self,
        ClusterIdentifier: str,
        Database: str,
        ConnectedDatabase: str = None,
        DbUser: str = None,
        MaxResults: int = None,
        NextToken: str = None,
        SchemaPattern: str = None,
        SecretArn: str = None,
    ) -> ListSchemasResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/redshift-data.html#RedshiftDataAPIService.Client.list_schemas)
        [Show boto3-stubs documentation](./client.md#list_schemas)
        """

    def list_statements(
        self,
        MaxResults: int = None,
        NextToken: str = None,
        RoleLevel: bool = None,
        StatementName: str = None,
        Status: StatusStringType = None,
    ) -> ListStatementsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/redshift-data.html#RedshiftDataAPIService.Client.list_statements)
        [Show boto3-stubs documentation](./client.md#list_statements)
        """

    def list_tables(
        self,
        ClusterIdentifier: str,
        Database: str,
        ConnectedDatabase: str = None,
        DbUser: str = None,
        MaxResults: int = None,
        NextToken: str = None,
        SchemaPattern: str = None,
        SecretArn: str = None,
        TablePattern: str = None,
    ) -> ListTablesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/redshift-data.html#RedshiftDataAPIService.Client.list_tables)
        [Show boto3-stubs documentation](./client.md#list_tables)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_table"]) -> DescribeTablePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/redshift-data.html#RedshiftDataAPIService.Paginator.DescribeTable)[Show boto3-stubs documentation](./paginators.md#describetablepaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_statement_result"]
    ) -> GetStatementResultPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/redshift-data.html#RedshiftDataAPIService.Paginator.GetStatementResult)[Show boto3-stubs documentation](./paginators.md#getstatementresultpaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_databases"]) -> ListDatabasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/redshift-data.html#RedshiftDataAPIService.Paginator.ListDatabases)[Show boto3-stubs documentation](./paginators.md#listdatabasespaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_schemas"]) -> ListSchemasPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/redshift-data.html#RedshiftDataAPIService.Paginator.ListSchemas)[Show boto3-stubs documentation](./paginators.md#listschemaspaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_statements"]) -> ListStatementsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/redshift-data.html#RedshiftDataAPIService.Paginator.ListStatements)[Show boto3-stubs documentation](./paginators.md#liststatementspaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_tables"]) -> ListTablesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/redshift-data.html#RedshiftDataAPIService.Paginator.ListTables)[Show boto3-stubs documentation](./paginators.md#listtablespaginator)
        """
