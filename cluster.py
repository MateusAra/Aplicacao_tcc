import numpy as np
import pandas as pd
import matplotlib.pyplot as pl
import seaborn as sb
from sklearn.cluster import KMeans
from Profiles import *

def verify_student_in_list(username: str, student_list: list):
    for line in student_list:
        if line[0] == username:
            return True
    return False

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
        return data_frame.values.tolist()

def get_students_in_alert(clusters: list):
    alerts = []
    profile = Profile.get_profile_critical()
    percentage_of_failed_students = 8.25
    for line in clusters:
        # Media de conclusão de uma tentativa está 29% acima ou abaixo da média de tempo do perfil de alunos reprovados
        # E a quantidade de tentativas realizadas é maior que média de tentativas do perfil de alunos reprovados
        kmeans_classe = int(line[11])
        if (kmeans_classe != 1 and kmeans_classe != 0): 
            media_time_above = (float(line[10]) * (percentage_of_failed_students / 100)) + profile.media_time
            media_time_below = profile.media_time - (float(line[10]) * (percentage_of_failed_students / 100))
            attempts_realized = int(line[1])
            time = int(line[10])

            if (time >= media_time_above or time <= media_time_below) \
            and (attempts_realized >= profile.media_attempts):
                name = line[5]
                email = line[12]
                grade = line[4]
                quiz = line[0]
                section = line[9]
                type_quiz = line[8]
                student = [name, email, grade, quiz, section, type_quiz, "Alert"]

                if student not in alerts:
                    alerts.append(student)
            
    return alerts

def get_students_in_critical_state(clusters: list):
    critical = []
    profile = Profile.get_profile_critical()
    # Lista de alunos que estão na classe 1 ou 0,
    # Media de conclusão de uma tentativa está acima da média de tempo do perfil de alunos reprovados
    # E a quantidade de tentativas realizadas é maior ou igual a quantidade media de tentativas
    # Do perfil de alunos reprovados
    for line in clusters:

        grade = float(line[4])
        kmeans_classe = int(line[11])
        attempts_realized = int(line[1])
        time = int(line[10])

        if (kmeans_classe != 2 and kmeans_classe != 3) \
        and (time >= profile.media_time) \
        and (attempts_realized >= profile.media_attempts) \
        and (grade <= profile.media_grade):
            name = line[5]
            email = line[12]
            grade = line[4]
            quiz = line[0]
            section = line[9]
            type_quiz = line[8]
            student = [name, email, grade, quiz, section, type_quiz, "Critical"]

            if student not in critical:
                critical.append(student)

    return critical

def get_students_in_good_state(clusters: list, critical: list):
    good = []
    profile = Profile.get_profile_good()
    # Lista de alunos que estão na classe 2 ou 3,
    # Media de conclusão de uma tentativa está abaixo da média de tempo de conclusão do quiz
    # E a quantidade de tentativas realizadas é menor a quantidade media de tentativas
    for line in clusters:
        
        grade = float(line[4])
        classe = int(line[11])
        attempts_realized = int(line[1])
        time = int(line[10])
 
        if (classe != 1 and classe != 0) \
        and (attempts_realized < profile.media_attempts) \
        and (time < profile.media_time) \
        and (grade >= profile.media_grade):
            name = line[5]
            email = line[12]
            grade = line[4]
            quiz = line[0]
            section = line[9]
            type_quiz = line[8]
            student = [name, email, grade, quiz, section, type_quiz, "Good"]

            is_critical = verify_student_in_list(name, critical)

            if (student not in good and not is_critical):
                good.append(student)

    return good

def get_students_in_regular_state(clusters: list, critical: list, good: list):
    regular = []
    profile_regular = Profile.get_profile_regular()
    profile_good = Profile.get_profile_good()
    # Lista de alunos que estão na classe 2 ou 3,
    # Media de conclusão de uma tentativa está menor ou igual da média de tempo de conclusão do 
    # perfil de alunos regulares
    # E a quantidade de tentativas realizadas é menor ou igual a quantidade media de tentativas do 
    # perfil de alunos regulares
    for line in clusters:

        grade = float(line[4])
        classe = int(line[11])
        attempts_realized = int(line[1])
        time = int(line[10])

        if (classe != 1 and classe != 0 \
        and (attempts_realized <= profile_regular.media_attempts) \
        and (time <= profile_regular.media_time) \
        and (grade > profile_regular.media_grade and grade < profile_good.media_grade)):
            name = line[5]
            email = line[12]
            grade = line[4]
            quiz = line[0]
            section = line[9]
            type_quiz = line[8]
            student = [name, email, grade, quiz, section, type_quiz, "Regular"]
            
            is_critical = verify_student_in_list(name, critical)
            is_good = verify_student_in_list(name, good)

            if (student not in regular and not is_critical and not is_good):
                regular.append(student)
    
    return regular

if __name__ == "__main__":
    general = []

    clusters = get_clusters(clustering=False)

    alert = get_students_in_alert(clusters)
    critical = get_students_in_critical_state(clusters)
    good = get_students_in_good_state(clusters, critical)
    regular = get_students_in_regular_state(clusters, critical, good)
    
    general.extend(alert)
    general.extend(critical)
    general.extend(good)
    general.extend(regular)

    df_general = pd.DataFrame({
        "Nome_do_usuario": [line[0] for line in general],
        "Email": [line[1] for line in general],
        "Nota": [line[2] for line in general],
        "Nome_da_atividade": [line[3] for line in general],
        "Secao": [line[4] for line in general],
        "Tipo_de_atividade": [line[5] for line in general],
        "Categoria": [line[6] for line in general]
    })

    sb.pairplot(df_general, 
                hue="Categoria", 
                palette=["m", "y", "g"]).savefig("Categorias.png")

    print("\nProcesso finalizado com sucesso!")
