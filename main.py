from turtle import dot

import discord
from discord.ext import commands
from datetime import datetime
import json

# ⚠️ ВСТАВЬТЕ СЮДА ВАШ ТОКЕН DISCORD
DISCORD_TOKEN = ""  # Замените на ваш токен
LOG_CHANNEL_ID = 

# Проверка токена
if DISCORD_TOKEN == "ВСТАВЬТЕ_ТОКЕН_СЮДА" or not DISCORD_TOKEN:
    print("❌ ОШИБКА: Токен не установлен!")
    print("\n📝 Что делать:")
    print("1. Перейдите на https://discord.com/developers/applications")
    print("2. Выберите ваше приложение")
    print("3. Перейдите на вкладку 'Bot'")
    print("4. Нажмите 'Copy' под 'TOKEN'")
    print("5. Замените строку выше на: DISCORD_TOKEN = 'скопированный_токен'")
    exit()



# Создаём бота с намерениями
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.moderation = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Словарь для хранения предупреждений
warnings_db = {}

def get_log_channel():
    """Получить канал логирования"""
    return bot.get_channel(LOG_CHANNEL_ID)

async def send_log(embed):
    """Отправить сообщение в канал логирования"""
    log_channel = get_log_channel()
    if log_channel:
        try:
            await log_channel.send(embed=embed)
        except Exception as e:
            print(f"⚠️ Ошибка при отправке логов: {e}")

# Словарь с анимированными GIF'ами для каждого события
ANIMATED_GIFS = {
    'delete': 'https://media.giphy.com/media/xT9IgEx8SbQ0teblJi/giphy.gif',
    'edit': 'https://media.giphy.com/media/xT9Igpp6lDsKCChpPK/giphy.gif',
    'join': 'https://media.giphy.com/media/3o7TKSOheuaL6V72ty/giphy.gif',
    'leave': 'https://media.giphy.com/media/xT9IgEx8SbQ0teblJi/giphy.gif',
    'voice_join': 'https://media.giphy.com/media/xT9IgEx94HqYBmn1Fe/giphy.gif',
    'voice_leave': 'https://media.giphy.com/media/3o7TKSOheuaL6V72ty/giphy.gif',
    'voice_switch': 'https://media.giphy.com/media/xT9Igpp6lDsKCChpPK/giphy.gif',
    'mute': 'https://media.giphy.com/media/xT9IgEx8SbQ0teblJi/giphy.gif',
    'role_change': 'https://media.giphy.com/media/xT9IgEx94HqYBmn1Fe/giphy.gif',
    'ban': 'https://media.giphy.com/media/xT9IgEx8SbQ0teblJi/giphy.gif',
    'warn': 'https://media.giphy.com/media/3o7TKSOheuaL6V72ty/giphy.gif',
    'kick': 'https://media.giphy.com/media/xT9Igpp6lDsKCChpPK/giphy.gif'
}

async def add_reaction(message, reaction="✅"):
    """Добавить реакцию к сообщению"""
    try:
        await message.add_reaction(reaction)
    except:
        pass

# ==================== СОБЫТИЯ СООБЩЕНИЙ ====================

@bot.event
async def on_message_delete(message):
    """Логирование удалённых сообщений"""
    if message.author.bot:
        return
    
    embed = discord.Embed(
        title="🗑️ Сообщение удалено",
        description=f"**Автор:** {message.author.mention}\n**Канал:** {message.channel.mention}",
        color=discord.Color.red(),
        timestamp=datetime.now()
    )
    embed.add_field(name="Содержание", value=message.content[:1024] or "[Пусто]", inline=False)
    embed.set_footer(text=f"ID сообщения: {message.id}")
    embed.set_thumbnail(url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)
    embed.set_image(url=ANIMATED_GIFS['delete'])
    
    await send_log(embed)

@bot.event
async def on_message_edit(before, after):
    """Логирование отредактированных сообщений"""
    if before.author.bot or before.content == after.content:
        return
    
    embed = discord.Embed(
        title="✏️ Сообщение отредактировано",
        description=f"**Автор:** {before.author.mention}\n**Канал:** {before.channel.mention}",
        color=discord.Color.yellow(),
        timestamp=datetime.now()
    )
    embed.add_field(name="Было", value=before.content[:1024] or "[Пусто]", inline=False)
    embed.add_field(name="Стало", value=after.content[:1024] or "[Пусто]", inline=False)
    embed.set_footer(text=f"ID сообщения: {before.id}")
    embed.set_thumbnail(url=before.author.avatar.url if before.author.avatar else before.author.default_avatar.url)
    embed.set_image(url=ANIMATED_GIFS['edit'])
    
    await send_log(embed)

