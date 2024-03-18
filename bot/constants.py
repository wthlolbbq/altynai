import operator
import re

# Greeter, GreeterWithStutter

greetings = {
    'hi',
    'hello',
    'howdy',
    'g\'day',
    'hey',
    'ciao'
}

greeting_emojis = [
    '😂', '❤️', '🤣', '🔥', '🎂', '😎'
]

# StutterChooser

stutter_choices = {
    'stop stuttering!': False,
    'start stuttering!': True
}

# Calculator

supported_operations = {
    'x': operator.mul,
    '*': operator.mul,
    '+': operator.add,
    '/': operator.truediv,
    ':': operator.truediv,
    '-': operator.sub,
    '%': operator.mod,
    'mod': operator.mod,
    '**': operator.pow,
    '^': operator.pow,
}
decimal_number_re = r'(?:ans|\d+(?:\.\d+)?)'
op_re = r'(?:[x*+/:%^\-]|mod|\*\*)'
calc_re = re.compile(
    r'(?P<first>' + decimal_number_re + r')' +
    r'\s*' +
    r'(?P<op>' + op_re + r')' +
    r'\s*' +
    r'(?P<second>' + decimal_number_re + r')',
    re.IGNORECASE
)

# Reactor

loveyou_re = re.compile(
    r'love\s+you',
    re.IGNORECASE
)

# ChannelMessageSender

send_msg_to_channel_re = re.compile(
    r'^'
    r'to:\s*'
    r'(?P<channel_name>.*)'
    r'\s*:\s*'
    r'(?P<user_message>.*)'
    r'$',
    re.IGNORECASE
)

# Other

channel_ids = {
    'general': 1120086074312642684
}

log_datetime_format = "%Y-%m-%d %H:%M:%S"  # 2022-03-28 16:45:31
entrance_lines = (
    'AltynAI in da house!',
    'What\'s up gang?',
    'What\'s up nerds?',
    'Here we go!',
    'Welcome to Summoner\'s Rift!',
    'Hey ladies!',
    'AltynAI reporting for duty.',
    'Did someone say... *AltynAI*?',
)
