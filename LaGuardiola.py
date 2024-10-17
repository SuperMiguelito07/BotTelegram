from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext
import json
import os

# Obtener el token del bot de una variable de entorno
Token: Final = '7475336910:AAErS0uJf_XzXZ6xl0OrLdkGzPMDnjtukJM'  # Asegúrate de establecer esta variable de entorno
BOT_USERNAME: Final = '@LaGuardiola_Bot'  # Nombre del Bot

# Ruta del archivo JSON donde se guardarán los datos
DATA_FILE = 'finanzas.json'

# Variables de control de espera por usuario
esperando_reserva = {}
esperando_quotes = {}
esperando_gastos_diaris = {}
esperando_ganancies_esporadiques = {}
esperando_ganancies_mensuals = {}

# Función para cargar los datos desde el archivo JSON
def cargar_datos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    else:
        return {}  # Si el archivo no existe, devolvemos un diccionario vacío

# Función para guardar los datos en el archivo JSON
def guardar_datos(datos):
    with open(DATA_FILE, 'w') as file:
        json.dump(datos, file, indent=4)

# Función para obtener o inicializar datos de un usuario
def obtener_datos_usuario(user_id):
    datos = cargar_datos()
    user_id_str = str(user_id)
    if user_id_str not in datos:
        # Si el usuario no existe, inicializamos sus datos
        datos[user_id_str] = {
            'salary': 0,
            'ingresos': 0,
            'estalvi': 0,
            'despeses': 0,
            'quotes': 0,
            'gastos_diaris': 0,
            'ganancies_esporadiques': 0,
            'ganancies_mensuals': 0
        }
        guardar_datos(datos)
    return datos

# Función para guardar los datos de un usuario
def guardar_datos_usuario(user_id, datos_usuario):
    datos = cargar_datos()
    datos[str(user_id)] = datos_usuario
    guardar_datos(datos)

# Comando /start
async def start_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('¡Hola! ¿Cómo puedo ayudarte?')

# Comando /help
async def help_command(update: Update, context: CallbackContext):
    help_text = (
        "/help\n"
        "Aquí tienes los comandos disponibles para el bot LA GUARDIOLA:\n"
        "/saldo: Muestra tu saldo actual.\n"
        "/reserva: Consulta los ahorros que tienes reservados.\n"
        "/introduir_reserva: Permite introducir y actualizar la cantidad que quieres reservar como ahorro.\n"
        "/despeses: Muestra el total de gastos acumulados.\n"
        "/quotesMensuals: Visualiza los gastos fijos mensuales.\n"
        "/introduirQuotesMensuals: Introduce o actualiza los gastos mensuales.\n"
        "/gastosDiaris: Consulta tus gastos diarios.\n"
        "/introduirGastosDiaris: Introduce o actualiza los gastos diarios.\n"
        "/ganancies: Muestra los ingresos totales que tienes.\n"
        "/introduirGananciesEsporadiques: Permite agregar ingresos esporádicos.\n"
        "/introduirGananciesMensuals: Introduce o actualiza tus ganancias mensuales."
    )
    await update.message.reply_text(help_text)

# Comando /reserva
async def reserva_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    datos = obtener_datos_usuario(user_id)
    estalvi = datos[str(user_id)]['estalvi']
    await update.message.reply_text(f'Tienes {estalvi}€ reservados para el ahorro.')

# Comando /introduir_reserva
async def introducir_reserva_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    esperando_reserva[user_id] = True
    await update.message.reply_text('Introduce la cantidad que deseas reservar como ahorro.')

async def manejar_reserva_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if esperando_reserva.get(user_id, False):
        datos = obtener_datos_usuario(user_id)
        try:
            quantitat = float(update.message.text.replace('€', '').strip())
            datos[str(user_id)]['estalvi'] += quantitat  # Sumar a estalvi
            esperando_reserva[user_id] = False

            # Recalcular valores
            datos[str(user_id)]['despeses'] = datos[str(user_id)]['quotes'] + datos[str(user_id)]['gastos_diaris']
            datos[str(user_id)]['ingresos'] = datos[str(user_id)]['ganancies_esporadiques'] + datos[str(user_id)]['ganancies_mensuals']
            datos[str(user_id)]['salary'] = datos[str(user_id)]['ingresos'] - datos[str(user_id)]['despeses'] - datos[str(user_id)]['estalvi']

            guardar_datos_usuario(user_id, datos[str(user_id)])
            await update.message.reply_text(f'Has reservado {quantitat}€ como ahorro. Total ahorrado: {datos[str(user_id)]["estalvi"]}€. Saldo actual: {datos[str(user_id)]["salary"]}€.')
        except ValueError:
            await update.message.reply_text('Por favor, introduce una cantidad válida.')

