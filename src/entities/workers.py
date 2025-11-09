import sqlite3


class Worker:
    uuid: int
    # position: Position
    sex: bool
    name: str
    birthday: str

    def __init__(self, uuid:int, position, sex:bool, name:str, birthday:str) -> None:
        """ sex = 0 = male """
        self.uuid = uuid
        self.position = position
        self.sex = sex
        self.name = name
        self.birthday = birthday
    
    def __str__(self) -> str:
        return f'<Worker #{self.uuid}: {self.name}>'


class Workers:
    workers: list[Worker]
    # positions: Positions

    def __init__(self, data:list, positions) -> None:
        self.positions = positions
        self.workers = []
        for el in data: self.workers.append(Worker(el[0], positions.get(el[1]), el[2], el[3], el[4]))

    def get(self, uuid:int) -> Worker:
        try: return self.workers[uuid-1]
        except IndexError: return None # type: ignore

    def search(self, params:dict[str, list[list[str]]]={}, data:list[Worker]=[]) -> list[Worker]:
        if data == []: data = self.workers
        searched = data.copy()
        params_all = ('uuid', 'position', 'sex', 'name', 'birthday')
        actions = (('==', '>', '<'), ('==',), ('==',), ('==', 'contain'), ('==', 'contain'))
        edited = False
        for param in params:
            if not param in params_all: return None # type: ignore
            i = params_all.index(param)
            for curparam in params[param]:
                if (not curparam[0] in actions[i]) or (curparam[1] == ''): continue
                edited = True
                for row in searched.copy():
                    match curparam[0]:
                        case '==':
                            if eval(f'row.{param}') != curparam[1]: searched.remove(row)
                        case '<':
                            if eval(f'row.{param}') >= curparam[1]: searched.remove(row)
                        case '>':
                            if eval(f'row.{param}') <= curparam[1]: searched.remove(row)
                        case _: # 'contain'
                            if not curparam[1].lower() in eval(f'row.{param}').lower(): searched.remove(row)
        if len(params) != 0 and not edited:
            print(2)
            return None # type: ignore
        return searched

    def add(self, position:int, department:int, sex:bool, name:str, birthday:str) -> int:
        if not (isinstance(position, int) and isinstance(department, int) and isinstance(sex, bool) and isinstance(name, str) and isinstance(birthday, str)): return 1
        if not self.positions.get(position): return 2
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            try: cur.execute('INSERT INTO workers(position, department, sex, name, birthday) VALUES(?, ?, ?, ?, ?)', (position, department, sex, name, birthday))
            except BaseException: return -1
        self.workers.append(Worker(len(self.workers), self.positions.get(position), sex, name, birthday))
        return 0

    def edit_pos(self, uuid:int, new_pos:int, uuid_from:int) -> int:
        if not (isinstance(uuid, int) and isinstance(new_pos, int) and isinstance(uuid_from, int)): return 1
        if not self.get(uuid): return 2
        if not self.get(uuid_from): return 3
        if self.get(uuid).position.anticheckright('edit_worker_pos'): return 4
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
        if self.get(uuid_from).position.anticheckright('kick_join') is int: return 4
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('DELETE FROM workers WHERE uuid = ?', (uuid,))
        self.workers.pop(uuid)
        return 0
