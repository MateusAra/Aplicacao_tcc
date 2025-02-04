import numpy as np
import pandas as pd
import matplotlib.pyplot as pl
import seaborn as sb
from sklearn.cluster import KMeans
from Profiles import *
from collections import defaultdict
import plotly.express as px

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

        data = []

        for line in clusters:
            if line[9] <= 20:
                data.append(line)
        
        return data
    
def group_attempts_by_student(clusters):
    student_attempts = defaultdict(list)
    
    for line in clusters:
        name = line[5]
        student_attempts[name].append(line)
    
    return student_attempts

def calculate_student_averages(student_attempts):
    student_averages = {}

    for name, attempts in student_attempts.items():

        attempts_by_activity = {}
        for attempt in attempts:
            activity = attempt[0]
            activity_type = attempt[8] 
            if activity not in attempts_by_activity:
                attempts_by_activity[activity] = {
                    'type': activity_type,
                    'attempts': []
                }
            attempts_by_activity[activity]['attempts'].append(attempt)

        activity_averages = {}

        total_weighted_grade = 0
        total_weighted_time = 0
        total_weighted_attempts = 0
        total_activities = 0

        for activity, activity_data in attempts_by_activity.items():
            activity_attempts = activity_data['attempts']
            activity_type = activity_data['type']
            importance = activity_type + 1

            sorted_attempts = sorted(activity_attempts, key=lambda x: float(x[4]), reverse=True)
            best_attempts = []

            for attempt in sorted_attempts:
                if ((float(attempt[4]) >= 1000.00) and (int(attempt[1]) <= 4) and (int(attempt[10]) <= 1800)):
                    best_attempts.append(attempt)

            total_grade = sum(float(attempt[4]) for attempt in best_attempts)
            total_time = sum(int(attempt[10]) for attempt in best_attempts)
            total_attempts = sum(int(attempt[1]) for attempt in best_attempts)

            num_best_attempts = len(best_attempts) if best_attempts else 1

            average_grade = total_grade / num_best_attempts
            average_time = total_time / num_best_attempts
            average_attempts = total_attempts / num_best_attempts

            weighted_grade = average_grade * importance
            weighted_time = average_time * importance
            weighted_attempts = average_attempts * importance

            total_weighted_grade += weighted_grade
            total_weighted_time += weighted_time
            total_weighted_attempts += weighted_attempts
            total_activities += 1

            activity_averages[activity] = {
                'average_grade': average_grade,
                'average_time': average_time,
                'average_attempts': average_attempts,
                'importance': importance,
                'best_attempts': best_attempts
            }

        if total_activities > 0:
            general_average_grade = total_weighted_grade / total_activities
            general_average_time = total_weighted_time / total_activities
            general_average_attempts = total_weighted_attempts / total_activities
        else:
            general_average_grade = general_average_time = general_average_attempts = 0

        student_averages[name] = {
            'activities': activity_averages,
            'average_grade': general_average_grade,
            'average_time': general_average_time,
            'average_attempts': general_average_attempts
        }

    return student_averages

