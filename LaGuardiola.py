from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext

# Declaración de constantes
Token: Final = '7725937567:AAHohQsxDB1lO9-_MZX_rQ1lgnAMM095C1E'  # Token del bot
BOT_USERNAME: Final = '@LaGuardiola_Bot'  # Nombre del Bot

# Variables globales
salary = 0  # Saldo actual
ingresos = 0  # Ingresos totales
estalvi = 0  # Estalvi
despeses = 0  # Despeses totals
quotes = 0  # Despeses mensuals fixes
gastos_diaris = 0  # Despeses diàries
ganancies_esporadiques = 0  # Ganàncies esporàdiques
ganancies_mensuals = 0  # Ganàncies mensuals
esperando_reserva = False  # Control de espera para la reserva
esperando_quotes = False  # Control de espera para las cuotas mensuales
esperando_gastos_diaris = False  # Control de espera para los gastos diarios
esperando_ganancies_esporadiques = False  # Control de espera para las ganancias esporádicas
esperando_ganancies_mensuals = False  # Control de espera para las ganancias mensuales

# Comando /start
async def start_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global salary, ingresos, estalvi, despeses, quotes, gastos_diaris, ganancies_esporadiques, ganancies_mensuals

    # Inicialización de variables
    estalvi = 0
    despeses = quotes + gastos_diaris
    ingresos = ganancies_esporadiques + ganancies_mensuals
    salary = ingresos - despeses - estalvi

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
    global estalvi
    await update.message.reply_text(f'Tienes {estalvi}€ reservados para el ahorro.')

async def introducir_reserva_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global esperando_reserva
    esperando_reserva = True
    await update.message.reply_text('Introduce la cantidad que deseas reservar como ahorro.')

async def manejar_reserva_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global estalvi, esperando_reserva, salary

    if esperando_reserva:
        try:
            quantitat = float(update.message.text.replace('€', '').strip())
            estalvi += quantitat  # Sumar a estalvi
            esperando_reserva = False
            salary = ingresos - despeses - estalvi  # Recalcular salary
            await update.message.reply_text(f'Has reservado {quantitat}€ como ahorro. Total ahorrado: {estalvi}€. Saldo actual: {salary}€.')
        except ValueError:
            await update.message.reply_text('Por favor, introduce una cantidad válida.')

# Comando /saldo
async def saldo_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global salary, ingresos, despeses, estalvi
    salary = ingresos - despeses - estalvi
    await update.message.reply_text(f'Tu saldo actual es de {salary}€.')

# Comando /despeses
async def despesses_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global quotes, gastos_diaris, despeses, salary
    despeses = quotes + gastos_diaris
    salary = ingresos - despeses - estalvi  # Recalcular salary
    await update.message.reply_text(f'El total de tus gastos hasta el momento es de {despeses}€. Saldo actual: {salary}€.')

# Comando /quotesMensuals
async def quotes_mensuals_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global quotes
    await update.message.reply_text(f'Los gastos mensuales fijos son de {quotes}€.')

# Comando /introduirQuotesMensuals
async def introduir_quotes_mensuals_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global esperando_quotes
    esperando_quotes = True
    await update.message.reply_text('Introduce las nuevas cuotas mensuales que quieres agregar.')

async def manejar_quotes_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global quotes, esperando_quotes, despeses, salary

    if esperando_quotes:
        try:
            cantidad = float(update.message.text.replace('€', '').strip())
            quotes = cantidad  # Actualizar las cuotas mensuales
            esperando_quotes = False
            despeses = quotes + gastos_diaris  # Recalcular despeses
            salary = ingresos - despeses - estalvi  # Recalcular salary
            await update.message.reply_text(f'Has actualizado las cuotas mensuales a {cantidad}€. Saldo actual: {salary}€.')
        except ValueError:
            await update.message.reply_text('Por favor, introduce una cantidad válida.')

# Comando /gastosDiaris
async def gastos_diaris_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global gastos_diaris
    await update.message.reply_text(f'Los gastos diarios hasta ahora son de {gastos_diaris}€.')

async def introducir_gastos_diaris_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global esperando_gastos_diaris
    esperando_gastos_diaris = True
    await update.message.reply_text('Introduce la cantidad de gastos diarios.')

