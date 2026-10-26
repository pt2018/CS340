from pymongo import MongoClient 
from bson.objectid import ObjectId 

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self, username, password):
        USER = username
        PASS = password
        HOST = 'localhost'
        PORT = 27017
        DB = 'aac'
        COL = 'animals'
        # 
        # Initialize Connection 
        # 
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT)) 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)] 

    # Create a method to return the next available record number for use in the create method
    def getNextAnimalID(self):
      animal_ids = self.collection.find(
        {"animal_id": {"$regex": "^A[0-9]+$"}},
          {"animal_id": 1}
        )
      max_id = 0
        
      for animal in animal_ids:
        number = int(animal["animal_id"][1:])
        if number > max_id:
          max_id = number
      
      return "A" + str(max_id + 1)
            

    def create(self, data):
      if isinstance(data, dict) and data:
        try:
          result = self.collection.insert_one(data)
          return result.acknowledged
        except Exception as error:
          print("Error creating document:", error)
          return False
      else:
        return False
    def read(self, data):
      if isinstance(data, dict):
        try:
          cursor = self.collection.find(data)
          return list(cursor)
        except Exception as error:
          print("Error reading documents:", error)
          return []
      else:
        return []
    # Implement the U in CRUD.
    def update(self, query, data):
      if isinstance(query, dict) and isinstance(data, dict) and data:
        try:
          # Update all matching documents using an update operator.
          result = self.collection.update_many(query, data)
          return result.modified_count
        except Exception as error:
          print("Error updating documents:", error)
          return 0
      else:
        return 0

    # Implement the D in CRUD.
    def delete(self, query):
      if isinstance(query, dict):
        try:
          # Delete all documents matching the query.
          result = self.collection.delete_many(query)
          return result.deleted_count
        except Exception as error:
          print("Error deleting documents:", error)
          return 0
      else:
        return 0