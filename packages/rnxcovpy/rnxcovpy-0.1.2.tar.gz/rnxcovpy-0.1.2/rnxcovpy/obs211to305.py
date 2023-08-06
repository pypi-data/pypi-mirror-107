# -*- coding: utf-8 -*-
# @Time : 2021/5/14 9:05

from . import element as el
import re


# 总转换函数
def doconvert(filepath):
    with open(filepath, 'r') as rf:
        infilelist = rf.readlines()
    lens = len(infilelist)
    outfilelist = []  # 存放转换后的文件数据
    loc_flag = 0  # 记录正在处理的文件的位置

    # 获取文件头结束的位置
    for singleline in infilelist:
        loc_flag += 1
        if singleline.find("END OF HEADER") != -1:
            break
    # 检测观测到的卫星系统的类型
    first_epoch_sate_num = int(infilelist[loc_flag][30:32])
    epoch_header_lines = int(first_epoch_sate_num / 12) + 1
    sate = re.sub('[^A-Z]', '', ''.join(infilelist[loc_flag:loc_flag + epoch_header_lines]))
    sate_sys = set()  # sate_sys 存储本文件观测值的卫星系统种类到集合中
    for i in sate:
        sate_sys.add(i)

    # -----------------------------
    list_obs_type211 = list()  # 2.11版本的观测类型列表
    list_obs_type305_G = list()  # 3.05版本的GPS系统的观测类型
    list_obs_type305_R = list()  # 3.05版本的GLONASS系统的观测类型
    list_obs_type305_E = list()  # 3.05版本的Galileo系统的观测类型
    list_obs_type305_S = list()  # 3.05版本的SBAS的观测类型
    # -----------------------------
    obs_type305_G_conv = list()  # GPS系统的观测值2.11对应3.05的关系
    obs_type305_R_conv = list()  # GLONASS系统的观测值2.11对应3.05的关系
    obs_type305_E_conv = list()  # Galileo系统的观测值2.11对应3.05的关系
    obs_type305_S_conv = list()  # SBAS系统的观测值2.11对应3.05的关系
    num_obs_type211 = 0  # 2.11版本观测类型的个数
    # -----------------------------

    # 文件头
    for singleline in infilelist[0:loc_flag]:
        headerlable = singleline[60:-1].strip()  # *文件头的各行的标签*

        # "# / TYPES OF OBSERV"
        if headerlable.find("# / TYPES OF OBSERV") != -1:
            if singleline[4:6] != ' ' * 2:
                num_obs_type211 = int(singleline[4:6])

            obs_type_line = singleline[10:60].rstrip()
            list_obs_type211.extend(obs_type_line.split(' ' * 4))
            # list_obs_type211 结构如 ['C1', 'P1', 'P2', 'L1', 'L2', 'S1', 'S2', 'D1', 'D2']

            if len(list_obs_type211) == num_obs_type211:  # 观测数据类型添加完整之后对观测值类型进行转换

                for i in range(0, len(list_obs_type211)):
                    if list_obs_type211[i][1] == '1':
                        list_obs_type305_G.append(list_obs_type211[i])
                        list_obs_type305_R.append(list_obs_type211[i])
                        list_obs_type305_E.append(list_obs_type211[i])
                        list_obs_type305_S.append(list_obs_type211[i])
                        obs_type305_G_conv.append(1)
                        obs_type305_R_conv.append(1)
                        obs_type305_E_conv.append(1)
                        obs_type305_S_conv.append(1)
                    elif list_obs_type211[i][1] == '2':
                        list_obs_type305_G.append(list_obs_type211[i])
                        list_obs_type305_R.append(list_obs_type211[i])
                        obs_type305_G_conv.append(1)
                        obs_type305_R_conv.append(1)
                        obs_type305_E_conv.append(-1)
                        obs_type305_S_conv.append(-1)
                    elif list_obs_type211[i][1] == '5':
                        list_obs_type305_G.append(list_obs_type211[i])
                        list_obs_type305_E.append(list_obs_type211[i])
                        list_obs_type305_S.append(list_obs_type211[i])
                        obs_type305_G_conv.append(1)
                        obs_type305_R_conv.append(-1)
                        obs_type305_E_conv.append(1)
                        obs_type305_S_conv.append(1)
                    elif list_obs_type211[i][1] == '6' or list_obs_type211[i][1] == '7' or \
                            list_obs_type211[i][1] == '8':
                        list_obs_type305_E.append(list_obs_type211[i])
                        obs_type305_G_conv.append(-1)
                        obs_type305_R_conv.append(-1)
                        obs_type305_E_conv.append(1)
                        obs_type305_S_conv.append(-1)
                if 'P1' in list_obs_type211:
                    list_obs_type305_E.remove('P1')
                    list_obs_type305_S.remove('P1')
                    obs_type305_E_conv[list_obs_type211.index('P1')] = -1
                    obs_type305_S_conv[list_obs_type211.index('P1')] = -1

                # 对GPS和GLONASS系统的观测类型进行转换
                list_obs_type305_G = [el.obs211to305_obs_map_G[i] for i in list_obs_type305_G]
                list_obs_type305_R = [el.obs211to305_obs_map_R[i] for i in list_obs_type305_R]
                list_obs_type305_E = [el.obs211to305_obs_map_E[i] for i in list_obs_type305_E]
                list_obs_type305_S = [el.obs211to305_obs_map_S[i] for i in list_obs_type305_S]

                type_obs_str_G = el.obs211to30x_obs_typr_str(list_obs_type305_G, 'G')
                type_obs_str_R = el.obs211to30x_obs_typr_str(list_obs_type305_R, 'R')
                type_obs_str_E = el.obs211to30x_obs_typr_str(list_obs_type305_E, 'E')
                type_obs_str_S = el.obs211to30x_obs_typr_str(list_obs_type305_S, 'S')
                if 'G' in sate_sys:
                    outfilelist.append(type_obs_str_G)
                if 'R' in sate_sys:
                    outfilelist.append(type_obs_str_R)
                if 'E' in sate_sys:
                    outfilelist.append(type_obs_str_E)
                if 'S' in sate_sys:
                    outfilelist.append(type_obs_str_S)
        elif headerlable not in el.obs211to305_funcdic.keys():
            print(f'Warning:"{headerlable}" is unidentifiable!')
        else:
            outfilelist.append(el.obs211to305_funcdic[headerlable](singleline))  # 根据文件头标签调用相应的函数

    # 历元观测数据
    while True:
        # print("loc_flag:", loc_flag)
        # ***loc_flag*** #   loc_flag 初始位置是观测值的第一行
        if infilelist[loc_flag][60:].strip() in el.obs211to304_funcdic:
            outfilelist.append(infilelist[loc_flag])
            loc_flag += 1
            continue
        try:
            epoch_record = infilelist[loc_flag][0:32]
            # print('infilelist[loc_flag]:', infilelist[loc_flag])
            epoch_year = int(epoch_record[1:3])
            epoch_month = int(epoch_record[4:6])
            epoch_day = int(epoch_record[7:9])
            epoch_hour = int(epoch_record[10:12])
            epoch_minute = int(epoch_record[13:15])
        except:
            loc_flag += 1
            continue
        if epoch_year <= 80:
            epoch_year += 2000
        else:
            epoch_year += 1900
        if epoch_month < 10:
            epoch_month = '0' + str(epoch_month)
        if epoch_day < 10:
            epoch_day = '0' + str(epoch_day)
        if epoch_hour < 10:
            epoch_hour = '0' + str(epoch_hour)
        if epoch_minute < 10:
            epoch_minute = '0' + str(epoch_minute)

        epoch_record = f"> {epoch_year} {epoch_month} {epoch_day} {epoch_hour} {epoch_minute} {epoch_record[16:]}\n"
        outfilelist.append(epoch_record)

        # 此历元的观测卫星的个数
        epo_sate_num = int(infilelist[loc_flag][30:32])

        # 将各个观测到的卫星PRN存入epo_sates字符串中  就像这样"G12G19G02G30G07G05G29"
        epo_sates = str()
        for i in range(0, int((epo_sate_num - 1) / 12) + 1):
            epo_sates = epo_sates + infilelist[loc_flag][32:68]
            loc_flag += 1
        # epo_sates = epo_sates + infilelist[loc_flag][32:-1]
        # loc_flag += 1  # 将标记下移至观测值行
        # print("epo_sates:", epo_sates)
        # 每个卫星的观测值占用的行数
        line_of_one_star = int((num_obs_type211 - 1) / 5) + 1
        lines_of_epoch_star = epo_sate_num * line_of_one_star

        for i in range(0, lines_of_epoch_star, line_of_one_star):
            obs_str = ''
            for j in range(0, line_of_one_star):
                obs_str = obs_str + infilelist[loc_flag + j] + ' ' * (81 - len(infilelist[loc_flag + j]))
            obs_str = obs_str.replace('\n', '')
            current_sate_sys = epo_sates[int((i / line_of_one_star) * 3):int((i / line_of_one_star) * 3) + 1]
            if current_sate_sys == 'G':
                for num in range(0, num_obs_type211):
                    if obs_type305_G_conv[num] == -1:
                        obs_str = obs_str[:16 * i] + ' ' * 16 + obs_str[16 * (i + 1):]
            elif current_sate_sys == 'R':
                for num in range(0, num_obs_type211):
                    if obs_type305_R_conv[num] == -1:
                        obs_str = obs_str[:16 * i] + ' ' * 16 + obs_str[16 * (i + 1):]
            elif current_sate_sys == 'E':
                for num in range(0, num_obs_type211):
                    if obs_type305_E_conv[num] == -1:
                        obs_str = obs_str[:16 * i] + ' ' * 16 + obs_str[16 * (i + 1):]
            elif current_sate_sys == 'S':
                for num in range(0, num_obs_type211):
                    if obs_type305_S_conv[num] == -1:
                        obs_str = obs_str[:16 * i] + ' ' * 16 + obs_str[16 * (i + 1):]
            outfilelist.append(epo_sates[int((i / line_of_one_star) * 3):int(
                (i / line_of_one_star) * 3) + 3] + obs_str.rstrip() + '\n')

            loc_flag += line_of_one_star

        if loc_flag >= lens:
            break
    # 将转换后的列表作为函数的返回值
    return outfilelist