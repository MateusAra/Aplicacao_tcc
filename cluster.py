import numpy as np
import pandas as pd
import matplotlib.pyplot as pl
import seaborn as sb
from sklearn.cluster import KMeans
from Profiles import *


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
                alerts.append(line)
            
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
            critical.append(line)

    return critical

def get_students_in_good_state(clusters: list):
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
            good.append(line)

    return good

def get_students_in_regular_state(clusters: list):
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
            regular.append(line)
    
    return regular

if __name__ == "__main__":

    clusters = get_clusters(clustering=False)

    alert = get_students_in_alert(clusters)
    critical = get_students_in_critical_state(clusters)
    good = get_students_in_good_state(clusters)
    regular = get_students_in_regular_state(clusters)
    
    df_alert = pd.DataFrame({
        "Nome_do_usuario": [line[5] for line in alert],
        "Identificador_do_usuario": [line[6] for line in alert],
        "Nome_da_atividade": [line[0] for line in alert],
        "Email": [line[12] for line in alert],
        "Nota": [line[4] for line in alert],
        "Tentativa_realizada": [line[1] for line in alert],
        "Tipo_de_atividade": [line[8] for line in alert],
        "Secao": [line[9] for line in alert],
        "Tempo": [line[10] for line in alert],
        "Classe": [line[11] for line in alert],
    })

    df_critical = pd.DataFrame({
        "Nome_do_usuario": [line[5] for line in critical],
        "Identificador_do_usuario": [line[6] for line in critical],
        "Nome_da_atividade": [line[0] for line in critical],
        "Email": [line[12] for line in critical],
        "Nota": [line[4] for line in critical],
        "Tentativa_realizada": [line[1] for line in critical],
        "Tipo_de_atividade": [line[8] for line in critical],
        "Secao": [line[9] for line in critical],
        "Tempo": [line[10] for line in critical],
        "Classe": [line[11] for line in critical],
    })

    df_good = pd.DataFrame({
        "Nome_do_usuario": [line[5] for line in good],
        "Identificador_do_usuario": [line[6] for line in good],
        "Nome_da_atividade": [line[0] for line in good],
        "Email": [line[12] for line in good],
        "Nota": [line[4] for line in good],
        "Tentativa_realizada": [line[1] for line in good],
        "Tipo_de_atividade": [line[8] for line in good],
        "Secao": [line[9] for line in good],
        "Tempo": [line[10] for line in good],
        "Classe": [line[11] for line in good],
    })

    df_regular = pd.DataFrame({
        "Nome_do_usuario": [line[5] for line in regular],
        "Identificador_do_usuario": [line[6] for line in regular],
        "Nome_da_atividade": [line[0] for line in regular],
        "Email": [line[12] for line in regular],
        "Nota": [line[4] for line in regular],
        "Tentativa_realizada": [line[1] for line in regular],
        "Tipo_de_atividade": [line[8] for line in regular],
        "Secao": [line[9] for line in regular],
        "Tempo": [line[10] for line in regular],
        "Classe": [line[11] for line in regular],
    })

    html_alert = df_alert.to_html(index=False)
    html_critical = df_critical.to_html(index=False)
    html_good = df_good.to_html(index=False)
    html_regular = df_regular.to_html(index=False)

    with open("tabela_alunos_alerta.html", "w") as file:
        file.write(html_alert)

    with open("tabela_alunos_critical.html", "w") as file:
        file.write(html_critical)

    with open("tabela_alunos_good.html", "w") as file:
        file.write(html_good)  

    with open("tabela_alunos_regular.html", "w") as file:
        file.write(html_regular)

    print("Arquivos HTML salvos com sucesso!")
    print("\nProcesso finalizado com sucesso!")
