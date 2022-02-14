# coding:utf-8
import binascii
import sqlite3
import os
import new_data, operator


class open_db():

    def __init__(self):

        self.db_name = None
        self.oldmap_name = None
        self.oldpath_name = None
        self.task_len = None
        self.config = {
            "BrushConfigValue": "value_id,description,value",
            "FlowConfigValue": "value_id,description,value",
            "LocationQRCode": "id,name,code_id,confidence,pose,reserved_1,reserved_2",
            "PlanQRCode": "name,code_id,plan_id,cycle_times,config_id,pose,reserved_1,reserved_2",
            "ReserveConfig": "config_id,key,value",
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
        map_nums = 0
        files = [x for x in os.listdir(filename) if os.path.isfile(os.path.join(filename, x))]
        for i in files:
            if len(i) > 32 and i.endswith(".db"):
                map_nums = map_nums + 1
        return map_nums

    def select_Map_version(self, filename):
        oldmap_version = []
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT version FROM Version"
        cursor.execute(sqlshell)
        result = cursor.fetchall()
        for i in result:
            oldmap_version.append(str(i).split("\'")[1])
        conne.close()
        return oldmap_version

    def select_Area1(self, filename):
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT area_id,name,zone_id,length, path_id_data FROM Area"
        cursor.execute(sqlshell)
        result = cursor.fetchall()
        return result

    def select_Area2(self, filename):
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT area_id,name,zone_id,length, path_id_data,type,sub_type,algorithm_params FROM Area"
        cursor.execute(sqlshell)
        result = cursor.fetchall()
        return result

    def select_Map(self, filename):
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
        sqlshell = "SELECT path_id,name,type,sub_type, cover_area,length,data FROM Path "
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

    def select_MaWF(self, filename):
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT area_id,p_idx_count,p_idx,wf_rect_count,wf_zone_id_data FROM ManualWFInfo"
        cursor.execute(sqlshell)
        result = cursor.fetchall()
        return result

    def select_UwbL(self, filename):
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT id,name,residual,forbidden,type,pose,reserved_1,reserved_2 FROM UwbLocationInfo"
        cursor.execute(sqlshell)
        result = cursor.fetchall()
        return result

    def select_Zone1(self, filename):
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT zone_id ,name,path_id,type,config_id FROM Zone  "
        cursor.execute(sqlshell)
        result = cursor.fetchall()
        return result

    def select_Zone2(self, filename):
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT zone_id ,name,path_id,type,config_id,sub_type FROM Zone  "
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

    def select_config(self, filename):
        key_db = self.config.keys()
        result = []
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        for i in key_db:
            sqlshell = "SELECT {} FROM {}".format(self.config[i], i)
            cursor.execute(sqlshell)
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
    local = os.getcwd()
    data = open_db()
    old_files = []
    new_files = []
    db_dir = [x for x in os.listdir(local) if os.path.isdir(x)]
    for i in db_dir:
        if "升级前" in i:
            old_db = os.path.join(local, i)
            for root, dirs, files in os.walk(old_db):
                for i in files:
                    if i.endswith(".db"):
                        root1 = root
                        old_files.append(os.path.join(root, i))
        if "升级后" in i:
            new_db = os.path.join(local, i)
            for root, dirs, files in os.walk(new_db):
                for i in files:
                    if i.endswith(".db"):
                        root2 = root
                        new_files.append(os.path.join(root, i))
    old_num = data.select_Map_nums(root1)
    new_num = data.select_Map_nums(root2)
    if old_num == new_num:
        for i in old_files:
            for j in new_files:
                if i.split("\\")[-1] == j.split("\\")[-1] and len(i.split("\\")[-1]) > 16:
                    old_vs = data.select_Map_version(i)
                    new_map = data.select_Map(j)
                    old_map = data.select_Map(i)
                    if operator.eq(new_map, old_map):
                        print("对比地图{}中的Map表12个元素，共{}个数据".format(i, len(old_map) * 12) + "Passed")
                    else:
                        print(j + "Map表Failed")
                    new_path = data.select_Path(j)
                    old_path = data.select_Path(i)

                    if operator.eq(old_path, new_path):
                        print("对比地图{}中的Path表4个元素，共{}个数据".format(i, len(old_path) * 4) + "Passed")
                    else:
                        print(j + "Path表Failed")
                    new_plan = data.select_Plan(j)
                    old_plan = data.select_Plan(i)
                    if operator.eq(new_plan, old_plan):
                        print("对比地图{}中的Plan表7个元素，共{}个数据".format(i, len(old_plan) * 7) + "Passed")
                    else:
                        print(j + "Plan表Failed")
                    new_task = data.select_Task(j)
                    old_task = data.select_Task(i)
                    if operator.eq(new_task, old_task):
                        print("对比地图{}中的Task表4个元素，共{}个数据".format(i, len(old_task) * 4) + "Passed")
                    else:
                        print(j + "Task表Failed")
                    if old_vs == ['rr.3.0']:
                        new_area = data.select_Area1(j)
                        old_area = data.select_Area1(i)
                        if operator.eq(new_area, old_area):
                            print("对比地图{}中的Area表6个元素，共{}个数据".format(i, len(old_area) * 6) + "Passed")
                        else:
                            print(j + "Area 表Failed")
                        new_zone = data.select_Zone1(j)
                        old_zone = data.select_Zone1(i)
                        if operator.eq(new_zone, old_zone):
                            print("对比地图{}中的Zone表6个元素，共{}个数据".format(i, len(old_path) * 6) + "Passed")
                        else:
                            print(j + "Zone表Failed")
                    elif old_vs == ['rr.3.1']:
                        new_area = data.select_Area2(j)
                        old_area = data.select_Area2(i)
                        if operator.eq(new_area, old_area):
                            print("对比地图{}中的Area表6个元素，共{}个数据".format(i, len(old_area) * 6) + "Passed")
                        else:
                            print(j + "Area 表Failed")
                        new_zone = data.select_Zone2(j)
                        old_zone = data.select_Zone2(i)
                        if operator.eq(new_zone, old_zone):
                            print("对比地图{}中的Zone表6个元素，共{}个数据".format(i, len(old_path) * 6) + "Passed")
                        else:
                            print(j + "Zone表Failed")
                        new_MaWF = data.select_MaWF(j)
                        old_MaWF = data.select_MaWF(i)
                        if operator.eq(new_zone, old_zone):
                            print("对比地图{}中的MaWF表6个元素，共{}个数据".format(i, len(old_MaWF) * 5) + "Passed")
                        else:
                            print(j + "MaWF表Failed")
                        new_UwbL = data.select_UwbL(j)
                        old_UwbL = data.select_UwbL(i)
                        if operator.eq(new_zone, old_zone):
                            print("对比地图{}中的UwbL表6个元素，共{}个数据".format(i, len(old_UwbL) * 6) + "Passed")
                        else:
                            print(j + "UwbL表Failed")
                elif i.split("\\")[-1] == j.split("\\")[-1] and "config" in i:
                    old_config = data.select_config(i)
                    new_config = data.select_config(j)
                    for x in range(9):
                        if operator.eq(old_config[x], new_config[x]):
                            print("对比config.db中的{}表的元素:Passed".format(list(data.config.keys())[x]))
                        else:
                            print(j + list(data.config.keys())[x] + "Failed")
                elif i.split("\\")[-1] == j.split("\\")[-1] and "statistics" in i:
                    old_record = data.select_statistics_record_01(i)
                    new_record = data.select_statistics_record_01(j)
                    if operator.eq(old_record, new_record):
                        print("对比statistics.db中的record表的元素:Passed")
                    else:
                        print(j + list(data.config.keys())[i] + "Failed")
                elif i.split("\\")[-1] == j.split("\\")[-1] and "user" in i:
                    old_user = data.select_user(i)
                    new_user = data.select_user(j)
                    if operator.eq(old_record, new_record):
                        print("对比user.db中的user表的元素:Passed")
                    else:
                        print(j + "对比user.db中的user表" + "Failed")
    else:

        print("waring!!文件中的地图数量不一样,请检查。")
