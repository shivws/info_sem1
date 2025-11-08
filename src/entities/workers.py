import sqlite3
from entities.departments import Department, Departments
from entities.positions import Position, Positions


class Worker:
    uuid: int
    position: Position
    department: Department
    sex: bool
    name: str
    birthday: str

    def __init__(self, uuid:int, position:Position, department:Department, sex:bool, name:str, birthday:str) -> None:
        """ sex = 0 = male """
        self.uuid = uuid
        self.position = position
        self.department = department
        self.sex = sex
        self.name = name
        self.birthday = birthday


class Workers:
    workers: list[Worker]
    positions: Positions
    departments: Departments

    def __init__(self, data:list, positions:Positions, departments:Departments) -> None:
        self.positions = positions
        self.departments = departments
        for el in data: self.workers.append(Worker(el[0], el[1], el[2], el[3], el[4], el[5]))

    def get(self, uuid:int) -> Worker:
        if uuid == 1: return None # type: ignore
        try: return self.workers[uuid-1]
        except IndexError: return None # type: ignore

    def add(self, position:int, department:int, sex:bool, name:str, birthday:str) -> int:
        if not (isinstance(position, int) and isinstance(department, int) and isinstance(sex, bool) and isinstance(name, str) and isinstance(birthday, str)): return 1
        if not self.positions.get(position): return 2
        if not self.departments.get(department): return 3
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('INSERT INTO workers(position, department, sex, name, birthday) VALUES(?, ?, ?, ?, ?)', (position, department, sex, name, birthday))
        self.workers.append(Worker(len(self.workers), self.positions.get(position), self.departments.get(department), sex, name, birthday))
        return 0

    def edit_pos(self, uuid:int, new_pos:int, uuid_from:int) -> int:
        if not (isinstance(uuid, int) and isinstance(new_pos, int) and isinstance(uuid_from, int)): return 1
        if not self.get(uuid): return 2
        if not self.get(uuid_from): return 3
        if not self.get(uuid_from).position.checkpower('edit_worker_pos'): return 4
        if not self.positions.get(new_pos): return 5
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('UPDATE workers SET position = ? WHERE uuid = ?', (new_pos, uuid))
        self.get(uuid).position = self.positions.get(new_pos)
        return 0

    def remove(self, uuid:int, uuid_from:int) -> int:
        if not (isinstance(uuid, int) and isinstance(uuid_from, int)): return 1
        if not self.get(uuid): return 2
        if not self.get(uuid_from): return 3
        if not self.get(uuid_from).position.checkpower('kick_join'): return 4
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('DELETE FROM workers WHERE uuid = ?', (uuid,))
        self.workers.pop(uuid)
        return 0
