"""
Type annotations for iot service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_iot import IoTClient
    from mypy_boto3_iot.paginator import (
        GetBehaviorModelTrainingSummariesPaginator,
        ListActiveViolationsPaginator,
        ListAttachedPoliciesPaginator,
        ListAuditFindingsPaginator,
        ListAuditMitigationActionsExecutionsPaginator,
        ListAuditMitigationActionsTasksPaginator,
        ListAuditSuppressionsPaginator,
        ListAuditTasksPaginator,
        ListAuthorizersPaginator,
        ListBillingGroupsPaginator,
        ListCACertificatesPaginator,
        ListCertificatesPaginator,
        ListCertificatesByCAPaginator,
        ListCustomMetricsPaginator,
        ListDetectMitigationActionsExecutionsPaginator,
        ListDetectMitigationActionsTasksPaginator,
        ListDimensionsPaginator,
        ListDomainConfigurationsPaginator,
        ListIndicesPaginator,
        ListJobExecutionsForJobPaginator,
        ListJobExecutionsForThingPaginator,
        ListJobsPaginator,
        ListMitigationActionsPaginator,
        ListOTAUpdatesPaginator,
        ListOutgoingCertificatesPaginator,
        ListPoliciesPaginator,
        ListPolicyPrincipalsPaginator,
        ListPrincipalPoliciesPaginator,
        ListPrincipalThingsPaginator,
        ListProvisioningTemplateVersionsPaginator,
        ListProvisioningTemplatesPaginator,
        ListRoleAliasesPaginator,
        ListScheduledAuditsPaginator,
        ListSecurityProfilesPaginator,
        ListSecurityProfilesForTargetPaginator,
        ListStreamsPaginator,
        ListTagsForResourcePaginator,
        ListTargetsForPolicyPaginator,
        ListTargetsForSecurityProfilePaginator,
        ListThingGroupsPaginator,
        ListThingGroupsForThingPaginator,
        ListThingPrincipalsPaginator,
        ListThingRegistrationTaskReportsPaginator,
        ListThingRegistrationTasksPaginator,
        ListThingTypesPaginator,
        ListThingsPaginator,
        ListThingsInBillingGroupPaginator,
        ListThingsInThingGroupPaginator,
        ListTopicRuleDestinationsPaginator,
        ListTopicRulesPaginator,
        ListV2LoggingLevelsPaginator,
        ListViolationEventsPaginator,
    )

    client: IoTClient = boto3.client("iot")

    get_behavior_model_training_summaries_paginator: GetBehaviorModelTrainingSummariesPaginator = client.get_paginator("get_behavior_model_training_summaries")
    list_active_violations_paginator: ListActiveViolationsPaginator = client.get_paginator("list_active_violations")
    list_attached_policies_paginator: ListAttachedPoliciesPaginator = client.get_paginator("list_attached_policies")
    list_audit_findings_paginator: ListAuditFindingsPaginator = client.get_paginator("list_audit_findings")
    list_audit_mitigation_actions_executions_paginator: ListAuditMitigationActionsExecutionsPaginator = client.get_paginator("list_audit_mitigation_actions_executions")
    list_audit_mitigation_actions_tasks_paginator: ListAuditMitigationActionsTasksPaginator = client.get_paginator("list_audit_mitigation_actions_tasks")
    list_audit_suppressions_paginator: ListAuditSuppressionsPaginator = client.get_paginator("list_audit_suppressions")
    list_audit_tasks_paginator: ListAuditTasksPaginator = client.get_paginator("list_audit_tasks")
    list_authorizers_paginator: ListAuthorizersPaginator = client.get_paginator("list_authorizers")
    list_billing_groups_paginator: ListBillingGroupsPaginator = client.get_paginator("list_billing_groups")
    list_ca_certificates_paginator: ListCACertificatesPaginator = client.get_paginator("list_ca_certificates")
    list_certificates_paginator: ListCertificatesPaginator = client.get_paginator("list_certificates")
    list_certificates_by_ca_paginator: ListCertificatesByCAPaginator = client.get_paginator("list_certificates_by_ca")
    list_custom_metrics_paginator: ListCustomMetricsPaginator = client.get_paginator("list_custom_metrics")
    list_detect_mitigation_actions_executions_paginator: ListDetectMitigationActionsExecutionsPaginator = client.get_paginator("list_detect_mitigation_actions_executions")
    list_detect_mitigation_actions_tasks_paginator: ListDetectMitigationActionsTasksPaginator = client.get_paginator("list_detect_mitigation_actions_tasks")
    list_dimensions_paginator: ListDimensionsPaginator = client.get_paginator("list_dimensions")
    list_domain_configurations_paginator: ListDomainConfigurationsPaginator = client.get_paginator("list_domain_configurations")
    list_indices_paginator: ListIndicesPaginator = client.get_paginator("list_indices")
    list_job_executions_for_job_paginator: ListJobExecutionsForJobPaginator = client.get_paginator("list_job_executions_for_job")
    list_job_executions_for_thing_paginator: ListJobExecutionsForThingPaginator = client.get_paginator("list_job_executions_for_thing")
    list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    list_mitigation_actions_paginator: ListMitigationActionsPaginator = client.get_paginator("list_mitigation_actions")
    list_ota_updates_paginator: ListOTAUpdatesPaginator = client.get_paginator("list_ota_updates")
    list_outgoing_certificates_paginator: ListOutgoingCertificatesPaginator = client.get_paginator("list_outgoing_certificates")
    list_policies_paginator: ListPoliciesPaginator = client.get_paginator("list_policies")
    list_policy_principals_paginator: ListPolicyPrincipalsPaginator = client.get_paginator("list_policy_principals")
    list_principal_policies_paginator: ListPrincipalPoliciesPaginator = client.get_paginator("list_principal_policies")
    list_principal_things_paginator: ListPrincipalThingsPaginator = client.get_paginator("list_principal_things")
    list_provisioning_template_versions_paginator: ListProvisioningTemplateVersionsPaginator = client.get_paginator("list_provisioning_template_versions")
    list_provisioning_templates_paginator: ListProvisioningTemplatesPaginator = client.get_paginator("list_provisioning_templates")
    list_role_aliases_paginator: ListRoleAliasesPaginator = client.get_paginator("list_role_aliases")
    list_scheduled_audits_paginator: ListScheduledAuditsPaginator = client.get_paginator("list_scheduled_audits")
    list_security_profiles_paginator: ListSecurityProfilesPaginator = client.get_paginator("list_security_profiles")
    list_security_profiles_for_target_paginator: ListSecurityProfilesForTargetPaginator = client.get_paginator("list_security_profiles_for_target")
    list_streams_paginator: ListStreamsPaginator = client.get_paginator("list_streams")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    list_targets_for_policy_paginator: ListTargetsForPolicyPaginator = client.get_paginator("list_targets_for_policy")
    list_targets_for_security_profile_paginator: ListTargetsForSecurityProfilePaginator = client.get_paginator("list_targets_for_security_profile")
    list_thing_groups_paginator: ListThingGroupsPaginator = client.get_paginator("list_thing_groups")
    list_thing_groups_for_thing_paginator: ListThingGroupsForThingPaginator = client.get_paginator("list_thing_groups_for_thing")
    list_thing_principals_paginator: ListThingPrincipalsPaginator = client.get_paginator("list_thing_principals")
    list_thing_registration_task_reports_paginator: ListThingRegistrationTaskReportsPaginator = client.get_paginator("list_thing_registration_task_reports")
    list_thing_registration_tasks_paginator: ListThingRegistrationTasksPaginator = client.get_paginator("list_thing_registration_tasks")
    list_thing_types_paginator: ListThingTypesPaginator = client.get_paginator("list_thing_types")
    list_things_paginator: ListThingsPaginator = client.get_paginator("list_things")
    list_things_in_billing_group_paginator: ListThingsInBillingGroupPaginator = client.get_paginator("list_things_in_billing_group")
    list_things_in_thing_group_paginator: ListThingsInThingGroupPaginator = client.get_paginator("list_things_in_thing_group")
    list_topic_rule_destinations_paginator: ListTopicRuleDestinationsPaginator = client.get_paginator("list_topic_rule_destinations")
    list_topic_rules_paginator: ListTopicRulesPaginator = client.get_paginator("list_topic_rules")
    list_v2_logging_levels_paginator: ListV2LoggingLevelsPaginator = client.get_paginator("list_v2_logging_levels")
    list_violation_events_paginator: ListViolationEventsPaginator = client.get_paginator("list_violation_events")
    ```
"""
from datetime import datetime
from typing import Iterator

