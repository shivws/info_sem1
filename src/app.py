import sqlite3
from time import sleep
from entities.workers import Workers
from entities.positions import Positions
from entities.departments import Departments
from entities.powers import Powers


def main(): # учет сотрудников и должностей
    create_tables()
    write_data()
    # workers, positions, departments, powers = read_data()
    print('Work with database...\n')
    while True:
        input('What to do? 1 - read all workers, 2 - add a worker, 3 - remove a worker. Input: ')


def create_tables():
    requests = [
                'CREATE TABLE IF NOT EXISTS Workers(uuid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, position INTEGER DEFAULT 1 REFERENCES Positions(uuid) ON DELETE SET DEFAULT, department INTEGER DEFAULT 1 REFERENCES Departments(uuid) ON DELETE SET DEFAULT, sex BLOB, name TEXT, birthday TEXT)',
                'CREATE TABLE IF NOT EXISTS Positions(uuid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, power INTEGER, name TEXT, description TEXT)',
                'CREATE TABLE IF NOT EXISTS Departments(uuid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, boss INTEGER DEFAULT 1 REFERENCES Workers(uuid) ON DELETE SET DEFAULT, name TEXT, description TEXT)',
                'CREATE TABLE IF NOT EXISTS Powers(uuid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, value BLOB, name TEXT, description TEXT)'
    ]
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        for request in requests: cur.execute(request)


def write_data():
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute('INSERT INTO workers(position, department, sex, name, birthday) VALUES(1, 1, 0, "", "")')
        cur.execute('INSERT INTO workers(position, department, sex, name, birthday) VALUES(2, 2, 0, "Иван Иванович Иванов", "01.01.1995")')
        cur.execute('INSERT INTO workers(position, department, sex, name, birthday) VALUES(3, 3, 0, "Михаил Михаилович Михалков", "01.01.1990")')
        cur.execute('INSERT INTO workers(position, department, sex, name, birthday) VALUES(4, 4, 1, "Мария Ивановна Иванова", "01.01.2000")')
        cur.execute('INSERT INTO positions(power, name, description) VALUES(0, "", "")')
        cur.execute('INSERT INTO positions(power, name, description) VALUES(7, "Директор", "Управляет всей компанией")')
        cur.execute('INSERT INTO positions(power, name, description) VALUES(7, "Менеджер персонала", "Главный HR, нанимает и увольняет")')
        cur.execute('INSERT INTO positions(power, name, description) VALUES(4, "Генеральный секретарь", "Создает финансовые отчеты")')
        cur.execute('INSERT INTO departments(boss, name, description) VALUES(1, "", "")')
        cur.execute('INSERT INTO departments(boss, name, description) VALUES(2, "Руководство", "Отдел, управляющий остальными")')
        cur.execute('INSERT INTO departments(boss, name, description) VALUES(3, "HR-отдел", "Вопросы найма и увольнения персонала")')
        cur.execute('INSERT INTO departments(boss, name, description) VALUES(4, "Секретариат", "Финансовая отчетность компании")')
        cur.execute('INSERT INTO powers(name, description) VALUES("kick_join", "Увольнение и найм сотрудника")')
        cur.execute('INSERT INTO powers(name, description) VALUES("edit_workers_pos", "Изменение должности сотрудника")')
        cur.execute('INSERT INTO powers(name, description) VALUES("view_every", "Просмотреть все данные")')


def read_data():
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        tworkers = cur.execute('SELECT * FROM Workers').fetchall()
        tpositions = cur.execute('SELECT * FROM Positions').fetchall()
        tdepartments = cur.execute('SELECT * FROM Departments').fetchall()
        tpowers = cur.execute('SELECT * FROM Powers').fetchall()
    powers = Powers([tpowers[i][1] for i in range(len(tpowers))], [tpowers[i][2] for i in range(len(tpowers))])
    departments = Departments(tdepartments)
    positions = Positions(tpositions, powers)
    workers = Workers(tworkers, positions, departments)
    return [workers, positions, departments, powers]



if __name__ == '__main__': main()
else: raise BaseException('You can\'t use it as a library')
