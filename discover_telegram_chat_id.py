#!/usr/bin/env python3
"""
Discover Telegram Channel Chat ID
Run this once to find your channel's chat_id
"""

import requests
import time
from telegram_config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_NAME

def discover_chat_id():
    """
    Discover chat ID by sending a test message and checking updates
    """
    print(f"🔍 Discovering chat ID for channel: @{TELEGRAM_CHANNEL_NAME}")
    print("\n⚠️  IMPORTANT:")
    print("1. Make sure the bot is ADMIN in the channel")
    print("2. The bot should have 'Post Messages' permission\n")

    # Test message
    test_message = "🤖 Test message from Backpackers Jobs Bot - ignore this!"

    # Try to send message
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    # Try with channel name (@ prefix)
    chat_ids_to_try = [
        f"@{TELEGRAM_CHANNEL_NAME}",  # @channelname format
        TELEGRAM_CHANNEL_NAME,         # channelname format
    ]

    for chat_id_attempt in chat_ids_to_try:
        print(f"Trying with: {chat_id_attempt}")

        payload = {
            "chat_id": chat_id_attempt,
            "text": test_message,
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            result = response.json()

            if response.status_code == 200:
                actual_chat_id = result.get('result', {}).get('chat', {}).get('id')
                print(f"\n✅ SUCCESS! Chat ID found: {actual_chat_id}")
                print(f"\n📝 Update telegram_config.py:")
                print(f"   TELEGRAM_CHAT_ID = {actual_chat_id}")
                return actual_chat_id
            else:
                error = result.get('description', 'Unknown error')
                print(f"   ❌ Failed: {error}\n")

        except Exception as e:
            print(f"   ❌ Error: {e}\n")

    # If direct message didn't work, try getUpdates
    print("\n💡 Trying alternative method...")
    print("Checking recent messages in your account...\n")

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"

    try:
        response = requests.get(url, timeout=10)
        updates = response.json().get('result', [])

        if updates:
            # Look for channel posts
            for update in updates:
                chat_id = update.get('channel_post', {}).get('chat', {}).get('id')
                if chat_id:
                    print(f"✅ Found chat ID in updates: {chat_id}")
                    return chat_id

                # Also check message updates
                chat_id = update.get('message', {}).get('chat', {}).get('id')
                if chat_id and chat_id < 0:  # Negative IDs are channels/groups
                    print(f"✅ Found chat ID in updates: {chat_id}")
                    return chat_id

            print("ℹ️  No channel updates found yet.")
            print("\n📋 Manual method:")
            print("1. Send any message in your channel")
            print("2. Open: https://api.telegram.org/bot{TOKEN}/getUpdates")
            print("   (Replace {TOKEN} with your bot token)")
            print("3. Look for 'chat' -> 'id' in the JSON")
            print("4. Update telegram_config.py with this ID")
        else:
            print("No updates found.")
            print("\n📋 Manual method:")
            print("1. Send a message in your channel")
            print("2. Visit: https://api.telegram.org/bot{TOKEN}/getUpdates")
            print("3. Find the 'id' field under 'chat'")
            print("4. Update telegram_config.py")

    except Exception as e:
        print(f"Error: {e}")
        print("\n📋 Try manual method:")
        print("1. Send a message in your channel")
        print("2. Visit: https://api.telegram.org/bot{TOKEN}/getUpdates")
        print("3. Copy the 'id' from the chat object")
        print("4. Update telegram_config.py with: TELEGRAM_CHAT_ID = -1001234567890")

    return None


if __name__ == "__main__":
    print("=" * 60)
    print("Telegram Channel Chat ID Discoverer")
    print("=" * 60 + "\n")

    chat_id = discover_chat_id()

    if chat_id:
        print("\n" + "=" * 60)
        print(f"✅ Chat ID: {chat_id}")
        print("=" * 60)
        print("\nNext step: Update telegram_config.py with this ID")
    else:
        print("\n" + "=" * 60)
        print("⚠️  Could not auto-discover chat ID")
        print("=" * 60)
        print("\nManual steps:")
        print("1. Open your channel in Telegram")
        print("2. Send any message")
        print(f"3. Visit: https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates")
        print("4. Look for 'chat' -> 'id' (should be negative number)")
        print("5. Update telegram_config.py: TELEGRAM_CHAT_ID = <the_id>")
