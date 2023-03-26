# importa os Arquivos da URL e os salvam na pasta src
import pandas as pd

def data_import_save(url =  "https://raw.githubusercontent.com/alura-cursos/ML_Classificacao_por_tras_dos_panos/main/Dados/Customer-Churn.csv", 
                         savepath = '..\\src\\data\\churn_detection_raw.csv'):
    df_temp = pd.read_csv(url)
    df_temp.to_csv(savepath)
    return df_temp

# uma fiunção que retorna os valores unicos e a quantidade de cada coluna 
def info_dados(df):
    columns = df.columns
    values = []
    
    for column in columns:
        tipo_dado = str(df[column].dtype)
        unico_dado = df[column].unique().shape[0]
        values.append([column,tipo_dado,unico_dado])
#         print(f'Column: {column}')
#         print(df[column].unique(), f'Shape: {df[column].unique().shape[0]}', df[column].dtype)
    return values
        
# procura coluna com numeros inteiros que tenham apenas zeros e uns e os transforma em uint8
def zeroum_to_uint8(df):
    for column in df.columns:
        if (str(df[column].dtype).startswith('int') or str(df[column].dtype).startswith('float')) and df[column].unique().sum() == 1:
            df[column] = df[column].astype('uint8')

# aplica o get dummies em cada coluna separadamente, retorna uma data frame sem os ultimos valores dos dummies            
def get_dummies_drop_last(df):
    columns = df.columns
    df_aux = pd.DataFrame()
    for column in columns:
        df_tmp = pd.get_dummies(df[[column]])
        if df_tmp.columns.shape[0]>=2:
            df_aux = pd.concat([df_aux,df_tmp.drop(df_tmp.columns[-1], axis=1)],axis=1)
        else:
            df_aux = pd.concat([df_aux,df_tmp], axis=1)
    return df_aux        