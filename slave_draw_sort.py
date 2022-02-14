from operator import itemgetter # 导入定位的头方便定位按照哪里排序
import csv
import os
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as md
import sys
import re
import time

def cpu_len_row(cpu_path):
    csv_file = os.path.join(cpu_path, "cpu.csv")
    op = open(csv_file)
    rd = csv.reader(op)

    for row in rd:
        list = []
        list.append(row)
    length = len(row)
    return length

def mem_len_row(cpu_path):
    csv_file = os.path.join(cpu_path, "mem.csv")
    op = open(csv_file)
    rd = csv.reader(op)

    for row in rd:
        list = []
        list.append(row)
    length = len(row)
    return length

def slave_cpu_reslut_sort_max(cpu_path,node):
    datas = []  # 开个列表存放排序过的数据
    with open(node+'_cpu_result.csv', 'r') as f:
        table = []
        for line in f:
            if 'max' in line:
                continue
            else:
                col = line.split(',')
                col[2] = float(col[2])
                col[3] = col[3].strip("\n")
                table.append(col)
        table_sorted = sorted(table, key=itemgetter(2), reverse=True)
        for row in table_sorted:
            datas.append(row)
    f.close()

    with open(node+"_cpu_result_sort_max.csv", "w+", newline='') as csvfile:
        writer = csv.writer(csvfile)
        for data in datas:
            writer.writerow(data)
    csvfile.close()
    df_diff_cpu = pd.read_csv( node+"_cpu_result_sort_max.csv", error_bad_lines=False)
    cpu_columns = df_diff_cpu.columns
    first = cpu_columns[0]
    im = df_diff_cpu[first].values
    return first, im[0], im[1], im[2], im[3]

def slave_cpu_reslut_sort_average(cpu_path,node):
    datas = []  # 开个列表存放排序过的数据
    with open(node+"_cpu_result.csv", 'r') as f:
        table = []
        for line in f:
            if 'max' in line:
                continue
            else:
                col = line.split(',')
                col[3] = float(col[3])
                col[2] = col[2].strip("\n")
                table.append(col)
        table_sorted = sorted(table, key=itemgetter(3), reverse=True)
        for row in table_sorted:
            datas.append(row)
    f.close()

    with open(node+"_cpu_result_sort_average.csv", "w+", newline='') as csvfile:
        writer = csv.writer(csvfile)
        for data in datas:
            writer.writerow(data)
    csvfile.close()
    df_diff_cpu = pd.read_csv( node+"_cpu_result_sort_average.csv", error_bad_lines=False)
    cpu_columns = df_diff_cpu.columns
    y = cpu_columns[0]
    im = df_diff_cpu[y].values
    return y, im[0], im[1], im[2], im[3]

def slave_mem_result_sort_max(mem_path, node):
    datas = []  # 开个列表存放排序过的数据
    with open(node+'_mem_result.csv', 'r') as f:
        table = []
        for line in f:
            if 'max' in line:
                continue
            else:
                col = line.split(',')
                col[2] = float(col[2])
                col[3] = col[3].strip("\n")
                table.append(col)
        table_sorted = sorted(table, key=itemgetter(2), reverse=True)
        for row in table_sorted:
            datas.append(row)
    f.close()

    with open(node+"_mem_result_sort_max.csv", "w+", newline='') as csvfile:
        writer = csv.writer(csvfile)
        for data in datas:
            writer.writerow(data)
    csvfile.close()
    df_diff_mem = pd.read_csv( node+"_mem_result_sort_max.csv", error_bad_lines=False)
    mem_columns = df_diff_mem.columns
    first = mem_columns[0]
    im = df_diff_mem[first].values
    return first, im[0], im[1], im[2], im[3]

def slave_mem_result_sort_average(mem_path, node):
    datas = []  # 开个列表存放排序过的数据
    with open(node+'_mem_result.csv', 'r') as f:
        table = []
        for line in f:
            if 'max' in line:
                continue
            else:
                col = line.split(',')
                col[3] = float(col[3])
                col[2] = col[2].strip("\n")
                table.append(col)
        table_sorted = sorted(table, key=itemgetter(3), reverse=True)
        for row in table_sorted:
            datas.append(row)
    f.close()

    with open(node+"_mem_result_sort_average.csv", "w+", newline='') as csvfile:
        writer = csv.writer(csvfile)
        for data in datas:
            writer.writerow(data)
    csvfile.close()
    df_diff_mem = pd.read_csv( node+"_mem_result_sort_average.csv", error_bad_lines=False)
    mem_columns = df_diff_mem.columns
    y = mem_columns[0]
    im = df_diff_mem[y].values
    return y, im[0], im[1], im[2], im[3]

