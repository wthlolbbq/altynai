import operator
import re
from re import Pattern

from bot.const.flag_quiz_constants import _country_code_to_name_map, _country_code_to_capital_map, \
    _country_code_to_population_map
from bot.models import CalculationOperation

# Greeter, GreeterWithStutter

greetings = {
    'hi',
    'hello',
    'howdy',
    'g\'day',
    'hey',
    'ciao',
    'good morning'
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

last_calc_answer_pattern = r'ans'
supported_operations: dict[str, CalculationOperation] = {
    'x': CalculationOperation(r'x', operator.mul),
    '*': CalculationOperation(r'\*', operator.mul),
    '+': CalculationOperation(r'\+', operator.add),
    '/': CalculationOperation(r'/', operator.truediv),
    ':': CalculationOperation(r'\:', operator.truediv),
    '-': CalculationOperation(r'\-', operator.sub),
    '%': CalculationOperation(r'%', operator.mod),
    'mod': CalculationOperation(r'mod', operator.mod),
    '**': CalculationOperation(r'\*\*', operator.pow),
    '^': CalculationOperation(r'\^', operator.pow),
}
op_re = r'(?:' + r'|'.join([i.re_pattern for i in supported_operations.values()]) + r')'
decimal_number_re = r'(?:' + last_calc_answer_pattern + r'|\d+(?:\.\d+)?)'

calc_pattern: Pattern[str] = re.compile(
    r'(?P<first>' + decimal_number_re + r')' +
    r'\s*' +
    r'(?P<op>' + op_re + r')' +
    r'\s*' +
    r'(?P<second>' + decimal_number_re + r')',
    re.IGNORECASE
)

# Reactor

loveyou_pattern: Pattern[str] = re.compile(
    r'love\s+you',
    re.IGNORECASE
)

# ChannelMessageSender

send_msg_to_channel_pattern: Pattern[str] = re.compile(
    r'^'
    r'to:\s*'
    r'(?P<channel_name>.*)'
    r'\s*:\s*'
    r'(?P<user_message>.*)'
    r'$',
    re.IGNORECASE
)

# YouTubeSearch

youtube_pattern: Pattern[str] = re.compile(
    r'^'
    r'yt\s*'
    r'(?P<search_term>\w.*)',
    re.IGNORECASE
)

rickroll_url = r'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

# Flag Quiz

non_alpha_pattern: Pattern[str] = re.compile(r'[^a-z]')
default_time_between_questions: float = 3  # seconds
start_quiz_pattern: Pattern[str] = re.compile(
    r'^(start|begin)\s*(?P<quiz_type>country|flag|capital|capitals|pop|population)\s*quiz!*$',
    re.IGNORECASE
)
end_quiz_pattern: Pattern[str] = re.compile(
    r'^(stop|end)\s*quiz!*$',
    re.IGNORECASE
)
skip_quiz_pattern: Pattern[str] = re.compile(
    r'^(skip|reveal)\s*question!*$',
    re.IGNORECASE
)

country_code2country_name = _country_code_to_name_map
country_code2capital = _country_code_to_capital_map
country_code2population = _country_code_to_population_map
country_codes = list(country_code2country_name.keys())

# Other

channel_ids = {
    'general': 1120086074312642684
}

log_datetime_format = '%Y-%m-%d %H:%M:%S'  # 2022-03-28 16:45:31
entrance_lines = (
    'AltynAI in da house!',
    'What\'s up gang?',
    'What\'s up nerds?',
    'Here we go!',
    'Welcome to Summoner\'s Rift!',
    'Hey ladies!',
    'AltynAI reporting for duty.',
    'Did someone say... *AltynAI*?',
    'Hippity, hoppity.'
)