# Comando /saldo
async def saldo_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    datos = obtener_datos_usuario(user_id)
    salary = datos[str(user_id)]['ingresos'] - datos[str(user_id)]['despeses'] - datos[str(user_id)]['estalvi']
    datos[str(user_id)]['salary'] = salary
    guardar_datos_usuario(user_id, datos[str(user_id)])
    await update.message.reply_text(f'Tu saldo actual es de {salary}€.')

# Comando /despeses
async def despeses_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    datos = obtener_datos_usuario(user_id)
    despeses = datos[str(user_id)]['quotes'] + datos[str(user_id)]['gastos_diaris']
    datos[str(user_id)]['despeses'] = despeses
    datos[str(user_id)]['salary'] = datos[str(user_id)]['ingresos'] - datos[str(user_id)]['despeses'] - datos[str(user_id)]['estalvi']
    guardar_datos_usuario(user_id, datos[str(user_id)])
    await update.message.reply_text(f'El total de tus gastos hasta el momento es de {despeses}€. Saldo actual: {datos[str(user_id)]["salary"]}€.')

# Comando /quotesMensuals
async def quotes_mensuals_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    datos = obtener_datos_usuario(user_id)
    quotes = datos[str(user_id)]['quotes']
    await update.message.reply_text(f'Los gastos mensuales fijos son de {quotes}€.')

# Comando /introduirQuotesMensuals
async def introduir_quotes_mensuals_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    esperando_quotes[user_id] = True
    await update.message.reply_text('Introduce las nuevas cuotas mensuales que quieres agregar.')

async def manejar_quotes_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if esperando_quotes.get(user_id, False):
        datos = obtener_datos_usuario(user_id)
        try:
            cantidad = float(update.message.text.replace('€', '').strip())
            datos[str(user_id)]['quotes'] = cantidad  # Actualizar las cuotas mensuales
            esperando_quotes[user_id] = False

            # Recalcular valores
            datos[str(user_id)]['despeses'] = datos[str(user_id)]['quotes'] + datos[str(user_id)]['gastos_diaris']
            datos[str(user_id)]['salary'] = datos[str(user_id)]['ingresos'] - datos[str(user_id)]['despeses'] - datos[str(user_id)]['estalvi']

            guardar_datos_usuario(user_id, datos[str(user_id)])
            await update.message.reply_text(f'Has actualizado las cuotas mensuales a {cantidad}€. Saldo actual: {datos[str(user_id)]["salary"]}€.')
        except ValueError:
            await update.message.reply_text('Por favor, introduce una cantidad válida.')

# Comando /gastosDiaris
async def gastos_diaris_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    datos = obtener_datos_usuario(user_id)
    gastos_diaris = datos[str(user_id)]['gastos_diaris']
    await update.message.reply_text(f'Los gastos diarios hasta ahora son de {gastos_diaris}€.')

# Comando /introduirGastosDiaris
async def introducir_gastos_diaris_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    esperando_gastos_diaris[user_id] = True
    await update.message.reply_text('Introduce la cantidad de gastos diarios.')

async def manejar_gastos_diaris_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if esperando_gastos_diaris.get(user_id, False):
        datos = obtener_datos_usuario(user_id)
        try:
            cantidad = float(update.message.text.replace('€', '').strip())
            datos[str(user_id)]['gastos_diaris'] += cantidad  # Sumar a gastos diarios
            esperando_gastos_diaris[user_id] = False

            # Recalcular valores
            datos[str(user_id)]['despeses'] = datos[str(user_id)]['quotes'] + datos[str(user_id)]['gastos_diaris']
            datos[str(user_id)]['salary'] = datos[str(user_id)]['ingresos'] - datos[str(user_id)]['despeses'] - datos[str(user_id)]['estalvi']

            guardar_datos_usuario(user_id, datos[str(user_id)])
            await update.message.reply_text(f'Has agregado {cantidad}€ a los gastos diarios. Total de gastos diarios: {datos[str(user_id)]["gastos_diaris"]}€. Saldo actual: {datos[str(user_id)]["salary"]}€.')
        except ValueError:
            await update.message.reply_text('Por favor, introduce una cantidad válida.')

# Comando /ganancies
async def ganancies_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    datos = obtener_datos_usuario(user_id)
    ingresos = datos[str(user_id)]['ganancies_esporadiques'] + datos[str(user_id)]['ganancies_mensuals']
    datos[str(user_id)]['ingresos'] = ingresos
    datos[str(user_id)]['salary'] = ingresos - datos[str(user_id)]['despeses'] - datos[str(user_id)]['estalvi']
    guardar_datos_usuario(user_id, datos[str(user_id)])
    await update.message.reply_text(f'Tus ganancias totales son de {ingresos}€. Saldo actual: {datos[str(user_id)]["salary"]}€.')