@bot.event
async def on_message(message):
    """Обработка сообщений"""
    if message.author == bot.user:
        return
    
    # Добавить реакцию на сообщение
    if message.content.startswith(bot.command_prefix):
        await add_reaction(message, "⚙️")
    
    await bot.process_commands(message)

# ==================== СОБЫТИЯ ГОЛОСОВЫХ КАНАЛОВ ====================

@bot.event
async def on_voice_state_update(member, before, after):
    """Логирование входа и выхода из голосовых каналов"""
    
    # Вход в голосовой канал
    if before.channel is None and after.channel is not None:
        embed = discord.Embed(
            title="🎤 Вход в голосовой канал",
            description=f"**Участник:** {member.mention}",
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        embed.add_field(name="Канал", value=after.channel.mention, inline=True)
        embed.add_field(name="Кол-во людей в канале", value=len(after.channel.members), inline=True)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_image(url=ANIMATED_GIFS['voice_join'])
        embed.set_footer(text=f"ID: {member.id}")
        
        await send_log(embed)
    
    # Выход из голосового канала
    elif before.channel is not None and after.channel is None:
        embed = discord.Embed(
            title="🎤 Выход из голосового канала",
            description=f"**Участник:** {member.mention}",
            color=discord.Color.red(),
            timestamp=datetime.now()
        )
        embed.add_field(name="Был в канале", value=before.channel.mention, inline=True)
        embed.add_field(name="Кол-во оставшихся", value=len(before.channel.members) - 1, inline=True)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text=f"ID: {member.id}")
        
        await send_log(embed)
    
    # Переход между голосовыми каналами
    elif before.channel != after.channel and before.channel is not None and after.channel is not None:
        embed = discord.Embed(
            title="🔄 Переход между голосовыми каналами",
            description=f"**Участник:** {member.mention}",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        embed.add_field(name="Был в", value=before.channel.mention, inline=False)
        embed.add_field(name="Перешел в", value=after.channel.mention, inline=False)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text=f"ID: {member.id}")
        
        await send_log(embed)
    
    # Отключение микрофона
    if before.self_mute != after.self_mute and after.channel is not None:
        status = "🔇 Отключил" if after.self_mute else "🔊 Включил"
        embed = discord.Embed(
            title=f"{status} микрофон",
            description=f"**Участник:** {member.mention}",
            color=discord.Color.orange(),
            timestamp=datetime.now()
        )
        embed.add_field(name="Канал", value=after.channel.mention, inline=True)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        
        await send_log(embed)
    
    # Отключение слуха
    if before.self_deaf != after.self_deaf and after.channel is not None:
        status = "🔕 Отключил" if after.self_deaf else "👂 Включил"
        embed = discord.Embed(
            title=f"{status} звук",
            description=f"**Участник:** {member.mention}",
            color=discord.Color.orange(),
            timestamp=datetime.now()
        )
        embed.add_field(name="Канал", value=after.channel.mention, inline=True)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        
        await send_log(embed)

# ==================== СОБЫТИЯ ЧЛЕНОВ СЕРВЕРА ====================

