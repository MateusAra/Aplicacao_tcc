import numpy as np
import pandas as pd
import matplotlib.pyplot as pl
import seaborn as sb
from sklearn.cluster import KMeans
from Profiles import *
from collections import defaultdict
import plotly.express as px


final_good = ['anon3', 'anon5', 'anon6', 'anon7', 'anon12', 'anon13', 'anon15', 'anon18', 'anon26', 'anon27', 'anon28', 'anon29', 'anon30', 'anon31', 'anon33', 'anon34', 'anon35', 'anon36', 'anon39', 'anon40', 'anon41', 'anon42', 'anon43', 'anon44', 'anon46', 'anon47', 'anon48', 'anon49', 'anon51', 'anon52', 'anon53', 'anon54', 'anon55', 'anon57', 'anon58', 'anon59', 'anon60', 'anon61', 'anon62', 'anon63', 'anon64', 'anon65', 'anon66', 'anon67', 'anon68', 'anon69', 'anon70', 'anon71', 'anon72', 'anon73', 'anon74', 'anon75', 'anon76', 'anon77', 'anon78', 'anon82', 'anon83', 'anon84', 'anon85', 'anon86', 'anon87', 'anon89', 'anon91', 'anon92', 'anon93', 'anon94', 'anon96', 'anon98']
final_regular = ['anon4', 'anon9', 'anon10', 'anon14', 'anon16', 'anon17', 'anon19', 'anon20', 'anon21', 'anon22', 'anon23', 'anon25', 'anon45', 'anon50', 'anon56', 'anon79', 'anon80', 'anon88', 'anon90', 'anon97']
final_critical = ['anon2', 'anon8', 'anon11', 'anon24', 'anon81', 'anon95', 'anon99', 'anon100']

def get_clusters(clustering: bool = False):

    if clustering:
        data_frame = pd.read_excel("dataframe.v2_kmeans.xlsx", sheet_name="dataframe.v1_formated")
        
        data_frame_original = data_frame.copy()

        kmeans = KMeans(n_clusters=4, random_state=0)

        data_frame = data_frame.drop(["Atividade", "Nome_do_usuario"], axis=1)
        data_frame = data_frame.dropna()

        X = np.array(data_frame)
        labels = kmeans.fit(X).labels_

        data_frame_original["K-classes"] = np.nan
        data_frame_original["Email_Usuario"] = "anonmail@notexists.com.br"
        data_frame_original.loc[data_frame.index, "K-classes"] = labels

        data_frame_original.to_csv("dataframe.quizes.csv", index=False)

        return data_frame_original.values.tolist()
    else:
        data_frame = pd.read_csv("dataframe.quizes.csv", dtype={'Atividade': 'str', 'Nome_do_usuario': 'str'})
        data_frame = data_frame.dropna()
        clusters = data_frame.values.tolist()

        return clusters
    
def group_attempts_by_student(clusters):
    student_attempts = defaultdict(list)
    
    for line in clusters:
        name = line[5]
        student_attempts[name].append(line)
    
    return student_attempts

def calculate_student_averages(student_attempts):
    student_averages = {}

    for name, attempts in student_attempts.items():
        total_grade = 0
        total_time = 0
        total_attempts = 0
        
        for attempt in attempts:
            grade = float(attempt[4])
            time = int(attempt[10])
            attempts_realized = int(attempt[1])
            
            total_grade += grade
            total_time += time
            total_attempts += attempts_realized

        num_attempts = len(attempts)
        average_grade = total_grade / num_attempts
        average_time = total_time / num_attempts
        average_attempts = total_attempts / num_attempts

        student_averages[name] = {
            'average_grade': average_grade,
            'average_time': average_time,
            'average_attempts': average_attempts,
            'attempts': attempts 
        }

    return student_averages