def slave_cpu_id(cpu_path, node):
    diff_path = os.path.dirname(cpu_path)
    df_diff_cpu = pd.read_csv(os.path.join(cpu_path, "cpu.csv"), error_bad_lines=False)
    cpu_columns = df_diff_cpu.columns
    plt.cla()
    csvfile = open(node + "_cpu_idle_result.csv", "w")
    writer = csv.writer(csvfile)
    writer.writerow(["param", "min", "max", "average"])
    for i in range(1, cpu_len_row(cpu_path)):
        x = cpu_columns[0]
        y = cpu_columns[i]
        a = np.isnan(df_diff_cpu[y])
        if False in a:
            if y == 'id' or y == 'sy' or y == 'us':
                ax = plt.gca()
                xfmt = md.DateFormatter('%H:%M')
                ax.xaxis.set_major_formatter(xfmt)
                plt.plot(pd.to_datetime(df_diff_cpu[x], format="%H:%M:%S"), df_diff_cpu[y], "-", label=y)
                plt.tight_layout()
                plt.grid()
                plt.legend()
                writer.writerow([cpu_columns[i],
                                 df_diff_cpu[y].min(),
                                 df_diff_cpu[y].max(),
                                 df_diff_cpu[y].sum() / df_diff_cpu[y].count()])
            else:
                continue
        else:
            continue


    plt.title("自动任务时{}上CPU概况".format(node.split("\\")[-1]))
    plt.rcParams['font.sans-serif'] = ['Simhei']
    plt.xlabel("")
    plt.ylabel("")
    plt.axis("auto")
    plt.savefig(os.path.join(cpu_path, "cpu-id-sy-us.png"), dpi=500)
    print("FILE: {} is saved!".format(diff_path + "cpu-id-sy-us.png"))
    csvfile.close()
    df_res = pd.read_csv(node + "_cpu_idle_result.csv")
    data = df_res.sort_values(by="average", ascending=False)
    data.to_csv(node + "_cpu_idle_result.csv", mode='w', index=False)

def slave_cpu(cpu_path, node):
    diff_path = os.path.dirname(cpu_path)
    print(cpu_path)
    df_diff_cpu = pd.read_csv(os.path.join(cpu_path, "cpu.csv"), error_bad_lines=False)
    cpu_columns = df_diff_cpu.columns
    plt.cla()
    csvfile = open(node + "_cpu_result.csv", "w")
    writer = csv.writer(csvfile)
    writer.writerow(["proc_name",  "min", "max", "average"])
    for i in range(1, cpu_len_row(cpu_path)):
        x = cpu_columns[0]
        y = cpu_columns[i]
        a = np.isnan(df_diff_cpu[y])
        im = df_diff_cpu[y].values
        if np.all(im == 0):
            continue
        else:
            if False in a.values:
                if y == 'id' or y == 'sy' or y == 'us' or y == 'ni' or y == 'wa' or y == 'hi' or y == 'si' or y == 'st':
                    continue
                else:
                    ax = plt.gca()
                    xfmt = md.DateFormatter('%H:%M')
                    ax.xaxis.set_major_formatter(xfmt)
                    plt.plot(pd.to_datetime(df_diff_cpu[x], format="%H:%M:%S"), df_diff_cpu[y], "-", label=y)
                    plt.tight_layout()
                    plt.grid()
                    plt.legend(bbox_to_anchor=(0, -0.98, 1, 0.2), loc="lower left",
                               mode="expand", borderaxespad=0, ncol=4, fontsize='small')
                    writer.writerow([cpu_columns[i],
                                     df_diff_cpu[y].min(),
                                     df_diff_cpu[y].max(),
                                     df_diff_cpu[y].sum() / df_diff_cpu[y].count()])
            else:
                continue

    plt.title("自动任务时{}各CPU使用情况".format(node.split("\\")[-1]))
    plt.rcParams['font.sans-serif'] = ['Simhei']
    plt.xlabel("")
    plt.ylabel("")
    plt.gcf().subplots_adjust(left=0.05, top=0.91, bottom=0.45)
    plt.axis("auto")
    plt.savefig(os.path.join(cpu_path, "cpu.png"), dpi=300)
    print("FILE: {} is saved!".format(diff_path + "cpu.png"))
    csvfile.close()
    df_res = pd.read_csv(node + "_cpu_result.csv")
    data = df_res.sort_values(by="average", ascending=False)
    data.to_csv(node + "_cpu_result.csv", mode='w', index=False)

