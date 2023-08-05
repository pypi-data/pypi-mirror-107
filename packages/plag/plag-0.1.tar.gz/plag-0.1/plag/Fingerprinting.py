import hashlib

class Fingerprinting:
    """
       Класс реализует конвертацию строк в отпечатки
    """
    def __init__(self, fingerprint_size: int = 10, token_substring_length: int = 10):
        """
            Конструктор сохраняет значение длины отпечатка и длины подстроки строки токенов
        """
        self.fingerprint_size = fingerprint_size
        self.token_substring_length = token_substring_length

    def get_hash_table(self, tokenized_string: str):
        """
            Функция возващает таблицу хешей строки
        """
        hash_list = list()
        for token_index in range(0, len(tokenized_string) - self.token_substring_length + 1):
            substring = tokenized_string[token_index: (token_index + self.token_substring_length)]
            hash_substring = self.get_hash(substring)
            hash_list.append(hash_substring)
        return hash_list

    def get_hash(self, substring: str):
        """
            Функция возващает хеш строки
        """
        substring_bit = substring.encode('utf8')
        hash_ = hashlib.sha256(substring_bit)
        return int(hash_.hexdigest(), base=16)

    def get_fingerprint_list(self, tokenized_string: str):
        """
            Функция возващает лист отпечатков
        """
        fingerprint_list = list()
        hash_table = self.get_hash_table(tokenized_string)
        previous_value = min(hash_table[0: (0 + self.fingerprint_size)])
        fingerprint_list.append(previous_value)
        for hash_index in range(1, len(hash_table) - self.fingerprint_size + 1):
            hash_ = hash_table[hash_index: (hash_index + self.fingerprint_size)]
            value = min(hash_)
            if previous_value != value:
                fingerprint_list.append(value)
            previous_value = value
        return fingerprint_list

    def get_percentage_similarity(self, fingerprint_list_first: list, fingerprint_list_second: list):
        """
            Функция возващает процент схожести двух множеств отпечатков
        """
        fingerprint_list_first = set(fingerprint_list_first)
        fingerprint_list_second = set(fingerprint_list_second)
        intersection_length = len(fingerprint_list_first & fingerprint_list_second)
        min_length = min(len(fingerprint_list_first), len(fingerprint_list_second))
        return intersection_length / min_length


