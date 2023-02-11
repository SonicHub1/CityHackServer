import glob
from inspect import Attribute
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
            raise FileNotFoundError(f"Database with name '{name}' at path '{path}' does not exist. Consider using `Database.create_database(name='{name}', path='{path}')` to create a database first.") from exc
        else:
            print(f"Database '{name}' loaded successfully.")
    
    def __getitem__(self, key:str) -> Any:
        return self.get_single_record(obj_id=key)
        
    def __setitem__(self, key:str, value:Any, overwrite=False) -> bool:
        return self.add_single_record(obj_id=key, obj=value, overwrite=overwrite)

    def __str__(self):
        return str(self._db)

    def __contains__(self, key:str) -> bool:
        return key in self._db

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
            raise TypeError(f"Expected 'str' for 'obj_id' but got {type(obj_id)} instead.")
        
        return True

    def _check_multiple_record_ids(self, record_ids: Iterable[str]) -> bool:
        err_str = ""
        try:
            if not all(isinstance(key, str) for key in record_ids):
                problematic_keys = tuple(filter(lambda x: not isinstance(x, str), record_ids))
                problematic_key_str = ", ".join(map(str, problematic_keys))
                problematic_key_type_str = ", ".join(map(lambda x: f"{type(x)}", problematic_keys))
                err_str = f"Expected 'str' for all keys in 'records' but got key(s) [{problematic_key_str}] with [{problematic_key_type_str}] instead."
                raise TypeError(err_str)

        except TypeError as exc:
            if str(exc) == err_str:
                raise exc
            raise TypeError(f"Expected 'Iterable[str]' for 'record_ids' but got {type(record_ids)} instead.") from exc
        
        return True
    
    def add_single_record(self, obj_id: str, obj: Any, overwrite: bool = False) -> bool:
        """Adds a single record to the database"""
        self._check_single_record_id(obj_id)
        
        if obj_id in self._db and not overwrite:
            raise ValueError(f"Record with id '{obj_id}' already exists in the database. Consider using '.add_single_record(obj_id, obj, overwrite=True)' to overwrite the existing record.")
        self._db[obj_id] = obj
        return self._write_DB(self._db)

    def add_multiple_records(self, records: dict[str, Any], overwrite: bool = False) -> bool:
        """Adds multiple records to the database"""
        try:
            self._check_multiple_record_ids(records.keys())
        except AttributeError as exc:
            raise AttributeError(f"Expected 'dict' for 'records' but got '{type(records)}' instead.") from exc
        
        for record_id, record_data in records.items():
            if record_id in self._db and not overwrite:
                raise ValueError(f"Record with id '{record_id}' already exists in the database. Consider using 'add_multiple_records(records, overwrite: bool = True)' to overwrite the existing record.")
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
            problematic_keys = filter(lambda x: x not in self._db, record_ids)
            problematic_key_str = ", ".join(problematic_keys)
            raise KeyError(f"Record(s) with id(s) [{problematic_key_str}] does not exist in the database.")
        
        return {record_id: self._db[record_id] for record_id in record_ids}
    
    def get_all_records(self) -> dict[str, Any]:
        """Returns all records in the database"""
        return self._db

    def keys(self) -> Iterable[str]:
        """Returns all the keys in the database"""
        return self._db.keys()

    def values(self) -> Iterable[Any]:
        """Returns all the values in the database"""
        return self._db.values()

    def items(self) -> Iterable[tuple[str, Any]]:
        """Returns all the items in the database"""
        return self._db.items()

    def delete_record(self, obj_id: str, silence_error:bool = False) -> bool:
        """Deletes the record with the given id"""
        self._check_single_record_id(obj_id)
        
        if obj_id not in self._db and not silence_error:
            raise KeyError(f"Record with id '{obj_id}' does not exist in the database. Consider using `obj.delete_record('{obj_id}', silence_error=True)` to silence this error.")
        
        del self._db[obj_id]
        return self._write_DB(self._db)

    def delete_records(self, record_ids: Iterable[str], silence_error:bool = False) -> bool:
        """Deletes the records with the given ids"""
        self._check_multiple_record_ids(record_ids)
        
        if any(record_id not in self._db for record_id in record_ids) and not silence_error:
            problematic_keys = filter(lambda x: x not in self._db, record_ids)
            problematic_key_str = ", ".join(problematic_keys)
            raise KeyError(f"Record(s) with id(s) [{problematic_key_str}] does not exist in the database. Consider using `obj.delete_records({record_ids}, silence_error:bool = True)` to silence this error.")
        
        for record_id in record_ids:
            del self._db[record_id]
        
        return self._write_DB(self._db)

    @classmethod
    def create_database(cls, name: str, path: str = "../DB", verbose: bool = True):
        dbs_already_at_path = set(glob.glob(f"{path}/*.pkl"))
        Database._all_databases = Database._all_databases.union(dbs_already_at_path)

        if (access_path := f"{path}/{name}.pkl") not in Database._all_databases:
            with open(access_path, "wb") as handle:
                pickle.dump({}, handle, protocol=pickle.HIGHEST_PROTOCOL)
            Database._all_databases.add(access_path)
            if verbose:
                print(f"Database with name '{name}' at '{path}' created successfully.")
            return Database(name, path)
        else:
            raise FileExistsError(f"Database with name '{name}' at '{path}' already exists. Consider using `Database(name='{name}', path='{path}')` to access the database.")
    
    @classmethod
    def delete_database(cls, name: str, path: str = "../DB"):
        dbs_already_at_path = set(glob.glob(f"{path}/*.pkl"))
        Database._all_databases = Database._all_databases.union(dbs_already_at_path)

        if (access_path := f"{path}/{name}.pkl") in Database._all_databases:
            surity_check = input(f"Are you sure you want to delete '{name}' at '{path}'? (y/n): ")
            if surity_check.lower() == "y":
                os.remove(access_path)
                Database._all_databases.remove(access_path)
        else:
            raise FileNotFoundError(f"Database with name '{name}' at '{path}' does not exist")

    @classmethod
    def get_all_databases(cls, path: str = "../DB") -> set[str]:
        dbs_already_at_path = set(glob.glob(f"{path}/*.pkl"))
        Database._all_databases = Database._all_databases.union(dbs_already_at_path)
        return Database._all_databases



