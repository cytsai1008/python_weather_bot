# 🤖 Discord Developer Portal Setup Guide

Complete guide to configure your bot as **both User-Installable and Guild-Installable**.

## Part 1: Create Application & Bot

### 1. Create New Application
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"**
3. Enter name: `Taiwan Weather Bot` (or your preferred name)
4. Click **"Create"**

### 2. Configure Bot
1. Click **"Bot"** in left sidebar
2. Click **"Add Bot"** → Confirm
3. **Bot Token**: Click **"Reset Token"** and save it securely
   - You'll need this for `.env` file as `DISCORD_BOT_TOKEN`

### 3. Enable Required Intents
Still in the **Bot** section, scroll to **Privileged Gateway Intents**:
- ✅ **Message Content Intent** - ENABLED

Click **Save Changes**

## Part 2: Enable User & Guild Installation

### 4. Configure Installation Settings
1. Click **"Installation"** in left sidebar
2. Under **"Installation Contexts"**, enable BOTH:
   - ✅ **Guild Install** (for server installation)
   - ✅ **User Install** (for personal installation)

### 5. Set Guild Install Settings
Under **"Guild Install"**:

**Scopes:**
- ✅ `bot`
- ✅ `applications.commands`

**Permissions:**
- ✅ Send Messages
- ✅ Embed Links
- ✅ Use Slash Commands

### 6. Set User Install Settings
Under **"User Install"**:

**Scopes:**
- ✅ `applications.commands`

**Permissions:**
- Leave empty (user apps don't need permissions)

### 7. Install Link
Under **"Install Link"**:
- Select: **Discord Provided Link**

This auto-generates installation URLs for both contexts.

## Part 3: Get Installation Links

### 8. Guild Installation URL
1. Go to **"OAuth2"** → **"URL Generator"**
2. Select scopes:
   - ✅ `bot`
   - ✅ `applications.commands`
3. Select permissions:
   - ✅ Send Messages
   - ✅ Embed Links
   - ✅ Use Slash Commands
4. Copy the generated URL
5. Open in browser and select your server

### 9. User Installation URL
The bot will automatically support user installation with the Installation settings configured above.

**Users can install by:**
1. Right-clicking on the bot's profile
2. Selecting **"Add to Account"** or **"Add App"**
3. Confirming installation

**Or share this link format:**
```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID
```
Replace `YOUR_CLIENT_ID` with your Application ID from the **"General Information"** page.

## Part 4: Verify Setup

### 10. Test Guild Installation
1. Use the Guild Installation URL to add bot to a server
2. In any channel, type: `/weather`
3. Select a location and verify response

### 11. Test User Installation
1. Install the bot to your account
2. Send the bot a DM
3. Type: `/weather`
4. Verify it works in DMs

### 12. Test in Other Servers
After user installation:
1. Go to ANY server (even where bot isn't installed as guild)
2. Type: `/weather`
3. It should work! (user-installed commands follow you everywhere)

## Configuration Summary

### ✅ Checklist
- [x] Bot created with token saved
- [x] Message Content Intent enabled
- [x] Guild Install enabled with bot + applications.commands
- [x] User Install enabled with applications.commands
- [x] Install link set to "Discord Provided Link"
- [x] Bot invited to test server
- [x] Commands tested in server
- [x] Commands tested in DMs

## Understanding the Two Installation Types

### Guild Installation (Server)
- **Installed by:** Server administrators
- **Scope:** Only works in that specific server
- **Permissions:** Can have server-level permissions
- **Use case:** Official server bots

### User Installation (Personal)
- **Installed by:** Individual users
- **Scope:** Works everywhere the user can use slash commands
- **Permissions:** No server permissions needed
- **Use case:** Personal tools that follow you

### Your Bot Supports BOTH! 🎉
- Users can install it personally to use in DMs or any server
- Servers can install it officially for all members
- Same commands, same features, different installation contexts

## Troubleshooting

### Issue: Commands not appearing
**Solution:**
- Wait 1-2 minutes after starting bot for command sync
- Restart Discord client
- Check bot is online

### Issue: "User Install" option not visible
**Solution:**
- Ensure you enabled "User Install" in Installation settings
- Make sure you saved changes
- Try logging out and back into Discord

### Issue: Commands work in server but not DMs
**Solution:**
- Verify `allowed_contexts(dms=True)` in bot.py
- Check bot is installed to your user account (not just server)
- Restart bot after code changes

### Issue: Bot offline
**Solution:**
- Check bot token is correct in `.env`
- Verify bot.py is running
- Check console for errors

## Advanced: Custom Installation URL

If you want a custom branded URL:

1. Use a URL shortener (bit.ly, etc.)
2. Point to your OAuth2 URL
3. Share the short link: `bit.ly/taiwan-weather-bot`

## Security Notes

- ⚠️ Never share your bot token
- ⚠️ User-installed bots can't access server data without permissions
- ⚠️ Keep Message Content Intent enabled for proper functionality
- ⚠️ Regenerate token if accidentally exposed

## Next Steps

After setup:
1. Share installation links with users
2. Monitor bot usage in Discord Developer Portal → Analytics
3. Update bot description and about section
4. Add a nice profile picture and banner
5. Consider verification if bot grows popular

---

Your bot is now configured for maximum flexibility! Users can choose how they want to use it. 🌤️
