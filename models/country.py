class Country:

    # def __init__(self):
    #     self.id
    #     self.country_id
    #     self.total_cases
    #     self.new_cases
    #     self.total_deaths
    #     self.new_deaths
    #     self.total_recovered
    #     self.active_cases
    #     self.serious_critical
    #     self.total_cases_1m_pop

    def __init__(self, country_id, total_cases, new_cases, total_deaths, new_deaths,
                 total_recovered, active_cases, serious_critical, total_cases_1m_pop):
        self.country_id = country_id
        self.total_cases = total_cases
        self.new_cases = new_cases
        self.total_deaths = total_deaths
        self.new_deaths = new_deaths
        self.total_recovered = total_recovered
        self.active_cases = active_cases
        self.serious_critical = serious_critical
        self.total_cases_1m_pop = total_cases_1m_pop