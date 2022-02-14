# coding:utf-8
import sqlite3
import os
import new_data


class open_db():

    def __init__(self):

        self.db_name = None
        self.oldmap_name = None
        self.oldpath_name = None
        self.task_len = None
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
            "LoactionQRCode": "id,name,code_id,confidence,pose,reserved_1,reserved_2",
            "PlanQRCode": "id,name,code_id,plan_id,cycle_times,config_id,pose,reserved_1,reserved_2",
            "ReserveConfig": "config_id,key,value",
            "ScrubberCoding": "config_id,name,squeegee,brush,flow,vacuum,speed",
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
        for i in result:
            self.oldmap_name.append(str(i).split("\'")[1])
        conne.close()
        return map_nums

    def select_Map_01(self, filename, uuid):
        self.oldpath_name = []
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT  name,create_time,modify_time,resolution,width,height,left,top,data,original_data," \
                   "pbstream,original_data FROM Map a,ProxyMap b ,MapData c " \
                   "WHERE a.map_id=b.map_id AND a.map_id=c.map_id AND  a.old =0 AND b.uuid='{}'".format(uuid)
        cursor.execute(sqlshell)
        result = cursor.fetchall()
        return result

    def select_Path(self, filename, uuid):
        self.oldpath_name = []
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT path_id,name,type,wall_follow_type, cover_area,length FROM Path a,ProxyMap b " \
                   "WHERE   a.old= 0 AND b.map_id = a.map_id AND b.uuid= '{}'".format(
            uuid)
        cursor.execute(sqlshell)
        result = cursor.fetchall()
        return result

    def select_Area(self, filename, uuid):
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT area_id,name,zone_id,length, path_id_data FROM Area a,ProxyMap b " \
                   "WHERE   a.old= 0 AND b.map_id = a.map_id AND b.uuid= '{}'".format(
            uuid)
        cursor.execute(sqlshell)
        result = cursor.fetchall()
        return result

    def select_Plan(self, filename, uuid):

        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT plan_id,name, create_time type,length,task_id_data FROM Plan a,ProxyMap b " \
                   "WHERE a.old=0 AND b.map_id = a.map_id   AND b.uuid= '{}'".format(
            uuid)
        cursor.execute(sqlshell)
        result = cursor.fetchall()
        return result

    def select_Task(self, filename, uuid):
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT DISTINCT task_id,v.name, config_id, type FROM (SELECT map_id FROM ProxyMap WHERE uuid ='{}') a ," \
                   "(SELECT * FROM Area b, ProxyMap c WHERE b.map_id=c.map_id) d ," \
                   "(SELECT m.task_id ,m.name , config_id, type, map_id FROM FollowPath e , Area f ,Task m " \
                   "WHERE e.area_id=f.area_id AND m.task_id=e.task_id AND f. old=0)  v " \
                   "WHERE d.old=0 AND a.map_id=v.map_id".format(uuid)
        cursor.execute(sqlshell)
        result = cursor.fetchall()
        return result

    def select_Task_len(self, filename, uuid):
        sum = 0
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT length FROM Plan a,ProxyMap b " \
                   "WHERE a.old=0 AND b.map_id = a.map_id   AND b.uuid= '{}'".format(uuid)
        cursor.execute(sqlshell)
        result = list(cursor.fetchall())
        for i in result:
            i=list(i)
            for j in i:
                sum+=j
        return sum

    def select_Zone(self, filename, uuid):
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT zone_id ,name,path_id,type,config_id FROM Zone a,ProxyMap b " \
                   "WHERE b.map_id=a.map_id AND  a.old =0 AND  b.uuid='{}' ".format(uuid)
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
            sqlshell = "SELECT {} FROM {}".format(self.config01[i], i)
            cursor.execute(sqlshell)
            result.append(cursor.fetchall())
        return result
    def select_statistics_record_01(self, filename):
        statistics = "a.record_id,type,b.uploaded, b.upload_time,c.uuid,name,path_id,create_time,config_id,area," \
                     "duration,water_comsumption,power_comsumption,cover_rate,start,end,expected_area,mileage," \
                     "exe_status,user_id,cycle_times,custom_id"
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT {} FROM Record a, ProxyRecord b,ProxyMap c  WHERE a.old=0 AND b.record_id=a.record_id  AND" \
                   " a.map_id=c.map_id GROUP BY a.record_id".format(statistics)
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
    def select_LocationQRCode(self, filename):
        statistics = ""
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT {} FROM CleanStatistic ".format(statistics)
        cursor.execute(sqlshell)
        result = cursor.fetchall()
        return result


