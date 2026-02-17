# 🏠 Smart Home Project

This project uses **MongoDB** to manage room configurations such as climate control, lighting, doors, and windows.  
To run the project successfully, you must configure your own MongoDB connection and create room documents manually.

---

## 🚀 Getting Started

### 1️⃣ MongoDB Setup
Make sure you have a running MongoDB instance (local or cloud).

You will need:
- MongoDB connection URI
- Database name
- Collection for rooms

---

## ⚙️ Configuration

### 🔹 Java Spring Boot (`application.properties`)

Add the following to your `src/main/resources/application.properties` file:

```properties
spring.data.mongodb.uri=mongodb://localhost:27017/smarthome
spring.data.mongodb.database=smarthome
server.port=8080

```
```.env
MONGO_URI=mongodb://localhost:27017/smarthome
MONGO_DB=smarthome
FLASK_ENV=development
FLASK_RUN_PORT=5000
```
