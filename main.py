import discord #Librería para hablar con discord
import feedparser #Librería para poder conectarse a YT
import os #Librería de seguridad para acceder al TOKEN desde local
from dotenv import load_dotenv
from discord.ext import commands, tasks #Comandos de bots y tareas en segundo plano (tasks)

# ==========================================
# INFORMACIÓN ÚTIL:
# ctx es un paquete JSON enviado desde Discord hasta mi programa que la librería 
# discord parsea para conocer de dónde viene el paquete, quién lo envía y datos del servidor.
# ==========================================

# Carga las variables del archivo .env al entorno del sistema
load_dotenv()

# ==========================================
# CONSTANTES Y CONFIGURACIÓN
# ==========================================

# La URL del RSS de YouTube con la ID de Ado
URL_RSS_ADO = "https://www.youtube.com/feeds/videos.xml?channel_id=UCln9P4Qm3-EAY4aiEPmRwEA"
# Buscar el canal de texto
ID_CANAL = int(os.getenv("ID_CANAL"))

# NUESTRA MEMORIA: Variable global para guardar el último vídeo visto
ultimo_enlace_conocido = None

# Configuración de qué puede ver el bot, default para ver si se ha conectado
# message_content para ver mensajes en el chat (comandos). 
intents = discord.Intents.default()
intents.message_content = True

# Crear el bot y decirle que nuestros comandos empezarán por "!"
bot = commands.Bot(command_prefix="!", intents=intents)

# ==========================================
# EVENTOS DEL SISTEMA
# ==========================================

@bot.event
async def on_ready():
    print(f'El bot: {bot.user} está en funcionamiento ')
    
    # Arrancamos el motor de vigilancia en segundo plano si no está encendido ya
    if not vigilar_youtube.is_running():
        vigilar_youtube.start()

# ==========================================
# BUCLE AUTOMÁTICO (BACKGROUND TASK)
# ==========================================

# NUEVO COMANDO AUTOMÁTICO: Un bucle que se repite cada 1 minuto
@tasks.loop(minutes=10)
async def vigilar_youtube():
    global ultimo_enlace_conocido # Le decimos a Python que use nuestra memoria global
    
    # 1. Obtenemos el canal de texto
    canal = bot.get_channel(ID_CANAL)
    
    if canal is None:
        print("Error: No he encontrado el canal de Discord.")
        return # Si no hay canal, abortamos el ciclo

    # 2. Leer YouTube (parseo del .xml obtenido)
    feed = feedparser.parse(URL_RSS_ADO)
    
    if len(feed.entries) > 0:
        video_actual = feed.entries[0]
        link_actual = video_actual.link
        titulo_actual = video_actual.title
        
        # 3. Lógica de comprobación de Estado (¿Es nuevo?)
        if ultimo_enlace_conocido is None:
            # La primera vez que arranca, solo memoriza el vídeo actual en silencio
            ultimo_enlace_conocido = link_actual
            print(f"Sistema inicializado. Último vídeo en memoria: {titulo_actual}")
            
        elif link_actual != ultimo_enlace_conocido:
            # Nuevo video. El enlace de internet es distinto al de la memoria
            await canal.send(f"LA ADOMINACIÓN CONTINUA\n**{titulo_actual}**\n{link_actual}")
            
            # Actualizamos la memoria con el nuevo vídeo
            ultimo_enlace_conocido = link_actual
        else:
            # El vídeo es el mismo, no hacemos nada (puedes quitar este print luego para no manchar la consola)
            print("Chequeo rutinario: No hay vídeos nuevos.")

# ==========================================
# COMANDOS MANUALES
# ==========================================

# Decorador necesario para que la función bot sepa usar mi función ado
@bot.command()
# Como se utilizan Sockets Web es necesario que sea asíncrono para que el bot no colapse si tiene muchas peticiones.
async def ado(ctx):
    # Cuando el servidor de Discord responda se libera del await.
    await ctx.send("Buscando el último vídeo de Ado...")

    # El bot lee el archivo (parseo del .xml obtenido usando la constante global)
    feed = feedparser.parse(URL_RSS_ADO)
    
    # Si encuentra vídeos, saca el título y el link
    if len(feed.entries) > 0:
        ultimo_video = feed.entries[0]
        titulo = ultimo_video.title
        link = ultimo_video.link
        
        await ctx.send(f"¡Aquí tienes! **{titulo}**\n{link}")
    else:
        await ctx.send("Vaya, no he encontrado ningún vídeo.")

# ==========================================
# ARRANQUE DEL BOT
# ==========================================

# Obtiene el valor de la variable de entorno
TOKEN = os.getenv("DISCORD_TOKEN") 

if TOKEN is None:
    print("Error: No se ha encontrado el token en las variables de entorno.")
else:
    bot.run(TOKEN)