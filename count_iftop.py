# encoding: utf-8
import re
import os
from analysis_scripts.common import parser_base

class count_iftop(parser_base.SingleFolderParserBase):
    def __init__(self, data_folder_path='', out_folder_path='', script_name=''):
        script_name = "count_iftop"
        super().__init__(data_folder_path, out_folder_path, script_name)

    def do_parse(self):
        local_dir = os.path.join(self.data_folder_path, 'unziped')
        return self.count_iftop(local_dir)

    def merge_log(self, log_path):
        log_path = os.path.join(self.data_folder_path, 'unziped')
        iftop_files = []
        files = []
        for x in os.listdir(log_path):
            if os.path.isfile(os.path.join(log_path, x)) and "iftop" in x:
                files.append(x)
        for i in files:
            iftop_files.append(os.path.join(log_path, i))
        iftop_files.sort()
        return iftop_files

    def count_iftop(self, log_dir):
        result2 = 0
        result1 = 0.0
        for i in self.merge_log(log_dir):
            file_path = i
            sum = 0
            for line in open(file_path, encoding='utf8', errors='ignore'):
                result = re.match("Cumulative.+\s+(\w+\.\w+)KB", line)
                resultM = re.match("Cumulative.+\s+(\w+\.\w+)MB", line)
                resultB = re.match("Cumulative.+\s+(\w+\.\w+)B", line)
                # print(resultM)
                if result:
                    sum = float(result.group(1)) + sum
                    result1 = float(result.group(1)) + result1
                    result2 = float("%.2f" % result1)
                elif resultM:
                    # print(111111111)
                    sum = float(resultM.group(1)) * 1024 + sum
                    result1 = float(resultM.group(1)) * 1024 + result1
                    result2 = float("%.2f" % result1)
                elif resultB:
                    # print(111111111)
                    sum = float(resultM.group(1)) / 1024 + sum
                    result1 = float(resultM.group(1)) / 1024 + result1
                    result2 = float("%.2f" % result1)
            # try:
            #     with open(os.path.join(log_dir, "result.txt"), "a") as f:
            #         f.write(file_path + "{:<30s}使用流量数据为".format("") + str(float("%.2f" % sum)) + "KB" + "\n")
            # except TypeError:
            #     pass
        self.add_attention(timestamp_s=23333, section='application', info="count iftop", level=2,
                           mentor='shl', colour='#ff0000', details=str(result2)+ "KB")
        # print(222222)
        # with open(os.path.join(log_dir, "result.txt"), "a") as f:
        #     f.write((log_dir) + "{:>50}一共使用流量数据为".format("") + str(result2) + "KB" + "\n")


if __name__ == '__main__':
    a = count_iftop(r"E:\share\log\B2-32\20211203\log\4067.20211204004446.slave",
                    r"E:\share\log\B2-32\20211203\log\4067.20211204004446.slave")
    a.run()
