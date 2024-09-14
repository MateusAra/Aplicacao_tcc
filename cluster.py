import numpy as np
import pandas as pd
import matplotlib.pyplot as pl
import seaborn as sb
from sklearn.cluster import KMeans


def get_clusters(clusterize: bool = False):
    if clusterize:
        data_frame = pd.read_excel("dataframe.v2_kmeans.xlsx", sheet_name="dataframe.v1_formated")

        kmeans = KMeans(n_clusters=4, random_state=0)

        data_frame = data_frame.drop("Atividade", axis=1)
        data_frame = data_frame.drop("Nome_do_usuario", axis=1)
        data_frame = data_frame.dropna()

        X = np.array(data_frame)
        labels = kmeans.fit(X).labels_
        data_frame["K-classes"] = labels

        return data_frame.values.tolist()
    else:
        data_frame = pd.read_csv("dataframe.quizes.csv")
        return data_frame.values.tolist()


def get_media_time(quiz: int, clusters: list):
    count = 0
    quiz_time = 0

    for line in clusters:
        if int(line[3]) == quiz:
            count += 1
            quiz_time += line[9]

    if count == 0:
        count = 1

    return int(quiz_time) / int(count)


def get_media_attempts(quiz: int, clusters: list):
    count = 0
    attempts = 0

    for line in clusters:
        if int(line[3]) == quiz:
            count += 1
            attempts += line[1]

    if count == 0:
        count = 1

    return int(attempts) / int(count)


def get_students_in_alert(clusters: list):
    alerts = []
    alert_not_duplicated = []

    for line in clusters:
        # Media de conclusão de uma tentativa está 20% acima ou abaixo da média de tempo de conclusão do quiz
        # E a quantidade de tentativas realizadas é maior que média de tentativas
        if line[10] != 1 and line[10] != 0:
            media_time = get_media_time(line[3], clusters)
            media_time_above = (line[9] * (20 / 100)) + media_time
            media_time_below = media_time - (line[9] * (20 / 100))
            media_attempts = get_media_attempts(line[3], clusters)

            if line[9] >= media_time_above or line[9] <= media_time_below:
                alerts.append(line)
            if line[1] > media_attempts:
                alerts.append(line)

    return alerts


def get_students_in_critical_state(clusters: list):
    critical = []
    # Lista de alunos que estão na classe 1 ou 0,
    # Media de conclusão de uma tentativa está 50% acima da média de tempo de conclusão do quiz
    # E a quantidade de tentativas realizadas é maior ou igual a quantidade media de tentativas
    for line in clusters:
        media_time = get_media_time(line[2], clusters)
        media_time_attempt = (line[9] * (50 / 100)) + media_time
        media_attempts = get_media_attempts(line[2], clusters)

        if line[10] != 2 or line[10] != 3 \
        and line[9] >= media_time_attempt \
        and line[1] >= media_attempts:
            critical.append(line)

def get_students_in_good_state(clusters: list):
    good = []
    # Lista de alunos que estão na classe 2 ou 3,
    # Media de conclusão de uma tentativa está abaixo da média de tempo de conclusão do quiz
    # E a quantidade de tentativas realizadas é menor a quantidade media de tentativas
    for line in clusters:
        media_time = get_media_time(line[2], clusters)
        media_attempts = get_media_attempts(line[2], clusters)

        if line[10] != 1 or line[10] != 0 \
        and line[1] < media_attempts \
        and line[9] < media_time:
            good.append(line)

def get_students_in_regular_state(clusters: list):
    regular = []
    # Lista de alunos que estão na classe 2 ou 3,
    # Media de conclusão de uma tentativa está menor ou igual da média de tempo de conclusão do quiz
    # E a quantidade de tentativas realizadas é menor ou igual a quantidade media de tentativas
    for line in clusters:
        media_time = get_media_time(line[2], clusters)
        media_attempts = get_media_attempts(line[2], clusters)

        if line[10] != 1 or line[10] != 0 \
        and line[1] <= media_attempts \
        and line[9] <= media_time:
            regular.append(line)

if __name__ == "__main__":
    
    clusters = get_clusters()

    alert = get_students_in_alert(clusters)
    critical = get_students_in_critical_state(clusters)
    good = get_students_in_good_state(clusters)
    regular = get_students_in_regular_state(clusters)
    

    print("\nAlunos em alerta:")

    df = pd.DataFrame({
        "Tentativas_Feitas": [line[1] for line in alert],
        "Tentativas_Permitidas": [line[2] for line in alert],
        "Quiz": [line[3] for line in alert],
        "Nota": [line[4] for line in alert],
        "UserId": [line[5] for line in alert],
        "Estado": [line[6] for line in alert],
        "Tipo_de_atividade": [line[7] for line in alert],
        "Secao": [line[8] for line in alert],
        "Tempo": [line[9] for line in alert],
        "Classe": [line[10] for line in alert],
    })

    print(df)
    print("\nProcesso finalizado com sucesso!")