def slave_mem_free(mem_path, node):
    diff_path = os.path.dirname(mem_path)
    print(mem_path)
    df_diff_mem = pd.read_csv(os.path.join(mem_path, "mem.csv"), error_bad_lines=False)
    mem_columns = df_diff_mem.columns
    plt.cla()
    csvfile = open(node + "_mem_result.csv", "w")
    writer = csv.writer(csvfile)
    writer.writerow(["proc_name", "min", "max", "average"])
    for i in range(1, mem_len_row(mem_path)):

        x = mem_columns[0]
        y = mem_columns[i]
        a = np.isnan(df_diff_mem[y])
        im = df_diff_mem[y].values
        if np.all(im == 0):
            continue
        else:
            if False in a.values:
                if y == 'mem_total' or y == 'mem_free' or y == 'mem_used' or y == 'mem_cache' or y == 'swap_total' or y == 'swap_free' or y == 'swap_used' or y == 'swap_avail':
                    continue
                else:
                    ax = plt.gca()
                    xfmt = md.DateFormatter('%H:%M')
                    ax.xaxis.set_major_formatter(xfmt)
                    plt.plot(pd.to_datetime(df_diff_mem[x], format="%H:%M:%S"), df_diff_mem[y], "-", label=y)
                    plt.tight_layout()
                    plt.grid()
                    plt.legend(bbox_to_anchor=(0, -0.98, 1, 0.2), loc="lower left",
                               mode="expand", borderaxespad=0, ncol=4, fontsize='small')
                    writer.writerow([mem_columns[i],
                                     df_diff_mem[y].min(),
                                     df_diff_mem[y].max(),
                                     df_diff_mem[y].sum() / df_diff_mem[y].count()])
            else:
                continue

    plt.title("自动任务时{}各mem使用情况".format(node.split("\\")[-1]))
    plt.rcParams['font.sans-serif'] = ['Simhei']
    plt.xlabel("")
    plt.ylabel("")
    plt.gcf().subplots_adjust(left=0.05, top=0.91, bottom=0.45)
    plt.axis("auto")
    plt.savefig(os.path.join(mem_path, "mem.png"), dpi=300)
    print("FILE: {} is saved!".format(diff_path + "mem.png"))
    csvfile.close()
    df_res = pd.read_csv(node + "_mem_result.csv")
    data = df_res.sort_values(by="average", ascending=False)
    data.to_csv(node + "_mem_result.csv", mode='w', index=False)

def slave_mem(mem_path, node):
    diff_path = os.path.dirname(mem_path)
    df_diff_mem = pd.read_csv(os.path.join(mem_path, "mem.csv"), error_bad_lines=False)
    mem_columns = df_diff_mem.columns
    plt.cla()
    csvfile = open(node + "_mem_idle_result.csv", "w")
    writer = csv.writer(csvfile)
    writer.writerow(["param", "min", "max", "average"])
    for i in range(1, mem_len_row(mem_path)):
        x = mem_columns[0]
        y = mem_columns[i]
        a = np.isnan(df_diff_mem[y])
        if False in a:
            if y == 'mem_total' or y == 'mem_free' or y == 'mem_used':
                ax = plt.gca()
                xfmt = md.DateFormatter('%H:%M')
                ax.xaxis.set_major_formatter(xfmt)
                plt.plot(pd.to_datetime(df_diff_mem[x], format="%H:%M:%S"), df_diff_mem[y], "-", label=y)
                plt.tight_layout()
                plt.grid()
                plt.legend()
                writer.writerow([mem_columns[i],
                                 df_diff_mem[y].min(),
                                 df_diff_mem[y].max(),
                                 df_diff_mem[y].sum() / df_diff_mem[y].count()])
            else:
                continue
        else:
            continue


    plt.title("自动任务时{}上MEM概况".format(node.split("\\")[-1]))
    plt.rcParams['font.sans-serif'] = ['Simhei']
    plt.xlabel("")
    plt.ylabel("")
    plt.axis("auto")
    plt.savefig(os.path.join(mem_path, "mem_free.png"), dpi=500)
    print("FILE: {} is saved!".format(diff_path + "mem_free.png"))
    csvfile.close()
    df_res = pd.read_csv(node + "_mem_idle_result.csv")
    data = df_res.sort_values(by="average", ascending=False)
    data.to_csv(node + "_mem_idle_result.csv", mode='w', index=False)

