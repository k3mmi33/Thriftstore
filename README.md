# Thrift Store Management System - Phase 3 CLI+ORM Application

**Owner:** Natasha Kemunto

## Overview
A comprehensive CLI application built with Python and SQLAlchemy ORM to manage a thrift store's inventory, customers, and sales operations. This application demonstrates advanced database relationships, CRUD operations, and professional CLI interface design.

## Description
This thrift store management system provides a complete solution for managing retail operations through a command-line interface. The application handles inventory tracking, customer management, and sales processing with a robust database backend using SQLAlchemy ORM and Alembic migrations.

**Key Features:**
- Full CRUD operations for items, customers, and sales
- Complex database relationships with proper foreign key constraints
- Professional CLI interface with organized menu systems
- Database migrations support with Alembic
- Service layer architecture for business logic separation
- Data validation and error handling

## Technologies Used
- **Python 3.8+** - Core programming language
- **SQLAlchemy** - ORM for database operations
- **Alembic** - Database migration tool
- **Pipenv** - Dependency management and virtual environment
- **SQLite** - Database backend (development)
- **Click** or **argparse** - CLI framework (if applicable)

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Pipenv installed (`pip install pipenv`)

### Setup Steps
1. **Clone/Create the project directory:**
   ```bash
   mkdir thrift_store_cli
   cd thrift_store_cli
   ```

2. **Install dependencies:**
   ```bash
   pipenv install
   pipenv shell
   ```

3. **Initialize the database:**
   ```bash
   alembic upgrade head
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```

## File Structure
```
thrift_store_cli/
├── Pipfile                     # Project dependencies
├── Pipfile.lock               # Locked dependency versions
├── README.md                  # Project documentation
├── alembic.ini               # Alembic configuration
├── main.py                   # Application entry point
├── lib/                      # Main application package
│   ├── __init__.py
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── base.py         # Base model class
│   │   ├── item.py         # Item model
│   │   ├── customer.py     # Customer model
│   │   ├── sale.py         # Sale model
│   │   └── sale_item.py    # Sale-Item association model
│   ├── services/           # Business logic layer
│   │   ├── __init__.py
│   │   ├── item_service.py     # Item operations
│   │   ├── customer_service.py # Customer operations
│   │   └── sales_service.py    # Sales operations
│   └── cli/               # Command-line interface
│       ├── __init__.py
│       ├── main_menu.py   # Main menu controller
│       ├── item_menu.py   # Item management menu
│       ├── customer_menu.py # Customer management menu
│       └── sales_menu.py  # Sales management menu
└── migrations/           # Database migrations
    ├── versions/        # Migration files
    └── env.py          # Alembic environment
```

## Core Functionality

### Models & Relationships
- **Item Model**: Manages inventory with attributes like name, price, category, and quantity
- **Customer Model**: Stores customer information and purchase history
- **Sale Model**: Records transaction details with timestamps and totals
- **SaleItem Model**: Many-to-many association between sales and items

### Service Layer
- **ItemService**: CRUD operations for inventory management
- **CustomerService**: Customer registration, updates, and retrieval
- **SalesService**: Transaction processing and sales reporting

### CLI Interface
- **Main Menu**: Primary navigation hub
- **Item Menu**: Add, view, update, delete inventory items
- **Customer Menu**: Customer management operations
- **Sales Menu**: Process sales and view transaction history

## Usage Examples

### Starting the Application
```bash
python main.py
```

### Main Menu Navigation
```
=== THRIFT STORE MANAGEMENT SYSTEM ===
1. Manage Items
2. Manage Customers
3. Process Sales
4. View Reports
5. Exit
Enter your choice:
```

### Sample Operations
- **Add New Item**: Navigate to Items → Add Item
- **Register Customer**: Navigate to Customers → Add Customer
- **Process Sale**: Navigate to Sales → New Sale
- **View Inventory**: Navigate to Items → View All Items

## Database Schema
The application uses the following core relationships:
- **One-to-Many**: Customer → Sales (one customer can have multiple sales)
- **Many-to-Many**: Sales ↔ Items (through SaleItem association table)
- **Foreign Keys**: Proper referential integrity maintained

## Features Implemented
- **Complete CRUD Operations** for all entities
- **Database Relationships** with proper foreign key constraints
- **CLI Menu System** with organized navigation
- **Data Validation** and error handling
- **Migration Support** with Alembic
- **Service Layer Architecture** for clean code organization
- **Session Management** for database operations

## Technical Highlights
- **ORM Best Practices**: Proper model design with relationships
- **Separation of Concerns**: Models, services, and CLI layers
- **Database Migrations**: Version-controlled schema changes
- **Error Handling**: Graceful handling of user input and database errors
- **Code Organization**: Modular structure for maintainability

## Development Notes
- Database operations use SQLAlchemy sessions properly
- All models inherit from a base class for consistency
- Service classes handle business logic separately from CLI
- Menu systems provide user-friendly navigation
- Input validation prevents database errors

## Future Enhancements
- Add reporting features (sales by date, top customers)
- Implement item categories and filtering
- Add inventory alerts for low stock
- Export functionality for sales reports
- Admin user authentication system
- REST API layer for web integration

## Assignment Requirements Met
✅ SQLAlchemy ORM implementation
✅ Multiple related models with foreign keys
✅ CRUD operations for all entities
✅ Professional CLI interface
✅ Database migrations with Alembic
✅ Service layer architecture
✅ Proper project structure and organization
✅ Error handling and data validation

## Dependencies
Key packages used (defined in Pipfile):
- SQLAlchemy - Database ORM
- Alembic - Database migrations
- Click (optional) - CLI framework

## Contact
Natasha Onsongo
kemmienatasha@gmail.com
