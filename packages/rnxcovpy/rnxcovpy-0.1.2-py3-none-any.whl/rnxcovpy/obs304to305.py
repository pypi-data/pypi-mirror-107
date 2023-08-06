# -*- coding: utf-8 -*-
# @Time : 2021/5/14 23:33


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
    for i in range(0, loc_flag):
        if infilelist[i].find("# OF SATELLITES")!=-1 or infilelist[i].find("PRN / # OF OBS")!=-1:
            infilelist[i] = ''
    system = ''
    BDS_obs_type = list()

    loc_BDSh = -1  # 记录北斗的观测值类型在文件头中的位置
    flag_L1N = -1  #
    flag_D1N = -1  # 记录这三种北斗观测值在版本3.04中的数据位置
    flag_S1N = -1  # 在转3.05版本时要舍弃

    for i in range(0, loc_flag):
        if infilelist[i].find("RINEX VERSION / TYPE") != -1:
            infilelist[i] = infilelist[i].replace("3.04", "3.05")
        elif infilelist[i].find("SYS / # / OBS TYPES") != -1:
            if infilelist[i][0] != " ":
                system = infilelist[i][0]
            if system == 'C':
                BDS_obs_type = BDS_obs_type + infilelist[i][7:60].strip().split()
        if infilelist[i].find("SYS / # / OBS TYPES") != -1 and infilelist[i][0] == 'C':
            loc_BDSh = i
    if loc_BDSh != -1:
        # 将BDS的观测值类型行删除
        del infilelist[loc_BDSh]
        loc_flag -= 1
        if len(BDS_obs_type) > 13:
            BDline = int((len(BDS_obs_type) - 1) / 13)
            for i in range(0, BDline):
                del infilelist[loc_BDSh]
                loc_flag -= 1


        # 对BDS_obs_type进行修改并且格式化
        for i in range(0, len(BDS_obs_type)):
            if BDS_obs_type[i][1:] == '6A':
                BDS_obs_type[i] = BDS_obs_type[i][0] + '6D'
            elif BDS_obs_type[i][1:] == '1A':
                BDS_obs_type[i] = BDS_obs_type[i][0] + '1S'
            elif BDS_obs_type[i] == 'L1N':
                flag_L1N = i  # 从0开始
            elif BDS_obs_type[i] == 'D1N':
                flag_D1N = i
            elif BDS_obs_type[i] == 'S1N':
                flag_S1N = i
        if 'L1N' in BDS_obs_type:  # 删除
            BDS_obs_type.remove('L1N')
        if 'L1D' in BDS_obs_type:
            BDS_obs_type.remove('L1D')
        if 'L1S' in BDS_obs_type:
            BDS_obs_type.remove('L1S')
            # 格式化
        if len(BDS_obs_type) < 10:
            str_num_obs = ' ' + str(len(BDS_obs_type))
        else:
            str_num_obs = str(len(BDS_obs_type))

            # tmpstr = 'C' + ' ' * 3 + str_num_obs + ' ' + ' '.join(
            #     BDS_obs_type[1:13]) + "  SYS / # / OBS TYPES\n" + ' ' * 7 \
            #          + ' '.join(BDS_obs_type[13:]) + ' ' * (54 - (len(BDS_obs_type) - 13) * 4) + "SYS / # / OBS TYPES\n"
            # infilelist.insert(loc_BDSh, tmpstr)
            # loc_flag += 1
        tmpBDS_obs_type = BDS_obs_type
        if len(tmpBDS_obs_type) <= 13:
            tmpstr = 'C' + ' ' * 3 + str_num_obs + ' ' + ' '.join(tmpBDS_obs_type) + ' ' * (54 - len(tmpBDS_obs_type) * 4) \
                     + "SYS / # / OBS TYPES\n"
            infilelist.insert(loc_BDSh, tmpstr)
            loc_flag += 1
        elif len(tmpBDS_obs_type) > 13:
            BDline = int((len(tmpBDS_obs_type)-1)/13)
            tmpstr = 'C' + ' ' * 3 + str_num_obs + ' ' + ' '.join(tmpBDS_obs_type[0:13]) + "  SYS / # / OBS TYPES\n"
            infilelist.insert(loc_BDSh, tmpstr)
            loc_flag += 1
            tmpBDS_obs_type = tmpBDS_obs_type[13:]

            for i in range(0, BDline):
                tmpstr = ' '*7 + ' '.join(tmpBDS_obs_type[0:13])
                lentmpstr = len(tmpstr)
                tmpstr = tmpstr + ' ' * (60 - lentmpstr) + "SYS / # / OBS TYPES\n"
                infilelist.insert(loc_BDSh + i + 1, tmpstr)
                loc_flag += 1
                if i == BDline-1:
                    pass
                else:
                    tmpBDS_obs_type = tmpBDS_obs_type[13:]

            # tmpstr = 'C' + ' ' * 3 + str_num_obs + ' ' + ' '.join(
            #     BDS_obs_type[1:13]) + "  SYS / # / OBS TYPES\n" + ' ' * 7 \
            #          + ' '.join(BDS_obs_type[13:]) + ' ' * (54 - (len(BDS_obs_type) - 13) * 4) + "SYS / # / OBS TYPES\n"
            # infilelist.insert(loc_BDSh, tmpstr)
            # loc_flag += 1
        # 数据部分
    if flag_L1N != -1 or flag_D1N != -1 or flag_S1N != -1:
        listdrop = [flag_L1N, flag_D1N, flag_S1N]
        while -1 in listdrop:
            listdrop.remove(-1)
        listdrop.sort()
        if len(listdrop) == 1:
            for i in range(loc_flag, len(infilelist)):
                if infilelist[i][0] == 'C':
                    linestr = infilelist[i] + ' ' * (len(BDS_obs_type) * 16 + 3 - len(infilelist[i]))
                    linestr = linestr[0: 3] + linestr[3: 3 + listdrop[0] * 16] + linestr[19 + listdrop[0] * 16:]
                    infilelist[i] = linestr
        elif len(listdrop) == 2:
            for i in range(loc_flag, len(infilelist)):
                if infilelist[i][0] == 'C':
                    linestr = infilelist[i] + ' ' * (len(BDS_obs_type) * 16 + 3 - len(infilelist[i]))
                    linestr = linestr[0: 3] + linestr[3: 3 + listdrop[0] * 16] \
                              + linestr[19 + listdrop[0] * 16: 3 + listdrop[1] * 16] \
                              + linestr[19 + listdrop[1] * 16:]
                    infilelist[i] = linestr
        elif len(listdrop) == 3:
            for i in range(loc_flag, len(infilelist)):
                if infilelist[i][0] == 'C':
                    linestr = infilelist[i] + ' ' * (len(BDS_obs_type) * 16 + 3 - len(infilelist[i]))
                    linestr = linestr[0: 3] + linestr[3: 3 + listdrop[0] * 16] \
                              + linestr[19 + listdrop[0] * 16: 3 + listdrop[1] * 16] \
                              + linestr[19 + listdrop[1] * 16: 3 + listdrop[2] * 16] + linestr[19 + listdrop[2] * 16:]
                    infilelist[i] = linestr
    return infilelist
