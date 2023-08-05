#!/usr/bin/env python
# coding: utf-8

import string
import sys
import re
import datetime
import math
from unidecode import unidecode
import unicodedata
from string import punctuation


class RegexHandler:
    def __init__(self):
        pass

    url_pattern = r'''(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s(
    )<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))'''
    url_pattern2 = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([" \
                   r"^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    email_pattern = r'([\w\.-]+@[\w\.-]+\.\w+)'
    emoji_pattern = u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])'
    number_pattern = r'\d+'
    join_spaces_pattern = r' {2,}'
    join_nl_pattern = r'\n{2,}'
    html_pattern = r'<.*?>'
    time_pattern = r'^(([01]\d|2[0-3]):([0-5]\d)|24:00)$'
    has_time_pattern = r'(\d+):(\d+)'
    contact_prefixes_pattern = ['email', 'whatsapp', 'linkedin', 'twitter', 'mail']
    contact_prefixes_pattern = '(' + '|'.join(contact_prefixes_pattern) + ')[: ]+'

    url = re.compile(url_pattern)
    url2 = re.compile(url_pattern2)
    email = re.compile(email_pattern)
    emoji = re.compile(emoji_pattern, flags=re.UNICODE)
    number = re.compile(number_pattern)
    merge_lines = re.compile(join_nl_pattern)
    merge_spaces = re.compile(join_spaces_pattern)
    html = re.compile(html_pattern)
    time = re.compile(time_pattern)
    has_time = re.compile(has_time_pattern)
    camelCase1 = re.compile(r'([A-Z][a-z]+)')
    camelCase2 = re.compile(r'([A-Z]+)')
    camelCase3 = re.compile(r'(.)([A-Z][a-z]+)')
    camelCase4 = re.compile(r'([a-z0-9])([A-Z])')
    camelCase5 = re.compile(r'([A-Z])_([A-Z]+[0-9]*[A-Z]+)')
    bad_decoding = re.compile(r'^(\s*=?[A-F][A-F0-9]=?\s*){1,}$')
    square_brackets = re.compile(r'\[[^)^\]]*\]')
    brackets_cid = re.compile(r'\(cid:[^)]*\)')
    usd_amount = re.compile(r'\$\d{2,}\.?\d*')

    keywords = []

    word2num = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, \
                'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, \
                'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, \
                'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19, \
                'twenty': 20, 'thirty': 20, 'forty': 40, 'fifty': 50, 'sixty': 60, 'seventy': 70, 'eighty': 80,
                'ninety': 90 \
                }

    months = ['january', 'jan', 'february', 'feb', 'march', 'mar', 'april', 'apr']
    months += ['may', 'june', 'jun', 'july', 'jul', 'august', 'aug', 'september', 'sep', 'sept']
    months += ['october', 'oct', 'november', 'nov', 'december', 'dec']

    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    days += ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

    # build a table mapping all non-printable characters to None
    NOPRINT_TRANS_TABLE = {
        i: None for i in range(0, sys.maxunicode + 1) if not chr(i).isprintable()
    }

    @staticmethod
    def remove_non_printable_chars(s):
        """Replace non-printable characters in a string."""
        # the translate method on str removes characters
        # that map to None from the string
        return s.translate(RegexHandler.NOPRINT_TRANS_TABLE)

    @staticmethod
    def condense_numbers(t):
        return re.sub(r'(\d+),(\d+)', r'\1\2', t)

    @staticmethod
    def contain_usd_amounts(t):
        return len(RegexHandler.usd_amount.findall(t)) > 0

    @staticmethod
    def get_usd_amounts(t):
        return RegexHandler.usd_amount.findall(t)

    @staticmethod
    def set_keywords(t_list):
        if type(t_list) is not list:
            t_list = [t_list]
        RegexHandler.keywords = [t.lower() for t in t_list]

    @staticmethod
    def add_keyword(t):
        RegexHandler.keywords.append(t.lower())

    @staticmethod
    def is_keyword(t):
        return bool(t.lower() in RegexHandler.keywords)

    @staticmethod
    def get_keyword_id(t):
        return 0 if t.lower() not in RegexHandler.keywords else (RegexHandler.keywords.index(t.lower()) + 1)

    @staticmethod
    def get_emails(t, unique=True):
        emails = RegexHandler.email.findall(t)
        if (unique):
            return list(set(emails))
        return emails

    @staticmethod
    def count_substr_in_str(substr, full_str):
        count = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(substr), full_str))
        return count

    @staticmethod
    def get_domains_and_users(text, emails=[], return_emails=False):
        if not emails or type(emails) is not list:
            emails = RegexHandler.get_emails(str(text), unique=True)
        domains = []
        users = []
        for email in emails:
            domain = '.'.join(email.split('@')[1].split('.')[0:-1])
            user = email.split('@')[0]
            domains.append(domain)
            users.append(user)
        if return_emails:
            return list(set(domains)), list(set(users)), list(set(emails))
        return list(set(domains)), list(set(users))

    @staticmethod
    def get_domains(t, unique=True, no_social=False, emails=True, urls=True):
        domains = []
        if emails:
            domains = ['.'.join(email.split('@')[1].split('.')[0:-1]) for email in RegexHandler.get_emails(t, unique)]
        if urls:
            urls = RegexHandler.get_urls(t, True)
            for url in urls:
                url_split = url.split('.')
                if len(url_split) > 2:
                    domains += [url_split[-2]]
                elif len(url_split) == 2:
                    if 'www' not in url_split[0].lower():
                        domains += [url_split[0]]
        if (unique):
            domains = list(set(domains))
        if (no_social):
            social_domains = ['linkedin', 'goo', 'google', 'facebook', 'skype', 'pintrest', 'youtube', 'tinyurl']
            domains = list(filter(lambda domain: domain not in social_domains, domains))
        return domains

    @staticmethod
    def get_urls(t, unique=True):
        url = RegexHandler.url2.findall(t)
        urls = [x[0] for x in url]
        if (unique):
            urls = list(set(urls))
        return urls

    @staticmethod
    def get_urls_old(t, unique=True):
        urls = RegexHandler.url.findall(t)
        if (unique):
            z = []
            for ul in urls:
                ls = [ll for ll in list(set(ul)) if ll]
                z += ls
            return list(set(z))
        return urls

    @staticmethod
    def get_emojis(t, unique=True):
        emojis = RegexHandler.emoji.findall(t)
        if (unique):
            return list(set(emojis))
        return emojis

    @staticmethod
    def get_numbers(t, unique=True):
        numbers = RegexHandler.number.findall(t)
        if (unique):
            return list(set(numbers))
        return numbers

    @staticmethod
    def contain_email(t):
        return len(RegexHandler.get_emails(t)) > 0

    @staticmethod
    def contain_url(t):
        return len(RegexHandler.get_urls(t)) > 0

    @staticmethod
    def contain_emoji(t):
        return len(RegexHandler.get_emojis(t)) > 0

    @staticmethod
    def contain_number(t):
        return len(RegexHandler.get_numbers(t)) > 0

    @staticmethod
    def get_number_of_digits_in_number(n):
        if n == '':
            return 0
        if type(n) is str:
            return len(n)
        if n > 0:
            digits = int(math.log10(n)) + 1
        elif n == 0:
            digits = 1
        else:
            digits = int(math.log10(-n)) + 2  # +1 if you don't count the
        return digits

    @staticmethod
    def get_number_of_digits_and_digits_groups_in_text(t):
        groups = []
        n_digits = 0
        group = ''
        for c in t:
            if c.isdigit():
                n_digits += 1
                group += c
            else:
                if len(group):
                    groups.append(group)
                    group = ''
        if len(group):
            groups.append(group)
        return n_digits, groups

    @staticmethod
    def get_users(text):
        emails = RegexHandler.get_emails(text, unique=True)
        users = []
        for email in emails:
            user = email.split('@')[0]
            users.append(user)
        return list(set(users))

    @staticmethod
    def now_as_string():
        currentDT = datetime.datetime.now()
        return currentDT.strftime("%a, %b %d, %Y at %I:%M:%S %p")

    @staticmethod
    def contain_month(t):
        for tt in RegexHandler.remove_punct(t.lower()).split():
            if tt in RegexHandler.months:
                return True
        return False

    @staticmethod
    def contain_day(t):
        for tt in RegexHandler.remove_punct(t.lower()).split():
            if tt in RegexHandler.days:
                return True
        return False

    @staticmethod
    def is_time_format(t):
        return bool(RegexHandler.time.match(t))

    @staticmethod
    def has_time_format(t):
        t = t.lower().replace('am', ' ').replace('pm', ' ')
        r_list = RegexHandler.has_time.findall(t)
        if not len(r_list):
            return False
        else:
            for l in r_list:
                h = int(l[0])
                m = int(l[1])
                if h not in range(0, 25) or m not in range(0, 61):
                    return False
            return True

    @staticmethod
    def remove_html(t):
        return RegexHandler.html.sub(r'', t)

    @staticmethod
    def merge_multiple_spaces(t):
        return RegexHandler.merge_spaces.sub(r' ', t)

    @staticmethod
    def merge_multiple_new_lines(t):
        return RegexHandler.merge_lines.sub('\n', t).strip()

    @staticmethod
    def contain_camel_case(t):
        num_tokens_before_split_on_case = len(t.split())
        camel_case_splitted = RegexHandler.camelCase1.sub(r' \1', RegexHandler.camelCase2.sub(r' \1', t)).split()
        num_tokens_after_split_on_case = len(camel_case_splitted)
        return num_tokens_after_split_on_case > num_tokens_before_split_on_case

    @staticmethod
    def camel_to_snake(t):
        s1 = RegexHandler.camelCase3.sub(r'\1_\2', t)
        s2 = RegexHandler.camelCase4.sub(r'\1_\2', s1)
        if '_' in s2:
            # check if we have several UPPERS - if so split differently
            s3 = RegexHandler.camelCase5.sub(r'\1\2_', s2)
            return s3
        return s2

    @staticmethod
    def is_hashtag(t, edit=False):
        if t.startswith('#'):
            return True if not edit else (True, t.replace('#', ''))
        return False if not edit else (False, t)

    @staticmethod
    def is_user(t, edit=False):
        if t.startswith('@'):
            return True if not edit else (True, t.replace('@', ''))
        return False if not edit else (False, t)

    @staticmethod
    def contain_non_ascii_chars(t, edit=False, return_only_ascii=False):
        if not edit:
            return sum([(ord(s) >= 128) * 1 for s in t])
        asciis = ''
        non_asciis = ''
        for s in t:
            if ord(s) >= 128:
                non_asciis += s
            else:
                asciis += s
        if return_only_ascii:
            return asciis
        return len(non_asciis), asciis, non_asciis

    @staticmethod
    def remove_punct(text='', right=True, left=True, middle=True):
        if right and left and middle:
            return text.translate(str.maketrans('', '', punctuation))

        token = text
        if left:
            while (token and token[0] in punctuation):
                token = token[1:] if len(token) > 1 else ''

        if right:
            while (token and token[-1] in punctuation):
                token = token[:-1] if len(token) > 1 else ''

        if middle and len(token) > 2:
            token = token[0] + token.translate(str.maketrans('', '', punctuation)) + token[-1]

        return token

    @staticmethod
    def is_bad_decoding_line(line):
        return (len(re.findall(RegexHandler.bad_decoding, line, flags=0)) > 0)

    @staticmethod
    def contain_date(tt):
        def remove_punct(s):
            return " ".join(s.translate(str.maketrans('', '', string.punctuation)).split()).strip()

        for t in tt.split():
            for marker in ['.', '|', '/', '-']:
                if marker in t:
                    if remove_punct(t).isdigit():
                        template = "%m/%d/%y" if '/' in t else "%m|%d|%y" if '|' in t else "%m-%d-%y" if '-' in t else "%m.%d.%y"
                        try:
                            datetime.datetime.strptime(t, template)
                            return True
                        except:
                            continue
                    continue
        return False

    @staticmethod
    def remove_brackets_content_from_email_text(text):
        t = text.replace('[mailto:', '')
        #             t = RegexHandler.square_brackets.sub('', t)
        t = text.replace('[', '').replace(']', '')
        t = RegexHandler.brackets_cid.sub('', t)
        return t

    @staticmethod
    def extract_emojies_codes(input_string, check_first=True):
        if check_first:
            if not RegexHandler.contain_emoji(input_string):
                return input_string

        returnString = ""
        emojies = []
        ascies = []
        for character in input_string:
            try:
                character.encode("ascii")
                returnString += character
            except UnicodeEncodeError:
                replaced = unidecode(str(character))
                if replaced != '':
                    returnString += replaced
                    ascies += [character]
                else:
                    try:
                        emojies += [unicodedata.name(character).replace(' ', '_')]
                    except ValueError:
                        ascies += [character]

        return returnString, emojies, ascies

    @staticmethod
    def normalize_space(text):
        """
            Remove multiple space characters and keep single simple space. Also stripping new lines ending the text input.
            :param text: string input
            :return: processed string
            """
        return '\n'.join([' '.join(line.split()) for line in text.strip().split('\n')])

    @staticmethod
    def remove_space_before_semicolon(text):
        """
            Replace any non alphanumeric character preceded and followed by a space, with the character without space
            preceding. For example: 'Mobile : 972-54654' will output: 'Mobile: 972-54654'
            :param text: string input
            :return: processed string
            """
        return re.sub(r'\s+(:|,)', r'\1 ', text)

    @staticmethod
    def remove_brackets_for_digits(text):
        """
            Remove brackets around one or more digits that may be preceded by a plus sign (+). The output is the digits
            with the plus sign if present without the beackets.
            :param text: string input
            :return: processed string
            """
        return re.sub(r'\(\s?(\+?\d+)\s?\)', r'\1', text)

    @staticmethod
    def count_sequential_digits(text):
        matches = re.findall(r'\d[\d\s\-.]+\d', text)
        if matches:
            return max([len(match) for match in matches])
        return 0

    @staticmethod
    def insert_space(text):
        return re.sub(r'(\*|~|\|)', r' \1 ', text)

    @staticmethod
    def concat_numbers(text):
        return re.sub(r'(?<=\d) (?=\d)', '-', text)

    @staticmethod
    def fix_url(text):
        line_l = text.split('\n')
        line_l_out = []
        for line in line_l:
            token_l = line.split(' ')
            token_l_out = []
            for token in token_l:
                if '@' not in token and re.findall(r'\S+(\.org|\.gov|\.com|\.net|\.int|\.edu|\.mil)(\s|$)', token):
                    if not token.startswith('www.'):
                        token_l_out.append('www.' + token)
                    else:
                        token_l_out.append(token)
                else:
                    token_l_out.append(token)
            line_l_out.append(' '.join(token_l_out))
        return '\n'.join(line_l_out)

    @staticmethod
    def clear_url_junk(text):
        token_l = text.split()
        token_l_out = []
        for token in token_l:
            if token.count('%') > 1:
                if len(re.findall(r'[0-9a-fA-F%/-]', token)) == len(token):
                    continue
                else:
                    token_l_out.append(token)
            else:
                token_l_out.append(token)
        return ' '.join(token_l_out)

    @staticmethod
    def clear_contact_prefixes(text):
        return re.sub(RegexHandler.contact_prefixes_pattern, '', text, flags=re.IGNORECASE)

    @staticmethod
    def clear_number_suffixes(text):
        return re.sub(r'([\d\-\(\)\.\+]{5})_([a-zA-Z]+)($|\s)', r'\1 \2\3', text)

    @staticmethod
    def split_line_by_separator(text):
        split_sep = RegexHandler.split_by_separator(text)
        if len(split_sep) == 2:
            if len(split_sep) >= 2:
                return '\n'.join(split_sep)
        return text

    @staticmethod
    def split_by_separator(text):
        return re.split(r' *[\|~] *', text)
