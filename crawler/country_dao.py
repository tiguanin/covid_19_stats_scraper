from datetime import datetime, timezone, timedelta

import sqlalchemy as db
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

import crawler.config as conf
from models.country import Country

ENGINE = db.create_engine(conf.config['database_url'])
META = db.MetaData(ENGINE)
country_statistics_table = db.Table('country_statistics', META,
                                    db.Column('id', db.BIGINT()),
                                    db.Column('country_id', db.Integer()),
                                    db.Column('total_cases', db.Integer()),
                                    db.Column('new_cases', db.Integer()),
                                    db.Column('total_deaths', db.Integer()),
                                    db.Column('new_deaths', db.Integer()),
                                    db.Column('total_recovered', db.Integer()),
                                    db.Column('active_cases', db.Integer()),
                                    db.Column('serious_critical', db.Integer()),
                                    db.Column('total_cases_1m_pop', db.Float()),
                                    db.Column('create_date', db.TIMESTAMP()),
                                    db.Column('total_deaths_1m_pop', db.Float()),
                                    db.Column('first_case_date', db.VARCHAR(100))
                                    )

countries_table = db.Table('countries', META,
                           db.Column('id', db.BIGINT(), autoincrement=True),
                           db.Column('name', db.VARCHAR('255')),
                           db.Column('create_date', db.TIMESTAMP())
                           )


def create_country_statistics(country_model):
    Session = sessionmaker(bind=ENGINE)
    session = Session()
    session.execute(country_statistics_table.insert().values({
        "country_id": country_model.country_id,
        "total_cases": country_model.total_cases,
        "new_cases": country_model.new_cases,
        "total_deaths": country_model.total_deaths,
        "new_deaths": country_model.new_deaths,
        "total_recovered": country_model.total_recovered,
        "active_cases": country_model.active_cases,
        "serious_critical": country_model.serious_critical,
        "total_cases_1m_pop": country_model.total_cases_1m_pop,
        "create_date": country_model.create_date,
        "total_deaths_1m_pop": country_model.total_deaths_1m_pop,
        "first_case_date": country_model.first_case_date
    }))
    session.commit()


def upsert_country_if_not_exists(country_name, country_model):
    result = get_country_by_name(country_name)
    if is_empty(result):
        create_country_if_not_exits(country_name)
    else:
        result = get_country_by_name(country_name)
        country_model.country_id = result[0].id
        create_country_statistics(country_name)


def create_country_if_not_exits(country_name):
    Session = sessionmaker(bind=ENGINE)
    session = Session()
    session.execute(countries_table.insert().values({
        "name": country_name,
        "create_date": datetime.now(tz=None)
    }))
    session.commit()


def get_country_by_name(country_name):
    sql = text("select * from countries where name = '{}'".format(country_name))
    result = ENGINE.execute(sql)
    return result


def is_empty(result):
    rows = result.fetchall()
    if len(rows) > 0:
        return True
    else:
        return False


def get_country_id_by_country_name(country_name):
    result = get_country_by_name(country_name)
    result = result.fetchall()
    return result[0].id


def get_country_id_by_name(country_name):
    proxy_result = get_country_by_name(country_name)
    result = proxy_result.fetchall()
    if len(result) == 1:
        return result[0].id
        print('Id запрошенной страны: {}'.format(result[0].id))
    elif len(result) > 1:
        raise Exception('Нарушена уникальность данных')
    elif len(result) == 0:
        print("Страна '{}' отсутствует. Производится создание данной страны".format(country_name))
        create_country_if_not_exits(country_name)
        id = get_country_id_by_country_name(country_name)
        return id


def is_country_exists(country_name):
    result = get_country_by_name(country_name)
    res = result.fetchall()
    if len(res):
        return True
    else:
        return False


def dto_to_model(country_dto):
    moscow_current_datetime = _get_moscow_current_datetime
    country_id = get_country_id_by_name(country_dto.country_name)
    country_model = Country(country_id=country_id,
                            total_cases=country_dto.total_cases,
                            new_cases=country_dto.new_cases,
                            total_deaths=country_dto.total_deaths,
                            new_deaths=country_dto.new_deaths,
                            total_recovered=country_dto.total_recovered,
                            active_cases=country_dto.active_cases,
                            serious_critical=country_dto.serious_critical,
                            total_cases_1m_pop=country_dto.total_cases_1m_pop,
                            create_date=moscow_current_datetime(),
                            total_deaths_1m_pop=country_dto.total_deaths_1m_pop,
                            first_case_date=country_dto.first_case_date)
    return country_model


def parse_scrapped_countries_data(countries_dto_list):
    print('Scraped countries count: {}'.format(len(countries_dto_list)))
    for country_dto in countries_dto_list:
        country_model = dto_to_model(country_dto)
        print('Checking on exists county: {}'.format(country_dto.country_name))
        if is_country_exists(country_dto.country_name):
            create_country_statistics(country_model)
            print('Statistics by {} successfully inserted'.format(country_dto.country_name))
        else:
            create_country_if_not_exits(country_dto.country_name)
            # FIXME: получать ключ созданной страны сразу после инсерта выше
            # FIXME: сделать нормальный upsert-метод
            id = get_country_id_by_country_name(country_dto.country_name)
            country_model.country_id = id
            create_country_statistics(country_model)


def _get_moscow_current_datetime():
    utc_current_datetime = datetime.now(timezone.utc)
    return utc_current_datetime + timedelta(hours=3)
