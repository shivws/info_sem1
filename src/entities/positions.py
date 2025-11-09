import sqlite3
from entities.workers import Workers
from entities.rights import Right, Rights


class Position:
    uuid: int
    rights: list[Right]
    name: str
    description: str

    def __init__(self, uuid:int, rights:list[Right], name:str, description:str) -> None:
        self.uuid = uuid
        self.rights = rights
        self.name = name
        self.description = description

    def __str__(self) -> str:
        return f'<Position #{self.uuid}: {self.name}>'

    def anticheckright(self, right:str) -> int:
        if not isinstance(right, str): return 2
        for r in self.rights:
            if r.name == right: return 0
        return 1

    def anticheckright_uuid(self, right_uuid:int) -> int:
        if not isinstance(right_uuid, int): return 2
        for r in self.rights:
            if r.uuid == right_uuid: return 0
        return 1


class Positions:
    positions: list[Position]
    workers: Workers
    rights: Rights

    def __init__(self, data:list, rights:Rights, workers) -> None:
        self.rights = rights
        self.workers = workers
        self.positions = []
        for el in data:
            self.positions.append(Position(el[0], rights.data[el[0]], el[1], el[2]))

    def anticheckright(self, uuid:int, right:str) -> int:
        if not (isinstance(uuid, int) and isinstance(right, str)): return 2
        if not self.get(uuid): return 3
        for r in self.get(uuid).rights:
            if r.name == right: return 0
        return 1

    def get(self, uuid:int) -> Position:
        try: return self.positions[uuid-1]
        except IndexError: return None # type: ignore

    def getbyname(self, name:str) -> Position:
        l_name = name.lower()
        for pos in self.positions:
            if l_name == pos.name.lower(): return pos
        return None # type: ignore

    def search(self, params:dict[str, list[list[str]]]={}, data:list[Position]=[]) -> list[Position]:
        if data == []: data = self.positions
        searched = data.copy()
        params_all = ('uuid', 'name', 'description', 'with')
        actions = (('==', '>', '<'), ('==', 'contain'), ('==', 'contain'), ('right',))
        edited = False
        for i, param in enumerate(params_all):
            if not param in params: continue
            for curparam in params[param]:
                if (not curparam[0] in actions[i]) or (curparam[1] == ''): continue
                edited = True
                for row in data:
                    match curparam[0]:
                        case '==':
                            if eval(f'row.{param}') != int(curparam[1]): searched.remove(row)
                        case '<':
                            if eval(f'row.{param}') >= int(curparam[1]): searched.remove(row)
                        case '>':
                            if eval(f'row.{param}') <= int(curparam[1]): searched.remove(row)
                        case 'right':
                            if not curparam[1] in row.rights: searched.remove(row)
                        case _: # 'contain'
                            if not curparam[1].lower() in eval(f'row.{param}').lower(): searched.remove(row)
        if len(params) != 0 and not edited: return None # type: ignore
        return searched

    def add(self, rights_int:list[int], name:str, description:str, uuid_from:int) -> int:
        if not (isinstance(rights_int, list) and isinstance(name, str) and isinstance(description, str)): return 1
        if self.workers.get(uuid_from).position.anticheckright('edit_pos_rights'): return 2
        if self.rights.isrightsinvalid(rights_int): return 3
        rights_el = [self.rights.getbyuuid(r) for r in rights_int]
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('INSERT INTO Positions(name, description) VALUES(?, ?)', (name, description))
            pos_id = len(self.positions)
            for r in rights_el:
                cur.execute('INSERT INTO PositionsToRights(position, right) VALUES(?, ?)', (pos_id+1, r.uuid))
        self.positions.append(Position(len(self.positions), rights_el, name, description))
        return 0

    def add_right(self, uuid:int, need_right_str:str, uuid_from:int) -> int:
        if not (isinstance(uuid, int) and isinstance(need_right_str, str) and isinstance(uuid_from, int)): return 1
        if self.workers.get(uuid_from).position.anticheckright('edit_pos_rights'): return 2
        if not self.get(uuid): return 3
        if not self.workers.get(uuid_from): return 4
        need_right = self.rights.get(need_right_str)
        if need_right == False: return 5
        if not self.anticheckright(uuid, need_right_str): return 6
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('INSERT INTO positionstorights(position, right) VALUES(?, ?)', (uuid, need_right.uuid))
        self.get(uuid).rights.append(need_right)
        return 0

    def del_right(self, uuid:int, del_right_str:str, uuid_from:int) -> int:
        if not (isinstance(uuid, int) and isinstance(del_right_str, str) and isinstance(uuid_from, int)): return 1
        if not self.workers.get(uuid_from): return 2
        if self.workers.get(uuid_from).position.anticheckright('edit_pos_rights'): return 3
        if not self.get(uuid): return 4
        del_right = self.rights.get(del_right_str)
        if del_right == False: return 5
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('DELEFE FROM positionstorights WHERE uuid = ? AND right = ?', (uuid, del_right.uuid))
        self.get(uuid).rights.remove(del_right)
        return 0

    def edit_naming(self, uuid:int, new_naming:str, is_name:bool, uuid_from:int) -> int:
        if not (isinstance(uuid, int) and isinstance(new_naming, str) and isinstance(is_name, bool) and isinstance(uuid_from, int)): return 1
        if self.workers.get(uuid_from).position.anticheckright('edit_pos_naming'): return 2
        if not self.get(uuid): return 3
        if not self.workers.get(uuid_from): return 4
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            if is_name:
                try: cur.execute('UPDATE positions SET name = ? WHERE uuid = ?', (new_naming, uuid))
                except: return 2
                self.get(uuid).name = new_naming
            else:
                try: cur.execute('UPDATE positions SET description = ? WHERE uuid = ?', (new_naming, uuid))
                except: return 3
                self.get(uuid).description = new_naming
        return 0

    def remove(self, uuid:int, uuid_from:int) -> int:
        if not (isinstance(uuid, int) and isinstance(uuid_from, int)): return 1
        if self.workers.get(uuid_from).position.anticheckright('edit_pos'): return 2
        if not self.workers.get(uuid_from): return 3
        victim = self.get(uuid)
        if not victim: return 4
        if victim.rights != []: return 5
        for worker in self.workers.workers:
            if victim == worker.position: return 6
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            try: cur.execute('DELETE FROM positions WHERE uuid = ?', (uuid,))
            except: return 2
        self.positions.pop(uuid-1)
        return 0
