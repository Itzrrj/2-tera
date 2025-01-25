from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import logging
import asyncio
from datetime import datetime
from pyrogram.enums import ChatMemberStatus
from dotenv import load_dotenv
from os import environ
import os
import time
from status import format_progress_bar
from video import download_video, upload_video
from web import keep_alive
from pyrogram.types import WebAppInfo
from pymongo import MongoClient
from dotenv import load_dotenv

mongo_url = "mongodb+srv://cphdlust:cphdlust@cphdlust.ydeyw.mongodb.net/?retryWrites=true&w=majority"  # Change with your MongoDB URL
client = MongoClient(mongo_url)
db = client["cphdlust"]
users_collection = db["users"]

async def save_user(user_id):
    """Save user ID to the database if not already present."""
    if not users_collection.find_one({"user_id": user_id}):
        users_collection.insert_one({"user_id": user_id})
        logging.info(f"Added new user with ID {user_id} to the database.")
    else:
        logging.info(f"User with ID {user_id} already exists in the database.")

# Client Setup

logging.basicConfig(level=logging.INFO)
admins_str = os.getenv('ADMINS')

# Check if ADMINS is not None or empty
if admins_str:
    admins = admins_str.split(',')
    admins = [int(admin.strip()) for admin in admins]  # Convert to integers
    print(f"Admins: {admins}")
else:
    print("ADMINS variable is missing or empty.")
    admins = []  # Provide a fallback or raise an exception


api_id = os.environ.get('TELEGRAM_API','')
if len(api_id) == 0:
    logging.error("TELEGRAM_API variable is missing! Exiting now")
    exit(1)

api_hash = os.environ.get('TELEGRAM_HASH','')
if len(api_hash) == 0:
    logging.error("TELEGRAM_HASH variable is missing! Exiting now")
    exit(1)
    
bot_token = os.environ.get('BOT_TOKEN','')
if len(bot_token) == 0:
    logging.error("BOT_TOKEN variable is missing! Exiting now")
    exit(1)
dump_id = os.environ.get('DUMP_CHAT_ID','')
if len(dump_id) == 0:
    logging.error("DUMP_CHAT_ID variable is missing! Exiting now")
    exit(1)
else:
    dump_id = int(dump_id)

fsub_id = os.environ.get('FSUB_ID','')
if len(fsub_id) == 0:
    logging.error("FSUB_ID variable is missing! Exiting now")
    exit(1)
else:
    fsub_id = int(fsub_id)

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("start"))
async def start_command(client, message):
    sticker_message = await message.reply_sticker("CAACAgIAAxkBAAEYonplzwrczhVu3I6HqPBzro3L2JU6YAACvAUAAj-VzAoTSKpoG9FPRjQE")
    await asyncio.sleep(2)
    await sticker_message.delete()
    user_mention = message.from_user.mention
    reply_message = f"ᴡᴇʟᴄᴏᴍᴇ, {user_mention}.\n\n🌟 ɪ ᴀᴍ ᴀ ᴛᴇʀᴀʙᴏx ᴅᴏᴡɴʟᴏᴀᴅᴇʀ ʙᴏᴛ. sᴇɴᴅ ᴍᴇ ᴀɴʏ ᴛᴇʀᴀʙᴏx ʟɪɴᴋ ɪ ᴡɪʟʟ ᴅᴏᴡɴʟᴏᴀᴅ ᴡɪᴛʜɪɴ ғᴇᴡ sᴇᴄᴏɴᴅs ᴀɴᴅ sᴇɴᴅ ɪᴛ ᴛᴏ ʏᴏᴜ ✨."
    join_button = InlineKeyboardButton("ᴊᴏɪɴ ❤️🚀", url="https://t.me/Xstream_links2")
    developer_button = InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ ⚡️", url="t.me/terABoxTer_Instagrambot")
    reply_markup = InlineKeyboardMarkup([[join_button, developer_button]])
    video_file_id = "/app/1734351426786003.mov"
    if os.path.exists(video_file_id):
        await client.send_video(
            chat_id=message.chat.id,
            video=video_file_id,
            caption=reply_message,
            reply_markup=reply_markup
        )
    else:
        await message.reply_text(reply_message, reply_markup=reply_markup)

