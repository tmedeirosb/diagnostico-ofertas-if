
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
    if tipo == 6:
        sns.histplot(data=data, x="Renda Per Capita", hue="Situação no Curso",
                     element="step", stat="density", kde=True, common_norm=False) #, palette=palette)    
    
    # Configurar as marcas no eixo x
    x_start = 0  
    x_end = data['Renda Per Capita'].max() + 0.25  
    x_step = 0.25
    plt.xticks(np.arange(x_start, x_end, x_step), rotation=90)

    plt.title(f"Distribuição da Renda por Status ({modalidade_value})")
    plt.xlabel("Renda")
    plt.ylabel("Densidade")
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



# Load the data
df = pd.read_csv("merge2018-tratado.csv")

# Remove all values from "Tipo de Escola de Origem" that are not "Pública" or "Privada"
df = df[df['Tipo de Escola de Origem'].isin(['Pública', 'Privada'])]

# Define the options for the attribute selection
attributes_options = ['Código Curso', 'Campus', 'curso', 'Descrição do Curso', 'Ano Letivo de Previsão de Conclusão', 'Ano de Ingresso', 'Período Atual', 'Modalidade', 'Tipo de Escola de Origem']

# Tabs
tabs = ["Agregação por Situação no Curso", "Interação entre variáveis", "Detalhamento evasão", "Distribuição da Renda"]

selected_tab = st.sidebar.radio("Escolha uma aba:", tabs)

if selected_tab == "Agregação por Situação no Curso":

    # Add multiselect for the user to choose filters (with "Nenhum" option)
    modalidade = st.sidebar.selectbox('Selecione a modalidade:', ['Nenhum'] + list(df['Modalidade'].unique()))
    tipo_escola_origem = st.sidebar.selectbox('Selecione o tipo de escola de origem:', ['Nenhum'] + list(df['Tipo de Escola de Origem'].unique()))
    situacoes_to_display = st.sidebar.multiselect('Selecione as situações a serem exibidas:', list(df['Situação no Curso'].unique()))

    # Apply filters based on the selected options (skip if "Nenhum" is selected)
    if modalidade != 'Nenhum':
        df = df[df['Modalidade'] == modalidade]
    if tipo_escola_origem != 'Nenhum':
        df = df[df['Tipo de Escola de Origem'] == tipo_escola_origem]

    # Add a selectbox for the user to choose between absolute values and percentage
    values_or_percentage = st.sidebar.selectbox('Selecione a forma de exibição:', ['Valores Absolutos', 'Porcentagem'])

    # Add selectbox for the user to choose one attribute
    attribute1 = st.sidebar.selectbox('Selecione o atributo:', attributes_options)

    # Add a "Visualizar" button
    visualizar = st.sidebar.button('Visualizar')

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

elif selected_tab == "Interação entre variáveis":
    
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
    if st.sidebar.button('Visualizar'):
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

elif selected_tab == "Detalhamento evasão":

    st.title("Detalhamento evasão")
    
    # Filtros
    campus = st.sidebar.selectbox('Campus', options=['Todos'] + list(df['Campus'].unique()))
    curso = st.sidebar.selectbox('Curso', options=['Todos'] + list(df['curso'].unique()))
    desc_curso = st.sidebar.selectbox('Descrição do Curso', options=['Todos'] + list(df['Descrição do Curso'].unique()))
    ano_conclusao = st.sidebar.selectbox('Ano Letivo de Previsão de Conclusão', options=['Todos'] + list(df['Ano Letivo de Previsão de Conclusão'].unique()))
    ano_ingresso = st.sidebar.selectbox('Ano de Ingresso', options=['Todos'] + list(df['Ano de Ingresso'].unique()))
    periodo_atual = st.sidebar.selectbox('Período Atual', options=['Todos'] + list(df['Período Atual'].unique()))
    modalidade = st.sidebar.selectbox('Modalidade', options=['Todos'] + list(df['Modalidade'].unique()))
    tipo_escola = st.sidebar.selectbox('Tipo de Escola de Origem', options=['Todos'] + list(df['Tipo de Escola de Origem'].unique()))
    
    # Botão "Visualizar"
    if st.sidebar.button('Visualizar'):
    
        # Filtrar os dados com base nos valores selecionados
        filtered_data = df.copy()
        if campus != 'Todos':
            filtered_data = filtered_data[filtered_data['Campus'] == campus]
        if curso != 'Todos':
            filtered_data = filtered_data[filtered_data['curso'] == curso]
        if desc_curso != 'Todos':
            filtered_data = filtered_data[filtered_data['Descrição do Curso'] == desc_curso]
        if ano_conclusao != 'Todos':
            filtered_data = filtered_data[filtered_data['Ano Letivo de Previsão de Conclusão'] == ano_conclusao]
        if ano_ingresso != 'Todos':
            filtered_data = filtered_data[filtered_data['Ano de Ingresso'] == ano_ingresso]
        if periodo_atual != 'Todos':
            filtered_data = filtered_data[filtered_data['Período Atual'] == periodo_atual]
        if modalidade != 'Todos':
            filtered_data = filtered_data[filtered_data['Modalidade'] == modalidade]
        if tipo_escola != 'Todos':
            filtered_data = filtered_data[filtered_data['Tipo de Escola de Origem'] == tipo_escola]

        # Concatenar os motivos de ocorrência em uma única série
        all_motives = pd.concat([
            filtered_data["Principal motivo da ocorrência_2"],
            filtered_data["Motivo secundário da ocorrência"],
            filtered_data["Motivo terciário da ocorrência"]
        ])
        
        # Calcular a contagem de cada motivo único
        motive_counts = all_motives.value_counts()
        
        # Selecionar os 10 motivos com a maior contagem
        top_10_motives = motive_counts.nlargest(10)
        
        # Gráfico de barras
        st.subheader("Contagem dos 10 Principais Motivos de Ocorrência")
        
        plt.bar(top_10_motives.index, top_10_motives.values)
        plt.xlabel('Motivos da Ocorrência')
        plt.ylabel('Contagem')
        plt.title('Contagem dos 10 Principais Motivos de Ocorrência')
        plt.xticks(rotation=45, ha='right')
        st.pyplot(plt)