# Comando /introduirGananciesEsporadiques
async def introducir_ganancies_esporadiques_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    esperando_ganancies_esporadiques[user_id] = True
    await update.message.reply_text('Introduce los ingresos esporádicos que quieres agregar.')

async def manejar_ganancies_esporadiques_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if esperando_ganancies_esporadiques.get(user_id, False):
        datos = obtener_datos_usuario(user_id)
        try:
            cantidad = float(update.message.text.replace('€', '').strip())
            datos[str(user_id)]['ganancies_esporadiques'] += cantidad  # Sumar a ganancias esporádicas
            esperando_ganancies_esporadiques[user_id] = False

            # Recalcular valores
            datos[str(user_id)]['ingresos'] = datos[str(user_id)]['ganancies_esporadiques'] + datos[str(user_id)]['ganancies_mensuals']
            datos[str(user_id)]['salary'] = datos[str(user_id)]['ingresos'] - datos[str(user_id)]['despeses'] - datos[str(user_id)]['estalvi']

            guardar_datos_usuario(user_id, datos[str(user_id)])
            await update.message.reply_text(f'Has agregado {cantidad}€ a las ganancias esporádicas. Total de ganancias esporádicas: {datos[str(user_id)]["ganancies_esporadiques"]}€. Saldo actual: {datos[str(user_id)]["salary"]}€.')
        except ValueError:
            await update.message.reply_text('Por favor, introduce una cantidad válida.')

# Comando /introduirGananciesMensuals
async def introducir_ganancies_mensuals_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    esperando_ganancies_mensuals[user_id] = True
    await update.message.reply_text('Introduce las ganancias mensuales.')

async def manejar_ganancies_mensuals_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if esperando_ganancies_mensuals.get(user_id, False):
        datos = obtener_datos_usuario(user_id)
        try:
            cantidad = float(update.message.text.replace('€', '').strip())
            datos[str(user_id)]['ganancies_mensuals'] += cantidad  # Sumar a ganancias mensuales
            esperando_ganancies_mensuals[user_id] = False

            # Recalcular valores
            datos[str(user_id)]['ingresos'] = datos[str(user_id)]['ganancies_esporadiques'] + datos[str(user_id)]['ganancies_mensuals']
            datos[str(user_id)]['salary'] = datos[str(user_id)]['ingresos'] - datos[str(user_id)]['despeses'] - datos[str(user_id)]['estalvi']

            guardar_datos_usuario(user_id, datos[str(user_id)])
            await update.message.reply_text(f'Has agregado {cantidad}€ a las ganancias mensuales. Total de ganancias mensuales: {datos[str(user_id)]["ganancies_mensuals"]}€. Saldo actual: {datos[str(user_id)]["salary"]}€.')
        except ValueError:
            await update.message.reply_text('Por favor, introduce una cantidad válida.')

# Respuestas
def handle_response(text: str) -> str:
    processed: str = text.lower()
    if 'hello' in processed or 'hola' in processed:
        return '¡Hola!'
    return 'No entiendo lo que escribiste.'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type} : "{text}"')

    # Manejar las esperas
    if esperando_reserva.get(user_id, False):
        await manejar_reserva_(update, context)
        return

    if esperando_quotes.get(user_id, False):
        await manejar_quotes_(update, context)
        return

    if esperando_gastos_diaris.get(user_id, False):
        await manejar_gastos_diaris_(update, context)
        return

    if esperando_ganancies_esporadiques.get(user_id, False):
        await manejar_ganancies_esporadiques_(update, context)
        return

    if esperando_ganancies_mensuals.get(user_id, False):
        await manejar_ganancies_mensuals_(update, context)
        return

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)

# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Bot is running')
    app = Application.builder().token(Token).build()

    # Comandos
    app.add_handler(CommandHandler('start', start_))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('saldo', saldo_))
    app.add_handler(CommandHandler('reserva', reserva_))
    app.add_handler(CommandHandler('introduir_reserva', introducir_reserva_))
    app.add_handler(CommandHandler('despeses', despeses_))
    app.add_handler(CommandHandler('quotesMensuals', quotes_mensuals_))
    app.add_handler(CommandHandler('introduirQuotesMensuals', introduir_quotes_mensuals_))
    app.add_handler(CommandHandler('gastosDiaris', gastos_diaris_))
    app.add_handler(CommandHandler('introduirGastosDiaris', introducir_gastos_diaris_))
    app.add_handler(CommandHandler('ganancies', ganancies_))
    app.add_handler(CommandHandler('introduirGananciesEsporadiques', introducir_ganancies_esporadiques_))
    app.add_handler(CommandHandler('introduirGananciesMensuals', introducir_ganancies_mensuals_))

    # Respuestas
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    # Errors
    app.add_error_handler(error)

    # Polling
    print('Bot is polling')
    app.run_polling(poll_interval=3)
