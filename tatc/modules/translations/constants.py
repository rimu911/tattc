from tatc.core.constants import *
"""
Constants for translation modules
"""

# environment related constants
DEFAULT_TRANSLATION_ENGINE = 'default_translation_engine'
DEFAULT_IGNORE_WORDS = 'default_ignore_words'
LANGUAGE_DETECTION_MODEL = 'language_detection_model'
LANGUAGE_DETECTION_THRESHOLD = 'language_detection_threshold'

# configuration related constants
ENABLED = ENABLED
TRANSLATION_ENGINE = 'translation_engine'
TARGET_LANGUAGES = 'target_languages'
IGNORE_LANGUAGES = 'ignore_languages'
IGNORE_WORDS = 'ignore_words'
DEBUG_MODE = 'debug_mode'
SANITIZE_EMOJIS = 'sanitize_emojis'
SANITIZE_USERNAMES = 'sanitize_usernames'
MORSE_CODE_SUPPORT = 'morse_code_support'
MORSE_CODE_LANGUAGE_ID = 'morse_code'
MORSE_CODE_DECODED_LANGUAGE_ID = f'decoded_{MORSE_CODE_LANGUAGE_ID}'
MORSE_CODE_ENGINE = f'{MORSE_CODE_LANGUAGE_ID}_engine'

TRANSLATIONS = 'translations'