async def is_user_member(client, user_id):
    try:
        member = await client.get_chat_member(fsub_id, user_id)
        logging.info(f"User {user_id} membership status: {member.status}")
        if member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return True
        else:
            return False
    except Exception as e:
        logging.error(f"Error checking membership status for user {user_id}: {e}")
        return False

@app.on_message(filters.text)
async def handle_message(client, message: Message):
    if message.from_user is None:
        logging.error("Message does not contain user information.")
        return

    user_id = message.from_user.id
    user_mention = message.from_user.mention
    is_member = await is_user_member(client, user_id)

    if not is_member:
        join_button = InlineKeyboardButton("ᴊᴏɪɴ ❤️🚀", url="https://t.me/Xstream_links2")
        reply_markup = InlineKeyboardMarkup([[join_button]])
        await message.reply_text("ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴍʏ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴍᴇ.\nChannel 1 - https://t.me/+SwZARPAas7AwZjNl\nChannel 2 - https://t.me/+Q720C5GA9oRlNDg1\nChannel 3 - https://t.me/+QjM9OMbg4rU3ODc9", reply_markup=reply_markup)
        return

    valid_domains = [
    'terabox.com', 'nephobox.com', '4funbox.com', 'mirrobox.com', 
    'momerybox.com', 'teraboxapp.com', '1024tera.com', 
    'terabox.app', 'gibibox.com', 'goaibox.com', 'terasharelink.com', 'teraboxlink.com', 'terafileshare.com'
    ]

    terabox_link = message.text.strip()

    if not any(domain in terabox_link for domain in valid_domains):
        await message.reply_text("ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴀ ᴠᴀʟɪᴅ ᴛᴇʀᴀʙᴏx ʟɪɴᴋ.")
        return

    reply_msg = await message.reply_text("sᴇɴᴅɪɴɢ ʏᴏᴜ ᴛʜᴇ ᴍᴇᴅɪᴀ...🤤")
    
    try:
        file_path, thumbnail_path, video_title = await download_video(terabox_link, reply_msg, user_mention, user_id)
        await upload_video(client, file_path, thumbnail_path, video_title, reply_msg, dump_id, user_mention, user_id, message)
    except Exception as e:
        logging.error(f"Error handling message: {e}")
        await handle_video_download_failure(reply_msg, terabox_link)

async def handle_video_download_failure(reply_msg, url):
    """Provide a fallback option to watch the video online."""
    watch_online_button_1 = InlineKeyboardButton(
        "⚡️WATCH ONLINE 1📱", 
        web_app=WebAppInfo(url=f"https://terabox-watch.netlify.app/api2.html?url={url}")
    )
    watch_online_button_2 = InlineKeyboardButton(
        "⚡️WATCH ONLINE 2📱", 
        web_app=WebAppInfo(url=f"https://terabox-watch.netlify.app/api2.html?url={url}")
    )
    reply_markup = InlineKeyboardMarkup([
        [watch_online_button_1],
        [watch_online_button_2]
    ])
    await reply_msg.edit_text(
        "YOUR VIDEO IS READY❗️\nCLICK ON ANY OPTION BELOW TO WATCH👇👇👇",
        reply_markup=reply_markup
    )
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("broadcast") & filters.user(ADMINS))  # Only admins can use the broadcast command
async def broadcast_command(client, message):
    # Check if the message is a reply
    if message.reply_to_message:
        broadcast_msg = message.reply_to_message  # Get the message to broadcast
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        # Get all users from the database
        users = users_collection.find()

        pls_wait = await message.reply("<i>Broadcasting Message.. This may take some time</i>")

        for user in users:
            user_id = user["user_id"]
            try:
                # Send the message to each user
                await broadcast_msg.copy(user_id)
                successful += 1
            except Exception as e:
                logging.error(f"Failed to send message to {user_id}: {e}")
                unsuccessful += 1

            total += 1

        # Show broadcast status
        status = f"""<b><u>Broadcast Completed</u></b>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code>"""
        
        await pls_wait.edit(status)
    else:
        msg = await message.reply("Please reply to a message to broadcast it.")
        await asyncio.sleep(8)
        await msg.delete()


if __name__ == "__main__":
    keep_alive()
    app.run()
