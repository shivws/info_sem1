import sqlite3
from entities.workers import Workers
from entities.powers import Powers


class Position:
    uuid: int
    power: list
    power_num: int
    name: str
    description: str
    power_list: list

    def __init__(self, uuid:int, power_num:int, name:str, description:str, power_list:list) -> None:
        self.uuid = uuid
        self.power_num = power_num
        self.name = name
        self.description = description
        self.power_list = power_list
        self.update_powers()

    def update_powers(self) -> None:
        self.power = []
        getbit = lambda num, pos: (num >> pos) == 1
        for key, value in enumerate(self.power_list):
            if getbit(self.power_num, key): self.power.append(value)

    def checkpower(self, power:str) -> bool:
        return power in self.power
    
    def checkpower_int(self, need_powers:int) -> bool:
        return (self.power_num & need_powers) == need_powers


class Positions:
    positions: list[Position]
    workers: Workers
    powers: Powers

    def __init__(self, data:list, powers:Powers) -> None:
        self.powers = powers
        for el in data: self.positions.append(Position(el[0], el[1], el[2], el[3], powers.power_list))

    def get(self, uuid:int) -> Position:
        if uuid == 1: return None # type: ignore
        try: return self.positions[uuid]
        except IndexError: return None # type: ignore

    def add(self, power:int, name:str, description:str) -> int:
        if not (isinstance(power, int) and isinstance(name, str) and isinstance(description, str)): return 1
        if not self.powers.ispowervalid(power): return 2
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('INSERT INTO positions(power, name, discription) VALUES(?, ?, ?)', (power, name, description))
        self.positions.append(Position(len(self.positions), power, name, description, self.powers.power_list))
        return 0

    def edit_power(self, uuid:int, need_powers:int, uuid_from:int) -> int:
        if not (isinstance(uuid, int) and isinstance(need_powers, int) and isinstance(uuid_from, int)): return 1
        if not self.get(uuid): return 2
        if not self.workers.get(uuid_from): return 3
        if not self.workers.get(uuid_from).position.checkpower('edit_pos_power'): return 4
        if not self.powers.ispowervalid(need_powers): return 5
        if self.get(uuid).checkpower_int(need_powers): return 6
        new_power = self.get(uuid).power_num + need_powers
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('UPDATE positions SET power = ? WHERE uuid = ?', (new_power, uuid))
        self.get(uuid).power_num = new_power
        self.get(uuid).update_powers()
        return 0

    def edit_naming(self, uuid:int, new_naming:str, is_name:bool, uuid_from:int) -> int:
        if not (isinstance(uuid, int) and isinstance(new_naming, str) and isinstance(is_name, bool) and isinstance(uuid_from, int)): return 1
        if not self.get(uuid): return 2
        if not self.workers.get(uuid_from): return 3
        if not self.workers.get(uuid_from).position.checkpower('edit_pos_naming'): return 4
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            if is_name:
                cur.execute('UPDATE positions SET name = ? WHERE uuid = ?', (new_naming, uuid))
                self.get(uuid).name = new_naming
            else:
                cur.execute('UPDATE positions SET description = ? WHERE uuid = ?', (new_naming, uuid))
                self.get(uuid).description = new_naming
        return 0
    
    def remove(self, uuid:int, uuid_from:int) -> int:
        if not (isinstance(uuid, int) and isinstance(uuid_from, int)): return 1
        if not self.get(uuid): return 2
        if not self.workers.get(uuid_from): return 3
        if not self.workers.get(uuid_from).position.checkpower('edit_pos'): return 4
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('DELETE FROM positions WHERE uuid = ?', (uuid,))
        self.positions.pop(uuid-1)
        return 0
