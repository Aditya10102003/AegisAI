from enum import Enum

class EmploymentStatus(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    TERMINATED = "Terminated"

class EmploymentType(str, Enum):
    FULL_TIME = "Full-Time"
    PART_TIME = "Part-Time"
    CONTRACT = "Contract"
    INTERN = "Intern"

class SensitivityLevel(str, Enum):
    PUBLIC = "Public"
    INTERNAL = "Internal"
    CONFIDENTIAL = "Confidential"
    RESTRICTED = "Restricted"
    CRITICAL = "Critical"

class ResourceType(str, Enum):
    DATABASE = "Database"
    FILE = "File"
    API = "API"
    APPLICATION = "Application"

class AccessRequestStatus(str, Enum):
    PENDING = "Pending"
    MANAGER_APPROVED = "Manager_Approved"
    APPROVED = "Approved"
    REJECTED = "Rejected"

class RequestType(str, Enum):
    NEW = "New"
    MODIFY = "Modify"
    REVOKE = "Revoke"

class GrantType(str, Enum):
    TEMPORARY = "Temporary"
    PERMANENT = "Permanent"
    AUTOMATED = "Automated"
    MANUAL = "Manual"

class AccessGrantStatus(str, Enum):
    ACTIVE = "Active"
    EXPIRED = "Expired"
    REVOKED = "Revoked"

class ReviewStatus(str, Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    OVERDUE = "Overdue"

class DecisionType(str, Enum):
    ALLOWED = "Allowed"
    DENIED = "Denied"

class EnvironmentType(str, Enum):
    PRODUCTION = "Production"
    STAGING = "Staging"
    DEVELOPMENT = "Development"
    TESTING = "Testing"