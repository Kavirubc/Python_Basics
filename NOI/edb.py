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

def fetch_unique_fullname_and_emails_from_mongodb():
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

    # Fetch unique full names and emails from MongoDB
    unique_fullnames_and_emails = set()
    for user in collection.find():
        full_name = user["name"]["full"]
        email = user["email"]
        unique_fullnames_and_emails.add((full_name, email))

    client.close()  # Close MongoDB connection
    return unique_fullnames_and_emails

def save_fullname_and_emails_to_csv(unique_fullnames_and_emails, filename):
    if unique_fullnames_and_emails:
        # Write unique full names and emails to CSV
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["full_name", "email"])
            writer.writerows(unique_fullnames_and_emails)
        print("Unique full names and emails saved to", filename)
    else:
        print("No unique full names and emails fetched.")

def main():
    unique_fullnames_and_emails = fetch_unique_fullname_and_emails_from_mongodb()
    save_fullname_and_emails_to_csv(unique_fullnames_and_emails, "unique_fullnames_and_emails.csv")

if __name__ == "__main__":
    main()
