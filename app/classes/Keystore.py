"""keystore to handle all redis data"""
from app.classes.Record import Mode, Record


class KeyStore:
    """Class that will handle all data"""
    def __init__(self):
        """initialize and empty dictionary"""
        self.keys: dict[str, Record] = {}
        self.keys.clear()

    def clear(self):
        """clear datastore, mostly used for testing"""
        self.keys.clear()

    def set_array(self, data: list[str]) -> str | None:
        """setting data with key value pair"""
        key: str = data[0]
        val: str = data[1]
        px: int  = -1  # pylint: disable=invalid-name
        if len(data) > 2:
            px = int(data[3])  # pylint: disable=invalid-name

        return self.set(key=key, value=val, px=px)

    async def push_list(self, key:str, value: str, right:bool) -> int:
        """pushing data into a list, creating a new one is non exists"""
        if not key in self.keys:
            record: Record = Record(Mode.LIST)
            self.keys[key] = record

        return await self.keys[key].push(value, right)


    def set(self, key:str, value: str, args: str = "", px:int = -1) -> str | None: # pylint: disable=unused-argument
        """setting data with key value pair"""
        if not key in self.keys:
            record: Record = Record(Mode.STRING)
            self.keys[key] = record

        self.keys[key].set(value=value, px=px)

        if not key in self.keys:
            return None  # "-ERR unable to set record into the datastore"
        return "OK"

    def get(self, key: str | list[str]) -> bytes | None:
        """getting data with specific key"""
        match (key):
            case str():
                return self._get(key=key)
            case list():
                return self._get(key=key[0])
            case _:
                return None

    def _get(self, key:str) -> bytes | None:
        """internal get command"""
        if not key in self.keys:
            return None
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

    def lrange(self, key:str, start:str, end:str) -> list[str]:
        """get set of record values"""
        if key in self.keys:
            return self.keys[key].get_records(start=start, end=end)
        return []

    def length(self, key:str) -> int:
        """get length of list"""
        if key in self.keys:
            return self.keys[key].length()
        return 0

    async def lpop(self, key:str, val: str) -> str | list[str] | None:
        """left pop of rlist"""
        if key in self.keys:
            if val:
                return self.keys[key].mpop(val=int(val))
            return self.keys[key].pop()
        return None

    async def blpop(self, key:str, timeout:float) -> str | None | list[str]:
        """blocking left pop"""
        if not key in self.keys:
            self.keys[key] = Record(Mode.LIST)
        output = await self.keys[key].blpop(timeout=timeout)
        if output is None:
            return output
        return [key, output]

    def incr(self, key:str):
        """increment int value"""
        if not key in self.keys:
            self.keys[key] = Record(Mode.STRING)
        return self.keys[key].incr()

    def xadd(self, key:str, entry_id:str, args:tuple[str, ...]):
        """xadd for streams"""
        if not key in self.keys:
            self.keys[key] = Record(Mode.STREAM)
        return self.keys[key].xadd(entry_id, args)

# singleton instance
keystore = KeyStore()
