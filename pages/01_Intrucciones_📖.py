import streamlit as st
st.image("imagenes\PortadaYoutube.png")



# Glosario
st.title("Glosario")
st.header("1. Carga de Datos:")
st.write("- **Archivo Excel:** El usuario debe cargar un archivo Excel que contenga una columna denominada 'Resultado' con los datos a analizar.")

st.header("2. Filtrado de Datos:")
st.write("- **Filtro de Dixon:** Método utilizado para detectar valores atípicos (outliers) en una muestra de datos. Este filtro se basa en la diferencia entre el valor máximo y mínimo de la muestra.")
st.write("- **Tests de Grubbs:** Método estadístico utilizado para detectar valores atípicos en una muestra de datos. El usuario puede seleccionar diferentes niveles de confianza (alfa) para realizar la prueba.")

st.header("3. Validación de la Media Propia con 'Zscore':")
st.write("- **Analito:** El nombre del analito o variable que se está analizando en los datos.")
st.write("- **Unidades:** Las unidades en las que se expresan los valores del analito.")
st.write("- **Nivel del Control:** El nivel del control al que pertenecen los datos (puede ser 'Bajo', 'Normal' o 'Alto').")
st.write("- **Media Propia:** La media de los datos después de aplicar el filtro de Dixon o Grubbs.")
st.write("- **Media Comparación:** La media proporcionada por el fabricante o referencia para el analito.")
st.write("- **DE Comparación:** La desviación estándar proporcionada por el fabricante o referencia para el analito.")
st.write("- **Zscore:** El valor Z calculado para comparar la media propia con la media de comparación.")
st.write("- **Criterio:** El criterio de aceptabilidad, que puede ser 1.65 o 2.0, dependiendo de la elección del usuario.")
st.write("- **Interpretación:** Indica si la media propia cumple o no cumple con el criterio de aceptabilidad según el valor Z calculado.")

# Instrucciones de Uso
st.title("Instrucciones de Uso de la Aplicación Maubox V1.0")

# Carga de Datos
st.header("Carga de Datos:")
st.write("1. Haga clic en el área designada para cargar un archivo Excel que contenga una columna denominada 'Resultado' con los datos a analizar.")

# Filtrado de Datos
st.header("Filtrado de Datos:")
st.write("2. Seleccione uno de los métodos de filtrado disponibles: 'Filtro Dixon' o 'Tests de Grubbs'.")
st.write("3. Si selecciona 'Filtro Dixon,' haga clic en 'Aplicar Filtro Dixon' para aplicar el filtro.")
st.write("4. Si selecciona 'Tests de Grubbs,' elija el nivel de confianza (alfa) deseado y haga clic en 'Aplicar Tests de Grubbs' para aplicar el filtro.")

# Análisis de Tendencia Central y Variabilidad Antes del Filtro
st.header("Análisis de Tendencia Central y Variabilidad Antes del Filtro:")
st.write("Antes de aplicar cualquiera de los filtros, se realizarán los siguientes cálculos y visualizaciones:")
st.write("- Media Antes: La media de los datos cargados inicialmente se calculará, proporcionando una medida de tendencia central antes del filtro.")
st.write("- Desviación Estándar Antes: Se calculará la desviación estándar de los datos iniciales para evaluar la variabilidad antes del filtro.")
st.write("- Gráficos de Distribución Normal Antes: Se mostrarán gráficos de distribución normal para visualizar la distribución de los datos antes de la aplicación del filtro. Estas gráficas se pueden descargar haciendo clic derecho sobre ellas.")

# Análisis de Tendencia Central y Variabilidad Después del Filtro
st.header("Análisis de Tendencia Central y Variabilidad Después del Filtro:")
st.write("Después de aplicar cualquiera de los filtros, se mostrarán las siguientes medidas de tendencia central y variabilidad:")
st.write("- Media Después: La media de los datos filtrados se calculará nuevamente después de aplicar el filtro Dixon o Grubbs.")
st.write("- Desviación Estándar Después: Se recalcula la desviación estándar de los datos filtrados para evaluar la variabilidad posterior al filtro.")
st.write("- Gráficos de Distribución Normal Después: Se mostrarán gráficos de distribución normal para visualizar la distribución de los datos después de la aplicación del filtro. Estas gráficas también se pueden descargar haciendo clic derecho sobre ellas.")

# Validación de la Media Propia con "Zscore"
st.header("Validación de la Media Propia con 'Zscore':")
st.write("5. Después de aplicar el filtro y analizar la tendencia central y la variabilidad, proceda con la validación de la media propia utilizando el 'Zscore' siguiendo estos pasos:")
st.write("- Ingrese el nombre del analito en el campo 'Analito.'")
st.write("- Ingrese las unidades del analito en el campo 'Unidades.'")
st.write("- Seleccione el nivel del control al que pertenecen los datos (Bajo, Normal o Alto) en el campo 'Nivel.'")
st.write("- Ingrese la media de comparación proporcionada por el fabricante en el campo 'Media Comparación.'")
st.write("- Ingrese la desviación estándar de comparación proporcionada por el fabricante en el campo 'DE Comparación.'")
st.write("- Seleccione el criterio de aceptabilidad (1.65 o 2.0) en el campo 'Criterio.'")
st.write("- Haga clic en 'Validar Media con Zscore' para calcular el valor Z y determinar si la media propia cumple con el criterio de aceptabilidad.")
st.write("6. Se mostrará una tabla con los resultados, incluyendo la interpretación.")

# Descargar Resultados
st.header("Descargar Resultados:")
st.write("7. Después de aplicar el filtro y validar la media propia, puede descargar los resultados haciendo clic en los botones de descarga disponibles en la interfaz.")

st.write("**Nota:** Si en algún momento necesita cargar un nuevo archivo o realizar un nuevo análisis, puede volver a la sección correspondiente y seguir las instrucciones.")

# Puedes agregar más contenido o personalización según tus necesidades.
