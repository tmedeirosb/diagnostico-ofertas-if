
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

def plot_boxplot_renda(data, hue_option):
    plt.figure(figsize=(12, 6))

    #sns.violinplot(data=data, x="Situação no Curso", y="Renda Per Capita", hue="Tipo de Escola de Origem", split=True)

    if hue_option != 'Nenhum':
        #sns.boxenplot(data=data, x="Renda Per Capita", y="Situação no Curso", hue=hue_option, orient="h", scale="linear")
        sns.violinplot(data=data, x="Renda Per Capita", y="Situação no Curso", hue=hue_option, orient="h", cut=0)
    else:
        #sns.boxenplot(data=data, x="Renda Per Capita", y="Situação no Curso", orient="h", scale="linear")
        sns.violinplot(data=data, x="Renda Per Capita", y="Situação no Curso", orient="h", cut=0)

    # Configurar as marcas no eixo x
    x_start = 0  
    x_end = data['Renda Per Capita'].max() + 0.25  
    x_step = 0.25
    plt.xticks(np.arange(x_start, x_end, x_step), rotation=90)
    plt.grid(axis='x', linestyle='--', which='both', linewidth=0.5, alpha=1.)
    plt.title(f"Boxplot da Renda por Situação no Curso agregado por {hue_option}")

    # Deslocar os rótulos do eixo y para a esquerda
    #ax = plt.gca()
    #ax.set_yticklabels(ax.get_yticklabels(), position=(0.5, 0))    
    
    #plt.xlabel("Renda")
    #plt.ylabel("Densidade")
    #plt.tight_layout()
    st.pyplot(plt)

def plot_graph_egressos(eg_columns, filtered_data, hue_option):
    for option in eg_columns:
        # Filtrar os dados para remover NaN de 'option'
        filtered_data = filtered_data[~filtered_data[option].isna()]

        # Display a bar plot
        fig, ax = plt.subplots(figsize=(10,5))
        plt.title(f'Contagem do atributo {option}')
        if hue_option != 'Nenhum':
            plot = sns.countplot(data=filtered_data, x=option, hue=hue_option, ax=ax, order=sorted(filtered_data[option].unique()))
        else:
            plot = sns.countplot(data=filtered_data, x=option, ax=ax, order=sorted(filtered_data[option].unique()))

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
attributes_options = ['Campus', 'curso', 'Descrição do Curso', 
                      'Ano Letivo de Previsão de Conclusão', 'Ano de Ingresso', 
                      'Período Atual', 'Modalidade', 'Tipo de Escola de Origem']

st.sidebar.markdown(
    f"Diagnóstico de Ofertas: IFRN <br/> ASITEC/PROEN <br/>"
    f"asitec.re@ifrn.edu.br <br/> v. 0.1 <br/>"
    f"Atualizado em: 22/08/2023",
    unsafe_allow_html=True
)


