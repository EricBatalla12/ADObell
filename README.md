# 🟦 ADObell: The ADOMINATION Sentinel

![Status](https://img.shields.io/badge/Status-Active-blue)
![Python](https://img.shields.io/badge/Python-3.10+-yellow)
![Library](https://img.shields.io/badge/Library-Discord.py-blueviolet)

> **"You will see the future songs with ADObell"**

**ADObell** bot creado para la comunidad de **Ado**. Su misión es vigilar el canal oficial de YouTube de Ado las 24 horas del díapara avisar de nuevos avisos.

## Funcionalidades

* **Vigilancia 24/7 (Polling)**: Escanea el feed RSS de YouTube cada minuto buscando actualizaciones.
* **Sistema de Memoria**: Utiliza una lógica de estado para evitar notificaciones duplicadas (solo avisa cuando hay video nuevo).
* **Comando On-Demand**: Usa `!ado` en Discord para consultar el último vídeo subido en cualquier momento.
* **Comando setter**: Usa `!setcanal` en Dicord para establecer dónde quieres que el bot te avise de nuevos lanzamientos.
* **Sistema de filtrado**: Mediante comprobaciones de redireccionamiento se filtra para que solo tenga en cuenta los nuevos videos (no shorts).
* **Arquitectura Asíncrona**: Construido sobre `discord.ext.tasks` para un rendimiento eficiente sin bloquear el bot.

## Tecnológia utilizada

* **Lenguaje:** [Python]
* **Librería de Discord:** [discord.py]
* **Parser de Datos:** [feedparser] (para procesar el XML de YouTube).
* **Lectura de cabeceras** [requests] (conocer el redireccionamiento de las cabeceras).
* **Hosting:** [Railway](railway.com) (Despliegue en la nube).

![ADObell](blob:https://gemini.google.com/7837546c-e82d-46ff-91b6-3c25e24480a6)
