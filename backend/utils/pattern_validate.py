import re


def search_string(pattern: str, text: str) -> re.Match[str]:
    """
    全字段正则匹配

    :param pattern: 正则表达式模式
    :param text: 待匹配的文本
    :return:
    """
    return re.search(pattern, text)


def match_string(pattern: str, text: str) -> re.Match[str]:
    """
    从字段开头正则匹配

    :param pattern: 正则表达式模式
    :param text: 待匹配的文本
    :return:
    """
    return re.match(pattern, text)


def is_phone(number: str) -> re.Match[str]:
    """
    检查手机号码格式

    :param number: 待检查的手机号码
    :return:
    """
    phone_pattern = r'^1[3-9]\d{9}$'
    return match_string(phone_pattern, number)


def is_git_url(url: str) -> re.Match[str]:
    """
    检查 git URL 格式（仅允许 HTTP/HTTPS 协议）

    :param url: 待检查的 URL
    :return:
    """
    git_pattern = r'^(?P<scheme>https?)://(?P<host>[^/]*)(?P<path>(?:/[^/]*)*/)(?P<repo>[^/]+?)(?:\.git)?$'
    return match_string(git_pattern, url)


def is_has_number(value: str) -> re.Match[str]:
    """
    检查数字

    :param value: 待检查的值
    :return:
    """
    number_pattern = r'\d'
    return search_string(number_pattern, value)


def is_has_letter(value: str) -> re.Match[str]:
    """
    检查字母

    :param value: 待检查的值
    :return:
    """
    letter_pattern = r'[a-zA-Z]'
    return search_string(letter_pattern, value)


def is_has_special_char(value: str) -> re.Match[str]:
    """
    检查特殊字符

    :param value: 待检查的值
    :return:
    """
    special_char_pattern = r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]'
    return search_string(special_char_pattern, value)


def is_english_identifier(value: str) -> re.Match[str]:
    """
    检查英文标识符

    :param value: 待检查的值
    :return:
    """
    identifier_pattern = r'^[a-zA-Z][a-zA-Z_]*$'
    return match_string(identifier_pattern, value)
