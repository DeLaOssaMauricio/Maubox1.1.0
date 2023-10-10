import streamlit as st
import pandas as pd
import openpyxl 
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import io
import xlsxwriter
from io import BytesIO

st.image("imagenes\PortadaYoutube.png")

data = 0
#media_grubbs = 0
# Título y descripción del componente
st.title("Aplicacion Maubox V1.0")


st.info("#### 1 Carga de datos")
# Subir archivo Excel
uploaded_file = st.file_uploader("##### Has clic y carga un archivo excel que debe tener la columna (Resultado)"
                                 , type=["xlsx", "xls"])




if uploaded_file is not None:
    # Leer archivo Excel y mostrar contenido
    df = pd.read_excel(uploaded_file, engine='openpyxl')  # engine='openpyxl' para archivos xlsx
    

    # Renombrar primera columna a 'Resultado' 
    df = df.rename(columns={df.columns[0]: 'Resultado'})
    #########################################################
    ##### Definir funcines de descarga de archivos CSV y EXCEL
    @st.cache_data
    def to_excel(df):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        writer.close()
        return output.getvalue()

    # Definir función to_csv
    def to_csv(df):
        return df.to_csv(index=False)
    ########################################
    #######################################

    # Ordenar los valores por la columna "Resultado"
    data = df.sort_values(by="Resultado",ascending= True)
    st.success("Contenido del archivo:")
    st.write(data)
    st.markdown("_____")
    
    
    



        ###########################################################       


st.success('#### 2 Filtrado de Datos')
         ###########################################################



mostrar_nivel = False
mostrar_nivel_placeholder = st.empty()  # Espacio vacío para mostrar el radiobutton
if "opcion" not in st.session_state:
   st.session_state.opcion = None
boton_filtro = st.radio("Seleccione un método:", ["Filtro Dixon", "Tests Grubbs"], key="boton_filtro", horizontal=True)




##### Filtro de Dixon

#data = data["Resultado"]
data_dixon = data


# Convertir la columna "Resultado" a valores numéricos
data_dixon["Resultado"] = pd.to_numeric(data_dixon["Resultado"], errors="coerce")

# ... Continúa con tu código ...


