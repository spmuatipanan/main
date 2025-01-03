import streamlit as st
from pymongo import MongoClient
import json

# ฟังก์ชันสำหรับเชื่อมต่อ MongoDB
@st.cache_resource
def get_mongo_client():
    mongo_uri = st.secrets["MONGO_URI"]
    client = MongoClient(mongo_uri)
    return client

# ส่วนติดต่อผู้ใช้
st.title("MongoDB Management WebApp")

# สร้างการเชื่อมต่อ
try:
    client = get_mongo_client()
    db_name = st.secrets["MONGO_DB_NAME"]
    db = client[db_name]

    # เลือกคอลเลกชัน
    st.sidebar.header("Database Control Panel")
    collection_name = st.sidebar.selectbox("Select Collection", db.list_collection_names())
    collection = db[collection_name]

    # **1. เพิ่มข้อมูลใหม่**
    st.header("Insert New Document")
    new_document = st.text_area("Enter JSON document (e.g., {'key': 'value'})", "{}")
    if st.button("Insert Document"):
        try:
            document = json.loads(new_document)
            collection.insert_one(document)
            st.success("Document inserted successfully!")
        except Exception as e:
            st.error(f"Error inserting document: {e}")

    # **2. แสดงข้อมูล**
    st.header("Query Collection")
    query = st.text_area("Enter Query (JSON format)", "{}")
    if st.button("Run Query"):
        try:
            query_dict = json.loads(query)
            results = list(collection.find(query_dict))
            if results:
                st.write(f"Found {len(results)} documents:")
                st.json(results)
            else:
                st.write("No documents matched the query.")
        except Exception as e:
            st.error(f"Error running query: {e}")

    # **3. อัปเดตข้อมูล**
    st.header("Update Document")
    filter_query = st.text_area("Filter Query (JSON format)", "{}")
    update_query = st.text_area("Update Query (JSON format)", "{}")
    if st.button("Update Document"):
        try:
            filter_dict = json.loads(filter_query)
            update_dict = {"$set": json.loads(update_query)}
            result = collection.update_many(filter_dict, update_dict)
            st.success(f"Matched {result.matched_count}, Updated {result.modified_count} documents!")
        except Exception as e:
            st.error(f"Error updating documents: {e}")

    # **4. ลบข้อมูล**
    st.header("Delete Document")
    delete_query = st.text_area("Delete Query (JSON format)", "{}")
    if st.button("Delete Document"):
        try:
            delete_dict = json.loads(delete_query)
            result = collection.delete_many(delete_dict)
            st.success(f"Deleted {result.deleted_count} documents!")
        except Exception as e:
            st.error(f"Error deleting documents: {e}")

except Exception as e:
    st.error(f"Failed to connect to MongoDB: {e}")
