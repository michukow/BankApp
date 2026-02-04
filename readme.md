# 🏦 BankApp – Console Banking System (Python)

## 📌 About the Project
**BankApp** is a console-based banking system written in Python.  
The project simulates core banking operations with a strong focus on **business logic, security, and data persistence**.

It is designed as a learning project that evolves step by step toward a real-world backend application.

### Currently supported features:
- User registration and login
- Secure password hashing (SHA-256)
- Account balance management
- Deposits and withdrawals
- Transaction history
- Password change mechanism
- Account lockout after multiple failed login attempts
- Persistent data storage using JSON

## 🛠️ Technologies
- **Python**
- **JSON** (used as a temporary data store instead of a relational database)

> JSON is intentionally used at this stage for simplicity and learning purposes.  
> The project is planned to be migrated to an SQL database in future iterations.

## 🔐 Security Features
- Passwords are never stored in plain text
- SHA-256 hashing algorithm
- Account blocking after 3 failed login attempts
- Failed login attempts are persisted between sessions
- Temporary account lock with automatic unlock after 3-days

## 🚀 Planned Improvements
- Logging system (`logging` module)
- Role-based access (admin / user)
- Migration to SQL database
- Full OOP refactor
- FastAPI (?)

## 📅 Last Update
**03.02.2026**
