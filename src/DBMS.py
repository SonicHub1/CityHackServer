import os
import pickle
from typing import Any, Iterable

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
    
    def _check_single_record_id(self, obj_id: str) -> bool:
        if not isinstance(obj_id, str):
            raise TypeError(f"Expected 'str' for 'obj_id' but got '{type(obj_id)}' instead.")
        
        return True

    def _check_multiple_record_ids(self, record_ids: Iterable[str]) -> bool:
        try:
            if not all(isinstance(key, str) for key in record_ids):
                problematic_keys = tuple(filter(lambda x: not isinstance(x, str), record_ids))
                raise TypeError("Expected 'str' for all keys in 'records' but got key(s) ({}) with '{}' instead.".format(*problematic_keys, type(problematic_keys[0])))

        except TypeError as exc:
            raise TypeError(f"Expected 'Iterable[str]' for 'record_ids' but got '{type(record_ids)}' instead.") from exc
        
        return True
    
    def add_single_record(self, obj: Any, obj_id: str, overwrite: bool = False) -> bool:
        """Adds a single record to the database"""
        self._check_single_record_id(obj_id)
        
        if obj_id in self._db and not overwrite:
            raise ValueError(f"Record with id '{obj_id}' does not exist in the database.")
        self._db[obj_id] = obj
        return self._write_DB(self._db)

    def add_multiple_records(self, records: dict[str, Any], overwrite: bool = False) -> bool:
        """Adds multiple records to the database"""
        self._check_multiple_record_ids(records.keys())
        
        for record_id, record_data in records.items():
            if record_id in self._db and not overwrite:
                raise ValueError(f"Record with id '{record_id}' already exists in the database. Consider using 'overwrite=True' to overwrite the existing record.")
            else:
                self._db[record_id] = record_data
            
        return self._write_DB(self._db)

    def get_single_record(self, obj_id: str) -> Any:
        """Returns the record with the given id"""
        self._check_single_record_id(obj_id)
        
        if obj_id not in self._db:
            raise KeyError(f"Record with id '{obj_id}' does not exist in the database.")
        
        return self._db[obj_id]
    
    def get_multiple_records(self, record_ids: Iterable[str]) -> dict[str, Any]:
        """Returns the records with the given ids"""
        self._check_multiple_record_ids(record_ids)
        
        if any(record_id not in self._db for record_id in record_ids):
            problematic_keys = tuple(filter(lambda x: x not in self._db, record_ids))
            raise KeyError("Record(s) with id(s) ({}) does not exist in the database.".format(*problematic_keys))
        
        return {record_id: self._db[record_id] for record_id in record_ids}
    
    def delete_record(self, obj_id: str, silence_error:bool = False) -> bool:
        """Deletes the record with the given id"""
        self._check_single_record_id(obj_id)
        
        if obj_id not in self._db and not silence_error:
            raise KeyError(f"Record with id '{obj_id}' does not exist in the database. Consider using 'silence_error=True' to silence this error.")
        
        del self._db[obj_id]
        return self._write_DB(self._db)

    def delete_records(self, record_ids: Iterable[str], silence_error:bool = False) -> bool:
        """Deletes the records with the given ids"""
        self._check_multiple_record_ids(record_ids)
        
        if any(record_id not in self._db for record_id in record_ids) and not silence_error:
            problematic_keys = tuple(filter(lambda x: x not in self._db, record_ids))
            raise KeyError("Record(s) with id(s) ({}) does not exist in the database. Consider using 'silence_error=True' to silence this error.".format(*problematic_keys))
        
        for record_id in record_ids:
            del self._db[record_id]
        
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