if boton_filtro == "Filtro Dixon":
    if st.button("Aplicar Filtro Dixon"):
        mostrar_nivel = False
        mostrar_nivel_placeholder.empty()  # Vaciar el espacio si se selecciona Dixon
        st.write("#### Filtro de Dixon Escogido")
        
        st.info('#### 2 Medidas de Tendencia Central (Media, DS y CV) y Graficos Antes de Filtrar')

        # Calcular medidas de tendencia central la media, el coeficiente de variación (CV) y la variación estándar de 
        # la columna "Resultado" antes de aplicar cualquier cambio o filtro
        media_antes = data["Resultado"].mean()
        ds_antes = data["Resultado"].std()
        cv_antes = (data["Resultado"].std() / media_antes) * 100  # Coeficiente de variación en porcentaje


        data_antes = {
        "Media": [f"{media_antes:.2f}"],
        "Desviacion Estándar": [f"{ds_antes:.2f}"],
        "Coeficiente de Variación (CV)": [f"{cv_antes:.2f}%"]
            }

        # Convertir el diccionario en un DataFrame
        df_resultados_antes = pd.DataFrame(data_antes)

        # Mostrar el DataFrame
        
        st.write(df_resultados_antes, Index = False)

        

        # Graficamos antes con una distribucion normal para saber el estado de los datos y 
        # su distribucion Gaussiana
        def grafica_inicial(data, media_antes, ds_antes, column="Resultado"):
            valores_columna = data[column]  # Obtener los valores de la columna especificada
            x = np.linspace(valores_columna.min(), valores_columna.max(), 1000)
        
            # Calcular los valores de la función de densidad de probabilidad (PDF) de la distribución normal
            pdf = (1 / (ds_antes * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - media_antes) / ds_antes) ** 2)

            # Crear la gráfica de densidad antes
            fig = plt.figure(figsize=(8, 6))
            sns.lineplot(x=x, y=pdf, color='r', label='Distribución Normal')
            plt.title('Grafico de Distribuccion Normal con Datos Iniciales')
            plt.xlabel('Resultado')
            plt.ylabel('Densidad de Probabilidad')
            plt.legend()
            plt.grid(True)
            #plt.figure()
            plt.show()
            
            return (fig)
        
        fig = grafica_inicial(data, media_antes, ds_antes, column="Resultado")
   
        st.pyplot(fig)


        #data_dixon = data_dixon.reset_index(drop=True)
        X1A = data_dixon.at[data_dixon.index[0], "Resultado"]
        X2A = data_dixon.at[data_dixon.index[1], "Resultado"]
        XnA = data_dixon.at[data_dixon.index[-1], "Resultado"]
        Xn1A = data_dixon.at[data_dixon.index[-2], "Resultado"]

        # Calcular los rangos
        rango_dixon = (XnA - X1A) / 3
        rango_menor = X2A - X1A
        rango_mayor = XnA - Xn1A
     
        dframe_Dixon = {
        "Rango Menor": rango_menor,
        "Rango Mayor": rango_mayor,
        "Rango Dixon": rango_dixon,
        "Valor X1": X1A,
        "Valor X2": X2A,
        "Valor Xn-1": Xn1A,
        "Valor Xn": XnA,
        "N Datos Iniciales": len(data),
        "N Datos Finales": len(data_dixon)
        }

        st.info("Tabla de Dixon antes")
        # Convertir a DataFrame
        df0 = pd.DataFrame(dframe_Dixon, index=[0])
        st.table(df0)
        
        
        while True:

            data_dixon = data_dixon.reset_index(drop=True)

            #data_dixon = data_dixon.reset_index(drop=True)
            X1 = data_dixon.at[data_dixon.index[0], "Resultado"]
            X2 = data_dixon.at[data_dixon.index[1], "Resultado"]
            Xn = data_dixon.at[data_dixon.index[-1], "Resultado"]
            Xn1 = data_dixon.at[data_dixon.index[-2], "Resultado"]

            # Calcular los rangos
            rango_dixon = (Xn - X1) / 3
            rango_menor = X2 - X1
            rango_mayor = Xn - Xn1


            if rango_menor <= rango_dixon and rango_mayor <= rango_dixon:
                break


            
            ####Calculos

            # Menor aberrante
            if (rango_menor > rango_dixon):
                #data_dixon = data_dixon.drop(data_dixon.index[-1])
                st.write(X1, "Es Menor Aberrante")

            # Mayor aberrante
            if (rango_mayor > rango_dixon):
                #data_dixon = data_dixon.drop(data_dixon.index[-1])
                st.write(Xn, "Es Mayor Aberrante")

            
            if (rango_menor > rango_dixon):
                data_dixon = data_dixon.drop(index=0)  # Eliminar la fila con índice 0


            if (rango_mayor > rango_dixon):
                data_dixon = data_dixon.drop(index=-1)


            if rango_menor <= rango_dixon and rango_mayor <= rango_dixon:
                break

            #data_dixon = data_dixon.reset_index(drop=True)
     
        st.write(len(data) - len(data_dixon),"Datos eliminados")

        st.success("Filtro de Dixon aplicado exitosamente!")

        st.write(data_dixon)

        #########################################
        #########################################
        #########################################
        

        #if st.button("Realizar calculos despues de aplicado el filtro"):
        # Calcular medidas de tendencia central la media, el coeficiente de variación (CV) y la variación estándar de 
        # la columna "Resultado" despues de aplicar cualquier cambio o filtro
        media_despues = data_dixon["Resultado"].mean()
        ds_despues = data_dixon["Resultado"].std()
        cv_despues = (data_dixon["Resultado"].std() / media_despues) * 100 


        data_despues = {
        "Media": [f"{media_despues:.2f}"],
        "Desviacion Estándar": [f"{ds_despues:.2f}"],
        "Coeficiente de Variación (CV)": [f"{cv_despues:.2f}%"]
            }

        # Convertir el diccionario en un DataFrame
        df_resultados_despues = pd.DataFrame(data_despues)

        # Mostrar el DataFrame
        st.info("Análisis de Tendencia Central y Variabilidad Despues del Filtro de Dixon")
        st.write(df_resultados_despues, Index = False)


        # Graficamos despues con una distrubucion normal para saber el estado de los datos y 
        # su distribucion Gaussiana
        def grafica_filtrada(data_dixon, media_despues, ds_despues, column="Resultado"):
            valores_columna = data_dixon[column]  # Obtener los valores de la columna especificada
            x = np.linspace(valores_columna.min(), valores_columna.max(), 1000)
        
            # Calcular los valores de la función de densidad de probabilidad (PDF) de la distribución normal
            pdf = (1 / (ds_despues * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - media_despues) / ds_despues) ** 2)

            # Crear la gráfica de densidad despues
            fig = plt.figure(figsize=(8, 6))
            sns.lineplot(x=x, y=pdf, color='g', label='Distribución Normal')
            plt.title('Distribución Normal de los resultados filtrados')
            plt.xlabel('Resultado')
            plt.ylabel('Densidad de Probabilidad')
            plt.legend()
            plt.grid(True)
            #plt.figure()
            plt.show()
            
            return (fig)
        
        fig = grafica_filtrada(data_dixon, media_despues, ds_despues, column="Resultado")
   
        st.pyplot(fig)

    