async def manejar_gastos_diaris_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global gastos_diaris, esperando_gastos_diaris, despeses, salary

    if esperando_gastos_diaris:
        try:
            cantidad = float(update.message.text.replace('€', '').strip())
            gastos_diaris += cantidad  # Sumar a gastos diarios
            esperando_gastos_diaris = False
            despeses = quotes + gastos_diaris  # Recalcular despeses
            salary = ingresos - despeses - estalvi  # Recalcular salary
            await update.message.reply_text(f'Has agregado {cantidad}€ a los gastos diarios. Total de gastos diarios: {gastos_diaris}€. Saldo actual: {salary}€.')
        except ValueError:
            await update.message.reply_text('Por favor, introduce una cantidad válida.')

# Comando /ganancies
async def ganancies_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ganancies_esporadiques, ganancies_mensuals, ingresos, salary
    ingresos = ganancies_esporadiques + ganancies_mensuals
    salary = ingresos - despeses - estalvi  # Recalcular salary
    await update.message.reply_text(f'Tus ganancias totales son de {ingresos}€. Saldo actual: {salary}€.')

# Comando /introduirGananciesEsporadiques
async def introducir_ganancies_esporadiques_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global esperando_ganancies_esporadiques
    esperando_ganancies_esporadiques = True
    await update.message.reply_text('Introduce los ingresos esporádicos que quieres agregar.')

async def manejar_ganancies_esporadiques_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ganancies_esporadiques, esperando_ganancies_esporadiques, ingresos, salary

    if esperando_ganancies_esporadiques:
        try:
            cantidad = float(update.message.text.replace('€', '').strip())
            ganancies_esporadiques += cantidad  # Sumar a ganancies esporadiques
            esperando_ganancies_esporadiques = False
            ingresos = ganancies_esporadiques + ganancies_mensuals  # Recalcular ingresos
            salary = ingresos - despeses - estalvi  # Recalcular salary
            await update.message.reply_text(f'Has agregado {cantidad}€ a las ganancias esporádicas. Total de ganancias esporádicas: {ganancies_esporadiques}€. Saldo actual: {salary}€.')
        except ValueError:
            await update.message.reply_text('Por favor, introduce una cantidad válida.')

# Comando /introduirGananciesMensuals
async def introducir_ganancies_mensuals_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global esperando_ganancies_mensuals
    esperando_ganancies_mensuals = True
    await update.message.reply_text('Introduce las ganancias mensuales.')

async def manejar_ganancies_mensuals_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ganancies_mensuals, esperando_ganancies_mensuals, ingresos, salary

    if esperando_ganancies_mensuals:
        try:
            cantidad = float(update.message.text.replace('€', '').strip())
            ganancies_mensuals += cantidad  # Sumar a ganancies mensuals
            esperando_ganancies_mensuals = False
            ingresos = ganancies_esporadiques + ganancies_mensuals  # Recalcular ingresos
            salary = ingresos - despeses - estalvi  # Recalcular salary
            await update.message.reply_text(f'Has agregado {cantidad}€ a las ganancias mensuales. Total de ganancias mensuales: {ganancies_mensuals}€. Saldo actual: {salary}€.')
        except ValueError:
            await update.message.reply_text('Por favor, introduce una cantidad válida.')

# Respuestas
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return '¡Hola!'
    return 'No entiendo lo que escribiste.'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global esperando_reserva, esperando_quotes, esperando_gastos_diaris, esperando_ganancies_esporadiques, esperando_ganancies_mensuals

    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type} : "{text}"')

    if esperando_reserva:
        await manejar_reserva_(update, context)
        return

    if esperando_quotes:
        await manejar_quotes_(update, context)
        return

    if esperando_gastos_diaris:
        await manejar_gastos_diaris_(update, context)
        return

    if esperando_ganancies_esporadiques:
        await manejar_ganancies_esporadiques_(update, context)
        return

    if esperando_ganancies_mensuals:
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
    app.add_handler(CommandHandler('despeses', despesses_))
    app.add_handler(CommandHandler('quotesMensuals', quotes_mensuals_))
    app.add_handler(CommandHandler('introduirQuotesMensuals', introduir_quotes_mensuals_))
    app.add_handler(CommandHandler('gastosDiaris', gastos_diaris_))
    app.add_handler(CommandHandler('introduirGastosDiaris', introducir_gastos_diaris_))
    app.add_handler(CommandHandler('ganancies', ganancies_))
    app.add_handler(CommandHandler('introduirGananciesEsporadiques', introducir_ganancies_esporadiques_))
    app.add_handler(CommandHandler('introduirGananciesMensuals', introducir_ganancies_mensuals_))


    # Respuestas
    app.add_handler(MessageHandler(filters.TEXT, handle_message))


    # Errors
    app.add_error_handler(error)

    # Polling
    print('Bot is polling')
    app.run_polling(poll_interval=3)
