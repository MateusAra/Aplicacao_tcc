import numpy as np
import pandas as pd
import matplotlib.pyplot as pl
import seaborn as sb
from sklearn.cluster import KMeans


def get_clusters(clusterize: bool = False):
    if clusterize:
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

def get_media_time(quiz: int, clusters: list):
    count = 0
    quiz_time = 0

    for line in clusters:
        if int(line[3]) == quiz:
            count += 1
            quiz_time += line[10]

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
        classe = int(line[11])
        if (classe != 1 and classe != 0):
            media_time = get_media_time(line[3], clusters)
            media_time_above = (float(line[10]) * (20 / 100)) + media_time
            media_time_below = media_time - (float(line[10]) * (20 / 100))
            media_attempts = get_media_attempts(line[3], clusters)

            note = float(line[4])
            attemps_realizaded = int(line[1])
            time = int(line[10])

            if (time >= media_time_above or time <= media_time_below) \
            and (attemps_realizaded > media_attempts):
                alerts.append(line)
    
    for line in alerts:
        if line not in alert_not_duplicated:
            alert_not_duplicated.append(line)
            
    return alert_not_duplicated

def get_students_in_critical_state(clusters: list):
    critical = []
    critical_not_duplicated = []
    # Lista de alunos que estão na classe 1 ou 0,
    # Media de conclusão de uma tentativa está 30% acima da média de tempo de conclusão do quiz
    # E a quantidade de tentativas realizadas é maior ou igual a quantidade media de tentativas
    for line in clusters:
        media_time = get_media_time(line[3], clusters)
        media_time_attempt = (float(line[10]) * (30 / 100)) + media_time
        media_attempts = get_media_attempts(line[3], clusters)

        note = float(line[4])
        classe = int(line[11])
        attemps_realizaded = int(line[1])
        time = int(line[10])

        if (classe != 2 and classe != 3) \
        and (time >= media_time_attempt) \
        and (attemps_realizaded >= media_attempts) \
        and (note < 5000.00):
            critical.append(line)
    
    for line in critical:
        if line not in critical:
            critical_not_duplicated.append(line)

    return critical_not_duplicated

def get_students_in_good_state(clusters: list):
    good = []
    good_not_duplicated = []
    # Lista de alunos que estão na classe 2 ou 3,
    # Media de conclusão de uma tentativa está abaixo da média de tempo de conclusão do quiz
    # E a quantidade de tentativas realizadas é menor a quantidade media de tentativas
    for line in clusters:
        media_time = get_media_time(line[3], clusters)
        media_attempts = get_media_attempts(line[3], clusters)

        note = float(line[4])
        classe = int(line[11])
        attemps_realizaded = int(line[1])
        time = int(line[10])
 
        if (classe != 1 and classe != 0) \
        and (attemps_realizaded < media_attempts) \
        and (time < media_time) and (note >= 9000.00):
            good.append(line)

    for line in good:
        if line not in good_not_duplicated:
            good_not_duplicated.append(line)

    return good_not_duplicated

def get_students_in_regular_state(clusters: list):
    regular = []
    regular_not_duplicated = []
    # Lista de alunos que estão na classe 2 ou 3,
    # Media de conclusão de uma tentativa está menor ou igual da média de tempo de conclusão do quiz
    # E a quantidade de tentativas realizadas é menor ou igual a quantidade media de tentativas
    for line in clusters:
        media_time = get_media_time(line[3], clusters)
        media_attempts = get_media_attempts(line[3], clusters)

        note = float(line[4])
        classe = int(line[11])
        attemps_realizaded = int(line[1])
        time = int(line[10])

        if (classe != 1 and classe != 0 \
        and (attemps_realizaded <= media_attempts) \
        and (time <= media_time) 
        and (note >= 7000.00 and note <= 8900.00)):
            regular.append(line)
    
    for line in regular:
        if line not in regular_not_duplicated:
            regular_not_duplicated.append(line)
    
    return regular_not_duplicated

if __name__ == "__main__":

    clusters = get_clusters(clusterize=False)

    alert = get_students_in_alert(clusters)
    critical = get_students_in_critical_state(clusters)
    good = get_students_in_good_state(clusters)
    regular = get_students_in_regular_state(clusters)
    

    print("\nAlunos em alerta:")

    df_alert = pd.DataFrame({
        "Nome_do_usuario": [line[5] for line in alert],
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