if __name__ == '__main__':
    db_nums = 1

    global old_mapnums, new_db_mapnums
    old_db = open_db()
    new_db = new_data.open_db()
    loaclfile = os.getcwd()
    for root, dir, files in os.walk(loaclfile):
        if "real_db.db" in files:
            old_db_file = os.path.join(root, "real_db.db")
            old_mapnums = old_db.select_Map_nums(old_db_file)
            old_map_names = old_db.oldmap_name

        if "升级后" in root and "config.db" in files:
            new_db_file = os.path.join(root)
            new_db_mapnums = len(files) - 5
            # print(new_db_mapnums)
            # print(new_db_file)
        if "升级前HF0.1" in root:
            old_db_file = os.path.join(root, "real_db.db")
        if "升级前HF1.0" in root:
            old_db_file_01 = os.path.join(root, "real_db.db")
    if old_mapnums == new_db_mapnums:

        for i in old_map_names:

            new_db_files = os.path.join(new_db_file, i + ".db")
            # print(new_db_files)
            new_area = new_db.select_Area(new_db_files)
            old_area = old_db.select_Area(old_db_file, i)
            if new_area == old_area:
                print("对比地图{}中的Area表6个元素，共{}个数据".format(i, len(old_area) * 6) + "Passed")
            else:
                print(new_db_files + "Area 表Failed")
            new_map = new_db.select_Map_01(new_db_files)
            old_map = old_db.select_Map_01(old_db_file, i)
            if new_map == old_map:
                print("对比地图{}中的Map表12个元素，共{}个数据".format(i, len(old_map) * 12) + "Passed")
            else:
                print(new_db_files + "Map表Failed")
            new_path = new_db.select_Path(new_db_files)
            old_path = old_db.select_Path(old_db_file, i)

            if old_path == new_path:
                print("对比地图{}中的Path表4个元素，共{}个数据".format(i, len(old_path) * 4) + "Passed")
            else:
                print(new_db_files + "Path表Failed")
            new_plan = new_db.select_Plan(new_db_files)
            old_plan = old_db.select_Plan(old_db_file, i)
            if new_plan == old_plan:
                print("对比地图{}中的Plan表7个元素，共{}个数据".format(i, len(old_plan) * 7) + "Passed")
            else:
                print(new_db_files + "Plan表Failed")
            new_task = new_db.select_Task(new_db_files)
            old_task = old_db.select_Task(old_db_file, i)
            new_task_len = new_db.select_Task_len(new_db_files)
            old_task_len = old_db.select_Task_len(old_db_file, i)
            if new_task == old_task:
                print("对比地图{}中的Task表4个元素，共{}个数据".format(i, len(old_task) * 4) + "Passed")
            elif new_task_len==old_task_len:
                print("对比地图{}中的Task表4个元素，共{}个数据".format(i, len(old_task) * 4) + "Passed")
            else:
                print(new_db_files + "Task表Failed")
            new_zone = new_db.select_Zone(new_db_files)
            old_zone = old_db.select_Zone(old_db_file, i)
            if new_zone == old_zone:
                print("对比地图{}中的Zone表6个元素，共{}个数据".format(i, len(old_path) * 6) + "Passed")
            else:
                print(new_db_files + "Zone表Failed")

        old_config = old_db.select_config_01(old_db_file)
        config_file = os.path.join(new_db_file, "config.db")
        new_config = new_db.select_config_01(config_file)
        for i in range(4):
            if old_config[i] == new_config[i]:
                print("对比config.db中的{}表的元素:Passed".format(list(old_db.config01.keys())[i]))
            else:
                print(config_file + list(old_db.config01.keys())[i] + "Failed")
        old_record = old_db.select_statistics_record_01(old_db_file)
        new_record_file = os.path.join(new_db_file, "statistics.db")
        new_record = new_db.select_statistics_record_01(new_record_file)
        if old_record == new_record:
            print("对比statistics.db中的record表元素:Passed")
        else:
            print("对比statistics.db中的record表元素:Failed，请查看")
        old_CleanStatistic = old_db.select_statistics_CleanStatistic_01(old_db_file)
        new_record_file = os.path.join(new_db_file, "statistics.db")
        new_CleanStatistic = new_db.select_statistics_CleanStatistic_01(new_record_file)
        if old_CleanStatistic == new_CleanStatistic:
            print("对比statistics.db中的CleanStatistic表元素:Passed")
        else:
            print(old_CleanStatistic)
            print(new_CleanStatistic)
            print("对比statistics.db中的CleanStatistic表元素:Failed，请查看")
    else:
        print(old_db_file)
        print("请查看升级前是否有其他的数据库，如果没有问题请查看下数据库中的图数量。")