tabla_grubbs = pd.DataFrame({
    "N": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
        21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
    "Alfa 0.01": [2.4822, 2.5642, 2.6362, 2.6992, 2.7552, 2.8062, 2.8522, 2.8942, 2.9322, 2.9682, 3.0012,
                3.0312, 3.0602, 3.0872, 3.1122, 3.1352, 3.1582, 3.1792, 3.1992, 3.2182, 3.2362],
    "Alfa 0.05": [2.2902, 2.3552, 2.4122, 2.4622, 2.5072, 2.5482, 2.5862, 2.6202, 2.6522, 2.6812, 2.7082,
                2.7342, 2.7582, 2.7802, 2.8022, 2.8222, 2.8412, 2.8592, 2.8762, 2.8932, 2.9082],
    "Alfa 0.10": [2.1761, 2.2342, 2.2852, 2.3314, 2.3725, 2.4096, 2.4437, 2.4758, 2.5049, 2.531, 2.5571,
                2.5801, 2.6031, 2.6241, 2.6441, 2.6631, 2.6811, 2.6981, 2.7141, 2.7291, 2.7431]
})

media_antes = data["Resultado"].mean()
ds_antes = data["Resultado"].std()
cv_antes = (data["Resultado"].std() / media_antes) * 100  # Coeficiente de variación en porcentaje
data = df.sort_values(by="Resultado")

data_grubbs = data.copy()
media_grubbs = 0