def slave_cpu_average_top(cpu_path, node):
    diff_path = os.path.dirname(cpu_path)
    df_diff_cpu = pd.read_csv(os.path.join(cpu_path, "cpu.csv"), error_bad_lines=False)
    cpu_columns = df_diff_cpu.columns
    plt.cla()
    print(cpu_path)
    for i in range(1, cpu_len_row(cpu_path)):
        x = cpu_columns[0]
        y = cpu_columns[i]
        a = np.isnan(df_diff_cpu[y])
        first = slave_cpu_reslut_sort_average(cpu_path, node)
        if False in a:
            if y == first[0] or y == first[1] or y == first[2] or y == first[3] or y == first[4]:
                ax = plt.gca()
                xfmt = md.DateFormatter('%H:%M')
                ax.xaxis.set_major_formatter(xfmt)
                plt.plot(pd.to_datetime(df_diff_cpu[x], format="%H:%M:%S"), df_diff_cpu[y], "-", label=y)
                plt.tight_layout()
                plt.grid()
                plt.legend()
            else:
                continue
        else:
            continue

    plt.title("{}上CPU均值TOP5".format(node))
    plt.rcParams['font.sans-serif'] = ['Simhei']
    plt.xlabel("")
    plt.ylabel("")
    plt.axis("auto")
    plt.gcf().subplots_adjust(left=0.05, top=0.9, bottom=0.2, right=1.0)
    plt.savefig(os.path.join(cpu_path, "slave_cpu_average_top5.png"), dpi=500)
    print("FILE: {} is saved!".format(diff_path + "slave_cpu_average_top5.png"))

def slave_cpu_max_top(cpu_path, node):
    diff_path = os.path.dirname(cpu_path)
    df_diff_cpu = pd.read_csv(os.path.join(cpu_path, "cpu.csv"), error_bad_lines=False)
    cpu_columns = df_diff_cpu.columns
    plt.cla()
    for i in range(1, cpu_len_row(cpu_path)):
        x = cpu_columns[0]
        y = cpu_columns[i]
        a = np.isnan(df_diff_cpu[y])
        first = slave_cpu_reslut_sort_max(cpu_path, node)
        if False in a:
            if y == first[0] or y == first[1] or y == first[2] or y == first[3] or y == first[4]:
                ax = plt.gca()
                xfmt = md.DateFormatter('%H:%M')
                ax.xaxis.set_major_formatter(xfmt)
                plt.plot(pd.to_datetime(df_diff_cpu[x], format="%H:%M:%S"), df_diff_cpu[y], "-", label=y)
                plt.tight_layout()
                plt.grid()
                plt.legend()
            else:
                continue
        else:
            continue

    plt.title("{}上CPU最大值TOP5".format(node))
    plt.rcParams['font.sans-serif'] = ['Simhei']
    plt.xlabel("")
    plt.ylabel("")
    plt.axis("auto")
    plt.gcf().subplots_adjust(left=0.05, top=0.9, bottom=0.2, right=1.0)
    plt.savefig(os.path.join(cpu_path, "slave_cpu_max_top5.png"), dpi=500)
    print("FILE: {} is saved!".format(diff_path + "slave_cpu_max_top5.png"))

def slave_mem_average_top(mem_path, node):
    diff_path = os.path.dirname(mem_path)
    df_diff_mem = pd.read_csv(os.path.join(mem_path, "mem.csv"), error_bad_lines=False)
    mem_columns = df_diff_mem.columns
    plt.cla()
    for i in range(1, mem_len_row(mem_path)):
        x = mem_columns[0]
        y = mem_columns[i]
        a = np.isnan(df_diff_mem[y])
        first = slave_mem_result_sort_average(mem_path, node)
        if False in a:
            if y == first[0] or y == first[1] or y == first[2] or y == first[3] or y == first[4]:
                ax = plt.gca()
                xfmt = md.DateFormatter('%H:%M')
                ax.xaxis.set_major_formatter(xfmt)
                plt.plot(pd.to_datetime(df_diff_mem[x], format="%H:%M:%S"), df_diff_mem[y], "-", label=y)
                plt.tight_layout()
                plt.grid()
                plt.legend()
            else:
                continue
        else:
            continue

    plt.title("{}上mem均值TOP5".format(node))
    plt.rcParams['font.sans-serif'] = ['Simhei']
    plt.xlabel("")
    plt.ylabel("")
    plt.axis("auto")
    plt.gcf().subplots_adjust(left=0.05, top=0.9, bottom=0.2, right=1.0)
    plt.savefig(os.path.join(mem_path, "slave_mem_average_top5.png"), dpi=500)
    print("FILE: {} is saved!".format(diff_path + "slave_mem_average_top5.png"))

