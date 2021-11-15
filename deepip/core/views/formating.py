

class Color:
    """Collect color codes and methods for working with it"""

    BORDER_START = '\033['
    BORDER_END = '\033[0m'

    CEND = '0m'
    CBOLD = '1m'
    CITALIC = '3m'
    CURL = '4m'
    CBLINK = '5m'
    CBLINK2 = '6m'
    CSELECTED = '7m'

    CBLACK = '30m'
    CRED = '31m'
    CGREEN = '32m'
    CYELLOW = '33m'
    CBLUE = '34m'
    CVIOLET = '35m'
    CBEIGE = '36m'
    CWHITE = '37m'

    CBLACKBG = '40m'
    CREDBG = '41m'
    CGREENBG = '42m'
    CYELLOWBG = '43m'
    CBLUEBG = '44m'
    CVIOLETBG = '45m'
    CBEIGEBG = '46m'
    CWHITEBG = '47m'

    CGREY = '90m'
    CRED2 = '91m'
    CGREEN2 = '92m'
    CYELLOW2 = '93m'
    CBLUE2 = '94m'
    CVIOLET2 = '95m'
    CBEIGE2 = '96m'
    CWHITE2 = '97m'

    CGREYBG = '100m'
    CREDBG2 = '101m'
    CGREENBG2 = '102m'
    CYELLOWBG2 = '103m'
    CBLUEBG2 = '104m'
    CVIOLETBG2 = '105m'
    CBEIGEBG2 = '106m'
    CWHITEBG2 = '107m'

    @staticmethod
    def fill(string: str, color_code: str) -> str:
        """Set the color design of the string to console output"""
        return ''.join((Color.BORDER_START, color_code, string, Color.BORDER_END))
