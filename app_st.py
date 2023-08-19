
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import datetime

def plot_kde_renda(data, tipo):
    """Generate a KDE plot for a given modalidade value."""

    # Plotting the KDE
    #palette = {"evasão": "red", "outro": "blue"}
    plt.figure(figsize=(12, 6))

    if tipo == 4:
        sns.histplot(data=data, x="Renda Per Capita", hue="Situação no Curso",
                     common_norm=True, kde=True) #, palette=palette)
        plt.ylabel("Contagem")
    if tipo == 6:
        sns.histplot(data=data, x="Renda Per Capita", hue="Situação no Curso",
                     element="step", stat="density", kde=True, common_norm=False) #, palette=palette)  
        plt.ylabel("Densidade")  
    
    # Configurar as marcas no eixo x
    x_start = 0  
    x_end = data['Renda Per Capita'].max() + 0.25  
    x_step = 0.25
    plt.xticks(np.arange(x_start, x_end, x_step), rotation=90)

    plt.title(f"Distribuição da Renda por Situação do Curso")
    plt.xlabel("Renda")
    
    plt.tight_layout()
    st.pyplot(plt)

def plot_boxplot_renda(data):
    plt.figure(figsize=(12, 6))

    sns.violinplot(data=data, x="Situação no Curso", y="Renda Per Capita", hue="Tipo de Escola de Origem", split=True)

    plt.title(f"Violino da Renda por Situação no Curso e Tipo de Escola de Origem")
    #plt.xlabel("Renda")
    #plt.ylabel("Densidade")
    #plt.tight_layout()
    st.pyplot(plt)

def show_filtros(df):
    # Filtros
    st.sidebar.header("Filtros")
    modalidade_value = st.sidebar.selectbox('Modalidade', options=['Todos'] + list(df['Modalidade'].unique()))
    campus = st.sidebar.selectbox('Campus', options=['Todos'] + list(df['Campus'].unique()))
    curso = st.sidebar.selectbox('Curso', options=['Todos'] + list(df['curso'].unique()))
    desc_curso = st.sidebar.selectbox('Descrição do Curso', options=['Todos'] + list(df['Descrição do Curso'].unique()))
    ano_conclusao = st.sidebar.selectbox('Ano Letivo de Previsão de Conclusão', options=['Todos'] + list(df['Ano Letivo de Previsão de Conclusão'].unique()))
    ano_ingresso = st.sidebar.selectbox('Ano de Ingresso', options=['Todos'] + list(df['Ano de Ingresso'].unique()))
    periodo_atual = st.sidebar.selectbox('Período Atual', options=['Todos'] + list(df['Período Atual'].unique()))
    tipo_escola = st.sidebar.selectbox('Tipo de Escola de Origem', options=['Todos'] + list(df['Tipo de Escola de Origem'].unique()))

    return {"modalidade_value": modalidade_value, 
            "campus": campus, 
            "curso": curso, 
            "desc_curso": desc_curso, 
            "ano_conclusao": ano_conclusao, 
            "ano_ingresso": ano_ingresso, 
            "periodo_atual": periodo_atual, 
            "tipo_escola": tipo_escola}

def apply_filtros(df, var):
    # Filtrar os dados com base nos valores selecionados

    #st.write(var)

    filtered_data = df.copy()
    if var['campus'] != 'Todos':
        filtered_data = filtered_data[filtered_data['Campus'] == var['campus']]
    if var['curso'] != 'Todos':
        filtered_data = filtered_data[filtered_data['curso'] == var['curso']]
    if var['desc_curso'] != 'Todos':
        filtered_data = filtered_data[filtered_data['Descrição do Curso'] == var['desc_curso']]
    if var['ano_conclusao'] != 'Todos':
        filtered_data = filtered_data[filtered_data['Ano Letivo de Previsão de Conclusão'] == var['ano_conclusao']]
    if var['ano_ingresso'] != 'Todos':
        filtered_data = filtered_data[filtered_data['Ano de Ingresso'] == var['ano_ingresso']]
    if var['periodo_atual'] != 'Todos':
        filtered_data = filtered_data[filtered_data['Período Atual'] == var['periodo_atual']]
    if var['modalidade_value'] != 'Todos':
        filtered_data = filtered_data[filtered_data['Modalidade'] == var['modalidade_value']]
    if var['tipo_escola'] != 'Todos':
        filtered_data = filtered_data[filtered_data['Tipo de Escola de Origem'] == var['tipo_escola']] 

    return filtered_data
        

