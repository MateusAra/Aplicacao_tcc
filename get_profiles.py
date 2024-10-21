import numpy as np
import pandas as pd
import matplotlib.pyplot as pl
import seaborn as sb
from Profiles import *

def get_clusters():
    data_frame = pd.read_csv("dataframe.quizes.csv", dtype={'Atividade': 'str', 'Nome_do_usuario': 'str'})
    data_frame = data_frame.dropna()
    return data_frame.values.tolist()

def get_grades():
    data_frame = pd.read_csv("profiles_updated.csv", dtype={'finalgrade': 'float', 'userid': 'int', 'username': 'str'})
    data_frame = data_frame.dropna(subset=['finalgrade'])
    return data_frame

def categorize_students(data_frame):
    disapproved = data_frame[data_frame['finalgrade'] <= 5.0]['username'].tolist()
    regular = data_frame[(data_frame['finalgrade'] > 5.0) & (data_frame['finalgrade'] <= 7.0)]['username'].tolist()
    good = data_frame[data_frame['finalgrade'] > 7.0]['username'].tolist()
    
    return disapproved, regular, good

def calculate_profile(users, clusters):
    count = 0
    media_grade = 0
    media_time = 0
    media_attempts = 0
    
    for line in clusters:
        if line[5] in users:
            count += 1
            media_grade += float(line[4])
            media_time += int(line[10])
            media_attempts += int(line[1])
    
    if count > 0:
        media_grade /= count
        media_time /= count
        media_attempts /= count
    
    return media_grade, media_time, media_attempts

def get_profiles():
    grades_df = get_grades()
    disapproved, regular, good = categorize_students(grades_df)

    clusters = get_clusters()  

    print("Perfil Reprovado:")
    print(disapproved)

    print("Perfil Regular:")
    print(regular)

    print("Perfil Bom:")
    print(good)

if __name__ == "__main__":
    get_profiles()

