import pandas as pd
import os

def pregunta_01():
    file_path = 'files/input/solicitudes_de_credito.csv'
    DATOS = pd.read_csv(file_path, sep=';')

    if 'Unnamed: 0' in DATOS.columns:
        DATOS.drop('Unnamed: 0', axis=1, inplace=True)

    DATOS.dropna(inplace=True)
    DATOS.drop_duplicates(inplace=True)

    fechas = DATOS['fecha_de_beneficio'].str.split('/', expand=True)
    fechas.columns = ['día', 'mes', 'año']
    mask = fechas['año'].str.len() < 4
    fechas.loc[mask, ['día', 'año']] = fechas.loc[mask, ['año', 'día']].values
    DATOS['fecha_de_beneficio'] = fechas['año'] + '-' + fechas['mes'] + '-' + fechas['día']

    object_columns = ['sexo', 'tipo_de_emprendimiento', 'idea_negocio', 'línea_credito']
    DATOS[object_columns] = DATOS[object_columns].apply(lambda x: x.str.lower().replace(['-', '_'], ' ', regex=True).str.strip())
    DATOS['barrio'] = DATOS['barrio'].str.lower().replace(['-', '_'], ' ', regex=True)

    DATOS['monto_del_credito'] = DATOS['monto_del_credito'].str.replace(r'[$,\s]', '', regex=True)
    DATOS['monto_del_credito'] = pd.to_numeric(DATOS['monto_del_credito'], errors='coerce').fillna(0).astype(int).astype(str)

    DATOS.drop_duplicates(inplace=True)

    output_dir = 'files/output'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'solicitudes_de_credito.csv')
    DATOS.to_csv(output_path, sep=';', index=False)

    return DATOS.head()

dataframe_limpio = pregunta_01()
print(dataframe_limpio.head())
