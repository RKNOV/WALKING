async def ensure_user_data(chat_id, user_id):
    if chat_id not in user_data:
        user_data[chat_id] = {
            'user_id': user_id,
            'last_location': None,
            'previous_location': None,
            'session_steps': 0,
            'tracking': False,
            'task': None,
            'level': await db.get_user_data(user_id, 'level'),
            'session_start_time': None,
            'milestones': set(),
            'inactive_stopped': False,
            'update_interval': DEFAULT_UPDATE_INTERVAL
        }
    return user_data[chat_id]

async def start_walking(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if not isinstance(chat_id, int) or not isinstance(user_id, int):
        await message.reply("Invalid chat or user ID.")
        return
    data = await ensure_user_data(chat_id, user_id)
    data.update({
        'tracking': False,
        'session_ready': True,
        'session_steps': 0,
        'session_start_time': datetime.now()
    })
    data['milestones'].clear()
    data.pop('last_message_id', None)
    data.pop('last_message_text', None)
    await update_session_data(chat_id, data)
    await message.reply("Please send your geolocation broadcast to start walking.")

@router.message(lambda m: m.content_type == ContentType.LOCATION)
async def handle_location(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    data = await ensure_user_data(chat_id, user_id)
    current_location = (message.location.latitude, message.location.longitude)
    data['last_location'] = current_location
    if data.get('inactive_stopped'):
        return
    if data.get('session_ready') and not data['tracking']:
        data.update({
            'tracking': True,
            'session_start_time': datetime.now(),
            'session_steps': 0,
            'previous_location': current_location
        })
        try:
            msg = await bot.send_message(chat_id, "Walking process started.")
            data['last_message_id'] = msg.message_id
            data['last_message_text'] = msg.text
        except Exception:
            pass
        await asyncio.sleep(3)
    if data['tracking'] and (data['task'] is None or data['task'].done()):
        data['task'] = asyncio.create_task(check_location(chat_id))

async def check_location(chat_id):
    data = user_data.get(chat_id)
    if not data:
        return
    data.setdefault('start_time', datetime.now())
    interval = data.get('update_interval', 15)
    no_steps_counter = 0
    while data['tracking']:
        if data.get('last_location'):
            current_location = data['last_location']
            previous_location = data.get('previous_location')
            if previous_location:
                steps = int(geodesic(previous_location, current_location).meters / 0.8)
                max_steps = 111 if interval == 15 else 333
                if steps > max_steps:
                    await bot.send_message(chat_id, "You're walking too fast! Don't cheat.")
                    steps = 0
                if steps > 0:
                    data['session_steps'] += steps
                    no_steps_counter = 0
                else:
                    no_steps_counter += interval
                data['previous_location'] = current_location
                try:
                    total_steps = await db.get_user_data(data['user_id'], 'steps') + data['session_steps']
                    current_level = await db.get_user_data(data['user_id'], 'level')
                    progress_msg = "keep motivation for domination!" if LEVEL_UP_STEPS.get(current_level) else ""
                    new_text = f'You walked {data["session_steps"]} steps. {progress_msg}'
                    if data.get('last_message_text') != new_text:
                        if 'last_message_id' in data:
                            await bot.edit_message_text(chat_id=chat_id, message_id=data['last_message_id'], text=new_text)
                        else:
                            msg_obj = await bot.send_message(chat_id, new_text)
                            data['last_message_id'] = msg_obj.message_id
                        data['last_message_text'] = new_text
                    steps_needed = await db.get_user_data(data['user_id'], 'steps')
                    if steps_needed:
                        milestone_steps = steps_needed / 10
                        milestones_reached = min(data['session_steps'] // milestone_steps, 10)
                        for milestone in range(1, 11):
                            if milestone <= milestones_reached and milestone not in data['milestones']:
                                if 'last_milestone_message_id' in data:
                                    await bot.delete_message(chat_id, data['last_milestone_message_id'])
                                m_msg = await bot.send_message(chat_id, f"wa{milestone}kinG%..." if milestone < 10 else "wa1kinGG%...")
                                data['last_milestone_message_id'] = m_msg.message_id
                                data['milestones'].add(milestone)
                except Exception:
                    pass
            if random.random() < 0.01:
                try:
                    m_msg = await bot.send_message(chat_id, random.choice(MOTIVATIONAL_MESSAGES))
                    asyncio.create_task(delete_message_after_delay(chat_id, m_msg.message_id, 15))
                except Exception:
                    pass
        await update_session_data(chat_id, data)
        if no_steps_counter >= 10 * interval:
            await stop_walking_session(chat_id, no_steps=True)
        await asyncio.sleep(interval)

async def stop_walking_session(chat_id, no_steps=False):
    data = await get_session_data(chat_id)
    if data.get("tracking"):
        data["tracking"] = False
        user_id = data.get("user_id")
        session_steps = data.get("session_steps", 0)
        current_steps = await db.get_user_data(user_id, "steps")
        woncoins = (current_steps + session_steps) // 100 - current_steps // 100 * 15
        summary = f"Walking is over. You walked {session_steps} steps, and received {woncoins} WONcoins."
        if no_steps:
            summary = "you stand afk too long. " + summary
        try:
            await bot.send_message(chat_id, summary)
        except Exception:
            pass
        if session_steps > 0:
            await db.increase_user_steps(user_id, session_steps)
        data.update({
            "session_steps": 0,
            "previous_location": None,
            "milestones": set()
        })
        data.pop("last_message_id", None)
        data.pop("last_message_text", None)
        if no_steps:
            data["inactive_stopped"] = True
        await update_session_data(chat_id, data)
    else:
        try:
            await bot.send_message(chat_id, "No active walking session to stop.")
        except Exception:
            pass
