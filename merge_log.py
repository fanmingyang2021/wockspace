import os, re, lzma, shutil

def natural_sort(list):
	convert = lambda text: int(text) if text.isdigit() else text.lower()
	alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
	return sorted(list, key=alphanum_key)

def merge_log(log_node_path):
	if(not os.path.isdir(log_node_path)):
		return
	result_file = open(log_node_path + '.log', 'w', encoding='utf8')
	files = natural_sort(os.listdir(log_node_path))
	if(not files):
		result_file.close()
        
		shutil.rmtree(log_node_path)
		return
	if(1 == len(files)):
		file_path = os.path.join(log_node_path, files[0])
		for line in open(file_path, encoding='utf8', errors='ignore'):
			result_file.writelines(line)
		result_file.close()
		shutil.rmtree(log_node_path)
		return
	folder_name = os.path.basename(os.path.normpath(log_node_path))
	if('top' == folder_name or 'topH' == folder_name or 'iftop' == folder_name):
		for filename in files:
			file_path = os.path.join(log_node_path, filename)
			for line in open(file_path, encoding='utf8', errors='ignore'):
				result_file.writelines(line)
		result_file.close()
		shutil.rmtree(log_node_path)
		return
	for filename in files[:]:
		file_path = os.path.join(log_node_path, filename)
		fields = filename.split('.')
		if(len(fields) < 3):
			files.remove(filename)
			continue
		if(14 == len(fields[len(fields) - 1])):
			for line in open(file_path, encoding='utf8', errors='ignore'):
				result_file.writelines(line)
			files.remove(filename)
	for filename in files[:]:
		file_path = os.path.join(log_node_path, filename)
		fields = filename.split('.')
		if(14 == len(fields[1])):
			for line in open(file_path, encoding='utf8', errors='ignore'):
				result_file.writelines(line)
			files.remove(filename)
			continue
		if('log' != fields[1] and 'tmp' != fields[1]):
			files.remove(filename)
	last_index = -1
	split_pos = 0
	for i in range(len(files)):
		fields = files[i].split('.')
		if(not fields[2].isdigit()):
			continue
		index = int(fields[2])
		if(last_index != -1 and index != last_index + 1):
			split_pos = i
			break
		last_index = index
	new_order_files = []
	new_order_files.extend(files[split_pos:])
	new_order_files.extend(files[0:split_pos])
	for filename in new_order_files:
		file_path = os.path.join(log_node_path, filename)
		for line in open(file_path, encoding='utf8', errors='ignore'):
			result_file.writelines(line)
	result_file.close()
	shutil.rmtree(log_node_path)

def scan_log_folder(folder_path):
	if(not os.path.isdir(folder_path)):
		return
	merge_log_path = os.path.join(folder_path, 'merge_log')
	if(os.path.exists(merge_log_path)):
		shutil.rmtree(merge_log_path)
	os.makedirs(merge_log_path)
	dir_files = natural_sort(os.listdir(folder_path))
	log_node_name = ''
	log_node_path = ''
	for filename in dir_files:
		if(not filename.endswith('.xz')):
			continue
		if(filename.split('.', 1)[0] != log_node_name):
			if('toptmp.log.xz' == filename):
				log_node_name = 'top'
			elif('topHtmp.log.xz' == filename):
				log_node_name = 'topH'
			elif('iftop.log.xz' == filename):
				log_node_name = 'iftop'
			else:
				log_node_name = filename.split('.', 1)[0]
			log_node_path = os.path.join(merge_log_path, log_node_name)
			os.makedirs(log_node_path, exist_ok=True)
		compress_file = os.path.join(folder_path, filename)
		if('toptmp.log.xz' == filename):
			decompress_file = os.path.join(log_node_path, 'top.beforestop.log')
		elif('topHtmp.log.xz' == filename):
			decompress_file = os.path.join(log_node_path, 'topH.beforestop.log')
		elif ('iftoptemp.log.xz' == filename):
			decompress_file = os.path.join(log_node_path, 'iftop.beforestop.log')
		else:
			decompress_file = os.path.join(log_node_path, os.path.splitext(filename)[0])
		try:
			with lzma.open(compress_file, 'rb') as input:
				with open(decompress_file, 'wb') as output:
					shutil.copyfileobj(input, output)
		except EOFError:
			continue
	log_node_list = os.listdir(merge_log_path)
	for log_node_name in log_node_list:
		merge_log(os.path.join(merge_log_path, log_node_name))

if __name__ == '__main__':
	current_path = os.getcwd()
	dir_files = os.listdir(current_path)
	for log_folder in dir_files:
		scan_log_folder(os.path.join(current_path, log_folder))