import os
import pickle
from typing import Any, Iterable


# class DBMS:

#     _DataStorageObjs: set[str] = set()

#     def __init__(self, path:str = "../DB"):

#         if path not in DBMS._DataStorageObjs:
#             self.path = path
#             self._catalogue = []
#             self._data: dict[str, Any] = {}
#             self._setup()

#     def _setup(self):
#         self._data = self._data_storage_handler()
#         self._load_catalogue()
#         DataStorage._DataStorageObjs.add(self.path)

#     def _data_storage_handler(self, obj_to_store=None) -> Union[dict[str, Any], None]:
#         if obj_to_store is not None:
#             with open(self.path, "wb") as handle:
#                 pickle.dump(obj_to_store, handle,
#                             protocol=pickle.HIGHEST_PROTOCOL)
#         else:
#             _data = None
#             try:
#                 with open(self.path, "rb") as handle:
#                     _data = pickle.load(handle)
#             except FileNotFoundError:
#                 create_file = {
#                     "creation": datetime.today().strftime('%Y-%m-%d')}
#                 self._data_storage_handler(create_file)
#                 _data = create_file
#             return _data

#     def store_object(self, **kwargs):
#         for obj in kwargs.items():
#             if obj[0] not in self._data.keys():
#                 self._catalogue.append(obj[0])
#             self._data[obj[0]] = obj[1]

#         self.save()

#     def load_object(self, *access_names):
#         if len(access_names) == 1:
#             return self._data.setdefault(access_names[0], None)
#         else:
#             return tuple(self._data.setdefault(access_name, None) for access_name in access_names)

#     def _load_catalogue(self):
#         self._catalogue = [key for key in self._data.keys()]

#     @property
#     def catalogue(self) -> list[str]:
#         return self._catalogue

#     def remove(self, *names):
#         for name in names:
#             del self._data[name]
#         self.save()

#     def __getitem__(self, key):
#         return self._data[key]

#     def __setitem__(self, key, value):
#         self._data[key] = value
#         self._load_catalogue()
#         self.save()

#     def __delitem__(self, key):
#         del self._data[key]
#         self.save()

#     def __contains__(self, key):
#         return key in self._data

#     def __iter__(self):
#         return iter(self._data)

#     def __len__(self):
#         return len(self._data)

#     def __repr__(self):
#         return "NotImplemented"

#     def __str__(self):
#         return str(self.catalogue)

#     def __call__(self, *args, **kwargs):
#         """When called without any arguments returns all data
#         When called with positional argument returns the data with the given name
#         When called with keyword arguments stores the data with the given name"""

#         if not any(args) and not any(kwargs):
#             return self._data

#         if any(args) and not any(kwargs):
#             return self.load_object(*args)

#         if any(kwargs) and not any(args):
#             return self.store_object(**kwargs)

#         if any(args) and any(kwargs):
#             return self.load_object(*args), self.store_object(**kwargs)

#     def save(self):
#         self._data_storage_handler(self._data)
#         self._load_catalogue()

class Database:
    """A database object that stores data in a file"""
    _all_databases: set[str] = set()

    def __init__(self, name:str, path:str = "../DB"):
        self._db_path = f"{path}/{name}.pkl"
        try:
            self._db = self._load_DB()
        except FileNotFoundError as exc:
            raise FileNotFoundError(f"Database with name '{name}' at path '{path}' does not exist. Consider using 'Database.create_database()' to create a database first.") from exc
        

    def _load_DB(self) -> dict[str, Any]:
        with open(self._db_path, "rb") as handle:
            db = pickle.load(handle)
        return db

    def _write_DB(self, db: dict[str, Any]) -> bool:
        if not isinstance(db, dict):
            raise TypeError(f"Expected 'dict' but got '{type(db)}'")
            
        write_status = False
        with open(self._db_path, "wb") as handle:
            pickle.dump(db, handle, protocol=pickle.HIGHEST_PROTOCOL)
            write_status = True
        
        return write_status
        
    
    def add_single_record(self, obj: Any, obj_id: str, overwrite: bool = False) -> bool:
        """Adds a single record to the database"""
        if not isinstance(obj_id, str):
            raise TypeError(f"Expected 'str' for 'obj_id' but got '{type(obj_id)}' instead.")
        
        if obj_id in self._db and not overwrite:
            raise ValueError(f"Record with id '{obj_id}' already exists in the database. Consider using 'overwrite=True' to overwrite the existing record.")
        
        self._db[obj_id] = obj
        return self._write_DB(self._db)

    def add_multiple_records(self, records: dict[str, Any], overwrite: bool = False) -> bool:
        """Adds multiple records to the database"""

        if not isinstance(records, dict):
            raise TypeError(f"Expected 'dict' for 'records' but got '{type(records)}' instead.")

        if not all(isinstance(key, str) for key in records.keys()):
            problematic_keys = tuple(filter(lambda x: not isinstance(x, str), records.keys()))
            raise TypeError("Expected 'str' for all keys in 'records' but got key(s) ({}) with '{}' instead.".format(*problematic_keys, *map(type, problematic_keys)))
        
        for record_id, record_data in records.items():
            if record_id in self._db and not overwrite:
                raise ValueError(f"Record with id '{record_id}' already exists in the database. Consider using 'overwrite=True' to overwrite the existing record.")
            else:
                self._db[record_id] = record_data
            
        return self._write_DB(self._db)



    @classmethod
    def create_database(name: str, path: str = "../DB"):
        if (access_path := f"{path}/{name}.pkl") not in Database._all_databases:
            with open(access_path, "wb") as handle:
                pickle.dump({}, handle, protocol=pickle.HIGHEST_PROTOCOL)
            Database._all_databases.add(access_path)
            return Database(name, path)
        else:
            raise FileExistsError(f"Database with name '{name}' at '{path}' already exists")
    
    @classmethod
    def delete_database(cls, name: str, path: str = "../DB"):
        if (access_path := f"{path}/{name}.pkl") in Database._all_databases:
            os.remove(access_path)
            Database._all_databases.remove(access_path)
        else:
            raise FileNotFoundError(f"Database with name '{name}' at '{path}' does not exist")



a = Database("test", "../DB")