# Load the data
df = pd.read_csv("merge2018-tratado.csv")

# Remove all values from "Tipo de Escola de Origem" that are not "Pública" or "Privada"
df = df[df['Tipo de Escola de Origem'].isin(['Pública', 'Privada'])]

# Define the options for the attribute selection
attributes_options = ['Código Curso', 'Campus', 'curso', 'Descrição do Curso', 
                      'Ano Letivo de Previsão de Conclusão', 'Ano de Ingresso', 
                      'Período Atual', 'Modalidade', 'Tipo de Escola de Origem']

# Tabs
tabs = [
    "Sobre", 
    "Evasão/Retenção: Geral", 
    "Evasão/Retenção: Detalhado", 
        "Evasão/Retenção: Renda", 
        "Evasão: Motivação", 
        "Egressos: Avaliação do Curso", 
        ]

selected_tab = st.sidebar.radio("Escolha uma aba:", tabs)

if selected_tab == "Sobre":
    qnt_registros = st.sidebar.slider('Selecione o número de registros:', 0, 1000, 10, 10)
    vars_filtros = show_filtros(df)

    st.title("Exibição dos dados")

    # Botão "Visualizar"
    if st.button('Visualizar'):
        filtered_data = apply_filtros(df, vars_filtros)
        st.write(filtered_data.drop('Unnamed: 0', axis='columns').head(qnt_registros))