def slave_mem_max_top(mem_path, node):
    diff_path = os.path.dirname(mem_path)
    df_diff_mem = pd.read_csv(os.path.join(mem_path, "mem.csv"), error_bad_lines=False)
    mem_columns = df_diff_mem.columns
    plt.cla()
    for i in range(1, mem_len_row(mem_path)):
        x = mem_columns[0]
        y = mem_columns[i]
        a = np.isnan(df_diff_mem[y])
        first = slave_mem_result_sort_max(mem_path, node)
        if False in a:
            if y == first[0] or y == first[1] or y == first[2] or y == first[3] or y == first[4]:
                ax = plt.gca()
                xfmt = md.DateFormatter('%H:%M')
                ax.xaxis.set_major_formatter(xfmt)
                plt.plot(pd.to_datetime(df_diff_mem[x], format="%H:%M:%S"), df_diff_mem[y], "-", label=y)
                plt.tight_layout()
                plt.grid()
                plt.legend()
            else:
                continue
        else:
            continue

    plt.title("{}上mem最大值TOP5".format(node))
    plt.rcParams['font.sans-serif'] = ['Simhei']
    plt.xlabel("")
    plt.ylabel("")
    plt.axis("auto")
    plt.gcf().subplots_adjust(left=0.05, top=0.9, bottom=0.2, right=1.0)
    plt.savefig(os.path.join(mem_path, "slave_mem_max_top5.png"), dpi=500)
    print("FILE: {} is saved!".format(diff_path + "slave_mem_max_top5.png"))
def copy_csv():
    log_to_path = r"D:\share\aaa"
    aaa = "aaa.txt"
    master_dir = "D:\python_demo\cpu_top5\perfTools\python\master"
    slave_dir = "D:\python_demo\cpu_top5\perfTools\python\slave"
    txt_file = os.path.join(log_to_path, aaa)
    with open(txt_file, "r") as f:
        date_line = f.read()

    top_logfile = os.listdir(os.path.join(log_to_path, date_line))

    for s in top_logfile:
        print(s)
        if s.endswith(".csv") and "master" in s:
            log_csv = os.path.join(log_to_path, date_line, s)
            if "mem" in s:
                master_csv = os.path.join(master_dir, "mem.csv")
                if os.path.exists(master_csv):
                    os.remove(master_csv)

                cmd = "copy {}  {}".format(log_csv, master_csv)
                os.system(cmd)
                print(1, log_csv)
            if "cpu" in s:
                master_csv = os.path.join(master_dir, "cpu.csv")
                if os.path.exists(master_csv):
                    os.remove(master_csv)
                cmd = "copy {}  {}".format(log_csv, master_csv)
                os.system(cmd)
        if s.endswith(".csv") and "slave" in s:
            log_csv = os.path.join(log_to_path, date_line, s)
            if "cpu" in s:
                slave_csv = os.path.join(slave_dir, "cpu.csv")
                if os.path.exists(slave_csv):
                    os.remove(slave_csv)
                cmd = "copy {}  {}".format(log_csv, slave_csv)
                os.system(cmd)
            if "mem" in s:
                slave_csv = os.path.join(slave_dir, "mem.csv")
                if os.path.exists(slave_csv):
                    os.remove(slave_csv)
                cmd = "copy {}  {}".format(log_csv, slave_csv)
                os.system(cmd)
    cmd="pause"
    os.system(cmd)
if __name__ == '__main__':
    copy_csv()
    cpu_dir = "D:\python_demo\cpu_top5\perfTools\python\\"
    draw_dir = [x for x in os.listdir(cpu_dir) if os.path.isdir(x)]
    print(draw_dir)
    for i in draw_dir:

        cpu2_dir = os.path.join(cpu_dir, i)
        draw_file1 = os.path.join(cpu_dir, i)
        print(draw_file1, cpu2_dir)
        cpulen = cpu_len_row(draw_file1)
        mem_len = mem_len_row(draw_file1)
        slave_cpu_id(draw_file1, draw_file1)
        slave_cpu(draw_file1, draw_file1)
        slave_mem_free(draw_file1, draw_file1)
        slave_mem(draw_file1, draw_file1)
        slave_cpu_average_top(draw_file1,i)
        slave_cpu_max_top(draw_file1,i)
        slave_cpu_reslut_sort_max(draw_file1,i)
        slave_cpu_reslut_sort_average(draw_file1,i)
        slave_mem_result_sort_max(draw_file1,i)
        slave_mem_result_sort_average(draw_file1,i)
        slave_mem_average_top(draw_file1,i)
        slave_mem_max_top(draw_file1,i)