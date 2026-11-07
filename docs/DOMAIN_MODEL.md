AegisAI Domain Model
Department ├── Employees └── Resources

Employee ├── Roles ├── Access Requests ├── Access Grants ├── Audit Logs └── Owned Resources

Role └── Permissions

Resource ├── Access Requests ├── Access Grants └── Audit Logs

Access Request ├── Requested Resource ├── Requested Action ├── Approval Workflow └── AI Recommendation

Access Grant ├── Resource ├── Action ├── Expiration └── Grant Type

Audit Log ├── User ├── Resource ├── Action ├── Decision └── Context