# -*- coding: utf-8 -*-
# @Time : 2021/4/24 16:34

from datetime import datetime

# ------------ALL-VERSION-APPLICABLE----------------
# 版本2中定义的波段数
v211_obs_freq = ['1', '2', '5', '6', '7', '8']


# "PGM / RUN BY / DATE"标签
def func02(singleline):
    PGM = "rnxcovpy"
    # line = singleline.replace(singleline[0:20], PGM + ' ' * (20 - len(PGM)))
    utct = datetime.utcnow()
    utctm = f"0{utct.month}" if utct.month < 10 else f"{utct.month}"
    utctd = f"0{utct.day}" if utct.day < 10 else f"{utct.day}"
    utcth = f"0{utct.hour}" if utct.hour < 10 else f"{utct.hour}"
    utctmi = f"0{utct.minute}" if utct.minute < 10 else f"{utct.minute}"
    utcts = f"0{utct.second}" if utct.second < 10 else f"{utct.second}"
    utctout = f"{utct.year}{utctm}{utctd} {utcth}{utctmi}{utcts} UTC "  # 时间部分
    add_comment = PGM + ' ' * (20 - len(PGM)) + "FILE CONVERSION     " + utctout + "COMMENT\n"
    return singleline + add_comment


# "COMMENT"、             "MARKER NAME"、         "MARKER NUMBER"、
# "OBSERVER / AGENCY"、   "REC # / TYPE / VERS"、 "ANT # / TYPE"、
# "APPROX POSITION XYZ"、 "ANTENNA: DELTA H/E/N"、"WAVELENGTH FACT L1/2"、
# "INTERVAL"、            "TIME OF FIRST OBS"、   "TIME OF LAST OBS"、
# "RCV CLOCK OFFS APPL"、 "LEAP SECONDS"、        "# OF SATELLITES"、
# "PRN / # OF OBS"、      "END OF HEADER"         label
def func03(singleline):
    return singleline


def func04(singleline):
    comstr = f"#{singleline[60:-1]}# was droped after format conversion."
    return comstr + ' ' * (60 - len(comstr)) + "COMMENT\n"


# 返回一个空字符
def func05(singleline):
    return ''


# 观测类型转换以及计算数据对应关系
def obs30xto211_convobstype(obs_type211, obs_type304_linelist, data_map, rank, obs_map):
    for item in obs_type304_linelist:
        if item[1] in v211_obs_freq:
            temp_obs211 = item[0:2] if (item != 'C1W' and item != 'C1P' and item != 'C2W' and item != 'C2P') \
                else 'P' + item[1]
            try:
                pri_point = obs_map[item[1:]]
            except KeyError:
                pri_point = 10
            if temp_obs211 not in obs_type211:  # 如果列表中不存在此类型转换后的类型  'C1'、'C2'
                obs_type211.append(temp_obs211)
                rank[temp_obs211] = pri_point
                data_map.append(obs_type211.index(temp_obs211))
            else:
                if temp_obs211 in rank:
                    if pri_point > rank[temp_obs211]:
                        rank[temp_obs211] = pri_point
                        data_map[obs_type211.index(temp_obs211)] = -1
                        data_map.append(obs_type211.index(temp_obs211))
                    else:
                        data_map.append(-1)
                else:
                    rank[temp_obs211] = pri_point
                    data_map.append(obs_type211.index(temp_obs211))
        else:
            data_map.append(-1)


# 返回3位的观测类型个数的字符串
def obs211to30x_obs_type_num_str(lentmp):
    if lentmp < 10:
        return ' ' * 2 + str(lentmp)
    elif 10 <= lentmp < 100:
        return ' ' + str(lentmp)
    else:
        return str(lentmp)


def obs211to30x_obs_typr_str(list_obs_type302, sys_str):
    lentmp = len(list_obs_type302)
    type_obs_str = str()
    for i in range(0, int((lentmp - 1) / 13)):  # 大于13个 循环
        type_obs_str = type_obs_str + ' '.join(
            list_obs_type302[i * 13:(i + 1) * 13]) + "  SYS / # / OBS TYPES \n" + ' ' * 7
    type_obs_str = sys_str + ' ' * 2 + obs211to30x_obs_type_num_str(lentmp) + ' ' + type_obs_str
    if lentmp % 13 == 0 and lentmp > 0:
        type_obs_str = type_obs_str + ' '.join(list_obs_type302[-13:]) + "  SYS / # / OBS TYPES \n"
    else:
        type_obs_str = type_obs_str + ' '.join(list_obs_type302[-(lentmp % 13):]) + ' ' * (
                (13 - lentmp % 13) * 4) + "  SYS / # / OBS TYPES \n"
    return type_obs_str


