import discord #Librería para hablar con discord
import feedparser #Librería para poder conectarse a YT
import requests # Necesario para revisar cabeceras
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

# Función que devuelve un bool si es un short, se comprueba dependiendo el código que nos devuelve Youtube al acceder al short/...
def es_short(video_id):
    #Prueba si un ID de vídeo pertenece a un Short comprobando si YouTube nos redirige.
    url_prueba = f"https://www.youtube.com/shorts/{video_id}"
    try:
        # Se pide solo la cabecera para saber si nos quiere redirigir o no
        respuesta = requests.head(url_prueba, allow_redirects=False, timeout=5)
        
        # Si YouTube responde con un 200 (OK), es que la página del Short existe -> ES UN SHORT
        # Si responde con 303 o similar, es que nos está echando al reproductor normal -> ES VÍDEO
        return respuesta.status_code == 200
    except Exception as e:
        print(f"Error comprobando el Short: {e}")
        return False


# Crear el bot y decirle que nuestros comandos empezarán por "!"
bot = commands.Bot(command_prefix="!", intents=intents)

def obtener_feed_seguro(url):
    # 1. Creamos una identidad falsa (User-Agent)
    cabeceras = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        # 2. Hacemos la petición HTTP usando requests y nuestra identidad falsa
        respuesta = requests.get(url, headers=cabeceras, timeout=10)
        
        # 3. Le pasamos el texto bruto (el XML de YouTube) a feedparser para que lo ordene
        return feedparser.parse(respuesta.content)
    except Exception as e:
        print(f"Error en la petición: {e}")
        return None

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
    global ultimo_enlace_conocido 
    
    canal = bot.get_channel(ID_CANAL)
    if canal is None: return 

    feed = obtener_feed_seguro(URL_RSS_ADO)
    
    if feed and len(feed.entries) > 0:
        # Recorremos los vídeos desde el más nuevo al más viejo
        for video in feed.entries:
            video_id = video.yt_videoid # Sacamos el ID oculto en el XML
            
            # Si NO es un short, entonces es el vídeo que buscamos
            if not es_short(video_id):
                link_actual = video.link
                titulo_actual = video.title
                
                # --- Lógica de memoria ---
                if ultimo_enlace_conocido is None:
                    ultimo_enlace_conocido = link_actual
                    print(f"Sistema inicializado. Último VÍDEO (No Short) en memoria: {titulo_actual}")
                    
                elif link_actual != ultimo_enlace_conocido:
                    await canal.send(f"LA ADOMINACIÓN CONTINÚA\n**{titulo_actual}**\n{link_actual}")
                    ultimo_enlace_conocido = link_actual
                else:
                    print("Chequeo rutinario: No hay vídeos normales nuevos.")
                
                # Importante: Como ya hemos encontrado el último vídeo válido, rompemos el bucle
                break

# ==========================================
# COMANDOS MANUALES
# ==========================================

# Decorador necesario para que la función bot sepa usar mi función ado
# Como se utilizan Sockets Web es necesario que sea asíncrono para que el bot no colapse si tiene muchas peticiones.
@bot.command()
async def ado(ctx):
    await ctx.send("¿Ganas de escuchar a ADO? Normal, te llega en 3,2,1...")
    
    feed = obtener_feed_seguro(URL_RSS_ADO)
    
    if feed and len(feed.entries) > 0:
        for video in feed.entries:
            if not es_short(video.yt_videoid):
                titulo = video.title
                link = video.link
                await ctx.send(f"**{titulo}**\n{link}")
                return # Salimos de la función al encontrarlo
                
        await ctx.send("Vaya, parece que solo he encontrado Shorts recientemente.")
    else:
        await ctx.send("Error de conexión con la base de datos de YouTube.")

# ==========================================
# ARRANQUE DEL BOT
# ==========================================

# Obtiene el valor de la variable de entorno
TOKEN = os.getenv("DISCORD_TOKEN") 

if TOKEN is None:
    print("Error: No se ha encontrado el token en las variables de entorno.")
else:
    bot.run(TOKEN)