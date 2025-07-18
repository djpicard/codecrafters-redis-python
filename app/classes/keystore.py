"""keystore to handle all redis data"""
from app.classes.records import Record


class KeyStore:
    """Class that will handle all data"""
    def __init__(self):
        """initialize and empty dictionary"""
        self.keys: dict[str, Record] = {}
        print(self.keys)
        self.keys.clear()

    def clear(self):
        """clear datastore, mostly used for testing"""
        self.keys.clear()

    def set_array(self, data: list[str]) -> str:
        """setting data with key value pair"""
        key = data[0]
        val = data[1]
        px = -1  # pylint: disable=invalid-name
        if len(data) > 2:
            px = int(data[3])  # pylint: disable=invalid-name

        return self.set(key=key, value=val, px=px)

    def set(self, key:str, value: str, args: str = "", px:int = -1) -> str: # pylint: disable=unused-argument
        """setting data with key value pair"""
        # set record and put it into the datastore
        record: Record = Record(value=value, px=int(px))
        self.keys[key] = record
        if self.keys[key] != record:
            return "$-1"  # "-ERR unable to set record into the datastore"
        return "+OK"

    def get(self, key: str | list[str]) -> str:
        """getting data with specific key"""
        match (key):
            case str():
                return self._get(key=key)
            case list():
                return self._get(key=key[0])
            case _:
                return "$-1"

    def _get(self, key:str) -> str:
        """internal get command"""
        print(f"Checking keystore: {key}")
        if not key in self.keys:
            print(f"Keystore doesn't have key {key}")
            return "$-1"
        record: Record = self.keys[key]
        print(f"Found record: {record}")
        return record.get()

    def key_exists(self, key:str) -> bool:
        """checking key existance"""
        print(f"Keystore: {self.keys}")
        if key in self.keys:
            return True
        return False

# singleton instance
keystore = KeyStore()
