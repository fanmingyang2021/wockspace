# encoding: utf-8
import os
import csv
import tarfile
import zipfile

cpu_bases = ['timestamp', 'us', 'sy', 'ni', 'id', 'wa', 'hi', 'si', 'st']
memery_bases = [
    'timestamp', 'mem_total', 'mem_free', 'mem_used', 'mem_cache',
    'swap_total', 'swap_free', 'swap_used', 'swap_avail'
]

performance_csv_title = [
    'amcl', 'app_processor', 'BaseComponent', 'cartographer_no',
    'cartographer_oc', 'cmd_vel_smoothe', 'sensor_preproce', 'launcher',
    'launcher_manager', 'launcher_state_', 'master', 'mbf_costmap_nav',
    'move_base_flex', 'nodelet', 'robot_state_pub', 'roslaunch', 'rosmaster',
    'rosout', 'scrubber_databa', 'scrubber_node', 'ultrasonic',
    'wall_following'
]

performance_csv_title1 = [
    'semantic_mapper', 'marker_detector', 'dynamic_percept', 'semantic_scan_p',
    'xz', 'rosmaster', 'wall_following_', 'recovery_databa',
    'python', 'ultrasonic_cont', 'user_database', 'parking_point_f',
    'nvgpu_channel_p', 'rsyslogd', 'systemd-logind', 'tof_start_maste', 'robot_state_pub',
    'record', 'front_view_dete', 'tof_start_slave', 'proxyd',
    'rrlogd', 'sys_monitor', 'video_recorder', 'app_proxy', 'riot_rr', 'b_main', 'app_processor_n', 'launcher_state_',
    'scrubber_node', 'scrubber_audio', 'scrubber_databa', 'user_manager_no', 'send_msg', 'sensor_preproce',
    'mbf_costmap_nav', 'amcl', 'royale_in_ros_n', 'dm_preview_node', 'lds_lds_ground_obst', 'lds_data_node',
    'tof_ground_obst', 'ultrasonic_bump', 'main_ui', 'beautify_map', 'path_linker_nod', 'workspace_serve',
    'camera_sensor_m', 'rosout', 'roslaunch', 'roscore', 'ti_mmwave_rospk', 'sys_watchdog', 'sys_mem_mon',
    'sys_proc_mgr', 'prxd_cmdsrv', 'top_rotation.sh', 'prxd_filesrv', 'network_manager', 'pc_detectnet',
    'pc_post_fus', 'dialup_4g_modul', 'sys_ntp', 'sys_msg_rcv', 'sys_hb_mgr', 'vdrec_filep', 'app_upload_',
    'app_net_che', 'app_event_l', 'rriot_rr', 'rriot_adapt', 'nmwwanstren', 'nmwifistren', 'nm_boot_up',
    'prxd_hbclt', 'prxd_hbsrv', 'prxd_ipcsrv','cartographer_no','cartographer_oc'
]

start_key_order = [
    'top -', 'Tasks: ', '%Cpu(s):', 'KiB Mem ', 'KiB Swap', 'PID ', '*'
]


