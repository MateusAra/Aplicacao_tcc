import numpy as np
import pandas as pd
import matplotlib.pyplot as pl
import seaborn as sb
from Profiles import *

def get_grades():
    data_frame = pd.read_csv("profiles.csv", dtype={'finalgrade': 'float', 'userid': 'int'})
    data_frame = data_frame.dropna()
    return data_frame.values.tolist()  

def get_clusters():
    data_frame = pd.read_csv("dataframe.quizes.csv", dtype={'Atividade': 'str', 'Nome_do_usuario': 'str'})
    data_frame = data_frame.dropna()
    return data_frame.values.tolist()

def get_users_disapprove():
    userList = []
    clusters = get_grades()

    for line in clusters:
        if (float(line[0]) < 7.0 and line[0] != None):
            userList.append(line[1])

    return userList

def get_users_regular():
    userList = []
    clusters = get_grades()

    for line in clusters:
        if ((float(line[0]) >= 7.0 and float(line[0]) <= 8.9) and line[0] != None):
            userList.append(line[1])

    return userList

def get_users_good():
    userList = []
    clusters = get_grades()

    for line in clusters:
        if (float(line[0]) >= 9.0 and line[0] != None):
            userList.append(line[1])

    return userList

def get_profile_critical(clusters: list) -> Profile:
    userList = get_users_disapprove()

    count = 0
    media_grade = 0
    media_time = 0
    media_attempts = 0

    for line in clusters:
        if (float(line[6]) in userList):
            count += 1
            media_grade += float(line[4])
            media_time += int(line[10])
            media_attempts += int(line[1])

    media_grade_final = media_grade / count
    media_time_final = media_time / count
    media_attempts_final = media_attempts / count

    return Profile(media_grade_final, media_time_final, media_attempts_final)

def get_profile_regular(clusters: list) -> Profile:
    userList = get_users_regular()

    count = 0
    media_grade = 0
    media_time = 0
    media_attempts = 0

    for line in clusters:
        if (float(line[6]) in userList):
            count += 1
            media_grade += float(line[4])
            media_time += int(line[10])
            media_attempts += int(line[1])

    media_grade_final = media_grade / count
    media_time_final = media_time / count
    media_attempts_final = media_attempts / count

    print(f"Media_grade: {media_grade_final}")
    print(f"Media_time: {media_time_final}")
    print(f"Media_attempts: {media_attempts_final}")

def get_profile_good(clusters: list) -> Profile:
    userList = get_users_good()

    count = 0
    media_grade = 0
    media_time = 0
    media_attempts = 0

    for line in clusters:
        if (float(line[6]) in userList):
            count += 1
            media_grade += float(line[4])
            media_time += int(line[10])
            media_attempts += int(line[1])

    media_grade_final = media_grade / count
    media_time_final = media_time / count
    media_attempts_final = media_attempts / count

    print(f"Media_grade: {media_grade_final}")
    print(f"Media_time: {media_time_final}")
    print(f"Media_attempts: {media_attempts_final}")


if __name__ == "__main__":
    clusters = get_clusters()
    get_profile_good(clusters=clusters)

