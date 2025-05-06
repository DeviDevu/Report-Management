# Product Requirements Document (PRD)
## Admin Dashboard for Report Management

## 1. Overview
### 1.1 Purpose
The Admin Dashboard for Report Management is a web-based application that enables efficient management of staff, reports, and approvals through role-based access control.

### 1.2 Key Features
- Secure authentication and authorization system
- Role-based dashboards (Admin, Manager, Staff)
- Comprehensive report management
- Staff assignment and management
- Profile and password management

## 2. User Roles and Permissions
### 2.1 Role Definitions
1. **Admin** (Django admin)
   - Full system access
   - User creation and role assignment

2. **Manager**
   - Manage assigned staff members
   - Review and approve/reject reports
   - Manage personal profile

3. **Staff**
   - Submit and manage reports
   - View report status
   - Manage personal profile

### 2.2 Permission Matrix
| Feature                | Admin | Manager | Staff |
|------------------------|-------|---------|-------|
| User Management        | ✓     | Partial | ✗     |
| Report Approval        | ✓     | ✓       | ✗     |
| Report Submission      | ✗     | ✗       | ✓     |
| Profile Management     | ✓     | ✓       | ✓     |

## 3. Functional Requirements
### 3.1 Authentication
- Secure login using Django authentication
- Password change functionality
- Session management and logout
- Password strength requirements

### 3.2 Admin Features
- User creation with role assignment
- System-wide user management
- Access to Django admin interface

### 3.3 Manager Dashboard
- **Summary Cards**:
  - Total assigned staff
  - Total reports (with status breakdown)

- **Staff Management**:
  - Add new staff (assigned to current manager)
  - View/edit staff profiles

- **Report Management**:
  - Filterable report list (status, date range, staff member)
  - Approve/reject reports with comments
  - View report details

### 3.4 Staff Dashboard
- **Summary Cards**:
  - Total submitted reports
  - Report status breakdown

- **Report Submission**:
  - Multi-field form:
    - Report name
    - Project name
    - Description/notes
    - Date fields
    - File/screenshot upload

- **Report Management**:
  - Filterable list of submitted reports
  - View approval status

### 3.5 Profile Management (All Roles)
- Update personal information:
  - Name, email, contact details
- Change password

## 4. Non-Functional Requirements
### 4.1 Security
- Role-based access control
- Password encryption
- CSRF protection
- Session timeout after 30 minutes of inactivity

### 4.3 Usability
- Responsive design (desktop/tablet)
- Form validation with clear error messages

## 5. Technical Specifications
### 5.1 Technology Stack
- Backend: Django (Python)
- Frontend: HTML, CSS, JavaScript (Bootstrap/jQuery)
- Database: PostgreSQL
- Deployment: Docker

### 5.2 Dependencies
- django-role-permissions for advanced RBAC

## 6. Data Model (Key Entities)
1. **User**
   - Role (Admin/Manager/Staff)
   - Manager (for Staff users)
   - Profile information

2. **Report**
   - Title, description
   - Status (Submitted/Approved/Rejected)
   - Submission/approval dates
   - Associated files
   - Creator (Staff) and approver (Manager)