if boton_filtro == ("Tests Grubbs"):
    mostrar_nivel = True
    alfa_option = st.radio("Niveles de confianza", ("90%", "95%", "99% (Recomendado)"))
    if st.button("Aplicar Tests de Grubbs"):

           
        
        # Datos para buscar

        # Verificar la opción de alfa seleccionada
        if alfa_option == ("90%"):
            alfa_column = "Alfa 0.10"
        if alfa_option == ("95%"):
            alfa_column = "Alfa 0.05"
        if alfa_option == ("99% (Recomendado)"):
            alfa_column = "Alfa 0.01"

        st.info('#### 2 Medidas de Tendencia Central (Media, DS y CV) y Graficos Antes de Filtrar con Grubbs')

        # Calcular medidas de tendencia central la media, el coeficiente de variación (CV) y la variación estándar de 
        # la columna "Resultado" antes de aplicar cualquier cambio o filtro
        media_antes = data["Resultado"].mean()
        ds_antes = data["Resultado"].std()
        cv_antes = (data["Resultado"].std() / media_antes) * 100  # Coeficiente de variación en porcentaje


        data_antes = {
        "Media": [f"{media_antes:.2f}"],
        "Desviacion Estándar": [f"{ds_antes:.2f}"],
        "Coeficiente de Variación (CV)": [f"{cv_antes:.2f}%"]
            }

        # Convertir el diccionario en un DataFrame
        df_resultados_antes = pd.DataFrame(data_antes)

        # Mostrar el DataFrame
        
        st.write(df_resultados_antes, Index = False)

        

        # Graficamos antes con una distrubucion normal para saber el estado de los datos y 
        # su distribucion Gaussiana
        def grafica_inicial(data, media_antes, ds_antes, column="Resultado"):
            valores_columna = data[column]  # Obtener los valores de la columna especificada
            x = np.linspace(valores_columna.min(), valores_columna.max(), 1000)
        
            # Calcular los valores de la función de densidad de probabilidad (PDF) de la distribución normal
            pdf = (1 / (ds_antes * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - media_antes) / ds_antes) ** 2)

            # Crear la gráfica de densidad antes
            fig = plt.figure(figsize=(8, 6))
            sns.lineplot(x=x, y=pdf, color='r', label='Distribución Normal')
            plt.title('Grafico de Distribuccion Normal con Datos Iniciales')
            plt.xlabel('Resultado')
            plt.ylabel('Densidad de Probabilidad')
            plt.legend()
            plt.grid(True)
            #plt.figure()
            plt.show()
            
            return (fig)
        
        fig = grafica_inicial(data, media_antes, ds_antes, column="Resultado")
   
        st.pyplot(fig)

        

        st.info("Analizando outliers con Test de Grubbs...")

        n = len(data_grubbs)
        # Buscar el valor correspondiente en la columna seleccionada
        factor_grubbs = tabla_grubbs.loc[tabla_grubbs['N'] == n, alfa_column].values[0]

        # Aqui calculamos los limites superior e inferior de donde partimos para encontrar
        # los valores a tipicos u outliers

        limite_superior = media_antes + factor_grubbs * ds_antes
        limite_inferior = media_antes - factor_grubbs * ds_antes

        # Redondear y luego imprimir los límites
        st.success(f"Para n = {n} y alfa = {alfa_column}, el valor del factor de Grubbs es: {factor_grubbs}")
        st.markdown(f"#### Los datos deben estar en el rango de Lim. Inferior y Lim. Superior, los que esten fuera seran eliminados")
        st.write('Limite Inferior',round(limite_inferior, 2),'<--------------------->', 'Limite Superior',round(limite_superior, 2))
        
        

        # Codigo que se basa segun los limites antes calculados para eliminar y rectificar si hay
        # mas valores atipicos luego de los ciclos los imprime y los elimina tambien debne aparecer en la GUI
        while True:
       
            menor_atipico = data_grubbs.at[data_grubbs.index[0], "Resultado"]
            mayor_atipico = data_grubbs.at[data_grubbs.index[-1], "Resultado"]

            # Menor atípico
            if menor_atipico < limite_inferior:
                st.write(menor_atipico, "es Dato atípico")
                data_grubbs = data.drop(data.index[0])
                st.write(menor_atipico, "Eliminado")



            # Mayor atípico
            if mayor_atipico > limite_superior:
                st.write(mayor_atipico, "es Dato atípico")
                data_grubbs = data.drop(data.index[-1])
                st.write(mayor_atipico, "Eliminado")


            

             
            if menor_atipico >= limite_inferior and mayor_atipico <= limite_superior:
                break

        media_grubbs = data_grubbs.mean()
        #st.write(media_grubbs)
        st.write(f"Los valores extremos de la tabla ingresada {menor_atipico} y {mayor_atipico}, no son datos atipicos")
        st.success("Análisis de Grubbs completado con éxito.......")
        st.markdown("_________")

        st.info("#### Análisis de Tendencia Central y Variabilidad Despues del Tests de Grubbs")

        media_despues = data_grubbs["Resultado"].mean()
        ds_despues = data_grubbs["Resultado"].std()
        cv_despues = (data_grubbs["Resultado"].std() / media_despues) * 100 


        data_despues = {
        "Media": [f"{media_despues:.2f}"],
        "Desviacion Estándar": [f"{ds_despues:.2f}"],
        "Coeficiente de Variación (CV)": [f"{cv_despues:.2f}%"]
            }

        # Convertir el diccionario en un DataFrame
        df_resultados_despues = pd.DataFrame(data_despues)

        st.markdown("#### Tabla de medidas de tendencia central despues del Tests de Grubbs")
        st.write(df_resultados_despues, index=False)

        # Graficamos despues con una distrubucion normal para saber el estado de los datos y 
        # su distribucion Gaussiana
        def grafica_filtrada(data_grubbs, media_despues, ds_despues, column="Resultado"):
            valores_columna = data_grubbs[column]  # Obtener los valores de la columna especificada
            x = np.linspace(valores_columna.min(), valores_columna.max(), 1000)
        
            # Calcular los valores de la función de densidad de probabilidad (PDF) de la distribución normal
            pdf = (1 / (ds_despues * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - media_despues) / ds_despues) ** 2)

            # Crear la gráfica de densidad despues
            fig = plt.figure(figsize=(8, 6))
            sns.lineplot(x=x, y=pdf, color='g', label='Distribución Normal')
            plt.title('Distribución Normal de los Resultados Filtrados con Grubbs')
            plt.xlabel('Resultado')
            plt.ylabel('Densidad de Probabilidad')
            plt.legend()
            plt.grid(True)
            #plt.figure()
            plt.show()
            
            return (fig)
        
        fig = grafica_filtrada(data_grubbs, media_despues, ds_despues, column="Resultado")
        
        st.pyplot(fig)
        
        
        

st.markdown(" __________________________________________")

#####################################################
#####################################################
#####################################################
      

st.info('#### 3 Validacion de la media Propia con "Zscore"')