# --------------------------------------------------


# -----------------obs211to302----------------------

# "RINEX VERSION / TYPE"标签
def obs211to302_func01(singleline):
    if singleline.find("2.11"):
        return singleline.replace('2.11', '3.02')
    else:
        print("错误:文件格式或版本错误")


obs211to302_funcdic = {"RINEX VERSION / TYPE": obs211to302_func01,
                       "PGM / RUN BY / DATE": func02,
                       "COMMENT": func03,
                       "MARKER NAME": func03,
                       "MARKER NUMBER": func03,
                       "OBSERVER / AGENCY": func03,
                       "REC # / TYPE / VERS": func03,
                       "ANT # / TYPE": func03,
                       "APPROX POSITION XYZ": func03,
                       "ANTENNA: DELTA H/E/N": func03,
                       "WAVELENGTH FACT L1/2": func05,
                       "INTERVAL": func03,
                       "TIME OF FIRST OBS": func03,
                       "TIME OF LAST OBS": func03,
                       "RCV CLOCK OFFS APPL": func03,
                       "LEAP SECONDS": func03,
                       "# OF SATELLITES": func03,
                       "PRN / # OF OBS": func03,
                       "END OF HEADER": func03
                       }

#   GPS 和 GLONASS 转换图
obs211to302_obs_map_G = {'P1': 'C1W', 'C1': 'C1C', 'P2': 'C2W', 'C2': 'C2C'}
obs211to302_obs_map_R = {'P1': 'C1P', 'C1': 'C1C', 'P2': 'C2P', 'C2': 'C2C'}


# ---------------------------------------------------


# -----------------obs211to304----------------------
# "RINEX VERSION / TYPE"标签
def obs211to304_func01(singleline):
    if singleline.find("2.11"):
        return singleline.replace('2.11', '3.04')
    else:
        print("错误:文件格式或版本错误")


obs211to304_funcdic = {"RINEX VERSION / TYPE": obs211to304_func01,
                       "PGM / RUN BY / DATE": func02,
                       "COMMENT": func03,
                       "MARKER NAME": func03,
                       "MARKER NUMBER": func03,
                       "OBSERVER / AGENCY": func03,
                       "REC # / TYPE / VERS": func03,
                       "ANT # / TYPE": func03,
                       "APPROX POSITION XYZ": func03,
                       "ANTENNA: DELTA H/E/N": func03,
                       "WAVELENGTH FACT L1/2": func05,
                       "INTERVAL": func03,
                       "TIME OF FIRST OBS": func03,
                       "TIME OF LAST OBS": func03,
                       "RCV CLOCK OFFS APPL": func03,
                       "LEAP SECONDS": func03,
                       "# OF SATELLITES": func03,
                       "PRN / # OF OBS": func03,
                       "END OF HEADER": func03
                       }

obs211to304_obs_map_G = {'C1': 'C1C', 'P1': 'C1W', 'L1': 'L1C', 'D1': 'D1C', 'S1': 'S1C',
                         'C2': 'C2X', 'P2': 'C2W', 'L2': 'L2W', 'D2': 'D2W', 'S2': 'S2W',
                         'C5': 'C5X', 'L5': 'L5X', 'D5': 'D5X', 'S5': 'S5X'}
obs211to304_obs_map_R = {'C1': 'C1C', 'P1': 'C1P', 'L1': 'L1C', 'D1': 'D1C', 'S1': 'S1C',
                         'C2': 'C2C', 'P2': 'C2P', 'L2': 'L2P', 'D2': 'D2P', 'S2': 'S2P'}
obs211to304_obs_map_E = {'C1': 'C1X', 'L1': 'L1X', 'D1': 'D1X', 'S1': 'S1X',
                         'C5': 'C5X', 'L5': 'L5X', 'D5': 'D5X', 'S5': 'S5X',
                         'C7': 'C7X', 'L7': 'L7X', 'D7': 'D7X', 'S7': 'S7X',
                         'C8': 'C8X', 'L8': 'L8X', 'D8': 'D8X', 'S8': 'S8X',
                         'C6': 'C6X', '61': 'L6X', 'D6': 'D6X', 'S6': 'S6X'}
obs211to304_obs_map_S = {'C1': 'C1C', 'L1': 'L1C', 'D1': 'D1C', 'S1': 'S1C',
                         'C5': 'C5X', 'L5': 'L5X', 'D5': 'D5X', 'S5': 'S5X'}


# --------------------------------------------------

# -----------------obs211to305----------------------
# "RINEX VERSION / TYPE"标签
def obs211to305_func01(singleline):
    if singleline.find("2.11"):
        return singleline.replace('2.11', '3.05')
    else:
        print("错误:文件格式或版本错误")


