"""keystore to handle all redis data"""
from .Record import Mode, Record


class KeyStore:
    """Class that will handle all data"""
    def __init__(self):
        """initialize and empty dictionary"""
        self.keys: dict[str, Record] = {}
        self.keys.clear()

    def clear(self):
        """clear datastore, mostly used for testing"""
        self.keys.clear()

    def set_array(self, data: list[str]) -> str:
        """setting data with key value pair"""
        key: str = data[0]
        val: str = data[1]
        px: int  = -1  # pylint: disable=invalid-name
        if len(data) > 2:
            px = int(data[3])  # pylint: disable=invalid-name

        return self.set(key=key, value=val, px=px)

    def push_list(self, key:str, value: str) -> int:
        """pushing data into a list, creating a new one is non exists"""
        if not key in self.keys:
            record: Record = Record(Mode.LIST)
            self.keys[key] = record

        return self.keys[key].push(value)

    def set(self, key:str, value: str, args: str = "", px:int = -1) -> str: # pylint: disable=unused-argument
        """setting data with key value pair"""
        if not key in self.keys:
            record: Record = Record(Mode.STRING)
            self.keys[key] = record

        self.keys[key].set(value=value, px=px)

        if not key in self.keys:
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
        if not key in self.keys:
            return "$-1"
        return self.keys[key].get()

    def key_exists(self, key:str) -> bool:
        """checking key existance"""
        if key in self.keys:
            return True
        return False

    def get_type(self, key:str) -> str:
        """get record type"""
        if key in self.keys:
            return self.keys[key].type()
        return "none"

# singleton instance
keystore = KeyStore()
