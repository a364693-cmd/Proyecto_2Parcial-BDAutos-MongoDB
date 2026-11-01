import pymongo
from pymongo.errors import ConnectionFailure

class MongoBridge:
    def __init__(self, db_name="BDAutos", host="localhost", port=27017):
        self.db_name = db_name
        self.host = host
        self.port = port
        self.client = None
        self.db = None
        self.connect()

    def connect(self):
        """Conexión con local de MongoDB."""
        try:
            self.client = pymongo.MongoClient(
                f"mongodb://{self.host}:{self.port}/", 
                serverSelectionTimeoutMS=3000
            )
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            return True
        except ConnectionFailure as e:
            print(f"Error de conexión con MongoDB: {e}")
            self.client = None
            self.db = None
            return False

    def execute_pipeline(self, collection_name, pipeline):
        """Aggregation Pipeline."""
        if self.db is None and not self.connect():
            raise RuntimeError("No hay conexión con el servidor MongoDB. Verifica que mongod esté activo.")
        collection = self.db[collection_name]
        return list(collection.aggregate(pipeline))

    def execute_find(self, collection_name, filter_query=None, projection=None, sort=None):
        """Ejecucion de una consulta."""
        if filter_query is None:
            filter_query = {}
        if self.db is None and not self.connect():
            raise RuntimeError("No hay conexión con el servidor MongoDB.")
        collection = self.db[collection_name]
        cursor = collection.find(filter_query, projection)
        if sort:
            cursor = cursor.sort(sort)
        return list(cursor)

    def soft_delete_car(self, car_id):
        """Borrado lógico."""
        if self.db is None and not self.connect():
            return False
        result = self.db.cars.update_one(
            {"_id": car_id},
            {"$set": {"activo": False}}
        )
        return result.modified_count > 0

    def restore_car(self, car_id):
        """Restaura un vehículo."""
        if self.db is None and not self.connect():
            return False
        result = self.db.cars.update_one(
            {"_id": car_id},
            {"$set": {"activo": True}}
        )
        return result.modified_count > 0