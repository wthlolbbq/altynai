import operator
import re
from re import Pattern

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

flag_quiz_replace_pattern = re.compile(r'[^a-z]')
default_time_between_questions: float = 3  # seconds
start_quiz_pattern: Pattern[str] = re.compile(
    r'^(start|begin)\s*quiz!*$',
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

country_code2country_name = {
    'AC': ['Ascension Island', 'ascension'],
    'AD': ['Andorra'],
    'AE': ['United Arab Emirates', 'uae', 'emirates'],
    'AF': ['Afghanistan'],
    'AG': ['Antigua and Barbuda'],
    'AI': ['Anguilla'],
    'AL': ['Albania'],
    'AM': ['Armenia'],
    'AO': ['Angola'],
    'AQ': ['Antarctica'],
    'AR': ['Argentina'],
    'AS': ['American Samoa'],
    'AT': ['Austria'],
    'AU': ['Australia', 'aus'],
    'AW': ['Aruba'],
    'AX': ['Aland Islands', 'aland', 'alands'],
    'AZ': ['Azerbaijan'],
    'BA': ['Bosnia and Herzegovina', 'bosnia', 'bih'],
    'BB': ['Barbados'],
    'BD': ['Bangladesh'],
    'BE': ['Belgium'],
    'BF': ['Burkina Faso'],
    'BG': ['Bulgaria'],
    'BH': ['Bahrain'],
    'BI': ['Burundi'],
    'BJ': ['Benin'],
    'BM': ['Bermuda'],
    'BN': ['Brunei Darussalam', 'brunei'],
    'BO': ['Bolivia'],
    'BQ-BO': ['Bonaire'],
    'BQ-SE': ['Sint Eustatius', 'st eustatius'],
    'BQ-SA': ['Saba'],
    'BR': ['Brazil'],
    'BS': ['The Bahamas', 'bahamas'],
    'BT': ['Bhutan'],
    'BW': ['Botswana'],
    'BY': ['Belarus'],
    'BZ': ['Belize'],
    'CA': ['Canada'],
    'CC': ['Cocos (Keeling) Islands', 'cocos islands', 'keeling islands', 'cocos', 'keeling'],
    'CD': ['Democratic Republic of the Congo', 'drc', 'dr congo'],
    'CF': ['Central African Republic', 'car', 'central africa'],
    'CG': ['Republic of the Congo', 'roc'],
    'CH': ['Switzerland'],
    'CI': ['Cote d\'Ivoire', 'ivory coast'],
    'CK': ['Cook Islands', 'cook'],
    'CL': ['Chile'],
    'CM': ['Cameroon'],
    'CN': ['China'],
    'CO': ['Colombia'],
    'CR': ['Costa Rica'],
    'CU': ['Cuba'],
    'CV': ['Cape Verde', 'cabo verde'],
    'CW': ['Curacao'],
    'CX': ['Christmas Island', 'christmas'],
    'CY': ['Cyprus'],
    'CZ': ['Czech Republic', 'czechia', 'czech'],
    'DE': ['Germany'],
    'DJ': ['Djibouti'],
    'DK': ['Denmark'],
    'DM': ['Dominica'],
    'DO': ['Dominican Republic', 'dominican'],
    'DZ': ['Algeria'],
    'EC': ['Ecuador'],
    'EE': ['Estonia'],
    'EG': ['Egypt'],
    'EH': ['Western Sahara', 'Sahrawi Arab Democratic Republic', 'sahrawi republic', 'sahrawi'],
    'ER': ['Eritrea'],
    'ES': ['Spain'],
    'ET': ['Ethiopia'],
    'FI': ['Finland'],
    'FJ': ['Fiji'],
    'FK': ['Falkland Islands (Malvinas)', 'falklands', 'falkland', 'falkland islands', 'malvinas'],
    'FM': ['Micronesia'],
    'FO': ['Faroe Islands', 'faroe'],
    'FR': ['France'],
    'GA': ['Gabon'],
    'GB': ['United Kingdom', 'uk'],
    'GB-ENG': ['England'],
    'GB-NIR': ['Northern Ireland', 'ni'],
    'GB-SCT': ['Scotland'],
    'GB-WLS': ['Wales'],
    'GD': ['Grenada'],
    'GE': ['Georgia'],
    'GF': ['French Guiana'],
    'GG': ['Bailiwick of Guernsey', 'guernsey'],
    'GH': ['Ghana'],
    'GI': ['Gibraltar'],
    'GL': ['Greenland'],
    'GM': ['The Gambia', 'gambia'],
    'GN': ['Guinea'],
    'GP': ['Guadeloupe'],
    'GQ': ['Equatorial Guinea'],
    'GR': ['Greece'],
    'GS': ['South Georgia and the South Sandwich Islands', 'sandwich'],
    'GT': ['Guatemala'],
    'GU': ['Guam'],
    'GW': ['Guinea-Bissau'],
    'GY': ['Guyana'],
    'HK': ['Hong Kong'],
    'HN': ['Honduras'],
    'HR': ['Croatia', 'hrv', 'cro'],
    'HT': ['Haiti'],
    'HU': ['Hungary'],
    'IC': ['Canary Islands', 'canary'],
    'ID': ['Indonesia'],
    'IE': ['Ireland'],
    'IL': ['Israel'],
    'IM': ['Isle of Man'],
    'IN': ['India'],
    'IO': ['British Indian Ocean Territory', 'biot'],
    'IQ': ['Iraq'],
    'IR': ['Islamic Republic of Iran', 'iran'],
    'IS': ['Iceland'],
    'IT': ['Italy'],
    'JE': ['Jersey'],
    'JM': ['Jamaica'],
    'JO': ['Jordan'],
    'JP': ['Japan', 'weebland'],
    'KE': ['Kenya'],
    'KG': ['Kyrgyzstan', 'kyrg'],
    'KH': ['Cambodia'],
    'KI': ['Kiribati'],
    'KM': ['Comoros'],
    'KN': ['Saint Kitts and Nevis', 'st kitts and nevis'],
    'KP': ['North Korea', 'dprk', 'best korea', 'nk'],
    'KR': ['South Korea', 'sk'],
    'KW': ['Kuwait'],
    'KY': ['Cayman Islands', 'cayman', 'caymans'],
    'KZ': ['Kazakhstan'],
    'LA': ['Laos'],
    'LB': ['Lebanon'],
    'LC': ['Saint Lucia', 'st lucia'],
    'LI': ['Liechtenstein'],
    'LK': ['Sri Lanka'],
    'LR': ['Liberia'],
    'LS': ['Lesotho'],
    'LT': ['Lithuania'],
    'LU': ['Luxembourg', 'lux'],
    'LV': ['Latvia'],
    'LY': ['Libya'],
    'MA': ['Morocco'],
    'MC': ['Monaco'],
    'MD': ['Moldova'],
    'ME': ['Montenegro'],
    'MG': ['Madagascar'],
    'MH': ['Marshall Islands', 'marshall'],
    'MK': ['North Macedonia', 'macedonia'],
    'ML': ['Mali'],
    'MM': ['Myanmar', 'burma'],
    'MN': ['Mongolia', 'mongol'],
    'MO': ['Macau', 'macao'],
    'MP': ['Northern Mariana Islands', 'northern mariana', 'northern marianas'],
    'MQ': ['Martinique'],
    'MR': ['Mauritania'],
    'MS': ['Montserrat'],
    'MT': ['Malta'],
    'MU': ['Mauritius'],
    'MV': ['Maldives'],
    'MW': ['Malawi'],
    'MX': ['Mexico', 'mex'],
    'MY': ['Malaysia'],
    'MZ': ['Mozambique'],
    'NA': ['Namibia'],
    'NC': ['New Caledonia'],
    'NE': ['Niger'],
    'NF': ['Norfolk Island', 'norfolk'],
    'NG': ['Nigeria'],
    'NI': ['Nicaragua'],
    'NL': ['Netherlands', 'the netherlands', 'nl'],
    'NO': ['Norway', 'Svalbard and Jan Mayen', 'svalbard', 'norge'],
    'NP': ['Nepal'],
    'NR': ['Nauru'],
    'NU': ['Niue'],
    'NZ': ['New Zealand', 'nz', 'kiwiland'],
    'OM': ['Oman'],
    'PA': ['Panama'],
    'PE': ['Peru'],
    'PF': ['French Polynesia'],
    'PG': ['Papua New Guinea', 'papa johns'],
    'PH': ['Philippines', 'the philippines'],
    'PK': ['Pakistan'],
    'PL': ['Poland'],
    'PM': ['Saint Pierre and Miquelon', 'saint pierre', 'st pierre'],
    'PN': ['Pitcairn', 'pitcairn islands', 'pitcairns'],
    'PR': ['Puerto Rico'],
    'PS': ['Palestine'],
    'PT': ['Portugal'],
    'PW': ['Palau'],
    'PY': ['Paraguay'],
    'QA': ['Qatar'],
    'RO': ['Romania'],
    'RS': ['Serbia', 'enemies'],
    'RU': ['russia', 'russian federation', 'ru', 'cccp'],
    'RW': ['Rwanda'],
    'SA': ['Saudi Arabia', 'saudi'],
    'SB': ['Solomon Islands', 'solomon', 'solomons'],
    'SC': ['Seychelles'],
    'SD': ['Sudan'],
    'SE': ['Sweden'],
    'SG': ['Singapore'],
    'SH': ['Saint Helena, Ascension and Tristan da Cunha', 'st helena', 'saint helena'],
    'SI': ['Slovenia'],
    'SK': ['Slovakia'],
    'SL': ['Sierra Leone'],
    'SM': ['San Marino'],
    'SN': ['Senegal'],
    'SO': ['Somalia'],
    'SR': ['Suriname'],
    'SS': ['South Sudan'],
    'ST': ['Sao Tome and Principe', 'sao tome'],
    'SV': ['El Salvador'],
    'SX': ['Sint Maarten (Dutch part)', 'sint maarten', 'st martin', 'saint martin'],
    'SY': ['Syria'],
    'SZ': ['Swaziland', 'eswatini'],
    'TA': ['Tristan da Cunha'],
    'TC': ['Turks and Caicos Islands', 'turks and caicos'],
    'TD': ['Chad'],
    'TF': ['French Southern and Antarctic Lands', 'French Southern Territories', 'French Southern Lands', 'fst', 'fsal',
           'taaf'],
    'TG': ['Togo'],
    'TH': ['Thailand'],
    'TJ': ['Tajikistan', 'tajik'],
    'TK': ['Tokelau'],
    'TL': ['Timor-Leste', 'East Timor'],
    'TM': ['Turkmenistan', 'turkmen'],
    'TN': ['Tunisia'],
    'TO': ['Tonga'],
    'TR': ['Turkey', 'turkiye'],
    'TT': ['Trinidad and Tobago'],
    'TV': ['Tuvalu'],
    'TW': ['Taiwan'],
    'TZ': ['Tanzania'],
    'UA': ['Ukraine'],
    'UG': ['Uganda'],
    'US': ['United States of Amerca', 'united states', 'america', 'us', 'usa'],
    'UY': ['Uruguay'],
    'UZ': ['Uzbekistan', 'uzbek'],
    'VA': ['Holy See', 'vatican city', 'vatican'],
    'VC': ['Saint Vincent and the Grenadines', 'st vincent', 'saint vincent'],
    'VE': ['Venezuela'],
    'VG': ['British Virgin Islands', 'uk vi', 'british virgin'],
    'VI': ['United States Virgin Islands', 'us virgin islands', 'us vi', 'us virgin'],
    'VN': ['Vietnam'],
    'VU': ['Vanuatu'],
    'WF': ['Wallis and Futuna'],
    'WS': ['Samoa'],
    'XK': ['Kosovo'],
    'YE': ['Yemen'],
    'YT': ['Mayotte'],
    'ZA': ['South Africa'],
    'ZM': ['Zambia'],
    'ZW': ['Zimbabwe'],
}
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