if 'data_dixon' in globals():
  df_seleccionado = data_dixon
elif 'data_grubbs' in globals():
  df_seleccionado = data_grubbs

# Tabla final de nombre validaciuon de la media por el Zscore en donde el usuario va escoger
# el valor del Z score ya sea 2 o 1.68 y se muestra en la tabla la cual despues la GUI
# pregunta si deses exportar los datos
#media_grubbs = data_grubbs.mean()
###Solicitar entradas de usuario

#zscore = st.radio("Criterio de aceptabilidad", ["1.65 (Recomendado)", "2.0"], horizontal=True)
z_score=0
analito = 0
unidades = 0
nivel = 1
media_comparacion = 0
ds_comparacion = 0
criterio = 0
interpretacion = 0
   
analito = st.text_input("Ingresa el analito:")
if not analito:
    st.warning("¡El analito es obligatorio!")

unidades = st.text_input("Ingresa las unidades:")
if not unidades:
    st.warning("¡Las unidades son obligatorias!")

nivel = st.selectbox("Ingresa el nivel del control ", [1, 2, 3, "Bajo","Normal","Alto"])
if not nivel:
    st.warning("¡El nivel del control es obligatorio!")

media_comparacion = st.number_input("Ingresa la media del fabricante:", value=0.0)
if media_comparacion is None:
    st.warning("¡La media de comparación es obligatoria!")

ds_comparacion = st.number_input("Ingresa la desviación estándar del fabricante:", value=0.0)
if ds_comparacion is None:
    st.warning("¡La desviación estándar de comparación es obligatoria!")



opciones = st.radio("#### Escoja el Criterio de Aceptabilidad", ("1.65 (Recomendado)", "2.0"))
media_df_seleccionado = df_seleccionado.mean()       
if st.button("Validar Media con Zscore"):

    z_score = abs((media_df_seleccionado - media_comparacion) / ds_comparacion)
    

    # Calcular el criterio de aceptabilidad
    if opciones == "1.65 (Recomendado)":
        criterio = 1.65
    if opciones == "2.0":
        criterio = 2

    z_score = float(z_score)
    criterio = float(criterio)

    # Calcular la interpretación
    if z_score <= criterio:
        interpretacion = "Cumple"
    else:
        interpretacion = "No Cumple"


    # Crear el dataframe con los resultado
        
    data2 = {
        "Analito": [analito],
        "Unidades": [unidades],
        "Nivel": [nivel],
        "Media Propia": [media_df_seleccionado.iloc[0]],
        "Media Comparación": [media_comparacion],
        "DE Comparación": [ds_comparacion],
        "Zscore": [z_score],
        "Criterio": [criterio],
        "Interpretación": [interpretacion]
    }



    def apply_styles(val):
        # Definir estilos por defecto para las columnas obligatorias
        default_styles = "background-color: gray;"
        interpretaion_styles = ""  # Estilos para la columna "Interpretación"

        if val == "Cumple":
            interpretaion_styles = "background-color: green;"
        elif val == "No Cumple":
            interpretaion_styles = "background-color: red;"  # Cambiar a rojo si es "No Cumple"

        return default_styles + interpretaion_styles
    

    Tabla_Zscore = pd.DataFrame(data2).style.format({
        "Media Propia": "{:.2f}",
        "Media Comparación": "{:.2f}",
        "DE Comparación": "{:.2f}",
        "Zscore": "{:.2f}",
        "Criterio": "{:.2f}"
    }).applymap(apply_styles, subset=["Interpretación", "Analito", "Unidades", "Nivel", "Media Comparación", "DE Comparación"])

    st.write(Tabla_Zscore)



    
      #############################################table
        #############################################

    # Agregar botones de descarga para Excel y CSV
    #st.download_button("Descargar Resultados despues de aplicado Dixon CSV", to_csv(data_dixon), file_name="dixon_data.csv")


# Convertir DataFrame a Excel sin estilos
    # Ahora puedes guardar el DataFrame en un archivo Excel
    

    # Generar el Excel en bytes en memoria
    excel_bytes = io.BytesIO()
    Tabla_Zscore.to_excel(excel_bytes, index=False, sheet_name='Hoja1', engine='xlsxwriter')

    # Obtener el valor de los bytes en memoria
    excel_bytes = excel_bytes.getvalue() 

    # Pasar los bytes directamente al boton de descarga
    st.download_button(
        "Descargar Tabla Validación Zscore",
        excel_bytes,
        file_name="Tabla_Zscore.xlsx"
    )
    



                
                
                










        