# Tabs
tabs = [
        "Sobre", 
        "Geral", 
        "Evasão/Retenção: Detalhado", 
        "Evasão/Retenção: Renda", 
        "Evasão: Motivação", 
        "Egressos: Avaliação do Curso", 
        "Egressos: Prática", 
        "Egressos: Escolaridade", 
        "Egressos: Estudo Relação", 
        "Egressos: Trabalho"
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

elif selected_tab == "Geral":
    st.title("Geral")

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

        if not situacoes_to_display:
            st.error("Por favor, selecione pelo menos uma situação para exibir.")
        else:
            fig, ax = plt.subplots(figsize=(15, 10))

            if values_or_percentage == 'Valores Absolutos':
                plot = sns.countplot(data=df, x=attribute1, hue='Situação no Curso', order=df[attribute1].unique(), hue_order=situacoes_to_display, ax=ax)
                table_data = df.groupby(attribute1)['Situação no Curso'].value_counts().unstack().fillna(0)
            else:
                # For percentage, we need to adjust the data
                total_counts = df[attribute1].value_counts()
                status_counts = df.groupby(attribute1)['Situação no Curso'].value_counts()
                status_percentage = status_counts.div(total_counts, level=0) * 100
                status_percentage = status_percentage.reset_index(name='Percentage')
                plot = sns.barplot(data=status_percentage, x=attribute1, y='Percentage', hue='Situação no Curso', order=df[attribute1].unique(), hue_order=situacoes_to_display, ax=ax)
                table_data = status_percentage.pivot(index=attribute1, columns='Situação no Curso', values='Percentage')

            # Para fazer os rótulos do eixo x aparecerem na vertical
            ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha="right")
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

            #------ GRAFICO EMPILHADO ------#
            #grafico empilhado
            fig, ax = plt.subplots(figsize=(15, 10))
            filtered_data = df[df['Situação no Curso'].isin(situacoes_to_display)]

            if values_or_percentage == 'Valores Absolutos':
                # Create a pivot table
                pivot_df = filtered_data.groupby([attribute1, 'Situação no Curso']).size().unstack()

                # Sort based on the order you specified
                pivot_df = pivot_df.reindex(filtered_data[attribute1].value_counts().index)

                # Sort by the index (attribute1) alphabetically
                pivot_df = pivot_df.sort_index()

                # Plot
                pivot_df.plot(kind='bar', stacked=True, ax=ax)

                # Calculate the total height (sum) for each bar and annotate the plot
                totals = pivot_df.sum(axis=1)
                for i, total in enumerate(totals):
                    ax.text(i, total + 0.5, f'{int(total)}', ha='center', va='bottom')  # The 0.5 is for a slight offset, you can adjust as needed



                #plot = sns.countplot(data=df, x=attribute1, hue='Situação no Curso', order=df[attribute1].value_counts().index, hue_order=situacoes_to_display, ax=ax)
            else:
                # For percentage, we need to adjust the data
                total_counts = df[attribute1].value_counts()
                status_counts = df.groupby(attribute1)['Situação no Curso'].value_counts()
                status_percentage = status_counts.div(total_counts, level=0) * 100
                status_percentage = status_percentage.reset_index(name='Percentage')
                #plot = sns.barplot(data=status_percentage, x=attribute1, y='Percentage', hue='Situação no Curso', order=df[attribute1].value_counts().index, hue_order=situacoes_to_display, ax=ax, stacked=True)

                # Assuming your DataFrame is prepared properly for this
                df_plot = status_percentage.pivot_table(index=attribute1, columns='Situação no Curso', values='Percentage', aggfunc='sum')

                # Sort by the index (attribute1) alphabetically
                df_plot = df_plot.sort_index()

                # This will create a stacked bar plot
                df_plot[situacoes_to_display].plot(kind='bar', stacked=True, ax=ax)

                totals = df_plot[situacoes_to_display].sum(axis=1)  # Get the total height for each bar
                # Annotate the bars with their total sums
                for i, total in enumerate(totals):
                    ax.annotate(f'{total:.0f}', (i, total + 1), ha='center', va='bottom')  # Adjust the `+ 1` for vertical spacing if needed
                    #ax.text(i, total + 0.5, f'{int(total)}', ha='center', va='bottom')  # The 0.5 is for a slight offset, you can adjust as needed


            ax.set_title('Situação no Curso por ' + attribute1)
            ax.set_xlabel(attribute1)
            ax.set_ylabel('Quantidade' if values_or_percentage == 'Valores Absolutos' else 'Percentual (%)')
            ax.legend(title='Situação no Curso')

            # Annotate the bars with their sums
            for p in ax.patches:
                width = p.get_width()
                height = p.get_height()
                x, y = p.get_xy()
                
                # Check if the height (value) is not too small to prevent overlapping annotations
                if height > 2:  # or any other threshold that suits your data
                    ax.annotate(f'{height:.0f}', (x + width/2, y + height/2), ha='center', va='center')

            # Display the values on top of each bar
            #for p in plot.patches:
            #    plot.annotate(format(p.get_height(), '.1f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points')

            # Show the plot
            st.pyplot(fig)
            

