# coding:utf-8
import sqlite3
import os


class open_db():
    def __init__(self):

        self.db_name = None
        self.oldmap_name = None
        self.oldpath_name = None
        self.config01 = {
            "BrushConfigValue": "value_id,description,value",
            "FlowConfigValue": "value_id,description,value",
            "ScrubberConfig": "config_id,name,squeegee,brush,flow,vacuum,speed",
            "SpeedConfigValue": "value_id,description,value",
            "VacuumConfigValue": "value_id,description,value",
        }
        self.config10 = {
            "BrushConfigValue": "value_id,description,value",
            "FlowConfigValue": "value_id,description,value",
            "PlanQRCode": "name,code_id,plan_id,cycle_times,config_id,pose,reserved_1,reserved_2",
            "ScrubberConfig": "config_id,name,squeegee,brush,flow,vacuum,speed",
            "SpeedConfigValue": "value_id,description,value",
            "SpeedManualConfigValue": "value_id,description,value",
            "VacuumConfigValue": "value_id,description,value",
        }

    def sleclt_name(self, filename):
        self.db_name = []
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = """SELECT name FROM sqlite_master WHERE type="table" ORDER BY name"""
        cursor.execute(sqlshell)
        result = cursor.fetchall()
        for i in result:
            self.db_name.append(str(i).split("\'")[1])
        conne.close()
        return self.db_name

    def select_Map_nums(self, filename):
        self.oldmap_name = []
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT uuid FROM Map a,ProxyMap b WHERE a.old=0 AND b.map_id = a.map_id "
        cursor.execute(sqlshell)
        result = cursor.fetchall()
        map_nums = len(result)
        # print(result)
        for i in result:
            self.oldmap_name.append(str(i).split("\'")[1])
        conne.close()
        return map_nums

    def select_Map_01(self, filename):
        self.oldpath_name = []
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT  name,create_time,modify_time,resolution,width,height,left," \
                   "top,data,original_data,pbstream FROM Map "
        cursor.execute(sqlshell)
        result = cursor.fetchall()
        return result
    def select_Map_10(self, filename):
        self.oldpath_name = []
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT  name,create_time,modify_time,resolution,width,height,left," \
                   "top,data,original_data,pbstream,slam_data FROM Map "
        cursor.execute(sqlshell)
        result = cursor.fetchall()
        return result
    def select_Path(self, filename):
        self.oldpath_name = []
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT path_id,name,type,sub_type, cover_area,length FROM Path "
        cursor.execute(sqlshell)
        result = cursor.fetchall()
        return result

    def select_Plan(self, filename):
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT plan_id,name, create_time type,length,task_id_data FROM Plan "
        cursor.execute(sqlshell)
        result = cursor.fetchall()
        return result

    def select_Area(self, filename):
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT area_id,name,zone_id,length, path_id_data FROM Area"
        cursor.execute(sqlshell)
        result = cursor.fetchall()
        return result

    def select_Task(self, filename):
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT task_id ,name,config_id ,type FROM Task"
        cursor.execute(sqlshell)
        result = cursor.fetchall()
        return result
    def select_Task_len(self, filename):
        sum = 0
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT task_id FROM Task"
        cursor.execute(sqlshell)
        result = list(cursor.fetchall())
        return len(result)
    def select_Zone(self, filename):
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT zone_id ,name,path_id,type,config_id FROM Zone  "
        cursor.execute(sqlshell)
        result = cursor.fetchall()
        return result

    def select_config_01(self, filename):
        key_db = self.config01.keys()
        result = []

        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        for i in key_db:
            sqlshell = "SELECT {} FROM {}".format(self.config01[i], i)
            cursor.execute(sqlshell)
            result.append(cursor.fetchall())
        return result
    def select_config_10(self, filename):
        key_db = self.config10.keys()
        result = []
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        for i in key_db:
            sqlshell = "SELECT {} FROM {}".format(self.config10[i], i)
            cursor.execute(sqlshell)
            # print(i, cursor.fetchall())
            result.append(cursor.fetchall())
        return result
    def select_statistics_record_01(self, filename):
        statistics = "record_id,type, upload_time,map_uuid,name,path_id,create_time,config_id,area,duration," \
                     "water_comsumption,power_comsumption,cover_rate,start,end,expected_area,mileage,exe_status," \
                     "user_id,cycle_times,custom_id"
        result = []
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT {} FROM Record GROUP BY record_id ".format(statistics)
        cursor.execute(sqlshell)
        result = cursor.fetchall()
        return result

    def select_statistics_CleanStatistic_01(self, filename):
        statistics = "statistic_id,service_duration,clean_duration,remain_maintain_time,clean_mileage,clean_area," \
                     "clean_times,current_run_duration,absorbent_tape_used_duration,disk_brush_used_duration,type"
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT {} FROM CleanStatistic ".format(statistics)
        cursor.execute(sqlshell)
        result = cursor.fetchall()
        return result
    def select_user(self, filename):
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT user_id ,name,password,number,authority,company,status FROM User"
        cursor.execute(sqlshell)
        result = cursor.fetchall()
        return result

if __name__ == '__main__':
    b = 0
    old_db = open_db()
    loaclfile = os.getcwd()
    for root, dir, files in os.walk(loaclfile):
        if "real_db" in files:
            old_db_file = os.path.join(root, "real_db.db")
            old_mapnums = old_db.select_Map_nums(old_db_file)
            old_map_names = old_db.oldmap_name
        for i in dir:
            if "升级后" in i:
                new_db_file = os.path.join(root, i)
        if "user.db" in files:
            new_db_mapnums = len(files) - 5

    if old_mapnums == new_db_mapnums:
        print(old_map_names)
