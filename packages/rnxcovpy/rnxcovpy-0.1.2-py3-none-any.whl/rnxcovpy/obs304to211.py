# -*- coding: utf-8 -*-
# @Time : 2021/4/24 22:27

# -*- coding: utf-8 -*-
# @Time : 2021/4/23 23:06

from . import element as el


# 总转换函数
def doconvert(filepath):
    with open(filepath, 'r') as rf:
        infilelist = rf.readlines()
    lens = len(infilelist)  # 读入数据列表的总长度
    outfilelist = []  # 存放转换后的文件数据
    loc_flag = 0  # 记录正在处理的文件的位置

    # 获取文件头结束的位置
    for singleline in infilelist:
        loc_flag += 1
        if singleline.find("END OF HEADER") != -1:
            break

    # 对“SYS / # / OBS TYPES”标签中的观测值类型进行转换并添加到 obs_type211 中
    obs_type211 = list()
    sate_sys = ''
    data_map_G = list()
    data_map_R = list()
    data_map_E = list()
    data_map_S = list()
    rank_G = dict()
    rank_R = dict()
    rank_E = dict()
    rank_S = dict()
    # 对观测数据类型进行转换，并找出对应的关系
    for singleline in infilelist[0:loc_flag]:
        if singleline.find("SYS / # / OBS TYPES") != -1:
            # 获取当前卫星系统
            if singleline[0] != ' ':
                sate_sys = singleline[0]
            obs_type304_linestr = singleline[7:60].strip()

            obs_type304_linelist = obs_type304_linestr.split()  # 每行的观测类型列表 如['C1C', 'C2W', 'C2X', 'D1C', 'D2W']
            # 判断卫星系统并对每一行的观测类型进行处理
            if sate_sys == 'G':
                el.obs30xto211_convobstype(obs_type211, obs_type304_linelist,
                                           data_map_G, rank_G, el.obs304to211_obs_map_G_rank)
            elif sate_sys == 'R':
                el.obs30xto211_convobstype(obs_type211, obs_type304_linelist,
                                           data_map_R, rank_R, el.obs304to211_obs_map_R_rank)
            elif sate_sys == 'E':
                el.obs30xto211_convobstype(obs_type211, obs_type304_linelist, data_map_E,
                                           rank_E, el.obs304to211_obs_map_E_rank)
            elif sate_sys == 'S':
                el.obs30xto211_convobstype(obs_type211, obs_type304_linelist,
                                           data_map_S, rank_S, el.obs304to211_obs_map_S_rank)
            else:
                continue
        else:
            continue

    obs_type211_num = len(obs_type211)  # 转换后的观测类型的数量

    # 文件头----------------------------------------------------------------------------
    for singleline in infilelist[0:loc_flag]:
        headerlable = singleline[60:-1].strip()  # *文件头的各行的标签*
        if headerlable not in el.obs3045to211_funcdic.keys():
            print(f'Warning:"[{singleline[0:-1]}]" is unidentifiable!')
        elif headerlable.find("SYS / # / OBS TYPES") != -1:
            if outfilelist[-1].find("# / TYPES OF OBSERV") == -1:
                for i in range(0, int((obs_type211_num - 1) / 9) + 1):
                    if len(obs_type211) > 9 and i == 0:
                        obs_type211_linestr = (' ' * 4) + str(obs_type211_num) + ' ' * 4 + \
                                              (' ' * 4).join(obs_type211[0:9]) + '# / TYPES OF OBSERV\n'
                        outfilelist.append(obs_type211_linestr)
                        obs_type211 = obs_type211[9:]
                    elif len(obs_type211) <= 9 and i == 0:  # ' '*(50-(9-obs_type211_num)*6)
                        obs_type211_linestr = ' ' * 5 + str(obs_type211_num) + ' ' * 4 + \
                                              (' ' * 4).join(obs_type211) + \
                                              ' ' * (54 - len(obs_type211) * 6) + '# / TYPES OF OBSERV\n'
                        outfilelist.append(obs_type211_linestr)
                    elif len(obs_type211) > 9 and i > 0:
                        obs_type211_linestr = ' ' * 10 + (' ' * 4).join(obs_type211[0:9]) + '# / TYPES OF OBSERV\n'
                        outfilelist.append(obs_type211_linestr)
                        obs_type211 = obs_type211[9:]
                    elif len(obs_type211) <= 9 and i > 0:
                        obs_type211_linestr = ' ' * 10 + (' ' * 4).join(obs_type211) + \
                                              ' ' * (54 - len(obs_type211) * 6) + '# / TYPES OF OBSERV\n'
                        outfilelist.append(obs_type211_linestr)
            else:
                continue
        elif headerlable.find("ANTENNA: DELTA H/E/N") != -1:
            outfilelist.append(el.obs3045to211_funcdic[headerlable](singleline))
            outfilelist.append("     1     1     0                                          WAVELENGTH FACT L1/2\n")
        else:
            outfilelist.append(el.obs3045to211_funcdic[headerlable](singleline))  # 根据文件头标签调用相应的函数
    # 文件头转换完成----------------------------------------------------------------------------------

    # 历元观测数据
    epoch_header = str()  # 存储每个历元的头数据
    epoch_star_prn = str()  # 存储每个历元观测的卫星的PRN序列
    epoch_converted_data = list()  # 存储当前历元转换后的数据
    epoch_star_num = 0  # 转换后的一个历元的观测卫星的个数
    empty_obs_str211 = str()  # (211)转换后的当前的卫星的观测值(换行符的空格字符串)
    obs_type211_num_tmp = obs_type211_num

    # 将empty_obs_str02赋值为带换行符的空格字符列表
    while obs_type211_num_tmp != 0:
        if obs_type211_num_tmp > 5:
            empty_obs_str211 = empty_obs_str211 + ' ' * 80 + '\n'
            obs_type211_num_tmp -= 5
        else:
            empty_obs_str211 = empty_obs_str211 + ' ' * (obs_type211_num_tmp * 16) + '\n'
            obs_type211_num_tmp = 0
    empty_obs_str211 = list(empty_obs_str211)  # 分割转化为列表
    # print("输出测试：empty_obs_str211：\n", empty_obs_str211)
    # 转换历元观测数据
    for singleline in infilelist[loc_flag:]:
        if singleline[0] == '>':
            if epoch_star_num != 0:
                if epoch_star_num % 12 == 0:
                    epoch_star_prn = epoch_star_prn[:-33]
                epoch_header = epoch_header + f"{(epoch_star_num if epoch_star_num > 9 else '0' + str(epoch_star_num))}"\
                               + epoch_star_prn + '\n'
                epoch_converted_data.insert(0, epoch_header)
                outfilelist.extend(epoch_converted_data)

                epoch_star_num = 0  # \
                epoch_star_prn = ''  # ||--> 清空
                epoch_converted_data.clear()  # /
                epoch_header = ' ' + singleline[4:33]  # "19 10 19 02 49 23.0000000  0 "
            else:
                epoch_header = ' ' + singleline[4:33]  # "19 10 19 02 49 23.0000000  0 "
        elif singleline[0] == 'G':
            epoch_star_num += 1
            if epoch_star_num % 12 == 0:
                epoch_star_prn = epoch_star_prn + singleline[0:3] + '\n' + ' ' * 32
            else:
                epoch_star_prn = epoch_star_prn + singleline[0:3]
            temp_obs_str304 = singleline[3:-1]  # 不带行尾换行符
            a = len(temp_obs_str304)
            b = len(data_map_G) * 16
            if a < b:
                temp_obs_str304 = temp_obs_str304 + ' ' * (b - a)
            temp_obs_str211 = empty_obs_str211

            for i in range(0, len(data_map_G)):
                if data_map_G[i] != -1:
                    temp_obs_str211[data_map_G[i] * 16 + int(data_map_G[i] / 5):data_map_G[i] * 16 + int(
                        data_map_G[i] / 5) + 16] = temp_obs_str304[i * 16:i * 16 + 16]
                    # :data_map_G[i] + int((data_map_G[i] - 1 / 5)) + 16]
                else:
                    continue
            epoch_converted_data.append(''.join(temp_obs_str211))

        elif singleline[0] == 'R':
            epoch_star_num += 1
            if epoch_star_num % 12 == 0:
                epoch_star_prn = epoch_star_prn + singleline[0:3] + '\n' + ' ' * 32
            else:
                epoch_star_prn = epoch_star_prn + singleline[0:3]
            temp_obs_str304 = singleline[3:-1]  # 不带行尾换行符

            a = len(temp_obs_str304)
            b = len(data_map_R) * 16
            if a < b:
                temp_obs_str304 = temp_obs_str304 + ' ' * (b - a)
            temp_obs_str211 = empty_obs_str211

            for i in range(0, len(data_map_R)):
                if data_map_R[i] != -1:
                    # temp_obs_str211[data_map_R[i] + int(data_map_R[i] / 5)] = temp_obs_str304[i * 16:i * 16 + 16]
                    temp_obs_str211[data_map_R[i] * 16 + int(data_map_R[i] / 5):data_map_R[i] * 16 + int(
                        data_map_R[i] / 5) + 16] = temp_obs_str304[i * 16:i * 16 + 16]
                else:
                    continue
            epoch_converted_data.append(''.join(temp_obs_str211))
        elif singleline[0] == 'E':
            epoch_star_num += 1
            if epoch_star_num % 12 == 0:
                epoch_star_prn = epoch_star_prn + singleline[0:3] + '\n' + ' ' * 32
            else:
                epoch_star_prn = epoch_star_prn + singleline[0:3]
            temp_obs_str304 = singleline[3:-1]  # 不带行尾换行符

            a = len(temp_obs_str304)
            b = len(data_map_E) * 16
            if a < b:
                temp_obs_str304 = temp_obs_str304 + ' ' * (b - a)
            temp_obs_str211 = empty_obs_str211

            for i in range(0, len(data_map_E)):
                if data_map_E[i] != -1:
                    # temp_obs_str211[data_map_E[i] + int(data_map_E[i] / 5)] = temp_obs_str304[i * 16:i * 16 + 16]
                    temp_obs_str211[data_map_E[i] * 16 + int(data_map_E[i] / 5):data_map_E[i] * 16 + int(
                        data_map_E[i] / 5) + 16] = temp_obs_str304[i * 16:i * 16 + 16]
                else:
                    continue
            epoch_converted_data.append(''.join(temp_obs_str211))
        elif singleline[0] == 'S':
            epoch_star_num += 1
            if epoch_star_num % 12 == 0:
                epoch_star_prn = epoch_star_prn + singleline[0:3] + '\n' + ' ' * 32
            else:
                epoch_star_prn = epoch_star_prn + singleline[0:3]
            temp_obs_str304 = singleline[3:-1]  # 不带行尾换行符

            a = len(temp_obs_str304)
            b = len(data_map_S) * 16
            if a < b:
                temp_obs_str304 = temp_obs_str304 + ' ' * (b - a)
            temp_obs_str211 = empty_obs_str211

            for i in range(0, len(data_map_S)):
                if data_map_S[i] != -1:
                    # temp_obs_str211[data_map_S[i] + int(data_map_S[i] / 5)] = temp_obs_str304[i * 16:i * 16 + 16]
                    temp_obs_str211[data_map_S[i] * 16 + int(data_map_S[i] / 5):data_map_S[i] * 16 + int(
                        data_map_S[i] / 5) + 16] = temp_obs_str304[i * 16:i * 16 + 16]
                else:
                    continue
            epoch_converted_data.append(''.join(temp_obs_str211))
        else:
            continue
    return outfilelist
