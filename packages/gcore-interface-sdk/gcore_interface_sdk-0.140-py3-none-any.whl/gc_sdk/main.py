from witapi.main import WITClient
from gc_sdk import methods
from gc_sdk import functions


class MainController(WITClient):
    """ Класс-обертка, через методы которого происходит исполнение всех методов API GCore"""
    def __init__(self, api_ip, api_port, login="Login", password="Password", general_method='user_command',
                 methods_dict=methods.methods_dict):
        super().__init__(api_ip, api_port, login, password)
        self.api_ip = api_ip
        self.api_port = api_port
        self.make_connection()
        self.general_method = general_method
        self.methods_dict = methods_dict

    def get_api_methods(self, *args, **kwargs):
        """ Получить все методы API """
        return functions.extract_supported_methods(self)

    def get_sdk_methods(self, *args, **kwargs):
        """ Получить все поддерживаемые методы SDK """
        return methods.methods_dict

    def execute_method(self, method_name, *args, **kwargs):
        """ Отправить метод method_name в API и вернуть ответ """
        return functions.execute_method(self, self.general_method, self.methods_dict, method_name, *args, **kwargs)



