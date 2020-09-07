# Intro!

Este repositorio contiene el desarrollo de un modelo de clasificación para la recuperación de documentos. El modelo utiliza datos de entrenamiento, de modo que puede ordenar nuevos documentos acorde con sus grados de relevancia.

El modelo de clasificación es un modelo de asociación de tópicos que, a través de la recopilación de la evaluación, de la relevancia entre la similitud de un par de documentos, proporcionada por usuarios; busca mejorar un sistema de recuperación de documentos ya existente.


El presente proyecto forma parte del TFM de la Maestría en Ciencia de Datos de la UPM.

# Carpetas y archivos

## Carpetas
**Scripts** -> Todos los Scripts ejecutados en el entrenamiento y prueba del modelo

**Scripts/Training** -> Scripts ejecutados en la fase de entrenamiento del modelo

**Scripts/Test** -> Scripts ejecutados en la fase de prueba del modelo

## Archivos de la carpeta Training

`Algorithm1.py` -> Script de la implementación del primer algoritmo del modelo de generación de asociación de tópicos.

`Algorithm2.py` -> Script de la implementación del segundo algoritmo del modelo de generación de asociación de tópicos.

`GeneralFunctions.py` -> Script que tiene implementadas las funciones que usan en conjunto el algoritmo 1, algoritmo 2 del modelo y demás Scripts usados en la fase de prueba.

**results_rank_test.json** -> muestra de la estructura JSON que recibe el algoritmo como entrada, desde el sistema de retroalimentación del usuario. 

## Archivos de la carpeta Test

`NewScriptBefore.py` -> Script que calcula la precisión del sistema antes de aplicar las asociaciones de tópicos.

`NewScriptAfter.py` -> Script que calcula la precisión del sistema después de aplicar las asociaciones de tópicos.

`UpdateTopicDocuments.py` -> Script que actualiza los niveles de tópicos en los documentos con los tópicos asociados.

`PopulateTestDataset.py` -> Script que agrega documentos al dataset de pruebas.

**rank_template.json** -> plantilla que se usa para obtener el top k de documentos similares a un documento.

**log_precision_results_before_1.csv** -> log generado durante el cálculo de la precisión antes de aplicar las asociaciones de tópicos.

**log_test_before_1.csv** -> log generado por el Script `NewScriptBefore.py`

**log_precision_results_after_1.csv** -> log generado durante el cálculo de la precisión después de aplicar las asociaciones de tópicos.

**log_test_after_1.csv** -> log generado por el Script `NewScriptAfter.py`

**rules_tender_new_new.csv** -> reglas generadas en el entrenamiento del modelo.
 
# Proceso de ejecución de Scripts

Para proceder con la ejecución de Scripts como replicación del proyecto de TFM es necesario seguir los pasos de la Demo disponible en: https://github.com/librairy/demo y corroborar que el puerto de las url de las APIs sean los correctos en los Scripts.

## Ejecución de Scripts con retroalimentación CrowdsourcingDocumentSimilarity

Hay dos vías mediante las cuales se puede replicar el proceso de generación de reglas. La primera vía es mediante el Script `ScriptTrainingDataset.py` disponible en la carpeta Training. Se puede ejecutar directamente este Script que toma como muestra el archivo pairs_en.csv disponible en https://github.com/TBFY/CrowdsourcingDocumentSimilarity/tree/master/data que contiene la retroalimentación de los documentos con source_s = Tender y genera las reglas con base a esta retroalimentación

## Ejecución de Scripts desde el sistema de retroalimentación

- La segunda vía del proceso de generación de reglas es mediante el sistema de retroalimentación que aporta este TFM.
	> * Para ejecutar los Scripts desde el sistema de retroalimentación es necesario tener levantado el sistema disponible en: https://github.com/Ka77y/TFM-IR.
	> * Luego se debe levantar la API disponible en la carpeta *API* adjunta en el repositorio y comprobar que el puerto de conexión entre el sistema y la API sea el mismo.

Desde el sistema se introduce la retroalimentación de la relevancia de un par de documentos y se lo envía. La API y los Scripts se ejecutarán de manera ordenada una vez que se obtenga la API desde este Sistema. 
