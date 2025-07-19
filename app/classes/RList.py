"""handle list data in redis"""

class RList:
    """redis list record"""
    def __init__(self) -> None:
        """initilize rlist"""
        self.rlist = []

    def clear(self) -> None:
        """clear list"""
        self.rlist.clear()

    def push(self, data:str) -> int:
        """push data into list"""
        self.rlist.append(data)
        return len(self.rlist)