@bot.event
async def on_member_join(member):
    """Логирование входа участника"""
    embed = discord.Embed(
        title="👋 Участник присоединился",
        description=f"**Пользователь:** {member.mention}",
        color=discord.Color.green(),
        timestamp=datetime.now()
    )
    embed.add_field(name="Имя", value=str(member), inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Аккаунт создан", value=f"<t:{int(member.created_at.timestamp())}:F>", inline=False)
    embed.add_field(name="Всего участников", value=member.guild.member_count, inline=True)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    
    await send_log(embed)

@bot.event
async def on_member_remove(member):
    """Логирование выхода участника"""
    embed = discord.Embed(
        title="👋 Участник покинул сервер",
        description=f"**Пользователь:** {member.mention}",
        color=discord.Color.orange(),
        timestamp=datetime.now()
    )
    embed.add_field(name="Имя", value=str(member), inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Всего участников", value=member.guild.member_count, inline=True)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    
    await send_log(embed)

# ==================== СОБЫТИЯ РОЛЕЙ ====================

@bot.event
async def on_member_update(before, after):
    """Логирование изменения ролей"""
    before_roles = set(before.roles)
    after_roles = set(after.roles)
    
    added_roles = after_roles - before_roles
    removed_roles = before_roles - after_roles
    
    if added_roles or removed_roles:
        embed = discord.Embed(
            title="👑 Роли изменены",
            description=f"**Участник:** {after.mention}",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        
        if added_roles:
            roles_text = ", ".join([role.mention for role in added_roles])
            embed.add_field(name="➕ Добавлены", value=roles_text, inline=False)
        
        if removed_roles:
            roles_text = ", ".join([role.mention for role in removed_roles])
            embed.add_field(name="➖ Удалены", value=roles_text, inline=False)
        
        embed.set_thumbnail(url=after.avatar.url if after.avatar else after.default_avatar.url)
        embed.set_footer(text=f"ID: {after.id}")
        await send_log(embed)

# ==================== СОБЫТИЯ МОДЕРАЦИИ ====================

@bot.event
async def on_member_ban(guild, user):
    """Логирование бана участника"""
    embed = discord.Embed(
        title="🔨 Участник забанен",
        description=f"**Пользователь:** {user.mention}",
        color=discord.Color.dark_red(),
        timestamp=datetime.now()
    )
    embed.add_field(name="Имя", value=str(user), inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
    
    try:
        async for entry in guild.audit_logs(action=discord.AuditLogAction.ban, limit=1):
            if entry.target.id == user.id:
                embed.add_field(name="Модератор", value=entry.user.mention, inline=True)
                if entry.reason:
                    embed.add_field(name="Причина", value=entry.reason, inline=False)
                break
    except:
        pass
    
    await send_log(embed)

@bot.event
async def on_member_unban(guild, user):
    """Логирование разбана участника"""
    embed = discord.Embed(
        title="✅ Участник разбанен",
        description=f"**Пользователь:** {user.mention}",
        color=discord.Color.green(),
        timestamp=datetime.now()
    )
    embed.add_field(name="Имя", value=str(user), inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
    
    await send_log(embed)

# ==================== КОМАНДЫ МОДЕРАЦИИ ====================

@bot.command(name='kick')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="Не указана"):
    """Выкинуть участника с сервера"""
    if member == ctx.author:
        await ctx.send("❌ Ты не можешь выкинуть самого себя!")
        return
    
    if member == bot.user:
        await ctx.send("❌ Я не могу себя выкинуть!")
        return
    
    await member.kick(reason=reason)
    
    embed = discord.Embed(
        title="🚪 Участник выкинут",
        description=f"**Пользователь:** {member.mention}",
        color=discord.Color.orange(),
        timestamp=datetime.now()
    )
    embed.add_field(name="Модератор", value=ctx.author.mention, inline=True)
    embed.add_field(name="Причина", value=reason, inline=False)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    
    await send_log(embed)
    
    success_embed = discord.Embed(
        description=f"✅ {member.mention} выкинут с сервера!\nПричина: {reason}",
        color=discord.Color.green()
    )
    await ctx.send(embed=success_embed)
    await add_reaction(ctx.message, "✅")

@bot.command(name='ban')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Не указана"):
    """Забанить участника"""
    if member == ctx.author:
        await ctx.send("❌ Ты не можешь забанить самого себя!")
        return
    
    if member == bot.user:
        await ctx.send("❌ Я не могу себя забанить!")
        return
    
    await member.ban(reason=reason)
    
    embed = discord.Embed(
        title="🔨 Участник забанен",
        description=f"**Пользователь:** {member.mention}",
        color=discord.Color.dark_red(),
        timestamp=datetime.now()
    )
    embed.add_field(name="Модератор", value=ctx.author.mention, inline=True)
    embed.add_field(name="Причина", value=reason, inline=False)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    
    await send_log(embed)
    
    success_embed = discord.Embed(
        description=f"🔨 {member.mention} забанен!\nПричина: {reason}",
        color=discord.Color.dark_red()
    )
    await ctx.send(embed=success_embed)
    await add_reaction(ctx.message, "✅")

@bot.command(name='unban')
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, name):
    """Разбанить участника"""
    bans = [entry async for entry in ctx.guild.audit_logs(action=discord.AuditLogAction.ban)]
    
    for entry in bans:
        if entry.target.name.lower() == name.lower():
            await ctx.guild.unban(entry.target)
            
            embed = discord.Embed(
                title="✅ Участник разбанен",
                description=f"**Пользователь:** {entry.target.mention}",
                color=discord.Color.green(),
                timestamp=datetime.now()
            )
            embed.add_field(name="Модератор", value=ctx.author.mention, inline=True)
            
            await send_log(embed)
            
            success_embed = discord.Embed(
                description=f"✅ {entry.target.mention} разбанен!",
                color=discord.Color.green()
            )
            await ctx.send(embed=success_embed)
            await add_reaction(ctx.message, "✅")
            return
    
    await ctx.send(f"❌ Пользователь {name} не найден в банах!")

@bot.command(name='mute')
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason="Не указана"):
    """Замутить участника"""
    if member == ctx.author:
        await ctx.send("❌ Ты не можешь замутить самого себя!")
        return
    
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    
    if not mute_role:
        mute_role = await ctx.guild.create_role(name="Muted", reason="Для мутирования пользователей")
        
        for channel in ctx.guild.channels:
            try:
                await channel.set_permissions(mute_role, send_messages=False, speak=False)
            except:
                pass
    
    await member.add_roles(mute_role, reason=reason)
    
    embed = discord.Embed(
        title="🔇 Участник замучен",
        description=f"**Пользователь:** {member.mention}",
        color=discord.Color.red(),
        timestamp=datetime.now()
    )
    embed.add_field(name="Модератор", value=ctx.author.mention, inline=True)
    embed.add_field(name="Причина", value=reason, inline=False)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    
    await send_log(embed)
    
    success_embed = discord.Embed(
        description=f"🔇 {member.mention} замучен!\nПричина: {reason}",
        color=discord.Color.red()
    )
    await ctx.send(embed=success_embed)
    await add_reaction(ctx.message, "✅")

@bot.command(name='unmute')
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    """Размутить участника"""
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    
    if mute_role and mute_role in member.roles:
        await member.remove_roles(mute_role, reason="Размутирование")
        
        embed = discord.Embed(
            title="🔊 Участник размучен",
            description=f"**Пользователь:** {member.mention}",
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        embed.add_field(name="Модератор", value=ctx.author.mention, inline=True)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        
        await send_log(embed)
        
        success_embed = discord.Embed(
            description=f"🔊 {member.mention} размучен!",
            color=discord.Color.green()
        )
        await ctx.send(embed=success_embed)
        await add_reaction(ctx.message, "✅")
    else:
        await ctx.send(f"❌ {member.mention} не замучен.")

@bot.command(name='warn')
@commands.has_permissions(moderate_members=True)
async def warn(ctx, member: discord.Member, *, reason="Не указана"):
    """Выдать предупреждение"""
    
    # Инициализируем словарь для пользователя если его еще нет
    if member.id not in warnings_db:
        warnings_db[member.id] = []
    
    warnings_db[member.id].append({
        'reason': reason,
        'moderator': str(ctx.author),
        'timestamp': datetime.now().isoformat()
    })
    
    warn_count = len(warnings_db[member.id])
    
    embed = discord.Embed(
        title="⚠️ Предупреждение",
        description=f"**Пользователь:** {member.mention}",
        color=discord.Color.yellow(),
        timestamp=datetime.now()
    )
    embed.add_field(name="Модератор", value=ctx.author.mention, inline=True)
    embed.add_field(name="Причина", value=reason, inline=False)
    embed.add_field(name="Всего предупреждений", value=warn_count, inline=True)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    
    await send_log(embed)
    
    success_embed = discord.Embed(
        description=f"⚠️ {member.mention} получил предупреждение!\nПричина: {reason}\nВсего: {warn_count}/3",
        color=discord.Color.yellow()
    )
    await ctx.send(embed=success_embed)
    await add_reaction(ctx.message, "✅")
    
    # Автобан после 3 предупреждений
    if warn_count >= 3:
        await member.ban(reason="Автоматический бан после 3 предупреждений")
        auto_ban_embed = discord.Embed(
            title="🤖 Автоматический бан",
            description=f"**Пользователь:** {member.mention}\n**Причина:** 3 предупреждения",
            color=discord.Color.dark_red(),
            timestamp=datetime.now()
        )
        await send_log(auto_ban_embed)

@bot.command(name='warns')
async def warns(ctx, member: discord.Member = None):
    """Показать предупреждения пользователя"""
    if member is None:
        member = ctx.author
    
    if member.id not in warnings_db or not warnings_db[member.id]:
        await ctx.send(f"✅ {member.mention} не имеет предупреждений!")
        return
    
    warns = warnings_db[member.id]
    embed = discord.Embed(
        title=f"⚠️ Предупреждения {member}",
        description=f"Всего предупреждений: {len(warns)}",
        color=discord.Color.yellow()
    )
    
    for i, warn in enumerate(warns, 1):
        embed.add_field(
            name=f"Предупреждение #{i}",
            value=f"**Модератор:** {warn['moderator']}\n**Причина:** {warn['reason']}\n**Время:** <t:{int(datetime.fromisoformat(warn['timestamp']).timestamp())}:F>",
            inline=False
        )
    
    await ctx.send(embed=embed)

@bot.command(name='clear')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 10):
    """Удалить сообщения (максимум 100)"""
    if amount > 100:
        await ctx.send("❌ Максимум можно удалить 100 сообщений!")
        return
    
    if amount <= 0:
        await ctx.send("❌ Введите положительное число!")
        return
    
    deleted = await ctx.channel.purge(limit=amount + 1)  # +1 для команды
    
    embed = discord.Embed(
        title="🗑️ Сообщения удалены",
        description=f"**Канал:** {ctx.channel.mention}",
        color=discord.Color.red(),
        timestamp=datetime.now()
    )
    embed.add_field(name="Удалено сообщений", value=len(deleted) - 1, inline=True)
    embed.add_field(name="Модератор", value=ctx.author.mention, inline=True)
    
    await send_log(embed)
    
    success_embed = discord.Embed(
        description=f"✅ Удалено {len(deleted) - 1} сообщений!",
        color=discord.Color.green()
    )
    await ctx.send(embed=success_embed, delete_after=3)

@bot.command(name='stats')
async def stats(ctx):
    """Показать статистику сервера"""
    guild = ctx.guild
    
    total_members = guild.member_count
    bots = sum(1 for member in guild.members if member.bot)
    humans = total_members - bots
    
    embed = discord.Embed(
        title=f"📊 Статистика {guild.name}",
        color=discord.Color.blue(),
        timestamp=datetime.now()
    )
    
    embed.add_field(name="👥 Всего участников", value=total_members, inline=True)
    embed.add_field(name="👤 Людей", value=humans, inline=True)
    embed.add_field(name="🤖 Ботов", value=bots, inline=True)
    embed.add_field(name="📋 Каналов", value=len(guild.channels), inline=True)
    embed.add_field(name="👑 Ролей", value=len(guild.roles), inline=True)
    embed.add_field(name="📅 Создан", value=f"<t:{int(guild.created_at.timestamp())}:F>", inline=False)
    
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    embed.set_footer(text=f"ID сервера: {guild.id}")
    
    await ctx.send(embed=embed)

@bot.command(name='commands')
async def help_command(ctx):
    """Показать справку по командам"""
    embed = discord.Embed(
        title="📚 Справка по командам",
        description="Все доступные команды для модерации",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="🚪 Модерация",
        value="""
        `!kick @user <причина>` - Выкинуть пользователя
        `!ban @user <причина>` - Забанить пользователя
        `!unban <имя>` - Разбанить пользователя
        `!mute @user <причина>` - Замутить пользователя
        `!unmute @user` - Размутить пользователя
        `!warn @user <причина>` - Выдать предупреждение
        `!warns [@user]` - Показать предупреждения
        `!clear <число>` - Удалить сообщения
        """,
        inline=False
    )
    
    embed.add_field(
        name="📊 Информация",
        value="""
        `!stats` - Статистика сервера
        `!help` - Эта справка
        """,
        inline=False
    )
    
    embed.add_field(
        name="📝 Логирование",
        value="Бот логирует все события на сервере в канал логирования",
        inline=False
    )
    
    await ctx.send(embed=embed)

# ==================== ОБРАБОТКА ОШИБОК ====================

@bot.event
async def on_ready():
    """Бот готов"""
    print(f'✅ Бот {bot.user} подключился')
    print(f'📝 Канал логирования: {LOG_CHANNEL_ID}')
    print(f'📊 Сервер: {bot.guilds[0].name if bot.guilds else "Нет серверов"}')
    print(f'👥 Участников: {sum(g.member_count for g in bot.guilds)}')
    
    activity = discord.Activity(type=discord.ActivityType.watching, name="за нарушениями | !help")
    await bot.change_presence(activity=activity, status=discord.Status.online)

@bot.event
async def on_command_error(ctx, error):
    """Обработка ошибок команд"""
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            description="❌ У тебя нет прав для этой команды!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        await add_reaction(ctx.message, "❌")
    
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            description=f"❌ Неверное использование команды!\nИспользуй: `!help`",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        await add_reaction(ctx.message, "❌")
    
    elif isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(
            description="❌ Пользователь не найден!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        await add_reaction(ctx.message, "❌")
    
    else:
        print(f'❌ Ошибка: {error}')

# ==================== ЗАПУСК БОТА ====================

if __name__ == "__main__":
    print("🚀 Запуск бота...")
    bot.run(DISCORD_TOKEN)