from botocore.paginate import Paginator as Boto3Paginator

from .literals import (
    AuditMitigationActionsExecutionStatusType,
    AuditMitigationActionsTaskStatusType,
    AuditTaskStatusType,
    AuditTaskTypeType,
    AuthorizerStatusType,
    BehaviorCriteriaTypeType,
    JobExecutionStatusType,
    JobStatusType,
    LogTargetTypeType,
    MitigationActionTypeType,
    OTAUpdateStatusType,
    ReportTypeType,
    ServiceTypeType,
    StatusType,
    TargetSelectionType,
)
from .type_defs import (
    GetBehaviorModelTrainingSummariesResponseTypeDef,
    ListActiveViolationsResponseTypeDef,
    ListAttachedPoliciesResponseTypeDef,
    ListAuditFindingsResponseTypeDef,
    ListAuditMitigationActionsExecutionsResponseTypeDef,
    ListAuditMitigationActionsTasksResponseTypeDef,
    ListAuditSuppressionsResponseTypeDef,
    ListAuditTasksResponseTypeDef,
    ListAuthorizersResponseTypeDef,
    ListBillingGroupsResponseTypeDef,
    ListCACertificatesResponseTypeDef,
    ListCertificatesByCAResponseTypeDef,
    ListCertificatesResponseTypeDef,
    ListCustomMetricsResponseTypeDef,
    ListDetectMitigationActionsExecutionsResponseTypeDef,
    ListDetectMitigationActionsTasksResponseTypeDef,
    ListDimensionsResponseTypeDef,
    ListDomainConfigurationsResponseTypeDef,
    ListIndicesResponseTypeDef,
    ListJobExecutionsForJobResponseTypeDef,
    ListJobExecutionsForThingResponseTypeDef,
    ListJobsResponseTypeDef,
    ListMitigationActionsResponseTypeDef,
    ListOTAUpdatesResponseTypeDef,
    ListOutgoingCertificatesResponseTypeDef,
    ListPoliciesResponseTypeDef,
    ListPolicyPrincipalsResponseTypeDef,
    ListPrincipalPoliciesResponseTypeDef,
    ListPrincipalThingsResponseTypeDef,
    ListProvisioningTemplatesResponseTypeDef,
    ListProvisioningTemplateVersionsResponseTypeDef,
    ListRoleAliasesResponseTypeDef,
    ListScheduledAuditsResponseTypeDef,
    ListSecurityProfilesForTargetResponseTypeDef,
    ListSecurityProfilesResponseTypeDef,
    ListStreamsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTargetsForPolicyResponseTypeDef,
    ListTargetsForSecurityProfileResponseTypeDef,
    ListThingGroupsForThingResponseTypeDef,
    ListThingGroupsResponseTypeDef,
    ListThingPrincipalsResponseTypeDef,
    ListThingRegistrationTaskReportsResponseTypeDef,
    ListThingRegistrationTasksResponseTypeDef,
    ListThingsInBillingGroupResponseTypeDef,
    ListThingsInThingGroupResponseTypeDef,
    ListThingsResponseTypeDef,
    ListThingTypesResponseTypeDef,
    ListTopicRuleDestinationsResponseTypeDef,
    ListTopicRulesResponseTypeDef,
    ListV2LoggingLevelsResponseTypeDef,
    ListViolationEventsResponseTypeDef,
    PaginatorConfigTypeDef,
    ResourceIdentifierTypeDef,
)