def categorize_students(student_averages):
    good = []
    regular = []
    alert = []
    critical = []
    list_of_recommended = []
    
    profile_good = Profile.get_profile_good()
    profile_regular = Profile.get_profile_regular()
    profile_critical = Profile.get_profile_critical()

    for name, averages in student_averages.items():
        avg_grade = averages['average_grade']
        avg_time = averages['average_time']
        avg_attempts = averages['average_attempts']

        if avg_grade <= 1000.00 or avg_attempts >= 4 or avg_time >= 1800:
            continue

        if avg_grade >= profile_good.media_grade \
        and avg_time <= profile_good.media_time \
        and avg_attempts <= profile_good.media_attempts:
            good.append([name, avg_grade, avg_time, avg_attempts, "Good"])

        elif profile_critical.media_grade <= avg_grade <= profile_good.media_grade \
        and profile_good.media_time <= avg_time <= profile_critical.media_time \
        and profile_good.media_attempts <= avg_attempts <= profile_critical.media_attempts:
            regular.append([name, avg_grade, avg_time, avg_attempts, "Regular"])

        elif avg_grade <= profile_critical.media_grade \
        and avg_time >= profile_critical.media_time \
        and avg_attempts >= profile_critical.media_attempts:
            critical.append([name, avg_grade, avg_time, avg_attempts, "Critical"])

        else:
            if (avg_grade <= profile_good.media_grade and avg_grade >= profile_critical.media_grade):
                regular.append([name, avg_grade, avg_time, avg_attempts, "Regular"])
            elif (avg_grade >= profile_good.media_grade):
                good.append([name, avg_grade, avg_time, avg_attempts, "Good"])
            elif (avg_grade <= profile_critical.media_grade):
                critical.append([name, avg_grade, avg_time, avg_attempts, "Critical"])

            alert.append([name, avg_grade, avg_time, avg_attempts, "Alert"])
        
        activity = averages['activities'].items()

        for activity, line in activity:
            for line in line['best_attempts']:
                if float(line[4]) < 7000.00:
                    list_of_recommended.append([name, line[12], line[1], line[4], line[9], line[8], line[3], line[6]])

    return good, regular, alert, critical, list_of_recommended

def verify_student_in_list(student_name: str, student_list: list) -> bool:
    student_name = student_name.strip().lower()

    return any(student_name == student.strip().lower() for student in student_list)

if __name__ == "__main__":
    all_students = []

    clusters = get_clusters(clustering=False)
    student_attempts = group_attempts_by_student(clusters)
    student_averages = calculate_student_averages(student_attempts)

    good, regular, alert, critical, list_of_recommended = categorize_students(student_averages)

    for student in good:
        all_students.append(student)

    for student in regular:
        all_students.append(student)

    for student in critical:
        all_students.append(student)

    for student in alert:
        all_students.append(student)

    df_all = pd.DataFrame({
        "Nome_do_usuario": [line[0] for line in all_students],
        "Nota": [line[1] for line in all_students],
        "Tempo": [line[2] for line in all_students],
        "Tentativas": [line[3] for line in all_students],
        "Categoria": [line[4] for line in all_students]
    })

    df_contents = pd.DataFrame({
        "Nome_do_usuario": [line[0] for line in list_of_recommended],
        "Email_do_usuario": [line[1] for line in list_of_recommended],
        "Tentativa": [line[2] for line in list_of_recommended],
        "Nota": [line[3] for line in list_of_recommended],
        "Secao": [line[4] for line in list_of_recommended],
        "Tipo": [line[5] for line in list_of_recommended],
        "Atividade": [line[6] for line in list_of_recommended],
        "Identificador_usuario": [line[6] for line in list_of_recommended]
    })

    #Relaciona as notas dos alunos com a quantidade de tentativas realizadas, separado por categoria.
    pl.figure(figsize=(8, 6))
    sb.scatterplot(x='Nota', y='Tentativas', data=df_all, hue='Categoria')

    pl.title('Relação entre Nota vs Tentativas', fontsize=16)
    pl.xlabel('Nota', fontsize=12)
    pl.ylabel('Tentativas', fontsize=12)

    pl.savefig("Nota x Tentativas.png")
    pl.show()

    #Visão geral do desempenho dos alunos, destacando as áreas com mais estudantes.
    sb.pairplot(df_all, hue='Categoria').savefig("Categorias_Geral.png")
    pl.show()

    #Visão geral dos conteudos a recomendar.
    sb.pairplot(df_contents, hue='Secao').savefig("Conteudos.png")
    pl.show()

    #Relaciona as notas dos alunos com o tempo gasto nas atividades, separado por categoria. 
    #Isso ajuda a entender como a quantidade de tempo investido influencia o 
    #desempenho dos alunos em diferentes categorias.
    pl.figure(figsize=(8, 6))
    sb.scatterplot(x='Nota', y='Tempo', data=df_all, hue='Categoria')

    pl.title('Relação entre Nota vs Tempo', fontsize=16)
    pl.xlabel('Nota', fontsize=12)
    pl.ylabel('Tempo (segundos)', fontsize=12)

    pl.savefig("Nota x Tempo.png")
    pl.show()



