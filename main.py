from telegram.ext import Updater,CommandHandler,CallbackContext,MessageHandler,Filters,CallbackQueryHandler
from telegram import Update,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton
import os
from db import DB
from cartdb import Cart
# get token from env
TOKEN = os.environ['TOKEN']
db = DB('db.json')
cart = Cart('cartdb.json')


def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id

    keyboar = ReplyKeyboardMarkup([
        ['🛍 Shop','🛒 Cart'],
        ['📞 Contact','📝 About']
    ])
    bot = context.bot
    bot.sendMessage(
    chat_id=chat_id,
    text='Assalom alaykum xush kelibsiz botimizga 👍',
    reply_markup=keyboar
    )

def about(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id

    keyboar = ReplyKeyboardMarkup([
        ['📝 About Us','📝 About the bot'],
        ['Main menu']
    ])
    bot = context.bot
    bot.sendMessage(
    chat_id=chat_id,
    text='Assalom alaykum xush kelibsiz botimizga 👍',
    reply_markup=keyboar
    )

def contact(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id

    keyboar = InlineKeyboardMarkup([
        [InlineKeyboardButton(text='📞 Phone number',callback_data='number'),InlineKeyboardButton(text='📧 Email',callback_data='email')],
        [InlineKeyboardButton(text='📍 Location',callback_data='location'),InlineKeyboardButton(text='📌 Address',callback_data='address')],
        # [InlineKeyboardButton(text='📞 Phone number',url='txt')]
        
    ])
    bot = context.bot
    bot.sendMessage(
    chat_id=chat_id,
    text='Assalom alaykum xush kelibsiz botimizga 👍',
    reply_markup=keyboar
    )

def query(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    data = query.data
    bot = context.bot
    if data=='number':
        phone_1 ='+998661234567'
        phone_2 ='+998661234567'
        text = f'Our phone numbers:\n{phone_1}\n{phone_2}'
        bot.sendMessage(text=text,chat_id=chat_id)
    elif data=='email':
        email = 'Our email: smartphone@gmail.com'
        bot.sendMessage(text=email,chat_id=chat_id)
        
    elif data=='address':
        address = 'Our address: Samarkand, Uzbekistan'
        bot.sendMessage(text=address,chat_id=chat_id)

    elif data=='location':
        # 39.644053, 66.973233

        lat = 39.644053
        lon = 66.973233
        bot.sendLocation(chat_id=chat_id,latitude=lat,longitude=lon)

    query.answer('Hi')
    print(data)
    

def photo(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id        
    bot = context.bot
    bot.sendMessage(chat_id=chat_id,text='Photo qabul qilindi')

def shop(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id

    iphone = InlineKeyboardButton(text='Iphone',callback_data='phone_list Apple')
    samsung = InlineKeyboardButton(text='Samsung',callback_data='phone_list Samsung')
    huawei = InlineKeyboardButton(text='Huawei',callback_data='phone_list Huawei')
    xiaomi = InlineKeyboardButton(text='Redmi',callback_data='phone_list Redmi')
    vivo = InlineKeyboardButton(text='Vivo',callback_data='phone_list Vivo')
    oppo = InlineKeyboardButton(text='Oppo',callback_data='phone_list Oppo')

    # Define keyboard
    keyboar = InlineKeyboardMarkup([
        [iphone,samsung,huawei],
        [xiaomi,vivo,oppo]
    ])

    bot = context.bot
    bot.sendMessage(chat_id=chat_id,text='Choose a phone',reply_markup=keyboar)

def phone(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    data,brand,index = query.data.split()

    bot = context.bot
    phone = db.getPhone(brand,index)
    model = phone['model']
    color = phone['color']
    ram = phone['ram']
    price = phone['price']
    memory = phone['memory']
    img = phone['image']
    text = f'Phone model: {model}\nColor: {color}\nRAM: {ram}\nPrice: {price}\nMemory: {memory}'
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(text='🛒 add Cart',callback_data=f'add_cart:{brand}:{index}')],
    ])
    bot.sendPhoto(chat_id=chat_id,photo=img,caption=text,reply_markup=keyboard)       


    query.answer('Phone')


def phone_list(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    data,brand = query.data.split()

    phone_list =db.get_phone_list(brand)

    bot = context.bot
    keyboard = []
    row = []
    for phone in phone_list:
        row.append(InlineKeyboardButton(text=phone,callback_data=f'phone {brand} {phone}'))
        if len(row)==10:
            keyboard.append(row)
            row = []
        

    keyboar = InlineKeyboardMarkup(keyboard)
    bot.sendMessage(chat_id=chat_id,text='Choose a phone',reply_markup=keyboar)
def add_cart(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    data,brand,index = query.data.split(':')
    
   
    bot = context.bot
    bot.sendMessage(chat_id=chat_id,text='Added to cart')
    cart.add(brand=brand,model_id=index)

def get_cart(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    bot = context.bot
    cart_list = cart.get_cart()
    if len(cart_list)==0:
        bot.sendMessage(chat_id=chat_id,text='Cart is empty')
    else:
        text = 'Your cart:'
        for item in cart_list:
            phone = db.getPhone(item['brand'],item['model_id'])
            
            text += f"\n{phone['model']}:\nPrice: {phone['price']}\nMemory: {phone['memory']}\nRAM: {phone['ram']}\nColor: {phone['color']}\n "
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(text='🛒 Buy',callback_data='buy')],
            [InlineKeyboardButton(text='🛒 Clear cart',callback_data='clear_cart')],
        ])
        bot.sendMessage(chat_id=chat_id,text=text,reply_markup=keyboard)
        

        

            
def main():
    updater = Updater(token=TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start',start))
# Add handler for photo message
    updater.dispatcher.add_handler(MessageHandler(Filters.photo,photo))
    updater.dispatcher.add_handler(MessageHandler(Filters.text('🛍 Shop'),shop))
    updater.dispatcher.add_handler(MessageHandler(Filters.text('🛒 Cart'),get_cart))
    updater.dispatcher.add_handler(MessageHandler(Filters.text('📝 About'),about))
    updater.dispatcher.add_handler(MessageHandler(Filters.text('📞 Contact'),contact))
    updater.dispatcher.add_handler(MessageHandler(Filters.text('Main menu'),start))
    updater.dispatcher.add_handler(CallbackQueryHandler(phone_list,pattern='phone_list'))
    updater.dispatcher.add_handler(CallbackQueryHandler(phone,pattern='phone'))
    updater.dispatcher.add_handler(CallbackQueryHandler(add_cart,pattern='add_cart'))
    updater.dispatcher.add_handler(CallbackQueryHandler(query))

    updater.start_polling()
    updater.idle()

# main()