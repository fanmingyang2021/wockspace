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

    def select_Area2(self, filename):
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT area_id,name,zone_id,length, path_id_data,type,sub_type,algorithm_params FROM Area"
        cursor.execute(sqlshell)
        result = cursor.fetchall()
        return result

    def select_FollowPath(self, filename):
        self.oldpath_name = []
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT task_id,area_id FROM FollowPath "
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

    def select_Map(self, filename):
        self.oldpath_name = []
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT  resolution,width,height,left," \
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

    def select_PathToZone(self, filename):
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT path_id ,zone_id,type FROM PathToZone"
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


    def select_Task(self, filename):
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT task_id ,name,config_id ,type FROM Task"
        cursor.execute(sqlshell)
        result = cursor.fetchall()
        return result


    def select_UwbL(self, filename):
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT id,name,residual,forbidden_dis,type,pose,reserved_1,reserved_2 FROM UwbLocationInfo"
        cursor.execute(sqlshell)
        result = cursor.fetchall()
        return result


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

    def VersionPath(self, filename):
        oldmap_version = []
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT version_id,version FROM VersionPath"
        cursor.execute(sqlshell)
        result = cursor.fetchall()
        for i in result:
            oldmap_version.append(str(i).split("\'")[1])
        conne.close()
        return oldmap_version



    def select_Zone2(self, filename):
        conne = sqlite3.connect(filename)
        cursor = conne.cursor()
        sqlshell = "SELECT zone_id ,name,path_id,type,config_id,sub_type FROM Zone  "
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
        if "?????????" in i:
            old_db = os.path.join(local, i)
            for root, dirs, files in os.walk(old_db):
                for i in files:
                    if i.endswith(".db"):
                        root1 = root
                        old_files.append(os.path.join(root, i))
        if "?????????" in i:
            new_db = os.path.join(local, i)
            for root, dirs, files in os.walk(new_db):
                for i in files:
                    if i.endswith(".db"):
                        root2 = root
                        new_files.append(os.path.join(root, i))
    old_num = data.select_Map_nums(root1)
    new_num = data.select_Map_nums(root2)
    print(old_num,new_num)
    if old_num == new_num:

        for i in old_files:
            print(i)
            for j in new_files:

                    new_map = data.select_Map(j)
                    old_map = data.select_Map(i)
                    if operator.eq(new_map, old_map):
                        print("????????????{}??????Map???12???????????????{}?????????".format(i, len(old_map) * 12) + "Passed")
                    else:
                        print(j + "Map???Failed")
                    new_path = data.select_Path(j)
                    old_path = data.select_Path(i)

                    if operator.eq(old_path, new_path):
                        print("????????????{}??????Path???4???????????????{}?????????".format(i, len(old_path) * 4) + "Passed")
                    else:
                        print(j + "Path???Failed")
                    new_plan = data.select_Plan(j)
                    old_plan = data.select_Plan(i)
                    if operator.eq(new_plan, old_plan):
                        print("????????????{}??????Plan???7???????????????{}?????????".format(i, len(old_plan) * 7) + "Passed")
                    else:
                        print(j + "Plan???Failed")
                    new_task = data.select_Task(j)
                    old_task = data.select_Task(i)
                    if operator.eq(new_task, old_task):
                        print("????????????{}??????Task???4???????????????{}?????????".format(i, len(old_task) * 4) + "Passed")
                    else:
                        print(j + "Task???Failed")

                    new_area = data.select_Area2(j)
                    old_area = data.select_Area2(i)
                    if operator.eq(new_area, old_area):
                        print("????????????{}??????Area???6???????????????{}?????????".format(i, len(old_area) * 6) + "Passed")
                    else:
                        print(j + "Area ???Failed")
                    new_zone = data.select_Zone2(j)
                    old_zone = data.select_Zone2(i)
                    if operator.eq(new_zone, old_zone):
                        print("????????????{}??????Zone???6???????????????{}?????????".format(i, len(old_path) * 6) + "Passed")
                    else:
                        print(j + "Zone???Failed")
                    new_MaWF = data.select_MaWF(j)
                    old_MaWF = data.select_MaWF(i)
                    if operator.eq(new_zone, old_zone):
                        print("????????????{}??????MaWF???6???????????????{}?????????".format(i, len(old_MaWF) * 5) + "Passed")
                    else:
                        print(j + "MaWF???Failed")
                    new_UwbL = data.select_UwbL(j)
                    old_UwbL = data.select_UwbL(i)
                    if operator.eq(new_zone, old_zone):
                        print("????????????{}??????UwbL???6???????????????{}?????????".format(i, len(old_UwbL) * 6) + "Passed")
                    else:
                        print(j + "UwbL???Failed")
    else:

        print("waring!!?????????????????????????????????,????????????")