elif selected_tab == "Evasão/Retenção: Detalhado":
    
    st.title("Evasão/Retenção: Detalhado")

    st.sidebar.header("Visualização")
    # Valores absolutos ou porcentagem
    values_or_percentage = st.sidebar.selectbox('Selecione a forma de exibição:', ['Valores Absolutos', 'Porcentagem'])
    
    st.sidebar.header("Interação entre variáveis")
    # Seleção de atributos para interação
    attribute1 = st.sidebar.selectbox('Seleção do atributo 1:', attributes_options)
    attribute_values_1 = st.sidebar.multiselect(f'Valores para {attribute1}:', df[attribute1].unique())
    
    attribute2 = st.sidebar.selectbox('Selecione o segundo atributo (Opcional):', options=['Nenhum'] + attributes_options, index=0)

    if attribute_values_1:
        df_filtered_by_attr1 = df[df[attribute1].isin(attribute_values_1)]
        if attribute2 != 'Nenhum':
            attribute_values_2 = st.sidebar.multiselect(f'Valores para {attribute2} (baseado em {attribute1}):', df_filtered_by_attr1[attribute2].unique())
    else:
        attribute_values_2 = []

    # Botão para visualizar
    if st.button('Visualizar'):

        if attribute2 == 'Nenhum':
            if attribute_values_1:
                fig, ax = plt.subplots(figsize=(15, 10))
                data = df[df[attribute1].isin(attribute_values_1)]

                if values_or_percentage == 'Valores Absolutos':                    
                    sns.countplot(data=data, x=attribute1, hue='Situação no Curso', ax=ax)
                else:
                    # This will be a bit complex for percentage, as we'll need to compute the percentage per each situation
                    data_grouped = data.groupby([attribute1, 'Situação no Curso']).size().unstack(fill_value=0)
                    total = data.groupby(attribute1).size()
                    data_percentage = (data_grouped.divide(total, axis=0) * 100).fillna(0)
                    data_percentage.plot(kind='bar', stacked=False, ax=ax)
                
                ax.set_title(f'{attribute1}')
                ax.set_xlabel(attribute1)
                ax.set_ylabel('Count' if values_or_percentage == 'Valores Absolutos' else 'Percentage (%)')
                
                for container in ax.containers:
                    ax.bar_label(container)

                st.pyplot(fig)
                
                # Exibindo a tabela
                table = data.groupby([attribute1, 'Situação no Curso']).size().unstack().fillna(0)
                table['Total'] = table.sum(axis=1)
                table.loc['Total'] = table.sum()
                st.write(table) 
            else:
                st.error("Por favor, selecione valores para os atributos.")           

        else:
            if attribute_values_1 and attribute_values_2:
                fig, ax = plt.subplots(figsize=(15, 10))
                data = df[df[attribute1].isin(attribute_values_1) & df[attribute2].isin(attribute_values_2)]
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
                st.error("Por favor, selecione valores para os atributos.")

elif selected_tab == "Evasão/Retenção: Renda":
    st.title("Distribuição da Renda por Situação da Matrícula")

    # Visualizacao no sidebar
    st.sidebar.header("Visualização")
    situacao_curso = st.sidebar.multiselect('Situação no Curso', options=list(df['Situação no Curso'].unique()))
    
    # Filtros
    vars_filtros = show_filtros(df)

    hue_columns = ['Campus', 'curso', 'Descrição do Curso', 'Ano Letivo de Previsão de Conclusão', 
                   'Ano de Ingresso', 'Período Atual', 'Modalidade', 'Tipo de Escola de Origem']

    # Hue parameter
    hue_option = st.sidebar.selectbox('Escolha o atributo para agregação (opcional)', ['Nenhum'] + hue_columns)    

    # Botão "Visualizar"
    if st.button('Visualizar'):
        # Filtrar os dados com base nos valores selecionados
        filtered_data = apply_filtros(df, vars_filtros)

        if situacao_curso:
            filtered_data = filtered_data[filtered_data['Situação no Curso'].isin(situacao_curso)]


        # Chamar a função para gerar o gráfico
        plot_kde_renda(filtered_data, 4)
        plot_kde_renda(filtered_data, 6)
        plot_boxplot_renda(filtered_data, hue_option)

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
    
    #st.sidebar.header('Filtro de colunas do Egresso')
    #options = st.sidebar.selectbox('Escolha a coluna para visualizar', eg_columns)

    # Filters
    #attribute_values_1 = st.sidebar.multiselect(f'Valores para {options}:', df[options].unique())

    hue_columns = ['Campus', 'curso', 'Descrição do Curso', 'Ano Letivo de Previsão de Conclusão', 
                   'Ano de Ingresso', 'Período Atual', 'Modalidade', 'Tipo de Escola de Origem']

    # Hue parameter
    hue_option = st.sidebar.selectbox('Escolha o atributo para agregação (opcional)', ['Nenhum'] + hue_columns)

    if st.button('Visualizar'):

        # Filtrar os dados com base nos valores selecionados
        filtered_data = apply_filtros(df, vars_filtros)

        #plot os gráficios de egressos
        plot_graph_egressos(eg_columns, filtered_data, hue_option)
        
