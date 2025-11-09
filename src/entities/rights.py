class Right:
    uuid: int
    name: str
    description: str

    def __init__(self, uuid, name, description) -> None:
        self.uuid = uuid
        self.name = name
        self.description = description
    
    def __str__(self) -> str:
        return f'<Right #{self.uuid}: {self.name}>'


class Rights:
    right_uuids: list[Right]
    right_names: dict[str, Right]
    data: list[list[Right]]

    def __init__(self, rights:list[list], data:list[list[int]]) -> None:
        self.right_names = {}
        self.right_uuids = []
        for row in rights:
            right = Right(row[0], row[1], row[2])
            self.right_names[row[1]] = right
            self.right_uuids.append(right)
        positions_count = max([t[1] for t in data])
        res = [[] for _ in range(positions_count+1)]
        for row in data:
            res[row[1]].append(self.getbyuuid(row[2]))
        self.data = [list(set(t)) for t in res]

    def get(self, name:str) -> Right:
        if not isinstance(name, str): return 1 # type: ignore
        try: return self.right_names[name]
        except: return 2 # type: ignore

    def getbyuuid(self, uuid:int) -> Right:
        if not isinstance(uuid, int): return 1 # type: ignore
        try: return self.right_uuids[uuid-1]
        except: return 2 # type: ignore

    def getsbydesc(self, description:str) -> list[Right]:
        if not isinstance(description, str) or description == '': return None # type: ignore
        res = []
        l_description = description.lower()
        for right in self.right_uuids:
            if l_description in right.description.lower(): res.append(right)
        return res

    def isrightsinvalid(self, rights:list[int]) -> int:
        if not isinstance(rights, list): return 2
        for right in rights:
            if not right in self.right_uuids: return 1
        return 0

    # def add(self, name:str, description:str) -> int:
    #     pass
