from seeker.logger import logger
from seeker.db import get_db
from seeker.scraper.cp_case_scraper import CPCaseScraper


class serverside_table_scrape(object):

    def __init__(self, request):
        self.table_data = None
        scraper = CPCaseScraper()
        # singleton?
        self.cases_list = scraper.scrape_cases_via_date()
        self.db = get_db()
        self.cardinality = len(self.cases_list)
        # logger.debug("cardinality: %s" % self.cardinality)
        self.request_values = request.values
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
        logger.debug("limit: %s, %s" % (start, start + length))
        return self.cases_list[start:start + length]

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
