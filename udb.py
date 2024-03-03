import csv
from pymongo import MongoClient
from urllib.parse import quote_plus

# MongoDB credentials
DB_USERNAME = "kaviru"
DB_PASSWORD = "kaviru@BC1"
DB_CLUSTER = "crud-app.jgjleuo.mongodb.net"
DB_NAME = "delegates"
DB_AUTH_SOURCE = "admin"
DB_AUTH_MECHANISM = "SCRAM-SHA-1"

def fetch_users_from_mongodb():
    # Escape username and password
    escaped_username = quote_plus(DB_USERNAME)
    escaped_password = quote_plus(DB_PASSWORD)

    # MongoDB connection URI with tlsAllowInvalidCertificates option
    uri = f"mongodb+srv://{escaped_username}:{escaped_password}@{DB_CLUSTER}/{DB_NAME}?authSource={DB_AUTH_SOURCE}&authMechanism={DB_AUTH_MECHANISM}&tlsAllowInvalidCertificates=true"
    
    # Connect to MongoDB
    client = MongoClient(uri)

    # Access the database and collection
    db = client[DB_NAME]
    collection = db["users"]  # Replace "users" with your actual collection name

    # Fetch users from MongoDB
    users = list(collection.find())

    client.close()  # Close MongoDB connection
    
    # Get unique users
    unique_users = {user['email']: user for user in users}.values()

    return unique_users

def save_users_to_csv(users, filename):
    if users:
        # Flatten the user data into separate columns
        flattened_users = []
        for user in users:
            flattened_user = {
                "email": user["email"],
                "first_name": user["name"]["first"],
                "last_name": user["name"]["last"],
                "full_name": user["name"]["full"],
                "birthdate": user["birthdate"],
                "gender": user["gender"],
                "school_name": user["school"]["name"],
                "school_address": user["school"]["address"],
                "address_line1": user["address"]["line1"],
                "address_line2": user["address"]["line2"],
                "address_line3": user["address"]["line3"],
                "contact_number": user["contactNumber"],
                "document_type": user["document"]["type"],
                "document_path": user["document"]["path"],
                "updated_at": user["updated_at"],
                "created_at": user["created_at"]
            }
            flattened_users.append(flattened_user)

        # Write flattened user data to CSV
        fields = flattened_users[0].keys()
        with open(filename, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(flattened_users)
        print("Unique users saved to", filename)
    else:
        print("No users fetched.")

def main():
    users = fetch_users_from_mongodb()
    save_users_to_csv(users, "unique_users.csv")

if __name__ == "__main__":
    main()
