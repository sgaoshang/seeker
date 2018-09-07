from seeker.logger import logger
from seeker.db import get_db
from seeker.scraper.cp_case_scraper import CPCaseScraper


class newcase_table(object):

    def __init__(self, request, case_id_list):
        self.table_data = None
        self.db = get_db()
        self.scraper = CPCaseScraper()
        self.case_id_list = case_id_list
        self.cardinality = len(self.case_id_list)
        logger.debug("cardinality: %s" % self.cardinality)
        self.request_values = request.values
        # logger.debug("request_values: %s" % self.request_values)
        self.table_data = self._pagination()

    def _pagination(self):
        start = int(self.request_values['iDisplayStart'])
        length = int(self.request_values['iDisplayLength'])
        if self.cardinality <= length:
            # display only one page
            length = self.cardinality
        else:
            end = start + length
            if end >= self.cardinality:
                # display last page
                length = self.cardinality - start
        cases_list = []
        for case_id in self.case_id_list[start:start + length]:
            cases_list.append(self.scraper.scrape_case_dict(case_id))
        return cases_list

    def get_table(self):
        '''
        Generates a dict with the content of the response. It contains the
        required values by DataTables (echo of the reponse and cardinality
        values) and the data that will be displayed.
        '''
        response = {}
        response['sEcho'] = str(int(self.request_values['sEcho']))
        response['iTotalRecords'] = str(self.cardinality)
        response['iTotalDisplayRecords'] = str(self.cardinality)
        response['data'] = self.table_data
        return response

    def get_search_date(self):
        sql_search_date = 'SELECT search_date FROM cases_search_date WHERE component = "virt-who"'
#         search_date = self.db.execute(sql_search_date).fetchone()[0]
        search_date = "2018-08-21"
        logger.debug("search_date: %s" % search_date)
        return search_date

    def update_search_date(self, search_date):
        db = get_db()
        db.execute(
            'UPDATE cases_search_date SET search_date="%s" WHERE component = "virt-who"' % search_date
        )
        db.commit()
