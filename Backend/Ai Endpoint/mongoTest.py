from pymongo import MongoClient
import certifi

uri = "mongodb+srv://projetiot:PigZNQGf6lPy97Pk@projetiot.mwwvunz.mongodb.net/?retryWrites=true&w=majority"

try:
    # Use certifi to avoid SSL handshake errors
    client = MongoClient(uri, tlsCAFile=certifi.where())
    
    # The 'admin' database is always there, good for testing connectivity
    client.admin.command('ping')
    print("✅ Connection Successful! You are connected to MongoDB Atlas.")
    
    # List databases to see if your permissions work
    print("Available Databases:", client.list_database_names())

except Exception as e:
    print("❌ Connection Failed:")
    print(e)s