class TOP_log_parser():
    def __init__(self, log_path, name):
        self.chunk_size = 100
        # self.log_path = os.path.dirname(log_path)
        self.log_path = log_path
        self.current_time = None
        self.current_base_info = None
        self.process_data = None
        self.stage = 0
        self.next_line_should = start_key_order[0]
        self.name = name
        self.current_cpu_csv_line = []
        self.current_mem_csv_line = []

        self.cpu_csv_chunk = []
        self.mem_csv_chunk = []

        cpu_param_order = {}
        mem_param_order = {}

        for i in range(len(cpu_bases)):
            cpu_param_order[cpu_bases[i]] = i

        for i in range(len(memery_bases)):
            mem_param_order[memery_bases[i]] = i

        for i in range(len(performance_csv_title)):
            cpu_param_order[performance_csv_title[i]] = len(cpu_bases) + i
            mem_param_order[performance_csv_title[i]] = len(memery_bases) + i

        self.cpu_param_order = cpu_param_order
        self.mem_param_order = mem_param_order

        self.cpu_out_path = os.path.join(os.path.dirname(self.log_path), self.name+
                                         "cpu.csv")
        self.mem_out_path = os.path.join(os.path.dirname(self.log_path), self.name+
                                         "mem.csv")

        # 只有新文件才初始化头
        if not os.path.exists(self.cpu_out_path) or os.path.getsize(
                self.cpu_out_path) == 0:
            with open(self.cpu_out_path, 'w',newline="") as cpu_file:
                cpu_csv_writer = csv.writer(cpu_file)
                cpu_csv_writer.writerow(cpu_bases + performance_csv_title)

        if not os.path.exists(self.mem_out_path) or os.path.getsize(
                self.mem_out_path) == 0:
            with open(self.mem_out_path, 'w',newline="") as mem_file:
                mem_csv_writer = csv.writer(mem_file)
                mem_csv_writer.writerow(memery_bases + performance_csv_title)

    def line_init(self):
        self.current_cpu_csv_line = [0] * len(self.cpu_param_order)
        self.current_mem_csv_line = [0] * len(self.mem_param_order)

    def line_finish(self, force_save=False):
        self.stage = 0

        # 写入缓存
        self.cpu_csv_chunk.append(self.current_cpu_csv_line)
        self.mem_csv_chunk.append(self.current_mem_csv_line)

        # print (self.current_cpu_csv_line)
        # print (self.current_mem_csv_line)
        # force_save=True
        # 当前csv行清零
        self.current_cpu_csv_line = []
        self.current_mem_csv_line = []

        # 判断缓存是否该写入csv
        if len(self.current_cpu_csv_line) >= self.chunk_size or force_save:
            with open(self.cpu_out_path,
                      'a+',newline="") as cpu_file, open(self.mem_out_path,
                                              'a+',newline="") as mem_file:
                # cpu_file.writelines(self.cpu_csv_chunk)
                # mem_file.writelines(self.mem_csv_chunk)
                cpu_csv_writer = csv.writer(cpu_file)
                mem_csv_writer = csv.writer(mem_file)

                cpu_csv_writer.writerows(self.cpu_csv_chunk)
                mem_csv_writer.writerows(self.mem_csv_chunk)

                self.cpu_csv_chunk = []
                self.mem_csv_chunk = []

    def parse_line(self, line):

        try:

            # print (self.stage, line[0], 'looking for', self.next_line_should)
            # print (line)
            line = line.strip()

            # 空行, 说明是新的一段
            if line.startswith('\n') or not line:
                if self.stage == 5:
                    # self.stage += 1
                    pass
                elif self.stage == 0:
                    pass
                elif self.stage == 6:
                    self.line_finish()
                    self.stage = 0
                else:
                    pass

            else:
                # 分解line的关键字
                keys = []
                for i in line.split(' '):
                    if i:
                        keys.append(i)

                if len(keys) < 10:
                    return False

                # print (keys)

                # 一段top监控的起始
                if line.startswith('top -'):
                    self.line_init()
                    # 时间
                    self.current_cpu_csv_line[0] = keys[2]
                    self.current_mem_csv_line[0] = keys[2]
                    self.stage = 1

                elif line.startswith('Tasks:'):
                    self.stage = 2

                elif line.startswith('%Cpu(s)'):
                    # ['%Cpu(s):', '27.5', 'us,', '12.0', 'sy,', '0.0', 'ni,', '54.9', 'id,', '0.0', 'wa,', '3.5', 'hi,', '2.2', 'si,', '0.0', 'st']
                    self.current_cpu_csv_line[self.cpu_param_order['us']] = keys[1]
                    self.current_cpu_csv_line[self.cpu_param_order['sy']] = keys[3]
                    self.current_cpu_csv_line[self.cpu_param_order['ni']] = keys[5]
                    self.current_cpu_csv_line[self.cpu_param_order['id']] = keys[7]
                    self.current_cpu_csv_line[self.cpu_param_order['wa']] = keys[9]
                    self.current_cpu_csv_line[
                        self.cpu_param_order['hi']] = keys[11]
                    self.current_cpu_csv_line[
                        self.cpu_param_order['si']] = keys[13]
                    self.current_cpu_csv_line[
                        self.cpu_param_order['st']] = keys[15]

                    self.stage = 3

                elif line.startswith('KiB Mem'):
                    # ['KiB', 'Mem', ':', '4058324', 'total,', '1473932', 'free,', '1591536', 'used,', '992856', 'buff/cache']
                    self.current_mem_csv_line[
                        self.mem_param_order['mem_total']] = keys[3]
                    self.current_mem_csv_line[
                        self.mem_param_order['mem_free']] = keys[5]
                    self.current_mem_csv_line[
                        self.mem_param_order['mem_used']] = keys[7]
                    self.current_mem_csv_line[
                        self.mem_param_order['mem_cache']] = keys[9]
                    self.stage = 4

                elif line.startswith('KiB Swap'):
                    # ['KiB', 'Mem', ':', '4058324', 'total,', '1473932', 'free,', '1591536', 'used,', '992856', 'buff/cache']
                    self.current_mem_csv_line[
                        self.mem_param_order['swap_total']] = keys[2]
                    self.current_mem_csv_line[
                        self.mem_param_order['swap_free']] = keys[4]
                    self.current_mem_csv_line[
                        self.mem_param_order['swap_used']] = keys[6]
                    self.current_mem_csv_line[
                        self.mem_param_order['swap_avail']] = keys[8]
                    self.stage = 5

                elif line.startswith('PID '):
                    self.stage += 1
                    # pass

                elif line.startswith('='):
                    self.stage = 0

                # 详细的进程
                else:
                    if self.stage == 5 or self.stage == 6:
                        process_name = keys[-1]
                        if process_name.endswith('_'):
                            process_name = process_name[:-1]
                        cpu_per = float(keys[8])
                        mem_per = float(keys[9])
                        if process_name in performance_csv_title:
                            if float(mem_per) > 1:
                                self.current_mem_csv_line[
                                    self.mem_param_order[process_name]] += mem_per
                            if float(cpu_per) > 0.2:
                                self.current_cpu_csv_line[
                                    self.cpu_param_order[process_name]] += cpu_per

            self.next_line_should = start_key_order[self.stage]

            return True
        except Exception as e:
            pass

    def finish(self, ):
        self.line_finish(force_save=True)

        return (self.cpu_out_path, self.mem_out_path)

    def do_parse(self):
        self.log_path = os.path.join(self.log_path)
        with open(self.log_path, 'r') as f:
            for line in f:
                self.parse_line(line)

        return self.finish()