def categorize_students(student_averages):
    good = []
    regular = []
    alert = []
    critical = []
    
    profile_good = Profile.get_profile_good()
    profile_regular = Profile.get_profile_regular()
    profile_critical = Profile.get_profile_critical()

    for name, averages in student_averages.items():
        avg_grade = averages['average_grade']
        avg_time = averages['average_time']
        avg_attempts = averages['average_attempts']

        if avg_grade >= profile_good.media_grade \
        and avg_time <= profile_good.media_time \
        and avg_attempts <= profile_good.media_attempts:
            good.append([name, avg_grade, avg_time, avg_attempts, "Good"])

        elif profile_critical.media_grade <= avg_grade <= profile_good.media_grade \
        and avg_time <= profile_regular.media_time \
        and avg_attempts <= profile_regular.media_attempts:
            regular.append([name, avg_grade, avg_time, avg_attempts, "Regular"])

        elif avg_grade <= profile_critical.media_grade \
        and avg_time >= profile_critical.media_time \
        and avg_attempts >= profile_critical.media_attempts:
            critical.append([name, avg_grade, avg_time, avg_attempts, "Critical"])

        else:
            if (profile_good.media_grade >= avg_grade >= profile_critical.media_grade):
                regular.append([name, avg_grade, avg_time, avg_attempts, "Regular"])
            elif (avg_grade >= profile_good.media_grade):
                good.append([name, avg_grade, avg_time, avg_attempts, "Good"])
            elif (avg_grade <= profile_critical.media_grade):
                critical.append([name, avg_grade, avg_time, avg_attempts, "Critical"])

            alert.append([name, avg_grade, avg_time, avg_attempts, "Alert"])

    return good, regular, alert, critical

def verify_student_in_list(student_name: str, student_list: list) -> bool:
    student_name = student_name.strip().lower()

    return any(student_name == student.strip().lower() for student in student_list)

def verify_student_is_outlier(username: str, student_list: list):
    username = username.strip().lower()
    for line in student_list:
        if line[0].strip().lower() == username:
            return True
    return False

def categorize_outliers(student_averages, good, regular, alert, critical):
    outliers = []
    
    for name, averages in student_averages.items():
        avg_grade = averages['average_grade']
        avg_time = averages['average_time']
        avg_attempts = averages['average_attempts']
        
        if avg_grade < 1 or avg_attempts > 4 or avg_time > 1200:
            outliers.append([name, avg_grade, avg_time, avg_attempts, "Outlier"])
        
    return outliers

if __name__ == "__main__":
    all_students = []

    clusters = get_clusters(clustering=False)
    student_attempts = group_attempts_by_student(clusters)
    student_averages = calculate_student_averages(student_attempts)

    good, regular, alert, critical = categorize_students(student_averages)
    outliers = categorize_outliers(student_averages, good, regular, alert, critical)

    for student in good:
        if not verify_student_is_outlier(student[0], outliers):
            all_students.append(student)

    for student in regular:
        if not verify_student_is_outlier(student[0], outliers):
            all_students.append(student)

    for student in critical:
        if not verify_student_is_outlier(student[0], outliers):
            all_students.append(student)

    for student in alert:
        if not verify_student_is_outlier(student[0], outliers):
            all_students.append(student)

    df_all = pd.DataFrame({
        "Nome_do_usuario": [line[0] for line in all_students],
        "Nota": [line[1] for line in all_students],
        "Tempo": [line[2] for line in all_students],
        "Tentativas": [line[3] for line in all_students],
        "Categoria": [line[4] for line in all_students]
    })

    palette = {
        'Good': 'green',
        'Regular': 'blue',
        'Alert': 'orange',
        'Critical': 'red' 
    }

    pl.figure(figsize=(8, 6))
    sb.scatterplot(x='Nota', y='Tempo', data=df_all, palette=palette, hue='Categoria')

    pl.title('Relação entre Nota e Tempo', fontsize=16)
    pl.xlabel('Nota', fontsize=12)
    pl.ylabel('Tempo (segundos)', fontsize=12)

    pl.savefig("Nota x Tempo.png")
    pl.show()

    pl.figure(figsize=(8, 6))
    sb.scatterplot(x='Nota', y='Tentativas', data=df_all, palette=palette, hue='Categoria')

    pl.title('Relação entre Nota e Tentativas', fontsize=16)
    pl.xlabel('Nota', fontsize=12)
    pl.ylabel('Tentativas', fontsize=12)

    pl.savefig("Nota x Tentativas.png")
    pl.show()

    sb.pairplot(df_all, hue='Categoria', palette=palette).savefig("Categorias_Geral.png")
    pl.show()



