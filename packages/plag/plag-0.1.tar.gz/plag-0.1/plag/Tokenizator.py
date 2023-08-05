import re

class Tokenizator:
    """
       Класс реализует конвертацию кода программы в строку токенов
    """

    def __init__(self, path_token_file: str = None, string_tokens: str = None):
        """
           Коструктор задает массив токенов и массив параметров нормализации из файла или из строки
        """
        self.normal_list = list()
        self.token_list = list()
        if path_token_file:
            with open(path_token_file, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if 'NormalTypeStart' in line:
                        stringNormal = line[line.find('NormalTypeStart ') + 16: line.find(' NormalTypeEnd')]
                        self.normal_list.append(stringNormal)
                    elif 'TokenTypeStart' in line:
                        stringToken = line[line.find('TokenTypeStart ') + 15: line.find(' TokenTypeEnd')]
                        stringSign = line[line.find('TokenSignStart ') + 15: line.find(' TokenSignEnd')]
                        self.token_list.append([stringToken, stringSign])
        elif string_tokens:
            import io
            buf = io.StringIO(string_tokens)
            lines = buf.readlines()
            for line in lines:
                if 'NormalTypeStart' in line:
                    stringNormal = line[line.find('NormalTypeStart ') + 16: line.find(' NormalTypeEnd')]
                    self.normal_list.append(stringNormal)
                elif 'TokenTypeStart' in line:
                    stringToken = line[line.find('TokenTypeStart ') + 15: line.find(' TokenTypeEnd')]
                    stringSign = line[line.find('TokenSignStart ') + 15: line.find(' TokenSignEnd')]
                    self.token_list.append([stringToken, stringSign])

    def getN(self):
        return self.normal_list

    def getT(self):
        return self.token_list

    def get_normalized_string(self, data: str):
        """
           Функция принимает на вход строку для нормализации и
           возращает нормализованную строку
        """
        temp_data = data

        for normal_type in self.normal_list:
            temp_data = re.sub(normal_type, ' ', temp_data, flags=re.S)

        return temp_data

    def get_tokenization_string(self, data: str, is_save_location: bool = False):
        """
           Функция принимает на вход строку для токенизации и
           возращает строку токенов
           Параметр is_save_location отвечает за формат вывода токенизированной строки
        """
        temp_data = data
        identifier = ''
        is_first = True

        for token_type in self.token_list:
            temp_data = re.sub(token_type[0], ' @' + token_type[1] + ' ', temp_data)
            if is_first:
                is_first = False
                identifier += '[@' + token_type[1] + ']'
            else:
                identifier += '|[@' + token_type[1] + ']'

        identifier = '(?!(' + identifier + '))\w+'
        temp_data = re.sub(identifier, ' @I ', temp_data)
        temp_data = re.sub('@', '', temp_data)

        if not is_save_location:
            temp_data = re.sub('\s+', '', temp_data)

        return temp_data