def untar_log(log_tar_path, log_to_path):
    tar = tarfile.open(log_tar_path)

    # 遍历压缩内容，找到 top.log
    for i in tar.getnames():
        if i.endswith('top.log'):
            try:
                top_log = tar.extractfile(i)
                while True:
                    chunk_data = top_log.read(1 * 1024 * 1024)
                    if not chunk_data:
                        break
                    # with open("/home/ying/Downloads/try.log","ab+") as f_s:
                    with open(log_to_path, "ab+",newline="") as f_s:
                        f_s.write(chunk_data)

                return log_to_path
            except Exception as e:
                print(e)


# def read_content(log_path, name):
#     t = TOP_log_parser(log_path,name)

# with open(log_path, 'r') as f:
#     for line in f:
#         t.parse_line(line)

# return t.finish()

# return t.do_parse(name)


if __name__ == '__main__':
    # log_tar_path = r'/home/ying/Downloads/B1-17_12_b1-17_2020-11-19-15-51-14.log.tar.gz')
    log_to_path = r"D:\share\aaa"
    aaa = "aaa.txt"
    txt_file = os.path.join(log_to_path, aaa)
    with open(txt_file, "r") as f:
        date_line = f.read()

    top_logfile = os.listdir(os.path.join(log_to_path, date_line))
    for i in top_logfile:
        log_path = os.path.join(log_to_path, date_line, i)
        t = TOP_log_parser(log_path, i.split("_")[0])
        t.do_parse()
