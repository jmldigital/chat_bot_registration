import logging

from telegram import Update, ForceReply,InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from typing import Union, List
#from aiogram import types
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

from functools import wraps
import json
import requests


#2118251856:AAHjXUzS2gg9ubw4kIJNRpGJpBOJQwPVzsA - ml-registration_bot

#2110779709:AAFYcoJiVQP0ZSPfnARp0dBFJJzl1aAu8p8 -ml-Admin-bot

userss=[]

new_user_id='пусто'


TWO = 'ВЫ ЗДЕСЬ УЖЕ БЫЛИ'

#read_file.close()


userss=[]

with open("data.json", "r") as read_file:
    data = json.loads(read_file.read()) 
    for item in data['users']:
        userss.append(item['user_id'])

ONE = LIST_OF_ADMINS = data['users']


def field_array(json_field):
    fields=[]
    with open("data.json", "r") as read_file:
        data = json.loads(read_file.read()) 
        for item in data['users']:
            fields.append(item[json_field])
 
    return fields



def add_user_fake(new_user_id):
    new_user = {"user_id":new_user_id,"update_id": "admin_updates_id","description": 'new user'}
    data['users'].append(new_user)
    with open("data.json", "w") as write_file:
        json.dump(data, write_file)



def remove_user_fake():
    data['users'].pop(-1)
    with open("data.json", "w") as write_file:
        json.dump(data, write_file)

    
 



print(userss)

keyboard = [
        
        [
            InlineKeyboardButton("Хочу", callback_data='1'), 
            InlineKeyboardButton("Не хочу", callback_data='2')
            
        ],                         
                ]

reply_markups = InlineKeyboardMarkup(keyboard)




def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
 
        name = update.effective_user.username
        register_responce = ''
        admin_updates_id=[]



        reply_markups = InlineKeyboardMarkup(keyboard)
        response_all = requests.get('https://api.telegram.org/bot2110779709:AAFYcoJiVQP0ZSPfnARp0dBFJJzl1aAu8p8/getupdates')
        jsonall = response_all.json()
        max_upd = jsonall['result'][0]['update_id']
        offset = max_upd+1
    

        response2 = requests.get(f'https://api.telegram.org/bot2110779709:AAFYcoJiVQP0ZSPfnARp0dBFJJzl1aAu8p8/getupdates?offset=-1&chat_id=-1001618053787')
        #response2 = requests.get(f'https://api.telegram.org/bot2110779709:AAFYcoJiVQP0ZSPfnARp0dBFJJzl1aAu8p8/getupdates?offset={offset}')
        jsonstr=response2.json()



        chat_id = update.message.chat.id
        if chat_id == -1001618053787:
            register_responce = update.message.text.lower()
        

            if register_responce == 'да':
                userss = field_array('user_id')
                user_id=userss[-1]
                response_to_user = requests.get(f'https://api.telegram.org/bot2118251856:AAHjXUzS2gg9ubw4kIJNRpGJpBOJQwPVzsA/sendMessage?chat_id={user_id}&text=Заявка одобрена, ваши данные внесены, перезапусстите бота командой /start')
                response_to_admin = requests.get(f'https://api.telegram.org/bot2110779709:AAFYcoJiVQP0ZSPfnARp0dBFJJzl1aAu8p8/sendMessage?chat_id=-1001618053787&text=Пользователь добавлен')
                #yes_arr.append(register_responce)

            else:
                userss = field_array('user_id')
                user_id=userss[-1]
                print('что считывается если ответ другой', register_responce)
                remove_user_fake()
                response_to_user = requests.get(f'https://api.telegram.org/bot2118251856:AAHjXUzS2gg9ubw4kIJNRpGJpBOJQwPVzsA/sendMessage?chat_id={user_id}&text=Заявка отклонена')



        print('список пользователей перед входом' ,field_array('user_id'))
        if user_id not in field_array("user_id"):
            print("Unauthorized access denied for {}.".format(user_id))

            #name = update.effective_user.username
            try:
                update.message.reply_text(name+' Вас нет в списке участников,xотите зарегистрироваться?', reply_markup=reply_markups)
            except:
                update.message.reply_text('Вас нет в списке участников,xотите зарегистрироваться?', reply_markup=reply_markups)

    

 
            return
        return func(update, context, *args, **kwargs)
    return wrapped

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.



@restricted
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    
    user = update.effective_user


    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )
        


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

@restricted
def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    name = update.effective_user.username
    user_id = update.effective_user.id

    keyboard = [
        [
            InlineKeyboardButton("Ваши курсы", url="https://github.com"),
            InlineKeyboardButton("Связь с JUSTAI", url="https://t.me/milovidov_bot?start=start"),
        ],
        [InlineKeyboardButton("Удалите меня", callback_data='3')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(str(name)+' С возвращением:', reply_markup=reply_markup)
    


    
def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    user = update.effective_user
    user_id = update.effective_user.id
    

    # CallbackQueries need to be answered, even if no notification to the user is needed ыыыыы
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()


    if query.data == "1":
        payload = {"chat_id":"-1001618053787","text":user.mention_markdown_v2()+ " Хочет зарегистрироваться, пускаем его? (Да/Нет)"}
        add_user_fake(user_id)
        print(data)
        response_to_user = requests.get(f'https://api.telegram.org/bot2118251856:AAHjXUzS2gg9ubw4kIJNRpGJpBOJQwPVzsA/sendMessage?chat_id={user_id}&text=Заявка отправлена, пожалуйста ждите приглашения')

        
    if query.data == "2":
        payload = {"chat_id":"-1001618053787","text":user.mention_markdown_v2()+ " Зашел в чат, но не захотел регистрироваться"}


    if query.data == "3":
   
        payload = {"chat_id":"-1001618053787","text":user.mention_markdown_v2()+ " Пользователь захотел уйти",'entities':user_id}
        data['users'].pop(field_array('user_id').index(user_id))
        field_array('user_id').remove(user_id)
        with open("data.json", "w") as write_file:
            json.dump(data, write_file)
        response_to_user = requests.get(f'https://api.telegram.org/bot2118251856:AAHjXUzS2gg9ubw4kIJNRpGJpBOJQwPVzsA/sendMessage?chat_id={user_id}&text=Мы вас убрали из БД, спасибо, что были с нами')
        #print('после удаления',data)
  
    #query.edit_message_text(text=f"Selected option: {query.data}")

    response = requests.get('https://api.telegram.org/bot2118251856:AAHjXUzS2gg9ubw4kIJNRpGJpBOJQwPVzsA/sendMessage', data=payload)





def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("2118251856:AAHjXUzS2gg9ubw4kIJNRpGJpBOJQwPVzsA")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))


    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()