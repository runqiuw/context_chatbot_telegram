import json

with open('config.json') as f:
    config = json.load(f)
TOKEN = config['TOKEN']
bot_username = config['username']
mode = config['mode']
api_key = config['api_key']
base_url = config['base_url']
model = config['model']
max_stored_messages = config['context_length']

import logging
from collections import deque, defaultdict
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
if mode == "local":
    from chatbot import Chatbot
else:
    from deepseek import deepseek_get_response

system_prompt = f"You are {bot_username}, a helpful assistant. But you only answers the last questions that mentions you.\
    Any other context are given as reference, which can be ignored if they are not related to the last question."

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

messages_store = defaultdict(lambda: deque(maxlen=max_stored_messages))

async def store_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    latest_update = update.message
    chat_id = latest_update.chat.id
    thread_id = latest_update.message_thread_id if latest_update.message_thread_id else None
    user_name = latest_update.from_user.username
    message_text = latest_update.text
    keyword = "@" + bot_username.lower()
    if keyword in message_text.lower():
        temp = await context.bot.send_message(chat_id=chat_id, 
                                       text=f"Hi @{user_name}! Generating a response...", 
                                       message_thread_id=thread_id)
        await context.bot.send_chat_action(chat_id=chat_id, action="typing", message_thread_id=thread_id)
        await chat(update, context)
        await temp.delete()
    
    chat_key = (chat_id, thread_id)
    message_text = user_name + ": " + message_text if user_name else message_text
    messages_store[chat_key].append({"role": "user", "content": message_text})

async def summarize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args == [] or not context.args[0].isdigit() or (len(context.args)==2 and context.args[1] not in ['zh', 'en']):
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                        text="Invalid input. Usage: `/summarize <number> <(optional)zh/en>`", 
                                        parse_mode='Markdown',
                                        message_thread_id=update.effective_message.message_thread_id)
        return
    summarize_length =  context.args[0] if context.args else 20
    if int(summarize_length) > min(len(messages_store[(update.effective_chat.id, update.effective_message.message_thread_id)]), max_stored_messages):
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                        text="Number of messages to summarize exceeds the maximum limit.", 
                                        message_thread_id=update.effective_message.message_thread_id)
        return
    thread_id = update.effective_message.message_thread_id if update.effective_message.message_thread_id else None
    temp_message = await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text=f"<i>Summarizing last <b>{summarize_length}</b> messages...</i>", 
                                   parse_mode='HTML',
                                   message_thread_id=thread_id)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing", message_thread_id=thread_id)
    if len(context.args)==2 and context.args[1] == 'zh':
        prompt = "分析群聊记录，按主题对群消息进行分组，并总结每个主题。确保主题是不同的，总结是简洁的。如果主题数量太多，挑选最重要的10个。\
        以此格式用中文输出：-话题 [序号]: [话题类型]\n 总结: [话题概况]\n\n"
    else:
        prompt = "Analyze the group chat log, group messages by topic, and summarize each topic in English. \
        Ensure topics are distinct and summaries are concise. If there are too many topics, select 10 most important ones. \
        Output in this format: -Topic [# of topic]: [Topic name]\n Summary: [Brief summary]\n\n"
    messages = list(messages_store[(update.effective_chat.id, thread_id)])
    messages = messages[-int(summarize_length):] + [{"role": "system", "content": prompt}]
    messages_store[(update.effective_chat.id, thread_id)].appendleft({"role": "system", "content": system_prompt})
    if mode == "api":
        response = deepseek_get_response(api_key, base_url, model, messages, temperature=1.0)
    else:   
        response = telebot.generate_response(messages, system_prompt)
        
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response, message_thread_id=thread_id)
    await temp_message.delete()
    

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    thread_id = update.effective_message.message_thread_id if update.effective_message.message_thread_id else None
    user_name = update.effective_user.username
    message_text = update.effective_message.text
    chat_key = (update.effective_chat.id, thread_id)

    if chat_key not in messages_store: 
        messages_store[chat_key] = deque(maxlen=max_stored_messages)
    message_text = user_name + ": " + message_text if user_name else message_text
    messages_store[chat_key].append({"role": "user", "content": message_text})
    messages_store[chat_key].appendleft({"role": "system", "content": system_prompt})
    messages = list(messages_store[chat_key])
    if mode == "api":
        response = deepseek_get_response(api_key, base_url, model, messages, temperature=1.3)
    else:   
        response = telebot.generate_response(messages, system_prompt)
        telebot.clear_messages()
    messages_store[chat_key].append({"role": "assistant", "content": response})
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response, message_thread_id=thread_id)   

async def new_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Clears the chat history'''
    chat_id = update.effective_chat.id
    thread_id = update.effective_message.message_thread_id if update.effective_message.message_thread_id else None
    messages_store[(chat_id, thread_id)] = deque(maxlen=max_stored_messages)
    messages_store[(chat_id, thread_id)].append({"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."})
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text="Chat history cleared. Start chatting!", 
                                   message_thread_id=thread_id)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_message = "This is a chatbot which automatically keeps track of your chat history. Use: \n \
    `/new_chat`: to clear the chat history\n \
    `/summarize <number> <(optional)zh/en>`: to summarize the last <number> messages\n \
    add \"`@" + bot_username + "`\" in your message to chat with the bot"
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text=help_message, 
                                   parse_mode='Markdown', 
                                   message_thread_id=update.effective_message.message_thread_id)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    if mode =="local":
        telebot = Chatbot(system_prompt=system_prompt)
    store_message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), store_message)
    summarize_handler = CommandHandler('summarize', summarize)
    new_chat_handler = CommandHandler('new_chat', new_chat)
    help_handler = CommandHandler('help', help_command)

    application.add_handler(summarize_handler)
    application.add_handler(store_message_handler)
    application.add_handler(new_chat_handler)
    application.add_handler(help_handler)

    application.run_polling()
