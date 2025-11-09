import sqlite3
from time import sleep
from entities.workers import Workers
from entities.positions import Positions
from entities.rights import Rights


def main(): # учет сотрудников и должностей
    create_tables()
    # write_examples()
    data = read_data()
    workers:Workers = data[0]
    positions:Positions = data[1]
    rights:Rights = data[2]
    print('Working with database...\n')
    while True:
        iterat(workers, positions, rights)
        sleep(1)


def iterat(workers:Workers, positions:Positions, rights:Rights) -> None:
    match input('\nWhat will we do? 1 - get all female workers at the position, 2 - get the workers\'s rights,\n3 - get all positions with the right. Input: '):
        case '1':
            pos = positions.getbyname(input('Input position: '))
            if not pos: return print('Invalid position!')
            params = {'position': [['==', pos]], 'sex': [['==', 1]]}
            if (res := workers.search(params)) == None: return print('Invalid input at all!')
            if res == []: return print('Zero workers!')
            for worker in res: print(worker.name)
        case '2':
            params = {'name': [['contain', input('Input worker\'s name: ')]]}
            if (res := workers.search(params)) == None: return print('Invalid input at all!')
            match len(res):
                case 0: return print('Zero workers!')
                case 1: return print(f'{res[0].name}\'s rights: {", ".join([right.description for right in res[0].position.rights] or "Zero")}')
            # > 1
            params = {'birthday': [['contain', input('Input worker\'s birthday: ')]]}
            if (res := workers.search(params, res)) == None: return print('Invalid input at all!')
            match len(res):
                case 0: print('Zero workers!')
                case 1: print(f'{res[0].name}\'s rights: {", ".join([right.description for right in res[0].position.rights] or "Zero")}')
                case _: print('Too many workers!')
        case '3':
            right = rights.getsbydesc(input('Input right: '))
            if not right: return print('Zero rights!')
            if len(right) != 1: return print('Too many rights!')
            params = {'with': [['right', right[0]]]}
            if (res := positions.search(params)) == None: return print('Invalid input at all!')
            if res == []: return print('Zero positions!')
            for position in res: print(position.name)
        case _: print('Wrong input!')


def create_tables():
    requests = [
                'CREATE TABLE IF NOT EXISTS Workers(uuid INTEGER PRIMARY KEY, position INTEGER DEFAULT 1 REFERENCES Positions(uuid), sex BOOLEAN, name TEXT, birthday TEXT)',
                'CREATE TABLE IF NOT EXISTS Positions(uuid INTEGER PRIMARY KEY, name TEXT, description TEXT)',
                'CREATE TABLE IF NOT EXISTS Rights(uuid INTEGER PRIMARY KEY, name TEXT, description TEXT)',
                'CREATE TABLE IF NOT EXISTS PositionsToRights(uuid INTEGER PRIMARY KEY, position INTEGER REFERENCES Positions(uuid), right INTEGER REFERENCES Rights(uuid))'
    ]
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        for request in requests: cur.execute(request)


def write_examples():
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute('INSERT INTO workers(position, sex, name, birthday) VALUES(1, 0, "Иван Михаилович Иванов", "28.01.1975")')
        cur.execute('INSERT INTO workers(position, sex, name, birthday) VALUES(2, 0, "Иван Иванович Иванов", "12.08.1995")')
        cur.execute('INSERT INTO workers(position, sex, name, birthday) VALUES(3, 0, "Андрей Иванович Иванов", "17.05.1998")')
        cur.execute('INSERT INTO workers(position, sex, name, birthday) VALUES(3, 1, "Мария Ивановна Иванова", "08.07.2000")')
        cur.execute('INSERT INTO workers(position, sex, name, birthday) VALUES(4, 1, "Полина Павловна Павлова", "05.02.2005")')
        cur.execute('INSERT INTO positions(name, description) VALUES("Директор", "Управляет всей компанией")')
        cur.execute('INSERT INTO positions(name, description) VALUES("Менеджер персонала", "Главный HR, нанимает и увольняет")')
        cur.execute('INSERT INTO positions(name, description) VALUES("Генеральный секретарь", "Создает финансовые отчеты")')
        cur.execute('INSERT INTO positions(name, description) VALUES("Стажер", "На испытательном сроке")')
        cur.execute('INSERT INTO rights(name, description) VALUES("kick_join", "Увольнение и найм сотрудника")')
        cur.execute('INSERT INTO rights(name, description) VALUES("edit_workers_pos", "Изменение должности сотрудника")')
        cur.execute('INSERT INTO rights(name, description) VALUES("view_every", "Просмотреть все данные")')
        cur.execute('INSERT INTO rights(name, description) VALUES("view_own", "Просмотреть свои данные")')
        cur.execute('INSERT INTO positionstorights(position, right) VALUES(1, 1)')
        cur.execute('INSERT INTO positionstorights(position, right) VALUES(1, 2)')
        cur.execute('INSERT INTO positionstorights(position, right) VALUES(1, 3)')
        cur.execute('INSERT INTO positionstorights(position, right) VALUES(1, 4)')
        cur.execute('INSERT INTO positionstorights(position, right) VALUES(2, 1)')
        cur.execute('INSERT INTO positionstorights(position, right) VALUES(2, 2)')
        cur.execute('INSERT INTO positionstorights(position, right) VALUES(2, 3)')
        cur.execute('INSERT INTO positionstorights(position, right) VALUES(2, 4)')
        cur.execute('INSERT INTO positionstorights(position, right) VALUES(3, 3)')
        cur.execute('INSERT INTO positionstorights(position, right) VALUES(3, 4)')
        cur.execute('INSERT INTO positionstorights(position, right) VALUES(4, 4)')


def read_data() -> list:
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        tworkers = cur.execute('SELECT * FROM Workers').fetchall()
        tpositions = cur.execute('SELECT * FROM Positions').fetchall()
        trights = cur.execute('SELECT * FROM Rights').fetchall()
        tpositionstorights = cur.execute('SELECT * FROM PositionsToRights').fetchall()
    rights = Rights(trights, tpositionstorights)
    positions = Positions(tpositions, rights, Workers)
    workers = Workers(tworkers, positions)
    return [workers, positions, rights]



if __name__ == '__main__': main()
else: raise BaseException('You can\'t use it as a library')