__all__ = (
    "GetBehaviorModelTrainingSummariesPaginator",
    "ListActiveViolationsPaginator",
    "ListAttachedPoliciesPaginator",
    "ListAuditFindingsPaginator",
    "ListAuditMitigationActionsExecutionsPaginator",
    "ListAuditMitigationActionsTasksPaginator",
    "ListAuditSuppressionsPaginator",
    "ListAuditTasksPaginator",
    "ListAuthorizersPaginator",
    "ListBillingGroupsPaginator",
    "ListCACertificatesPaginator",
    "ListCertificatesPaginator",
    "ListCertificatesByCAPaginator",
    "ListCustomMetricsPaginator",
    "ListDetectMitigationActionsExecutionsPaginator",
    "ListDetectMitigationActionsTasksPaginator",
    "ListDimensionsPaginator",
    "ListDomainConfigurationsPaginator",
    "ListIndicesPaginator",
    "ListJobExecutionsForJobPaginator",
    "ListJobExecutionsForThingPaginator",
    "ListJobsPaginator",
    "ListMitigationActionsPaginator",
    "ListOTAUpdatesPaginator",
    "ListOutgoingCertificatesPaginator",
    "ListPoliciesPaginator",
    "ListPolicyPrincipalsPaginator",
    "ListPrincipalPoliciesPaginator",
    "ListPrincipalThingsPaginator",
    "ListProvisioningTemplateVersionsPaginator",
    "ListProvisioningTemplatesPaginator",
    "ListRoleAliasesPaginator",
    "ListScheduledAuditsPaginator",
    "ListSecurityProfilesPaginator",
    "ListSecurityProfilesForTargetPaginator",
    "ListStreamsPaginator",
    "ListTagsForResourcePaginator",
    "ListTargetsForPolicyPaginator",
    "ListTargetsForSecurityProfilePaginator",
    "ListThingGroupsPaginator",
    "ListThingGroupsForThingPaginator",
    "ListThingPrincipalsPaginator",
    "ListThingRegistrationTaskReportsPaginator",
    "ListThingRegistrationTasksPaginator",
    "ListThingTypesPaginator",
    "ListThingsPaginator",
    "ListThingsInBillingGroupPaginator",
    "ListThingsInThingGroupPaginator",
    "ListTopicRuleDestinationsPaginator",
    "ListTopicRulesPaginator",
    "ListV2LoggingLevelsPaginator",
    "ListViolationEventsPaginator",
)


class GetBehaviorModelTrainingSummariesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.GetBehaviorModelTrainingSummaries)[Show boto3-stubs documentation](./paginators.md#getbehaviormodeltrainingsummariespaginator)
    """

    def paginate(
        self, securityProfileName: str = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[GetBehaviorModelTrainingSummariesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.GetBehaviorModelTrainingSummaries.paginate)
        [Show boto3-stubs documentation](./paginators.md#getbehaviormodeltrainingsummariespaginator)
        """


class ListActiveViolationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListActiveViolations)[Show boto3-stubs documentation](./paginators.md#listactiveviolationspaginator)
    """

    def paginate(
        self,
        thingName: str = None,
        securityProfileName: str = None,
        behaviorCriteriaType: BehaviorCriteriaTypeType = None,
        listSuppressedAlerts: bool = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListActiveViolationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListActiveViolations.paginate)
        [Show boto3-stubs documentation](./paginators.md#listactiveviolationspaginator)
        """


class ListAttachedPoliciesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListAttachedPolicies)[Show boto3-stubs documentation](./paginators.md#listattachedpoliciespaginator)
    """

    def paginate(
        self, target: str, recursive: bool = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListAttachedPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListAttachedPolicies.paginate)
        [Show boto3-stubs documentation](./paginators.md#listattachedpoliciespaginator)
        """


class ListAuditFindingsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListAuditFindings)[Show boto3-stubs documentation](./paginators.md#listauditfindingspaginator)
    """

    def paginate(
        self,
        taskId: str = None,
        checkName: str = None,
        resourceIdentifier: "ResourceIdentifierTypeDef" = None,
        startTime: datetime = None,
        endTime: datetime = None,
        listSuppressedFindings: bool = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListAuditFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListAuditFindings.paginate)
        [Show boto3-stubs documentation](./paginators.md#listauditfindingspaginator)
        """


class ListAuditMitigationActionsExecutionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListAuditMitigationActionsExecutions)[Show boto3-stubs documentation](./paginators.md#listauditmitigationactionsexecutionspaginator)
    """

    def paginate(
        self,
        taskId: str,
        findingId: str,
        actionStatus: AuditMitigationActionsExecutionStatusType = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListAuditMitigationActionsExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListAuditMitigationActionsExecutions.paginate)
        [Show boto3-stubs documentation](./paginators.md#listauditmitigationactionsexecutionspaginator)
        """


class ListAuditMitigationActionsTasksPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListAuditMitigationActionsTasks)[Show boto3-stubs documentation](./paginators.md#listauditmitigationactionstaskspaginator)
    """

    def paginate(
        self,
        startTime: datetime,
        endTime: datetime,
        auditTaskId: str = None,
        findingId: str = None,
        taskStatus: AuditMitigationActionsTaskStatusType = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListAuditMitigationActionsTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListAuditMitigationActionsTasks.paginate)
        [Show boto3-stubs documentation](./paginators.md#listauditmitigationactionstaskspaginator)
        """


class ListAuditSuppressionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListAuditSuppressions)[Show boto3-stubs documentation](./paginators.md#listauditsuppressionspaginator)
    """

    def paginate(
        self,
        checkName: str = None,
        resourceIdentifier: "ResourceIdentifierTypeDef" = None,
        ascendingOrder: bool = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListAuditSuppressionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListAuditSuppressions.paginate)
        [Show boto3-stubs documentation](./paginators.md#listauditsuppressionspaginator)
        """


class ListAuditTasksPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListAuditTasks)[Show boto3-stubs documentation](./paginators.md#listaudittaskspaginator)
    """

    def paginate(
        self,
        startTime: datetime,
        endTime: datetime,
        taskType: AuditTaskTypeType = None,
        taskStatus: AuditTaskStatusType = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListAuditTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListAuditTasks.paginate)
        [Show boto3-stubs documentation](./paginators.md#listaudittaskspaginator)
        """


class ListAuthorizersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListAuthorizers)[Show boto3-stubs documentation](./paginators.md#listauthorizerspaginator)
    """

    def paginate(
        self,
        ascendingOrder: bool = None,
        status: AuthorizerStatusType = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListAuthorizersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListAuthorizers.paginate)
        [Show boto3-stubs documentation](./paginators.md#listauthorizerspaginator)
        """


class ListBillingGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListBillingGroups)[Show boto3-stubs documentation](./paginators.md#listbillinggroupspaginator)
    """

    def paginate(
        self, namePrefixFilter: str = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListBillingGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListBillingGroups.paginate)
        [Show boto3-stubs documentation](./paginators.md#listbillinggroupspaginator)
        """


class ListCACertificatesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListCACertificates)[Show boto3-stubs documentation](./paginators.md#listcacertificatespaginator)
    """

    def paginate(
        self, ascendingOrder: bool = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListCACertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListCACertificates.paginate)
        [Show boto3-stubs documentation](./paginators.md#listcacertificatespaginator)
        """


class ListCertificatesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListCertificates)[Show boto3-stubs documentation](./paginators.md#listcertificatespaginator)
    """

    def paginate(
        self, ascendingOrder: bool = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListCertificates.paginate)
        [Show boto3-stubs documentation](./paginators.md#listcertificatespaginator)
        """


class ListCertificatesByCAPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListCertificatesByCA)[Show boto3-stubs documentation](./paginators.md#listcertificatesbycapaginator)
    """

    def paginate(
        self,
        caCertificateId: str,
        ascendingOrder: bool = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListCertificatesByCAResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListCertificatesByCA.paginate)
        [Show boto3-stubs documentation](./paginators.md#listcertificatesbycapaginator)
        """


class ListCustomMetricsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListCustomMetrics)[Show boto3-stubs documentation](./paginators.md#listcustommetricspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListCustomMetricsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListCustomMetrics.paginate)
        [Show boto3-stubs documentation](./paginators.md#listcustommetricspaginator)
        """


class ListDetectMitigationActionsExecutionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListDetectMitigationActionsExecutions)[Show boto3-stubs documentation](./paginators.md#listdetectmitigationactionsexecutionspaginator)
    """

    def paginate(
        self,
        taskId: str = None,
        violationId: str = None,
        thingName: str = None,
        startTime: datetime = None,
        endTime: datetime = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListDetectMitigationActionsExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListDetectMitigationActionsExecutions.paginate)
        [Show boto3-stubs documentation](./paginators.md#listdetectmitigationactionsexecutionspaginator)
        """


class ListDetectMitigationActionsTasksPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListDetectMitigationActionsTasks)[Show boto3-stubs documentation](./paginators.md#listdetectmitigationactionstaskspaginator)
    """

    def paginate(
        self,
        startTime: datetime,
        endTime: datetime,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListDetectMitigationActionsTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListDetectMitigationActionsTasks.paginate)
        [Show boto3-stubs documentation](./paginators.md#listdetectmitigationactionstaskspaginator)
        """


class ListDimensionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListDimensions)[Show boto3-stubs documentation](./paginators.md#listdimensionspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListDimensionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListDimensions.paginate)
        [Show boto3-stubs documentation](./paginators.md#listdimensionspaginator)
        """


class ListDomainConfigurationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListDomainConfigurations)[Show boto3-stubs documentation](./paginators.md#listdomainconfigurationspaginator)
    """

    def paginate(
        self, serviceType: ServiceTypeType = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListDomainConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListDomainConfigurations.paginate)
        [Show boto3-stubs documentation](./paginators.md#listdomainconfigurationspaginator)
        """


class ListIndicesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListIndices)[Show boto3-stubs documentation](./paginators.md#listindicespaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListIndicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListIndices.paginate)
        [Show boto3-stubs documentation](./paginators.md#listindicespaginator)
        """


class ListJobExecutionsForJobPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListJobExecutionsForJob)[Show boto3-stubs documentation](./paginators.md#listjobexecutionsforjobpaginator)
    """

    def paginate(
        self,
        jobId: str,
        status: JobExecutionStatusType = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListJobExecutionsForJobResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListJobExecutionsForJob.paginate)
        [Show boto3-stubs documentation](./paginators.md#listjobexecutionsforjobpaginator)
        """


class ListJobExecutionsForThingPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListJobExecutionsForThing)[Show boto3-stubs documentation](./paginators.md#listjobexecutionsforthingpaginator)
    """

    def paginate(
        self,
        thingName: str,
        status: JobExecutionStatusType = None,
        namespaceId: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListJobExecutionsForThingResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListJobExecutionsForThing.paginate)
        [Show boto3-stubs documentation](./paginators.md#listjobexecutionsforthingpaginator)
        """


class ListJobsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListJobs)[Show boto3-stubs documentation](./paginators.md#listjobspaginator)
    """

    def paginate(
        self,
        status: JobStatusType = None,
        targetSelection: TargetSelectionType = None,
        thingGroupName: str = None,
        thingGroupId: str = None,
        namespaceId: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListJobs.paginate)
        [Show boto3-stubs documentation](./paginators.md#listjobspaginator)
        """


class ListMitigationActionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListMitigationActions)[Show boto3-stubs documentation](./paginators.md#listmitigationactionspaginator)
    """

    def paginate(
        self,
        actionType: MitigationActionTypeType = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListMitigationActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListMitigationActions.paginate)
        [Show boto3-stubs documentation](./paginators.md#listmitigationactionspaginator)
        """


class ListOTAUpdatesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListOTAUpdates)[Show boto3-stubs documentation](./paginators.md#listotaupdatespaginator)
    """

    def paginate(
        self,
        otaUpdateStatus: OTAUpdateStatusType = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListOTAUpdatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListOTAUpdates.paginate)
        [Show boto3-stubs documentation](./paginators.md#listotaupdatespaginator)
        """


class ListOutgoingCertificatesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListOutgoingCertificates)[Show boto3-stubs documentation](./paginators.md#listoutgoingcertificatespaginator)
    """

    def paginate(
        self, ascendingOrder: bool = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListOutgoingCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListOutgoingCertificates.paginate)
        [Show boto3-stubs documentation](./paginators.md#listoutgoingcertificatespaginator)
        """


class ListPoliciesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListPolicies)[Show boto3-stubs documentation](./paginators.md#listpoliciespaginator)
    """

    def paginate(
        self, ascendingOrder: bool = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListPolicies.paginate)
        [Show boto3-stubs documentation](./paginators.md#listpoliciespaginator)
        """


class ListPolicyPrincipalsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListPolicyPrincipals)[Show boto3-stubs documentation](./paginators.md#listpolicyprincipalspaginator)
    """

    def paginate(
        self,
        policyName: str,
        ascendingOrder: bool = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListPolicyPrincipalsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListPolicyPrincipals.paginate)
        [Show boto3-stubs documentation](./paginators.md#listpolicyprincipalspaginator)
        """


class ListPrincipalPoliciesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListPrincipalPolicies)[Show boto3-stubs documentation](./paginators.md#listprincipalpoliciespaginator)
    """

    def paginate(
        self,
        principal: str,
        ascendingOrder: bool = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListPrincipalPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListPrincipalPolicies.paginate)
        [Show boto3-stubs documentation](./paginators.md#listprincipalpoliciespaginator)
        """


class ListPrincipalThingsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListPrincipalThings)[Show boto3-stubs documentation](./paginators.md#listprincipalthingspaginator)
    """

    def paginate(
        self, principal: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListPrincipalThingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListPrincipalThings.paginate)
        [Show boto3-stubs documentation](./paginators.md#listprincipalthingspaginator)
        """


class ListProvisioningTemplateVersionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListProvisioningTemplateVersions)[Show boto3-stubs documentation](./paginators.md#listprovisioningtemplateversionspaginator)
    """

    def paginate(
        self, templateName: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListProvisioningTemplateVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListProvisioningTemplateVersions.paginate)
        [Show boto3-stubs documentation](./paginators.md#listprovisioningtemplateversionspaginator)
        """


class ListProvisioningTemplatesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListProvisioningTemplates)[Show boto3-stubs documentation](./paginators.md#listprovisioningtemplatespaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListProvisioningTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListProvisioningTemplates.paginate)
        [Show boto3-stubs documentation](./paginators.md#listprovisioningtemplatespaginator)
        """


class ListRoleAliasesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListRoleAliases)[Show boto3-stubs documentation](./paginators.md#listrolealiasespaginator)
    """

    def paginate(
        self, ascendingOrder: bool = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListRoleAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListRoleAliases.paginate)
        [Show boto3-stubs documentation](./paginators.md#listrolealiasespaginator)
        """


class ListScheduledAuditsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListScheduledAudits)[Show boto3-stubs documentation](./paginators.md#listscheduledauditspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListScheduledAuditsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListScheduledAudits.paginate)
        [Show boto3-stubs documentation](./paginators.md#listscheduledauditspaginator)
        """


class ListSecurityProfilesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListSecurityProfiles)[Show boto3-stubs documentation](./paginators.md#listsecurityprofilespaginator)
    """

    def paginate(
        self,
        dimensionName: str = None,
        metricName: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListSecurityProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListSecurityProfiles.paginate)
        [Show boto3-stubs documentation](./paginators.md#listsecurityprofilespaginator)
        """


class ListSecurityProfilesForTargetPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListSecurityProfilesForTarget)[Show boto3-stubs documentation](./paginators.md#listsecurityprofilesfortargetpaginator)
    """

    def paginate(
        self,
        securityProfileTargetArn: str,
        recursive: bool = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListSecurityProfilesForTargetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListSecurityProfilesForTarget.paginate)
        [Show boto3-stubs documentation](./paginators.md#listsecurityprofilesfortargetpaginator)
        """


class ListStreamsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListStreams)[Show boto3-stubs documentation](./paginators.md#liststreamspaginator)
    """

    def paginate(
        self, ascendingOrder: bool = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListStreamsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListStreams.paginate)
        [Show boto3-stubs documentation](./paginators.md#liststreamspaginator)
        """


class ListTagsForResourcePaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListTagsForResource)[Show boto3-stubs documentation](./paginators.md#listtagsforresourcepaginator)
    """

    def paginate(
        self, resourceArn: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListTagsForResource.paginate)
        [Show boto3-stubs documentation](./paginators.md#listtagsforresourcepaginator)
        """


class ListTargetsForPolicyPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListTargetsForPolicy)[Show boto3-stubs documentation](./paginators.md#listtargetsforpolicypaginator)
    """

    def paginate(
        self, policyName: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListTargetsForPolicyResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListTargetsForPolicy.paginate)
        [Show boto3-stubs documentation](./paginators.md#listtargetsforpolicypaginator)
        """


class ListTargetsForSecurityProfilePaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListTargetsForSecurityProfile)[Show boto3-stubs documentation](./paginators.md#listtargetsforsecurityprofilepaginator)
    """

    def paginate(
        self, securityProfileName: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListTargetsForSecurityProfileResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListTargetsForSecurityProfile.paginate)
        [Show boto3-stubs documentation](./paginators.md#listtargetsforsecurityprofilepaginator)
        """


class ListThingGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListThingGroups)[Show boto3-stubs documentation](./paginators.md#listthinggroupspaginator)
    """

    def paginate(
        self,
        parentGroup: str = None,
        namePrefixFilter: str = None,
        recursive: bool = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListThingGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListThingGroups.paginate)
        [Show boto3-stubs documentation](./paginators.md#listthinggroupspaginator)
        """


class ListThingGroupsForThingPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListThingGroupsForThing)[Show boto3-stubs documentation](./paginators.md#listthinggroupsforthingpaginator)
    """

    def paginate(
        self, thingName: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListThingGroupsForThingResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListThingGroupsForThing.paginate)
        [Show boto3-stubs documentation](./paginators.md#listthinggroupsforthingpaginator)
        """


class ListThingPrincipalsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListThingPrincipals)[Show boto3-stubs documentation](./paginators.md#listthingprincipalspaginator)
    """

    def paginate(
        self, thingName: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListThingPrincipalsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListThingPrincipals.paginate)
        [Show boto3-stubs documentation](./paginators.md#listthingprincipalspaginator)
        """


class ListThingRegistrationTaskReportsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListThingRegistrationTaskReports)[Show boto3-stubs documentation](./paginators.md#listthingregistrationtaskreportspaginator)
    """

    def paginate(
        self,
        taskId: str,
        reportType: ReportTypeType,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListThingRegistrationTaskReportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListThingRegistrationTaskReports.paginate)
        [Show boto3-stubs documentation](./paginators.md#listthingregistrationtaskreportspaginator)
        """


class ListThingRegistrationTasksPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListThingRegistrationTasks)[Show boto3-stubs documentation](./paginators.md#listthingregistrationtaskspaginator)
    """

    def paginate(
        self, status: StatusType = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListThingRegistrationTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListThingRegistrationTasks.paginate)
        [Show boto3-stubs documentation](./paginators.md#listthingregistrationtaskspaginator)
        """


class ListThingTypesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListThingTypes)[Show boto3-stubs documentation](./paginators.md#listthingtypespaginator)
    """

    def paginate(
        self, thingTypeName: str = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListThingTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListThingTypes.paginate)
        [Show boto3-stubs documentation](./paginators.md#listthingtypespaginator)
        """


class ListThingsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListThings)[Show boto3-stubs documentation](./paginators.md#listthingspaginator)
    """

    def paginate(
        self,
        attributeName: str = None,
        attributeValue: str = None,
        thingTypeName: str = None,
        usePrefixAttributeValue: bool = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListThingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListThings.paginate)
        [Show boto3-stubs documentation](./paginators.md#listthingspaginator)
        """


class ListThingsInBillingGroupPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListThingsInBillingGroup)[Show boto3-stubs documentation](./paginators.md#listthingsinbillinggrouppaginator)
    """

    def paginate(
        self, billingGroupName: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListThingsInBillingGroupResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListThingsInBillingGroup.paginate)
        [Show boto3-stubs documentation](./paginators.md#listthingsinbillinggrouppaginator)
        """


class ListThingsInThingGroupPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListThingsInThingGroup)[Show boto3-stubs documentation](./paginators.md#listthingsinthinggrouppaginator)
    """

    def paginate(
        self,
        thingGroupName: str,
        recursive: bool = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListThingsInThingGroupResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListThingsInThingGroup.paginate)
        [Show boto3-stubs documentation](./paginators.md#listthingsinthinggrouppaginator)
        """


class ListTopicRuleDestinationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListTopicRuleDestinations)[Show boto3-stubs documentation](./paginators.md#listtopicruledestinationspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListTopicRuleDestinationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListTopicRuleDestinations.paginate)
        [Show boto3-stubs documentation](./paginators.md#listtopicruledestinationspaginator)
        """


class ListTopicRulesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListTopicRules)[Show boto3-stubs documentation](./paginators.md#listtopicrulespaginator)
    """

    def paginate(
        self,
        topic: str = None,
        ruleDisabled: bool = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListTopicRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListTopicRules.paginate)
        [Show boto3-stubs documentation](./paginators.md#listtopicrulespaginator)
        """


class ListV2LoggingLevelsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListV2LoggingLevels)[Show boto3-stubs documentation](./paginators.md#listv2logginglevelspaginator)
    """

    def paginate(
        self, targetType: LogTargetTypeType = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListV2LoggingLevelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListV2LoggingLevels.paginate)
        [Show boto3-stubs documentation](./paginators.md#listv2logginglevelspaginator)
        """


class ListViolationEventsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListViolationEvents)[Show boto3-stubs documentation](./paginators.md#listviolationeventspaginator)
    """

    def paginate(
        self,
        startTime: datetime,
        endTime: datetime,
        thingName: str = None,
        securityProfileName: str = None,
        behaviorCriteriaType: BehaviorCriteriaTypeType = None,
        listSuppressedAlerts: bool = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListViolationEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iot.html#IoT.Paginator.ListViolationEvents.paginate)
        [Show boto3-stubs documentation](./paginators.md#listviolationeventspaginator)
        """
