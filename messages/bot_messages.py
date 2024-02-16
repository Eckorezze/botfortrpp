from main import _


def choose_lan(language):
    if language == "ru":
        return """Вы выбрали русский язык!
Вы всегда можете изменить язык написав / language
Теперь снова нажмите / start
"""
    elif language == "en":
        return """You have selected English!
You can always change the language by writing /language
Now click /start again
"""


def send_info():
    return _("""🤖This bot with various functions acts as a TRPP project, Here is a list of available functions:

️/start - start interaction with the bot
QR code - generate a QR code
🔢Random number - generate a random number
🔐Generate password - generate a random password
🎯Tasks - create and schedule tasks
🌦Weather - view the weather
🎮Entertainments - the entertainment section

*If you want to make an offer or ask a question, click the Feedback💬 button!*""")


def admin_panel(user_count):
    return _("""Hello, this is the admin panel.
🪪Number of bot users: *{user_count}*

Admin commands:
/get\_users - download table with all users info""").format(user_count=user_count)


def return_user_info(user_name, user_id, user_username, status):
    return _("""*USER INFO*
_Name_: *{user_name}*
_ID_: *{user_id}*
_Username_: *{user_username}*
_Status_: *{status}*""").format(user_name=user_name, user_id=user_id, user_username=user_username, status=status)


def finish_mailing():
    return _("Mailing is complete!")


def start_mailing():
    return _("Starting mailing...")


def mailing_message():
    return _('Enter the message to send:')


def not_groups():
    return _("This command cannot be used in a group!")


def canceled():
    return _("Action canceled")


def ban_message(reason):
    return _("🚫You have been banned, contact @mak5er for more information!\nReason: {reason}").format(reason=reason)


def unban_message():
    return _("🎉You have been unbanned!")


def successful_ban(banned_user_id):
    return _("User {banned_user_id} successfully banned!").format(banned_user_id=banned_user_id)


def successful_unban(unbanned_user_id):
    return _("User {unbanned_user_id} successfully unbanned!").format(unbanned_user_id=unbanned_user_id)


def feedback_message_send(user, feedback_message):
    return _("*New message* from user: *{user}*\n*Message:* `{feedback_message}`").format(user=user,
                                                                                          feedback_message=feedback_message)
