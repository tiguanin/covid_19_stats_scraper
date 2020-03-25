import json

with open("config.json", 'r') as f:
    config = json.load(f)


def get_data_from_cells(index, text, country):
    text = _text_preprocessing(index, text)
    print('INDEX: {}, TEXT: {}'.format(index, text))

    if index == 0:
        country.country_name = text
    elif index == 1:
        country.total_cases = text
    elif index == 2:
        country.new_cases = text
    elif index == 3:
        country.total_deaths = text
    elif index == 4:
        country.new_deaths = text
    elif index == 5:
        country.total_recovered = text
    elif index == 6:
        country.active_cases = text
    elif index == 7:
        country.serious_critical = text
    elif index == 8:
        country.total_cases_1m_pop = text
    elif index == 9:
        country.total_deaths_1m_pop = text


def _text_preprocessing(index, text):
    result = text.lstrip()
    result = result.replace('+', '')
    if index == 8 or index == 9:
        result = result.replace(',', '.')
    else:
        result = result.replace('.', '')
        result = result.replace(',', '')
    if result == '':
        result = None
    return result