elif selected_tab == "Egressos: Prática":

    st.title("Egressos: Prática")

    # Filtros
    vars_filtros = show_filtros(df)
    
    # Sidebar
    eg_columns = ['PRATICA_TIPO_1', 'PRATICA_TIPO_2', 'PRATICA_TIPO_3', 'PRATICA_TIPO_4',
                  'PRATICA_REALIZACAO', 'PRATICA_CONHECIMENTOS',
                  'PRATICA_ORIENTACAO', 'PRATICA_AREA_PROFISSAO']
    
    hue_columns = ['Campus', 'curso', 'Descrição do Curso', 'Ano Letivo de Previsão de Conclusão', 
                   'Ano de Ingresso', 'Período Atual', 'Modalidade', 'Tipo de Escola de Origem']

    # Hue parameter
    hue_option = st.sidebar.selectbox('Escolha o atributo para agregação (opcional)', ['Nenhum'] + hue_columns)

    if st.button('Visualizar'):

        # Filtrar os dados com base nos valores selecionados
        filtered_data = apply_filtros(df, vars_filtros)

        #plot os gráficios de egressos
        plot_graph_egressos(eg_columns, filtered_data, hue_option)

elif selected_tab == "Egressos: Escolaridade":

    st.title("Egressos: Escolaridade")

    # Filtros
    vars_filtros = show_filtros(df)
    
    # Sidebar
    eg_columns = ['ESCOLARIDADE_NIVEL', 'ESCOLARIDADE_IF']
    
    hue_columns = ['Campus', 'curso', 'Descrição do Curso', 'Ano Letivo de Previsão de Conclusão', 
                   'Ano de Ingresso', 'Período Atual', 'Modalidade', 'Tipo de Escola de Origem']

    # Hue parameter
    hue_option = st.sidebar.selectbox('Escolha o atributo para agregação (opcional)', ['Nenhum'] + hue_columns)

    # Botão "Visualizar"
    if st.button('Visualizar'):

        # Filtrar os dados com base nos valores selecionados
        filtered_data = apply_filtros(df, vars_filtros)

        #plot os gráficios de egressos
        plot_graph_egressos(eg_columns, filtered_data, hue_option)

elif selected_tab == "Egressos: Estudo Relação":

    st.title("Egressos: Estudo Relação")

    # Filtros
    vars_filtros = show_filtros(df)
    
    # Sidebar
    eg_columns = ['ESTUDO_RELACAO']
    
    hue_columns = ['Campus', 'curso', 'Descrição do Curso', 'Ano Letivo de Previsão de Conclusão', 
                   'Ano de Ingresso', 'Período Atual', 'Modalidade', 'Tipo de Escola de Origem']

    # Hue parameter
    hue_option = st.sidebar.selectbox('Escolha o atributo para agregação (opcional)', ['Nenhum'] + hue_columns)

    # Botão "Visualizar"
    if st.button('Visualizar'):

        # Filtrar os dados com base nos valores selecionados
        filtered_data = apply_filtros(df, vars_filtros)

        #plot os gráficios de egressos
        plot_graph_egressos(eg_columns, filtered_data, hue_option)

elif selected_tab == "Egressos: Trabalho":

    st.title("Egressos: Trabalho")

    # Filtros
    vars_filtros = show_filtros(df)
    
    # Sidebar
    eg_columns = ['TRAB_SITUACAO', 'TRAB_OCUPACAO', 'TRAB_AREA', 'TRAB_CAPACITACAO']
    
    hue_columns = ['Campus', 'curso', 'Descrição do Curso', 'Ano Letivo de Previsão de Conclusão', 
                   'Ano de Ingresso', 'Período Atual', 'Modalidade', 'Tipo de Escola de Origem']

    # Hue parameter
    hue_option = st.sidebar.selectbox('Escolha o atributo para agregação (opcional)', ['Nenhum'] + hue_columns)

    # Botão "Visualizar"
    if st.button('Visualizar'):

        # Filtrar os dados com base nos valores selecionados
        filtered_data = apply_filtros(df, vars_filtros)

        #plot os gráficios de egressos
        plot_graph_egressos(eg_columns, filtered_data, hue_option)