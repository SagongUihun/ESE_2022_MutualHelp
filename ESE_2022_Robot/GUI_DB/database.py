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

        sqlL = '''CREATE TABLE if not exists leftsensor(
        time DATETIME DEFAULT (DATETIME('now', 'localtime')),
        roll float not null,
        pitch float not null,
        yaw float not null)'''

        sqlR ='''CREATE TABLE if not exists rightsensor(
        time DATETIME DEFAULT (DATETIME('now', 'localtime')),
        roll float not null,
        pitch float not null,
        yaw float not null)'''

        self.sql_exec(sqlL)
        self.sql_exec(sqlR)
        self.close()

    # 센서 데이터 테이블에서 운동별 자세 측정을 위해 데이터 추출 함수
    def classifySensorData(self):
        self = sqlite_lib()
        self.open("database.db")

        num = int(raw_input('운동 종류 선택: ')
        )
        if num == 1:
            sql = '''SELECT * FROM sensor WHERE id="%s"'''%num
            self.sql_exec(sql)
            rows = self.cur.fetchall()

            for row in rows:
                print(row)

            self.close()

        elif num == 2:
            sql = '''SELECT * FROM sensor WHERE id="%s"'''%num

            self.sql_exec(sql)
            rows = self.cur.fetchall()

            for row in rows:
                print(row)

            self.close()

        elif num == 3:
            sql = '''SELECT * FROM sensor WHERE id="%s"'''%num

            self.sql_exec(sql)
            rows = self.cur.fetchall()

            for row in rows:
                print(row)

            self.close()

        elif num == 4:
            sql = '''SELECT * FROM sensor WHERE id="%s"'''%num

            self.sql_exec(sql)
            rows = self.cur.fetchall()

            for row in rows:
                print(row)

            self.close()

    # 센서 데이터 테이블에서 운동 종류에 따라 테이블 데이터 출력
    def getSensorData(self):
        self = sqlite_lib()
        self.open("database.db")

        num = int(raw_input("운동종류선택: "))

        while num != 0:
            for i in range(10):
                data = (num, random.random(), random.random(), random.random()
                    , random.random(), random.random(), random.random()
                    , random.random(), random.random(), random.random()
                    , random.random(), random.random(), random.random()
                    , random.random(), random.random(), random.random()
                    , random.random(), random.random(), random.random()
                    , random.random(), random.random(), random.random()
                    , random.random(), random.random(), random.random())

                sqlInsert = '''INSERT INTO sensor(
                    id, Lfsr1, Lfsr2, Lfsr3, Rfsr1, Rfsr2, Rfsr3,
                    LaccelX, LaccelY, LaccelZ, LgyroX, LgyroY, LgyroZ, LmagX, LmagY, LmagZ,
                    RaccelX, RaccelY, RaccelZ, RgyroX, RgyroY, RgyroZ, RmagX, RmagY, RmagZ
                    ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''

                self.cur.execute(sqlInsert, data)
                self.commit()
            num = int(raw_input("종료: 0 다른 운동종류선택: ?"))

        self.close()

    # 센서 데이터 저장 후 계산
    def saveSensorData(self):
        self = sqlite_lib()
        self.open("database.db")

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
            kcal float not null,
            set_result float not null,
            wrsit1 float not null,
            wrsit2 float not null,
            wrsit3 float not null,
            wrsit4 float not null,
            wrsit5 float not null,
            wrsit6 float not null
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

    # 운동 결과 데이터 추출 함수
    def returnDayworkoutRows(self, day):
        self = sqlite_lib()
        self.open("database.db")
        sql = '''SELECT name, time FROM daywork WHERE day = "%s"'''%day
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