elif selected_tab == "Distribuição da Renda":
    st.title("Distribuição da Renda por Modalidade e Situação da Matrícula")

    # Filtros no sidebar
    situacao_curso = st.sidebar.multiselect('Situação no Curso', options=list(df['Situação no Curso'].unique()))
    modalidade_value = st.sidebar.selectbox('Modalidade', options=['Todos'] + list(df['Modalidade'].unique()))

    # Filtros
    campus = st.sidebar.selectbox('Campus', options=['Todos'] + list(df['Campus'].unique()))
    curso = st.sidebar.selectbox('Curso', options=['Todos'] + list(df['curso'].unique()))
    desc_curso = st.sidebar.selectbox('Descrição do Curso', options=['Todos'] + list(df['Descrição do Curso'].unique()))
    ano_conclusao = st.sidebar.selectbox('Ano Letivo de Previsão de Conclusão', options=['Todos'] + list(df['Ano Letivo de Previsão de Conclusão'].unique()))
    ano_ingresso = st.sidebar.selectbox('Ano de Ingresso', options=['Todos'] + list(df['Ano de Ingresso'].unique()))
    periodo_atual = st.sidebar.selectbox('Período Atual', options=['Todos'] + list(df['Período Atual'].unique()))
    tipo_escola = st.sidebar.selectbox('Tipo de Escola de Origem', options=['Todos'] + list(df['Tipo de Escola de Origem'].unique()))
    
    # Botão "Visualizar"
    if st.button('Visualizar'):

        # Filtrar os dados com base nos valores selecionados
        filtered_data = df.copy()
        if campus != 'Todos':
            filtered_data = filtered_data[filtered_data['Campus'] == campus]
        if curso != 'Todos':
            filtered_data = filtered_data[filtered_data['curso'] == curso]
        if desc_curso != 'Todos':
            filtered_data = filtered_data[filtered_data['Descrição do Curso'] == desc_curso]
        if ano_conclusao != 'Todos':
            filtered_data = filtered_data[filtered_data['Ano Letivo de Previsão de Conclusão'] == ano_conclusao]
        if ano_ingresso != 'Todos':
            filtered_data = filtered_data[filtered_data['Ano de Ingresso'] == ano_ingresso]
        if periodo_atual != 'Todos':
            filtered_data = filtered_data[filtered_data['Período Atual'] == periodo_atual]
        if modalidade_value != 'Todos':
            filtered_data = filtered_data[filtered_data['Modalidade'] == modalidade_value]
        if tipo_escola != 'Todos':
            filtered_data = filtered_data[filtered_data['Tipo de Escola de Origem'] == tipo_escola]
        if situacao_curso:
            filtered_data = df[df['Situação no Curso'].isin(situacao_curso)]


        # Chamar a função para gerar o gráfico
        plot_kde_renda(filtered_data, 4)
        plot_kde_renda(filtered_data, 6)
        plot_boxplot_renda(filtered_data)