elif selected_tab == "Evasão/Retenção: Geral":
    st.title("Evasão/Retenção: Geral")

    # Add multiselect for the user to choose filters (with "Nenhum" option)
    situacoes_to_display = st.sidebar.multiselect('Selecione as situações a serem exibidas:', list(df['Situação no Curso'].unique()))

    # Add a selectbox for the user to choose between absolute values and percentage
    values_or_percentage = st.sidebar.selectbox('Selecione a forma de exibição:', ['Valores Absolutos', 'Porcentagem'])

    modalidade = st.sidebar.selectbox('Selecione a modalidade:', ['Todos'] + list(df['Modalidade'].unique()))
    tipo_escola_origem = st.sidebar.selectbox('Selecione o tipo de escola de origem:', ['Todos'] + list(df['Tipo de Escola de Origem'].unique()))

    # Apply filters based on the selected options (skip if "Todos" is selected)
    if modalidade != 'Todos':
        df = df[df['Modalidade'] == modalidade]
    if tipo_escola_origem != 'Todos':
        df = df[df['Tipo de Escola de Origem'] == tipo_escola_origem]

    # Add selectbox for the user to choose one attribute
    attribute1 = st.sidebar.selectbox('Selecione o atributo:', attributes_options)

    # Add a "Visualizar" button
    visualizar = st.button('Visualizar')

    # Variable to store table data
    table_data = None

    # If the "Visualizar" button is pressed
    if visualizar:
        fig, ax = plt.subplots(figsize=(15, 10))

        if values_or_percentage == 'Valores Absolutos':
            plot = sns.countplot(data=df, x=attribute1, hue='Situação no Curso', order=df[attribute1].value_counts().index, hue_order=situacoes_to_display, ax=ax)
            table_data = df.groupby(attribute1)['Situação no Curso'].value_counts().unstack().fillna(0)
        else:
            # For percentage, we need to adjust the data
            total_counts = df[attribute1].value_counts()
            status_counts = df.groupby(attribute1)['Situação no Curso'].value_counts()
            status_percentage = status_counts.div(total_counts, level=0) * 100
            status_percentage = status_percentage.reset_index(name='Percentage')
            plot = sns.barplot(data=status_percentage, x=attribute1, y='Percentage', hue='Situação no Curso', order=df[attribute1].value_counts().index, hue_order=situacoes_to_display, ax=ax)
            table_data = status_percentage.pivot(index=attribute1, columns='Situação no Curso', values='Percentage')

        ax.set_title('Situação no Curso por ' + attribute1)
        ax.set_xlabel(attribute1)
        ax.set_ylabel('Quantidade' if values_or_percentage == 'Valores Absolutos' else 'Percentual (%)')
        ax.legend(title='Situação no Curso')

        # Display the values on top of each bar
        for p in plot.patches:
            plot.annotate(format(p.get_height(), '.1f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points')

        # Show the plot
        st.pyplot(fig)

        # Add totals to the table data
        if table_data is not None:
            table_data['Total'] = table_data.sum(axis=1)
            table_data.loc['Total'] = table_data.sum()
            st.write(table_data)

elif selected_tab == "Evasão/Retenção: Detalhado":
    
    st.title("Evasão/Retenção: Detalhado")

    st.sidebar.header("Visualização")
    # Situação do curso
    situations = st.sidebar.multiselect('Selecione as situações do curso:', df['Situação no Curso'].unique())

    # Valores absolutos ou porcentagem
    values_or_percentage = st.sidebar.selectbox('Selecione a forma de exibição:', ['Valores Absolutos', 'Porcentagem'])
    
    st.sidebar.header("Interação variáveis")
    # Seleção de atributos para interação
    attribute1 = st.sidebar.selectbox('Seleção do atributo 1:', attributes_options)
    attribute_values_1 = st.sidebar.multiselect(f'Valores para {attribute1}:', df[attribute1].unique())
    
    attribute2 = st.sidebar.selectbox('Seleção do atributo 2:', attributes_options)
    if attribute_values_1:
        df_filtered_by_attr1 = df[df[attribute1].isin(attribute_values_1)]
        attribute_values_2 = st.sidebar.multiselect(f'Valores para {attribute2} (baseado em {attribute1}):', df_filtered_by_attr1[attribute2].unique())
    else:
        attribute_values_2 = []

    # Botão para visualizar
    if st.button('Visualizar'):
        if attribute_values_1 and attribute_values_2 and situations:
            fig, ax = plt.subplots(figsize=(15, 10))
            data = df[df[attribute1].isin(attribute_values_1) & df[attribute2].isin(attribute_values_2) & df['Situação no Curso'].isin(situations)]
            if values_or_percentage == 'Valores Absolutos':
                sns.countplot(data=data, x=attribute2, hue='Situação no Curso', ax=ax)
            else:
                # This will be a bit complex for percentage, as we'll need to compute the percentage per each situation
                data_grouped = data.groupby([attribute2, 'Situação no Curso']).size().unstack(fill_value=0)
                total = data.groupby(attribute2).size()
                data_percentage = (data_grouped.divide(total, axis=0) * 100).fillna(0)
                data_percentage.plot(kind='bar', stacked=False, ax=ax)
            
            ax.set_title(f'{attribute1} por {attribute2}')
            ax.set_xlabel(attribute2)
            ax.set_ylabel('Count' if values_or_percentage == 'Valores Absolutos' else 'Percentage (%)')
            for container in ax.containers:
                ax.bar_label(container)
            st.pyplot(fig)
            
            # Exibindo a tabela
            table = data.groupby([attribute2, 'Situação no Curso']).size().unstack().fillna(0)
            table['Total'] = table.sum(axis=1)
            table.loc['Total'] = table.sum()
            st.write(table)
        else:
            st.warning("Por favor, selecione valores para os atributos e situações.")

elif selected_tab == "Evasão/Retenção: Renda":
    st.title("Distribuição da Renda por Situação da Matrícula")

    # Visualizacao no sidebar
    st.sidebar.header("Visualização")
    situacao_curso = st.sidebar.multiselect('Situação no Curso', options=list(df['Situação no Curso'].unique()))
    
    # Filtros
    vars_filtros = show_filtros(df)

    # Botão "Visualizar"
    if st.button('Visualizar'):
        # Filtrar os dados com base nos valores selecionados
        filtered_data = apply_filtros(df, vars_filtros)

        if situacao_curso:
            filtered_data = filtered_data[filtered_data['Situação no Curso'].isin(situacao_curso)]


        # Chamar a função para gerar o gráfico
        plot_kde_renda(filtered_data, 4)
        plot_kde_renda(filtered_data, 6)
        plot_boxplot_renda(filtered_data)

elif selected_tab == "Evasão: Motivação":

    st.title("Evasão: Motivação")
    
    #quantidade de motivos
    qnt_registros = st.sidebar.slider('Selecione o número de registros:', 2, 20, 2)

    # Filtros
    vars_filtros = show_filtros(df)
    
    # Botão "Visualizar"
    if st.button('Visualizar'):
    
        # Filtrar os dados com base nos valores selecionados
        filtered_data = apply_filtros(df, vars_filtros)

        # Concatenar os motivos de ocorrência em uma única série
        all_motives = pd.concat([
            filtered_data["Principal motivo da ocorrência_2"],
            filtered_data["Motivo secundário da ocorrência"],
            filtered_data["Motivo terciário da ocorrência"]
        ])
        
        # Calcular a contagem de cada motivo único
        motive_counts = all_motives.value_counts()
        
        # Selecionar os 10 motivos com a maior contagem
        top_10_motives = motive_counts.nlargest(qnt_registros)
                
        plt.bar(top_10_motives.index, top_10_motives.values)
        plt.xlabel('Motivos da Ocorrência')
        plt.ylabel('Contagem')
        plt.title(f'Contagem dos {qnt_registros} Principais Motivos de Ocorrência')
        plt.xticks(rotation=45, ha='right')
        st.pyplot(plt)

elif selected_tab == "Egressos: Avaliação do Curso":

    st.title("Egressos: Avaliação do Curso")

    # Filtros
    vars_filtros = show_filtros(df)
    
    # Sidebar
    eg_columns = ['CURSO_ENSINO_APRENDIZAGEM', 'CURSO_HABIL_COMPETE', 'CURSO_TEORIA', 
                  'CURSO_PRATICA', 'CURSO_AVALIACAO', 'CURSO_VIDA_PROFISSAO', 
                  'CURSO_PERSPECTIVAS', 'CURSO_VIDA_QUALIDADE']
    
    st.sidebar.header('Filtro de colunas do Egresso')
    options = st.sidebar.selectbox('Escolha a coluna para visualizar', eg_columns)

    # Filters
    #attribute_values_1 = st.sidebar.multiselect(f'Valores para {options}:', df[options].unique())

    hue_columns = ['Campus', 'curso', 'Descrição do Curso', 'Ano Letivo de Previsão de Conclusão', 
                   'Ano de Ingresso', 'Período Atual', 'Modalidade', 'Tipo de Escola de Origem']

    # Hue parameter
    hue_option = st.sidebar.selectbox('Escolha o atributo para o agregar (opcional)', ['Nenhum'] + hue_columns)

    # Botão "Visualizar"
    if st.button('Visualizar'):

        # Filtrar os dados com base nos valores selecionados
        filtered_data = apply_filtros(df, vars_filtros)

        # Display a bar plot
        fig, ax = plt.subplots(figsize=(10,5))
        if hue_option != 'Nenhum':
            plot = sns.countplot(data=filtered_data, x=options, hue=hue_option, ax=ax)
        else:
            plot = sns.countplot(data=filtered_data, x=options, ax=ax)

        plot.set_xticklabels(plot.get_xticklabels(), rotation=90)

        # Add the values on top of each bar
        for p in plot.patches:
            plot.annotate(format(p.get_height(), '.0f'), 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha = 'center', 
                        va = 'center', 
                        xytext = (0, 10), 
                        textcoords = 'offset points')

        st.pyplot(fig)

        