obs211to305_funcdic = {"RINEX VERSION / TYPE": obs211to305_func01,
                       "PGM / RUN BY / DATE": func02,
                       "COMMENT": func03,
                       "MARKER NAME": func03,
                       "MARKER NUMBER": func03,
                       "OBSERVER / AGENCY": func03,
                       "REC # / TYPE / VERS": func03,
                       "ANT # / TYPE": func03,
                       "APPROX POSITION XYZ": func03,
                       "ANTENNA: DELTA H/E/N": func03,
                       "WAVELENGTH FACT L1/2": func05,
                       "INTERVAL": func03,
                       "TIME OF FIRST OBS": func03,
                       "TIME OF LAST OBS": func03,
                       "RCV CLOCK OFFS APPL": func03,
                       "LEAP SECONDS": func03,
                       "# OF SATELLITES": func03,
                       "PRN / # OF OBS": func03,
                       "END OF HEADER": func03
                       }

obs211to305_obs_map_G = {'C1': 'C1C', 'P1': 'C1W', 'L1': 'L1C', 'D1': 'D1C', 'S1': 'S1C',
                         'C2': 'C2X', 'P2': 'C2W', 'L2': 'L2W', 'D2': 'D2W', 'S2': 'S2W',
                         'C5': 'C5X', 'L5': 'L5X', 'D5': 'D5X', 'S5': 'S5X'}
obs211to305_obs_map_R = {'C1': 'C1C', 'P1': 'C1P', 'L1': 'L1C', 'D1': 'D1C', 'S1': 'S1C',
                         'C2': 'C2C', 'P2': 'C2P', 'L2': 'L2P', 'D2': 'D2P', 'S2': 'S2P'}
obs211to305_obs_map_E = {'C1': 'C1X', 'L1': 'L1X', 'D1': 'D1X', 'S1': 'S1X',
                         'C5': 'C5X', 'L5': 'L5X', 'D5': 'D5X', 'S5': 'S5X',
                         'C7': 'C7X', 'L7': 'L7X', 'D7': 'D7X', 'S7': 'S7X',
                         'C8': 'C8X', 'L8': 'L8X', 'D8': 'D8X', 'S8': 'S8X',
                         'C6': 'C6X', '61': 'L6X', 'D6': 'D6X', 'S6': 'S6X'}
obs211to305_obs_map_S = {'C1': 'C1C', 'L1': 'L1C', 'D1': 'D1C', 'S1': 'S1C',
                         'C5': 'C5X', 'L5': 'L5X', 'D5': 'D5X', 'S5': 'S5X'}


# --------------------------------------------------


# -------------------obs302to211---------------------
# "RINEX VERSION / TYPE"标签
def obs302to211_func01(singleline):
    if singleline.find("3.02"):
        return singleline.replace("3.02", "2.11")
    else:
        print("错误:文件格式或版本错误")


obs302to211_funcdic = {"RINEX VERSION / TYPE": obs302to211_func01,
                       "PGM / RUN BY / DATE": func02,
                       "COMMENT": func03,
                       "MARKER NAME": func03,
                       "MARKER NUMBER": func03,
                       "OBSERVER / AGENCY": func03,
                       "REC # / TYPE / VERS": func03,
                       "ANT # / TYPE": func03,
                       "APPROX POSITION XYZ": func03,
                       "ANTENNA: DELTA H/E/N": func03,
                       "INTERVAL": func03,
                       "TIME OF FIRST OBS": func03,
                       "TIME OF LAST OBS": func03,
                       "RCV CLOCK OFFS APPL": func03,
                       "LEAP SECONDS": func03,
                       "# OF SATELLITES": func03,
                       "PRN / # OF OBS": func05,
                       "END OF HEADER": func03,
                       "SYS / # / OBS TYPES": None,
                       "MARKER TYPE": func04,
                       "ANTENNA: DELTA X/Y/Z": func04,
                       "ANTENNA:PHASECENTER": func04,
                       "ANTENNA: B.SIGHT XYZ": func04,
                       "ANTENNA: ZERODIR AZI": func04,
                       "ANTENNA: ZERODIR XYZ": func04,
                       "CENTER OF MASS: XYZ": func04,
                       "SIGNAL STRENGTH UNIT": func04,
                       "SYS / DCBS APPLIED": func04,
                       "SYS / PCVS APPLIED": func04,
                       "SYS / SCALE FACTOR": func04,
                       "SYS / PHASE SHIFT": func04,
                       "GLONASS SLOT / FRQ #": func04,
                       "GLONASS COD/PHS/BIS": func04
                       }
