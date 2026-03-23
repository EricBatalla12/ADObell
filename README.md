# 🟦 ADObell: The ADOMINATION Sentinel

![Status](https://img.shields.io/badge/Status-Active-blue)
![Python](https://img.shields.io/badge/Python-3.10+-yellow)
![Library](https://img.shields.io/badge/Library-Discord.py-blueviolet)

> **"You will see the future songs with ADObell"**

**ADObell** es un centinela automatizado diseñado para la comunidad de fans de la artista japonesa **Ado**. Su misión es simple pero vital: vigilar el canal oficial de YouTube de Ado las 24 horas del día e interceptar cualquier nuevo lanzamiento de forma instantánea.

## 🚀 Funcionalidades

* **Vigilancia 24/7 (Polling)**: Escanea el feed RSS de YouTube cada minuto buscando actualizaciones.
* **Sistema de Memoria**: Utiliza una lógica de estado para evitar notificaciones duplicadas (solo avisa cuando el enlace es realmente nuevo).
* **Comando On-Demand**: Usa `!ado` en Discord para consultar el último vídeo subido en cualquier momento.
* **Disfraz de Tráfico (Stealth Mode)**: Implementa cabeceras `User-Agent` personalizadas mediante la librería `requests` para evitar bloqueos de seguridad de YouTube.
* **Arquitectura Asíncrona**: Construido sobre `discord.ext.tasks` para un rendimiento eficiente sin bloquear el bot.

## 🛠️ Stack Tecnológico

* **Lenguaje:** [Python](https://www.python.org/)
* **Librería de Discord:** [discord.py](https://discordpy.readthedocs.io/)
* **Parser de Datos:** [feedparser](https://pythonhosted.org/feedparser/) (para procesar el XML de YouTube).
* **Gestión de Red:** [requests](https://requests.readthedocs.io/) (para bypass de seguridad).
* **Hosting:** [Discloud](https://discloudbot.com/) (Despliegue en la nube).

## 📦 Instalación y Configuración

1. Clona el repositorio:
   ```bash
   git clone [https://github.com/tu-usuario/ADObell.git](https://github.com/tu-usuario/ADObell.git)
