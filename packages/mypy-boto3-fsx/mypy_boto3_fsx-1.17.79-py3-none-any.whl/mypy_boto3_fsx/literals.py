"""
Type annotations for fsx service literal definitions.

[Open documentation](./literals.md)

Usage::

    ```python
    from mypy_boto3_fsx.literals import AdministrativeActionTypeType

    data: AdministrativeActionTypeType = "FILE_SYSTEM_ALIAS_ASSOCIATION"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "AdministrativeActionTypeType",
    "AliasLifecycleType",
    "AutoImportPolicyTypeType",
    "BackupLifecycleType",
    "BackupTypeType",
    "DataRepositoryLifecycleType",
    "DataRepositoryTaskFilterNameType",
    "DataRepositoryTaskLifecycleType",
    "DataRepositoryTaskTypeType",
    "DescribeBackupsPaginatorName",
    "DescribeFileSystemsPaginatorName",
    "DriveCacheTypeType",
    "FileSystemLifecycleType",
    "FileSystemMaintenanceOperationType",
    "FileSystemTypeType",
    "FilterNameType",
    "ListTagsForResourcePaginatorName",
    "LustreDeploymentTypeType",
    "ReportFormatType",
    "ReportScopeType",
    "StatusType",
    "StorageTypeType",
    "WindowsDeploymentTypeType",
)


AdministrativeActionTypeType = Literal[
    "FILE_SYSTEM_ALIAS_ASSOCIATION",
    "FILE_SYSTEM_ALIAS_DISASSOCIATION",
    "FILE_SYSTEM_UPDATE",
    "STORAGE_OPTIMIZATION",
]
AliasLifecycleType = Literal["AVAILABLE", "CREATE_FAILED", "CREATING", "DELETE_FAILED", "DELETING"]
AutoImportPolicyTypeType = Literal["NEW", "NEW_CHANGED", "NONE"]
BackupLifecycleType = Literal[
    "AVAILABLE", "COPYING", "CREATING", "DELETED", "FAILED", "PENDING", "TRANSFERRING"
]
BackupTypeType = Literal["AUTOMATIC", "AWS_BACKUP", "USER_INITIATED"]
DataRepositoryLifecycleType = Literal[
    "AVAILABLE", "CREATING", "DELETING", "MISCONFIGURED", "UPDATING"
]
DataRepositoryTaskFilterNameType = Literal["file-system-id", "task-lifecycle"]
DataRepositoryTaskLifecycleType = Literal[
    "CANCELED", "CANCELING", "EXECUTING", "FAILED", "PENDING", "SUCCEEDED"
]
DataRepositoryTaskTypeType = Literal["EXPORT_TO_REPOSITORY"]
DescribeBackupsPaginatorName = Literal["describe_backups"]
DescribeFileSystemsPaginatorName = Literal["describe_file_systems"]
DriveCacheTypeType = Literal["NONE", "READ"]
FileSystemLifecycleType = Literal[
    "AVAILABLE", "CREATING", "DELETING", "FAILED", "MISCONFIGURED", "UPDATING"
]
FileSystemMaintenanceOperationType = Literal["BACKING_UP", "PATCHING"]
FileSystemTypeType = Literal["LUSTRE", "WINDOWS"]
FilterNameType = Literal["backup-type", "file-system-id", "file-system-type"]
ListTagsForResourcePaginatorName = Literal["list_tags_for_resource"]
LustreDeploymentTypeType = Literal["PERSISTENT_1", "SCRATCH_1", "SCRATCH_2"]
ReportFormatType = Literal["REPORT_CSV_20191124"]
ReportScopeType = Literal["FAILED_FILES_ONLY"]
StatusType = Literal["COMPLETED", "FAILED", "IN_PROGRESS", "PENDING", "UPDATED_OPTIMIZING"]
StorageTypeType = Literal["HDD", "SSD"]
WindowsDeploymentTypeType = Literal["MULTI_AZ_1", "SINGLE_AZ_1", "SINGLE_AZ_2"]