obs302to211_obs_map_G_rank = {'1P': 9, '1W': 8, '1C': 7, '1S': 6, '1L': 5, '1X': 4, '1Y': 3, '1M': 2, '1N': 1,
                              '2P': 10, '2Y': 9, '2W': 8, '2C': 7, '2M': 6, '2N': 5, '2D': 4, '2L': 3, '2S': 2, '2X': 1,
                              '5I': 3, '5Q': 2, '5X': 1
                              }
obs302to211_obs_map_R_rank = {'1P': 2, '1C': 1,
                              '2P': 2, '2C': 1,
                              '3I': 3, '3Q': 2, '3X': 1}
obs302to211_obs_map_E_rank = {'1C': 5, '1A': 4, '1B': 3, '1X': 2, '1Z': 1,
                              '5I': 3, '5Q': 2, '5X': 1,
                              '7I': 3, '7Q': 2, '7X': 1,
                              '8I': 3, '8Q': 2, '8X': 1,
                              '6C': 5, '6A': 4, '6B': 3, '6X': 2, '6Z': 1
                              }
obs302to211_obs_map_S_rank = {'1C': 1, '5I': 3, '5Q': 2, '5X': 1}


# ---------------------------------------------------


# -------------------obs304/305to211---------------------
# "RINEX VERSION / TYPE"标签
def obs3045to211_func01(singleline):
    if singleline.find("3.04"):
        return singleline.replace("3.04", "2.11")
    elif singleline.find("3.05"):
        return singleline.replace("3.05", "2.11")
    else:
        print("错误:文件格式或版本错误")


obs3045to211_funcdic = {"RINEX VERSION / TYPE": obs3045to211_func01,
                        "PGM / RUN BY / DATE": func02,
                        "COMMENT": func03,
                        "MARKER NAME": func03,
                        "MARKER NUMBER": func03,
                        "OBSERVER / AGENCY": func03,
                        "REC # / TYPE / VERS": func03,
                        "ANT # / TYPE": func03,
                        "APPROX POSITION XYZ": func03,
                        "ANTENNA: DELTA H/E/N": func03,
                        "INTERVAL": func03,
                        "TIME OF FIRST OBS": func03,
                        "TIME OF LAST OBS": func03,
                        "RCV CLOCK OFFS APPL": func03,
                        "LEAP SECONDS": func03,
                        "# OF SATELLITES": func03,
                        "PRN / # OF OBS": func05,
                        "END OF HEADER": func03,
                        "SYS / # / OBS TYPES": None,
                        "MARKER TYPE": func04,
                        "ANTENNA: DELTA X/Y/Z": func04,
                        "ANTENNA:PHASECENTER": func04,
                        "ANTENNA: B.SIGHT XYZ": func04,
                        "ANTENNA: ZERODIR AZI": func04,
                        "ANTENNA: ZERODIR XYZ": func04,
                        "CENTER OF MASS: XYZ": func04,
                        "SIGNAL STRENGTH UNIT": func04,
                        "SYS / DCBS APPLIED": func04,
                        "SYS / PCVS APPLIED": func04,
                        "SYS / SCALE FACTOR": func04,
                        "SYS / PHASE SHIFT": func04,
                        "GLONASS SLOT / FRQ #": func04,
                        "GLONASS COD/PHS/BIS": func04
                        }
# pri@ 9:higher > 1:lower
obs304to211_obs_map_G_rank = {'1P': 9, '1W': 8, '1C': 7, '1S': 6, '1L': 5, '1X': 4, '1Y': 3, '1M': 2, '1N': 1,
                              '2P': 10, '2Y': 9, '2W': 8, '2C': 7, '2M': 6, '2N': 5, '2D': 4, '2L': 3, '2S': 2, '2X': 1,
                              '5I': 3, '5Q': 2, '5X': 1
                              }
obs304to211_obs_map_R_rank = {'1P': 2, '1C': 1,
                              '4A': 3, '4B': 2, '4X': 1,
                              '2P': 2, '2C': 1,
                              '6A': 3, '6B': 2, '6X': 1,
                              '3I': 3, '3Q': 2, '3X': 1}
obs304to211_obs_map_E_rank = {'1C': 5, '1A': 4, '1B': 3, '1X': 2, '1Z': 1,
                              '5I': 3, '5Q': 2, '5X': 1,
                              '7I': 3, '7Q': 2, '7X': 1,
                              '8I': 3, '8Q': 2, '8X': 1,
                              '6C': 5, '6A': 4, '6B': 3, '6X': 2, '6Z': 1
                              }
obs304to211_obs_map_S_rank = {'1C': 1, '5I': 3, '5Q': 2, '5X': 1}

# ---------------------------------------------------
