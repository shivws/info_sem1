import sqlite3


class Department:
    uuid: int
    boss: int
    name: str
    description: str

    def __init__(self, uuid:int, boss:int, name:str, description:str):
        self.uuid = uuid
        self.boss = boss
        self.name = name
        self.description = description


class Departments:
    departments: list[Department]

    def __init__(self, data:list) -> None:
        for el in data: self.departments.append(Department(el[0], el[1], el[2], el[3]))

    def get(self, uuid:int) -> Department:
        if uuid == 1: return None # type: ignore
        try: return self.departments[uuid]
        except IndexError: return None # type: ignore
    # not ready
    def add(self, boss:int, name:str, description:str) -> int:
        return -1

    def edit_boss(self, uuid:int, new_boss:int, uuid_from:int) -> int:
        return -1
    
    def edit_naming(self, uuid:int, new_naming:str, is_name:bool, uuid_from:int) -> int:
        return -1

    def remove(self, uuid:int, uuid_from:int) -> int:
        return -1
