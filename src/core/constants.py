DESCRIPTIONS = {
    'PROGRE': 'Progressive Scan text for TV',
    'TRIAL': 'Command Mission demo texts',
    'SUB_TXT': 'Weapon descriptions and pause menu',
    'SUB_TIT': 'Weapon and part names',
    'SAVE_TIT': 'Saving and loading',
    'RESULT': 'Result screen after each level',
    'PAL': 'Video mode settings',
    'OPT_TXT': 'Options menu',
    'OPT_TIT': 'Options menu control buttons names',
    'LABO_TXT': 'RD Lab Menu descriptions',
    'LABO_TIT': 'RD Lab Menu labels (Stage Select, Chip Dev...)',
    'HB_TIT': 'Stage, character, navigator, and netural armor descriptions',
    'HB_IM': 'Intermission descriptions',
    'HB_DM': 'Stage Select cutscenes',
    'CHIP_TIT': 'RD Chip names',
    'CHIP_TXT': 'RD Chip descriptions'
}

DESCRIPTION_MAP = {
    'NV1': "Alia's dialogue ",
    'NV2': "Layer's dialogue ",
    'NV3': "Palette's dialogue ",
    'DM_': "Dr. Light and other events ",
    'DM1': "X's dialogue ",
    'DM2': "Zero's dialogue ",
    'DM3': "Axl's dialogue ",
    'MOV': 'Pre-Rendered Video Subtitles ',
    'VA': "that involve Vile",
    'ST00': "in Noah's Park",
    'ST01': 'in Troia Base',
    'ST02': 'in Primrose',
    'ST03': 'in Pitch Black',
    'ST04': 'in Dynasty',
    'ST05': 'in Inferno',
    'ST06': 'in Central White',
    'ST07': 'in Metal Valley',
    'ST08': 'in Booster Forest',
    'ST09': 'in Jakob Elevator',
    'ST10': 'in Gateway',
    'ST11': "in Sigma's Palace",
}

STAGE_NAMES = {
    '00': "Noah's Park",
    '01': 'Troia Base',
    '02': 'Primrose',
    '03': 'Pitch Black',
    '04': 'Dynasty',
    '05': 'Inferno',
    '06': 'Central White',
    '07': 'Metal Valley',
    '08': 'Booster Forest',
    '09': 'Jakob Elevator',
    '10': 'Gateway',
    '11': "Sigma's Palace",
}

ALPHABET = [' ', '!', '"', '%', '&', '(', ')', 'x', '+', '-', ',',
            '.', '/', ':', ';', '=', '?', '@', '[', ']', '_', '~', '`', '°', '…', '…'
    , '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
    , 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    , 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
            # 0x58, 59, 5A, 5B, 5C, 5D
    , "'", "||", "Σ", "◯", "△", "↑", '↓', '↙', '↘', '←', '→', '®', '€']

CHARACTERS = ['X', 'Zero', 'Axl', 'BG Alia', 'BG Layer', 'BG Pallette', 'Signas', 'Dr. Light', 'Optic Sunflower', 'Gravity Antonion', 'Dark Mantis',
              'Gigabolt Man-o-War', 'Burn Rooster', 'Avalanche Yeti', 'Earthrock Trilobyte', 'Bamboo Pandemonium', 'Vile', 'Sigma', 'Lumine', 'FG Alia',
              'FG Layer', 'FG Pallette', 'None']

# http://sprites-inc.co.uk/sprite.php?local=X/X8/Mugshots/
MUGSHOT_DESCRIPTIONS = [
    ['Serious', 'Surprised', 'Angry', 'Neutral Armor'],  # X
    ['Holding Sword', 'Serious', 'Eyes Closed'],  # Zero
    ['Smiling', 'Upset', 'Holding Gun', 'Serious'],  # Axl
    ['Speaking', 'Listening', 'Worried'],  # BG Alia
    ['Listening', 'Red Face', 'Slight Blush'],  # BG Layer
    ['Listening', 'Speaking', 'Thinking', 'RD Lab'],  # BG Pallette
    ['Serious'],  # Signas
    ['Hologram'],  # Dr. Light
    ['Default'],  # Optic Sunflower
    ['Default'],  # Gravity Antonion
    ['Default'],  # Dark Mantis
    ['Default'],  # Gigabolt Man-o-War
    ['Default'],  # Burn Rooster
    ['Default'],  # Avalanche Yeti
    ['Default'],  # Earthrock Trilobyte
    ['Default'],  # Bamboo Pandemonium
    ['Default'],  # Vile
    ['Copy', 'Real'],  # Sigma
    ['Regular', 'Psychopath Smirk', 'Defeated'],  # Lumine
    ['Speaking', 'Listening', 'Worried'],  # FG Alia
    ['Listening', 'Red Face', 'Slight Blush'],  # FG Layer
    ['Listening', 'Speaking', 'Thinking', 'RD Lab'],  # FG Pallette
    ['None'],  # None or Sigma?
]