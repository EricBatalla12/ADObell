import discord #Librería para hablar con discord
import feedparser #Librería para poder conectarse a YT
import requests # Necesario para revisar cabeceras
import json # Usado para guardar los canales
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

# NUESTRA MEMORIA: Variable global para guardar el último vídeo visto
ultimo_enlace_conocido = None

# Configuración de qué puede ver el bot, default para ver si se ha conectado
# message_content para ver mensajes en el chat (comandos). 
intents = discord.Intents.default()
intents.message_content = True

ARCHIVO_CANALES = "canales.json"

def cargar_canales():
    #Lee el archivo JSON. Si no existe, devuelve un diccionario vacío.
    if not os.path.exists(ARCHIVO_CANALES):
        return {}
    with open(ARCHIVO_CANALES, "r") as f:
        return json.load(f)

def guardar_canales(datos):
    #Guarda el diccionario actualizado en el archivo JSON.
    with open(ARCHIVO_CANALES, "w") as f:
        json.dump(datos, f, indent=4)

def canal_existe(canales, canal_id):
    return canal_id in canales.values()

# Función que devuelve un bool si es un short, se comprueba dependiendo el código que nos devuelve Youtube al acceder al short/...
def es_short(video_id):
    #Prueba si un ID de vídeo pertenece a un Short comprobando si YouTube nos redirige.
    url_prueba = f"https://www.youtube.com/shorts/{video_id}"
    try:
        # Se pide solo la cabecera para saber si nos quiere redirigir o no
        respuesta = requests.head(url_prueba, allow_redirects=False, timeout=5)
        
        # Si YouTube responde con un 200 (OK), es que la página del Short existe 
        # Si responde con 303 o similar, es que nos está echando al reproductor normal 
        return respuesta.status_code == 200
    except Exception as e:
        print(f"Error comprobando el Short: {e}")
        return False

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

# NUEVO COMANDO AUTOMÁTICO: Un bucle que se repite cada 10 minutos
@tasks.loop(minutes=10)
async def vigilar_youtube():
    global ultimo_enlace_conocido 
    
    feed = feedparser.parse(URL_RSS_ADO)
    
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
                    print(f"Sistema inicializado. Último VÍDEO en memoria: {titulo_actual}")
                    
                elif link_actual != ultimo_enlace_conocido:
                    # Nuevo video se avisa a TODOS los servidores
                    canales = cargar_canales()
                    
                    for server_id, canal_id in canales.items():
                        canal_destino = bot.get_channel(canal_id)
                        if canal_destino:
                            try:
                                await canal_destino.send(f"LA ADOMINACIÓN CONTINUA\n**{titulo_actual}**\n{link_actual}", silent = True)
                            except Exception as e:
                                print(f"Error al enviar al canal {canal_id}: {e}")
                                
                    ultimo_enlace_conocido = link_actual
                else:
                    print("Chequeo rutinario: No hay vídeos normales nuevos.")
                
                # CRÍTICO: Rompemos el bucle al encontrar el último vídeo válido para no leer los antiguos
                break 

# ==========================================
# COMANDOS MANUALES
# ==========================================

# Decorador necesario para que la función bot sepa usar mi función ado
# Como se utilizan Sockets Web es necesario que sea asíncrono para que el bot no colapse si tiene muchas peticiones.
@bot.command()
async def ado(ctx):
    await ctx.send("¿Ganas de escuchar a ADO? Normal, te llega en 3,2,1...", silent = True)
    
    feed = feedparser.parse(URL_RSS_ADO)
    
    if feed and len(feed.entries) > 0:
        for video in feed.entries:
            if not es_short(video.yt_videoid):
                titulo = video.title
                link = video.link
                await ctx.send(f"**{titulo}**\n{link}", silent = True)
                return # Salimos de la función al encontrarlo
                
        await ctx.send("Vaya, parece que solo he encontrado Shorts recientemente.", silent = True)
    else:
        await ctx.send("Error de conexión con la base de datos de YouTube.", silent = True) 


@bot.command()
@commands.has_permissions(administrator=True)
async def setcanal(ctx):
    #Configura el canal actual para recibir notificaciones de Ado.
    canales = cargar_canales()
    
    if canal_existe(canales, ctx.channel.id):
        await ctx.send("Este canal ya está establecido", silent = True)
        return

    # Guardamos la ID del servidor como llave y la ID del canal como valor
    canales[str(ctx.guild.id)] = ctx.channel.id
    guardar_canales(canales)
    
    await ctx.send(f"✅ Las alertas de la ADOMINATION llegarán a {ctx.channel.mention}", silent = True)


@setcanal.error
async def setcanal_error(ctx, error):
    #Maneja el error si alguien sin permisos intenta usar !setcanal.
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Necesitas permisos de Administrador para usar este comando.", silent = True)

# ==========================================
# ARRANQUE DEL BOT
# ==========================================

# Obtiene el valor de la variable de entorno
TOKEN = os.getenv("DISCORD_TOKEN") 

if TOKEN is None:
    print("Error: No se ha encontrado el token en las variables de entorno.")
else:
    bot.run(TOKEN)