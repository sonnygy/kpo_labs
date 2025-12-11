# TechCare - Device Repair Service Management System

## Overview

TechCare is a Django-based web application for managing a device repair service center. The system handles repair orders for computers, laptops, tablets, and smartphones. It supports three user roles: clients who submit repair requests, masters (technicians) who perform repairs, and administrators who manage the workflow and inventory.

The application is built entirely in Russian, serving a Russian-speaking user base for a tech repair business.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Framework and Backend
- **Django 5.0** web framework with Python
- **Custom User Model** extending Django's AbstractUser with role-based access (client, master, admin)
- **SQLite** as the default database (Django's default, can be migrated to PostgreSQL)

### Application Structure
The project follows Django's app-based architecture with three main apps:

1. **users** - User authentication and management
   - Custom User model with roles (CLIENT, MASTER, ADMIN)
   - Registration and login forms
   - Role-based redirects after authentication

2. **orders** - Repair order management
   - Order model with status workflow (created → in_progress → completed/cancelled)
   - Estimate model for cost tracking (parts + labor)
   - Client-device-master relationships

3. **warehouse** - Inventory and device management
   - Device model with type/brand/model classification
   - Abstract Part model for inventory items
   - Specialized parts for phones and PCs

### Authentication Strategy
- Django's built-in authentication system
- Custom forms for user registration and login
- Role-based access control through model properties (is_master, is_admin, is_client)
- Login required decorators for protected views

### Frontend Architecture
- Server-side rendering with Django templates
- Template inheritance from base.html
- Role-specific navigation includes (nav_master.html, nav_administrator.html)
- Static CSS files for styling (base.css, forms.css, tables.css, home.css)

### URL Routing
- Centralized URL configuration in techcare/urls.py
- Views mix function-based and class-based approaches
- ListView, DetailView, CreateView, UpdateView for CRUD operations

## External Dependencies

### Python/Django Dependencies
- Django 5.0+ (core framework)
- Django's built-in auth system (no external auth packages)

### Environment Configuration
- Uses Replit environment variables for domain configuration
- REPLIT_DOMAINS for ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS
- Debug mode enabled (development setting)

### Database
- Currently uses Django's default SQLite
- Migrations exist for users, warehouse, and orders apps
- Can be upgraded to PostgreSQL for production

### Static Assets
- Static files served from /static directory
- CSS organized by component (base, forms, tables, home, success)
- Images stored in static/images (logo, icons, success graphics)

### No External APIs
- Self-contained application with no third-party API integrations
- No payment processing or external service connections currently implemented

## Recent Changes (December 2025)

### Bug Fixes Applied
1. **Settings Module Fix**: Updated manage.py, wsgi.py, asgi.py to reference 'techcare' module instead of 'django_project'
2. **User Lookup Fix**: Fixed `get_client_for_user()` function that was trying to access non-existent `user` field
3. **Role Attribute Fix**: Changed all `user_type` references to `role` (the actual field name on User model)
4. **Circular Import Fix**: Removed circular import between users.views and orders.views
5. **Abstract Model Fix**: Updated warehouse views to use concrete `PKPart` model instead of abstract `Part`
6. **Missing Forms**: Added `ClientForm`, `ClientOrderForm`, `DeviceForm`, `OrderForm` to users/forms.py
7. **Template/Static Config**: Added template and static file directories to settings

### Known Type Checking Notes
- Remaining LSP diagnostics are Pyright type-checking limitations with Django's ORM (ForeignKey descriptors, model managers). These are not runtime bugs - Django's metaprogramming works correctly at runtime.