# Laboratorio 5  
## Variabilidad de la frecuencia cardíaca (HRV) y balance autonómico  

**Programa:** Ingeniería Biomédica  
**Asignatura:** Procesamiento Digital de Señales  
**Universidad:** Universidad Militar Nueva Granada  
**Estudiantes:** Danna Rivera, Duvan Paez

##  Introducción
 
El corazón no late a intervalos perfectamente regulares. Incluso en reposo, existe una variación natural en el tiempo entre latido y latido, conocida como variabilidad de la frecuencia cardíaca (HRV, por sus siglas en inglés). Esta variabilidad no es aleatoria: refleja el estado del sistema nervioso autónomo (SNA) y su influencia constante sobre el nodo sinusal del corazón.
 
El SNA opera a través de dos ramas con efectos opuestos sobre la frecuencia cardíaca. La rama simpática, asociada a situaciones de alerta, estrés o demanda cognitiva, acelera el corazón y reduce la variabilidad entre latidos. La rama parasimpática, predominante en el reposo, desacelera el corazón y permite una mayor variabilidad. El balance entre ambas ramas puede evaluarse de forma no invasiva a partir de la señal electrocardiográfica (ECG).
 
En este laboratorio se adquirió una señal ECG de 4 minutos dividida en dos condiciones: los primeros 2 minutos en reposo absoluto y los últimos 2 minutos durante la lectura en voz alta de un texto. La lectura en voz alta implica actividad cognitiva, motora y respiratoria, lo que se espera que produzca una activación simpática medible en la HRV.
 
El procesamiento de la señal incluyó filtrado IIR pasa banda, detección de picos R, cálculo de intervalos R-R y análisis tanto en el dominio del tiempo (media y SDNN) como mediante el diagrama de Poincaré (SD1, SD2, CSI, CVI). El objetivo es evidenciar, a través de estos parámetros, el cambio en el balance autonómico entre ambas condiciones.
 
---

## Parte A 
### a) Fundamento teórico

### Sistema nervioso autónomo
El sistema nervioso autónomo (SNA) regula funciones involuntarias del organismo a través de dos ramas:
 
- **Simpático:** activa al organismo ante situaciones de estrés o demanda cognitiva. Aumenta la frecuencia cardíaca y reduce la variabilidad (intervalos R-R más cortos y uniformes).
- **Parasimpático (vagal):** domina en estados de reposo. Disminuye la frecuencia cardíaca y aumenta la variabilidad (intervalos R-R más largos y variables).
### HRV – Variabilidad de la Frecuencia Cardíaca
La HRV mide las fluctuaciones en el tiempo entre latidos consecutivos (intervalos R-R), extraídos de la señal ECG. Es un indicador no invasivo del balance autonómico.
 
**Parámetros en el dominio del tiempo:**
- **Media R-R:** promedio de los intervalos entre picos R consecutivos (ms). Inversamente relacionado con la frecuencia cardíaca.
- **SDNN:** desviación estándar de los intervalos R-R. Refleja la variabilidad total de la señal.
### Diagrama de Poincaré
Representación gráfica donde cada intervalo R-R se grafica contra el siguiente (RRₙ vs RRₙ₊₁). La dispersión de la nube de puntos permite estimar el balance simpático/parasimpático mediante:
 - **SD1:**  Variabilidad a corto plazo → tono vagal
 - **SD2:**  Variabilidad a largo plazo → simpático + parasimpático
 - **CSI:**  Índice de actividad simpática
 - **CVI:**  Índice de actividad vagal
---
### b) Adquisición de la señal ECG

Se registró la señal ECG de un sujeto durante 4 minutos:
- **0–2 min:** reposo absoluto (inmóvil y en silencio)
- **2–4 min:** lectura en voz alta de un texto

## Parte B 
### c) Pre-procesamiento de la señal
**Filtro IIR Butterworth pasa banda:**
- Frecuencias de corte: 0.5 Hz – 40 Hz
- Orden: 4
- Implementado con condiciones iniciales en 0 (`lfilter`)
La señal filtrada se dividió en dos segmentos de 2 minutos. En cada segmento se detectaron los picos R con umbral dinámico (60% del máximo) y distancia mínima de 0.3 s entre picos.
 ---
 ### d) Análisis de la HRV en el dominio del tiempo
 Con los intervalos R-R de cada segmento se calcularon y compararon los parámetros básicos de la HRV:
 
- **Media R-R:** valor promedio de los intervalos entre picos R consecutivos, expresado en milisegundos. Inversamente relacionado con la frecuencia cardíaca: una media R-R mayor indica un corazón más lento y mayor predominio parasimpático.
- **SDNN:** desviación estándar de los intervalos R-R. Refleja la variabilidad total de la señal. Un SDNN alto indica mayor variabilidad y mejor regulación autonómica; un SDNN bajo sugiere predominio simpático o menor flexibilidad del sistema.
La comparación entre ambos segmentos permite evidenciar si la tarea de lectura en voz alta produce un cambio relevante en el balance autonómico respecto al reposo.
