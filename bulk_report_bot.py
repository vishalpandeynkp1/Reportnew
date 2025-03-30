 from pyrogram import Client, filters from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton from telethon.sync import TelegramClient from telethon.tl.functions.account import ReportPeerRequest from telethon.tl.types import InputReportReasonSpam

Bot credentials

API_ID = "your_api_id" API_HASH = "your_api_hash" BOT_TOKEN = "your_bot_token"

List of multiple session strings for bulk reporting

SESSION_STRINGS = [ "session_string_1", "session_string_2", "session_string_3", # Add more session strings as needed ]

bot = Client("MassReportBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN) admin_chat_id = 123456789  # Replace with your Telegram ID

Start multiple Telethon clients

user_clients = [TelegramClient(f"user_{i}", API_ID, API_HASH).start(session_string=session) for i, session in enumerate(SESSION_STRINGS)]

@bot.on_message(filters.command("start")) def start(client, message): message.reply_text( "👋 Welcome! Send a username or group link to report.", reply_markup=InlineKeyboardMarkup([ [InlineKeyboardButton("Report Scam", callback_data="report")] ]) )

@bot.on_message(filters.command("report")) def report(client, message): message.reply_text("📌 Send the username or group link to report.")

@bot.on_message(filters.text & ~filters.command) def handle_report(client, message): reported_content = message.text.strip() bot.send_message(admin_chat_id, f"🚨 Bulk Reporting Started for {reported_content}")

success_count = 0
failed_count = 0

for user_client in user_clients:
    try:
        user_client(ReportPeerRequest(
            peer=reported_content,
            reason=InputReportReasonSpam(),
            message="This account is involved in spam activities."
        ))
        success_count += 1
    except Exception as e:
        failed_count += 1
        print(f"Failed for one session: {e}")

message.reply_text(
    f"✅ Bulk Report Completed!\n\n✔️ Successful: {success_count}\n❌ Failed: {failed_count}"
)

print("Bot is running...") bot.run()

