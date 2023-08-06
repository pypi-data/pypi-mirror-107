""" Содержит все исполнительные функции """


def extract_supported_methods(sdk_cliend):
    """ Извлечь все методы из самого API """
    command = {'get_methods': None}
    sdk_cliend.send_data(command)
    response = sdk_cliend.get_data()
    return response


def execute_method(sdk_client, general_method, methods_dict, method_name, *args, **kwargs):
    """ Сформировать и отправить запрос """
    method = get_method(general_method, methods_dict, method_name, *args, **kwargs)
    sdk_client.send_data(method)


def get_method(general_method, methods_dict, method_name, *args, **kwargs):
    """ Сделать шаблонный запрос  """
    try:
        method_from_dict = methods_dict[method_name]
    except KeyError:
        return {'status': 'failed', 'info': 'Метод {} не поддерживается в GC_SDK. Что бы получить список поддреживаемых '
                                            'методов выполните get_sdk_methods.'.format(method_name)}
    all_arguments = method_from_dict['kwargs']
    all_arguments.update(kwargs)
    method = {general_method: {method_from_dict['command']: all_arguments}}
    return method
