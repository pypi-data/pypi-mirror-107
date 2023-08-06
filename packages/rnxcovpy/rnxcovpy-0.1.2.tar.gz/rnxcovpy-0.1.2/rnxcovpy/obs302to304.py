# -*- coding: utf-8 -*-
# @Time : 2021/5/14 14:30
"""可能有问题 @time-2021年5月15日09:31:31"""

from . import element as el


def doconvert(filepath):
    with open(filepath, 'r') as rf:
        infilelist = rf.readlines()
    loc_flag = 0  # 记录正在处理的文件的位置
    # 获取文件头结束的位置
    for singleline in infilelist:
        loc_flag += 1
        if singleline.find("END OF HEADER") != -1:
            break
    # 对文件头进行修改
    system = ''
    for i in range(0, loc_flag):
        if infilelist[i].find("RINEX VERSION / TYPE") != -1:
            infilelist[i] = infilelist[i].replace("3.02", "3.04")
        elif infilelist[i].find("SYS / # / OBS TYPES") != -1:
            if infilelist[i][0] != " ":
                system = infilelist[i][0]
            obs_type = infilelist[i][7:60].strip()
            obs_type = obs_type.split()
            print(obs_type)
            if system == "G":
                for j in range(0, len(obs_type)):
                    if len(obs_type[j]) == 2:
                        obs_type[j] = el.obs211to304_obs_map_G[obs_type[j]]
                obs_str = infilelist[i][0:7] + " ".join(obs_type)
                obs_str = obs_str + ' ' * (60 - len(obs_str)) + infilelist[i][60:]
                infilelist[i] = obs_str
            elif system == "R":
                for j in range(0, len(obs_type)):
                    if len(obs_type[j]) == 2:
                        obs_type[j] = el.obs211to304_obs_map_R[obs_type[j]]
                obs_str = infilelist[i][0:7] + " ".join(obs_type)
                obs_str = obs_str + ' ' * (60 - len(obs_str)) + infilelist[i][60:]
                infilelist[i] = obs_str
            elif system == "E":
                for j in range(0, len(obs_type)):
                    if len(obs_type[j]) == 2:
                        obs_type[j] = el.obs211to304_obs_map_E[obs_type[j]]
                obs_str = infilelist[i][0:7] + " ".join(obs_type)
                obs_str = obs_str + ' ' * (60 - len(obs_str)) + infilelist[i][60:]
                infilelist[i] = obs_str
            elif system == "S":
                for j in range(0, len(obs_type)):
                    if len(obs_type[j]) == 2:
                        obs_type[j] = el.obs211to304_obs_map_S[obs_type[j]]
                obs_str = infilelist[i][0:7] + " ".join(obs_type)
                obs_str = obs_str + ' ' * (60 - len(obs_str)) + infilelist[i][60:]
                infilelist[i] = obs_str
    return infilelist
