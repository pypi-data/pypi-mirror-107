from typing import List, Optional
from cloudrail.knowledge.context.aws.kms.kms_key import KmsKey

from cloudrail.knowledge.context.aws.networking_config.inetwork_configuration import INetworkConfiguration
from cloudrail.knowledge.context.aws.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.networking_config.network_entity import NetworkEntity


class RdsInstance(NetworkEntity, INetworkConfiguration):
    """
        Attributes:
            name: The name of the instance.
            arn: The ARN of the instance.
            port: The port the instance is listening on.
            publicly_accessible: True if the database is configured to have
                a public IP address.
            db_subnet_group_name: The name of the SB subnet group.
            security_group_ids: The IDs of the security groups in use
                with the instance.
            db_cluster_id: The cluster ID, if this instance is part of a cluster,
                or None otherwise.
            encrypted_at_rest: True is encryption at rest is enabled.
            performance_insights_enabled: True if performance insights is enabled.
            performance_insights_kms_key: The ARN of the KMS Key used to encrypt
                the performance insights, if any is used.
            performance_insights_kms_data: The actual KMS Key object, if a KMS key
                is used to encrypt performance insights.
    """
    def __init__(self,
                 account: str,
                 region: str,
                 name: str,
                 arn: str,
                 port: int,
                 publicly_accessible: bool,
                 db_subnet_group_name: str,
                 security_group_ids: List[str],
                 db_cluster_id: Optional[str],
                 encrypted_at_rest: bool,
                 performance_insights_enabled: bool,
                 performance_insights_kms_key: Optional[str]):
        super().__init__(name, account, region, AwsServiceName.AWS_RDS_CLUSTER_INSTANCE)
        self.arn: str = arn
        self.port: int = port
        self.db_subnet_group_name: str = db_subnet_group_name
        self.is_in_default_vpc: bool = db_subnet_group_name is None
        self.network_configuration: NetworkConfiguration = NetworkConfiguration(publicly_accessible, security_group_ids, None)
        self.db_cluster_id: Optional[str] = db_cluster_id
        self.encrypted_at_rest: bool = encrypted_at_rest
        self.performance_insights_kms_key: Optional[str] = performance_insights_kms_key
        self.performance_insights_enabled: bool = performance_insights_enabled
        self.performance_insights_kms_data: Optional[KmsKey] = None

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_name(self) -> str:
        return self.name

    def get_arn(self) -> str:
        return self.arn

    def get_extra_data(self) -> str:
        port = 'port: {}'.format(self.port) if self.port else ''
        db_subnet_group_name = 'db_subnet_group_name: {}'.format(self.db_subnet_group_name) if self.db_subnet_group_name else ''

        return ', '.join([port, db_subnet_group_name])

    def get_all_network_configurations(self) -> List[NetworkConfiguration]:
        return [self.network_configuration]

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'RDS Instance'
        else:
            return 'RDS Instances'

    def get_cloud_resource_url(self) -> Optional[str]:
        return '{0}rds/home?region={1}#database:id={2};is-cluster=false'\
            .format(self.AWS_CONSOLE_URL, self.region, self.db_cluster_id)

    @property
    def is_tagable(self) -> bool:
        return True
