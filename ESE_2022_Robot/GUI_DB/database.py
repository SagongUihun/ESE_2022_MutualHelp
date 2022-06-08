# -*- coding:utf-8 -*-

import sqlite3
import random

class sqlite_lib:

    dbname =""
    db = None
    cursor = None

    def open(self, name):
        self.dbname = name
        self.db = sqlite3.connect(self.dbname)
        self.cur = self.db.cursor()

    def close(self):
        if self.db != None:
            self.db.close()

    def commit(self):
        self.db.commit()

    def sql_exec(self, sql):
        self.cur.execute(sql)
        self.commit()

        return self.cur

class db(sqlite_lib):

    # 센서 데이터 테이블 생성 함수(roll pitch yaw)
    def createSensorTable(self):
        
        self = sqlite_lib()
        self.open("database.db")

        sql = '''CREATE TABLE if not exists handData(
        time DATETIME DEFAULT (strftime('%Y-%m-%d', DATETIME('now', 'localtime'))),
        name text,
        rollL float,
        pitchL float,
        yawL float,
        rollR float,
        pitchR float,
        yawR float)'''

        self.sql_exec(sql)
        self.close()

    def insertRPY(self, name, rowl, rowr):
        self = sqlite_lib()
        self.open("database.db")

        Rl = rowl[0]
        Pl = rowl[1]
        Yl = rowl[2]
        Rr = rowr[0]
        Pr = rowr[1]
        Yr = rowr[2]
        sql = '''INSERT INTO handData(name, time, set_result) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}')'''.format(name,Rl, Pl, Yl, Rr, Pr, Yr)
        self.sql_exec(sql)

    def returnHandData(self):
        self = sqlite_lib()
        self.open("database.db")
        sql = '''SELECT time, name, avg(rollL), avg(pitchL), avg(yawL), avg(rollR), avg(pitchR), avg(yawR) FROM handData Group by time, name'''
        self.sql_exec(sql)
        rows = self.cur.fetchall()
        self.close()
        return rows

    def deleteSensorData(self, day):
        self = sqlite_lib()
        self.open("database.db")

        sql = '''DELETE FROM handData'''
        self.sql_exec(sql)
        self.close()

    # 운동목표 데이터 베이스 생성 함수
    def createWorkoutData(self):
        self = sqlite_lib()
        self.open("database.db")
        
        # 운동 루틴 목표 데이터 베이스(루틴id, 운동이름, 목표 세트, 목표 개수, 쉬는시간)
        sql1 = '''CREATE TABLE if not exists routine(
            routine_id text not null,
            name text not null,
            aim_set int not null,
            aim_num int not null,
            rest_time int not null)'''

        # 장단기 피드백 데이터 베이스(날짜, 운동이름, 운동시간, kcal, 세트결과, 손목 점수 1~6)
        sql2 = '''CREATE TABLE if not exists daywork(
            day DATETIME DEFAULT (strftime('%Y-%m-%d', DATETIME('now', 'localtime'))),
            name text not null,
            time text not null,
            kcal float,
            set_result float not null,
            wrsit1 float,
            wrsit2 float,
            wrsit3 float,
            wrsit4 float,
            wrsit5 float,
            wrsit6 float
            )'''

        self.sql_exec(sql1)
        self.sql_exec(sql2)
        self.close()
    
    # for GUI INSERT DATA
    def GuiInsertWorkout(self, row):
        self = sqlite_lib()
        self.open("database.db")
        count = len(row)
        for x in range(count):
            routine_id, name, aim_set, aim_num, rest_time = row[x]
            sql = '''INSERT INTO routine(routine_id, name, aim_set, aim_num, rest_time) VALUES('{}', '{}', '{}', '{}', '{}')'''.format(routine_id, name, aim_set, aim_num, rest_time)
            self.sql_exec(sql)

    # workout data save function
    def saveDayworkoutData(self, row):
        self = sqlite_lib()
        self.open("database.db")
        count = len(row)
        for x in range(count):
            name, time, set_result = row[x]
            sql = '''INSERT INTO daywork(name, time, set_result) VALUES('{}', '{}', '{}')'''.format(name, time, set_result)
            self.sql_exec(sql)

    # 운동 결과 데이터 추출 함수
    def returnDayworkoutRows(self):
        self = sqlite_lib()
        self.open("database.db")
        sql = '''SELECT day, name, sum(set_result) FROM daywork GROUP BY name, day'''
        self.sql_exec(sql)
        rows = self.cur.fetchall()
        self.close()
        return rows

    # 운동 상세 결과 데이터 추출 함수
    def returnNameWorkoutRows(self):
        self = sqlite_lib()
        self.open("database.db")
        sql = '''SELECT name, sum(time), max(time), min(time), avg(time),
        sum(kcal), max(kcal), min(kcal), avg(kcal),
        sum(set_result), max(set_result), min(set_result), avg(set_result) FROM daywork GROUP BY name'''
        self.sql_exec(sql)
        rows = self.cur.fetchall()
        self.close()
        return rows

    # 운동 루틴 데이터 행렬 추출 함수
    def returnRoutineRows(self, id):
        self = sqlite_lib()
        self.open("database.db")
        id = "routine_"+str(id)
        sql = '''SELECT name, aim_set, aim_num, rest_time FROM routine WHERE routine_id = "%s"'''%id
        self.sql_exec(sql)
        rows = self.cur.fetchall()
        self.close()
        return rows

    # 루틴 삭제 함수
    def deleteRoutine(self, id):
        self = sqlite_lib()
        self.open("database.db")
        id = "routine_"+str(id)
        sql = '''DELETE FROM routine WHERE routine_id = "%s"'''%id
        self.sql_exec(sql)
        self.close()