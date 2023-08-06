"""
Type annotations for kafka service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_kafka import KafkaClient
    from mypy_boto3_kafka.paginator import (
        ListClusterOperationsPaginator,
        ListClustersPaginator,
        ListConfigurationRevisionsPaginator,
        ListConfigurationsPaginator,
        ListKafkaVersionsPaginator,
        ListNodesPaginator,
        ListScramSecretsPaginator,
    )

    client: KafkaClient = boto3.client("kafka")

    list_cluster_operations_paginator: ListClusterOperationsPaginator = client.get_paginator("list_cluster_operations")
    list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
    list_configuration_revisions_paginator: ListConfigurationRevisionsPaginator = client.get_paginator("list_configuration_revisions")
    list_configurations_paginator: ListConfigurationsPaginator = client.get_paginator("list_configurations")
    list_kafka_versions_paginator: ListKafkaVersionsPaginator = client.get_paginator("list_kafka_versions")
    list_nodes_paginator: ListNodesPaginator = client.get_paginator("list_nodes")
    list_scram_secrets_paginator: ListScramSecretsPaginator = client.get_paginator("list_scram_secrets")
    ```
"""
from typing import Iterator

from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ListClusterOperationsResponseTypeDef,
    ListClustersResponseTypeDef,
    ListConfigurationRevisionsResponseTypeDef,
    ListConfigurationsResponseTypeDef,
    ListKafkaVersionsResponseTypeDef,
    ListNodesResponseTypeDef,
    ListScramSecretsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListClusterOperationsPaginator",
    "ListClustersPaginator",
    "ListConfigurationRevisionsPaginator",
    "ListConfigurationsPaginator",
    "ListKafkaVersionsPaginator",
    "ListNodesPaginator",
    "ListScramSecretsPaginator",
)


class ListClusterOperationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kafka.html#Kafka.Paginator.ListClusterOperations)[Show boto3-stubs documentation](./paginators.md#listclusteroperationspaginator)
    """

    def paginate(
        self, ClusterArn: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListClusterOperationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kafka.html#Kafka.Paginator.ListClusterOperations.paginate)
        [Show boto3-stubs documentation](./paginators.md#listclusteroperationspaginator)
        """


class ListClustersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kafka.html#Kafka.Paginator.ListClusters)[Show boto3-stubs documentation](./paginators.md#listclusterspaginator)
    """

    def paginate(
        self, ClusterNameFilter: str = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kafka.html#Kafka.Paginator.ListClusters.paginate)
        [Show boto3-stubs documentation](./paginators.md#listclusterspaginator)
        """


class ListConfigurationRevisionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kafka.html#Kafka.Paginator.ListConfigurationRevisions)[Show boto3-stubs documentation](./paginators.md#listconfigurationrevisionspaginator)
    """

    def paginate(
        self, Arn: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListConfigurationRevisionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kafka.html#Kafka.Paginator.ListConfigurationRevisions.paginate)
        [Show boto3-stubs documentation](./paginators.md#listconfigurationrevisionspaginator)
        """


class ListConfigurationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kafka.html#Kafka.Paginator.ListConfigurations)[Show boto3-stubs documentation](./paginators.md#listconfigurationspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kafka.html#Kafka.Paginator.ListConfigurations.paginate)
        [Show boto3-stubs documentation](./paginators.md#listconfigurationspaginator)
        """


class ListKafkaVersionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kafka.html#Kafka.Paginator.ListKafkaVersions)[Show boto3-stubs documentation](./paginators.md#listkafkaversionspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListKafkaVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kafka.html#Kafka.Paginator.ListKafkaVersions.paginate)
        [Show boto3-stubs documentation](./paginators.md#listkafkaversionspaginator)
        """


class ListNodesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kafka.html#Kafka.Paginator.ListNodes)[Show boto3-stubs documentation](./paginators.md#listnodespaginator)
    """

    def paginate(
        self, ClusterArn: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListNodesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kafka.html#Kafka.Paginator.ListNodes.paginate)
        [Show boto3-stubs documentation](./paginators.md#listnodespaginator)
        """


class ListScramSecretsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kafka.html#Kafka.Paginator.ListScramSecrets)[Show boto3-stubs documentation](./paginators.md#listscramsecretspaginator)
    """

    def paginate(
        self, ClusterArn: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListScramSecretsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kafka.html#Kafka.Paginator.ListScramSecrets.paginate)
        [Show boto3-stubs documentation](./paginators.md#listscramsecretspaginator)
        """
