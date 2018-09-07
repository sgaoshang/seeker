from seeker.logger import logger
from seeker.db import get_db


class hiscase_table(object):

    def __init__(self, request):
        self.table_data = None
        self.db = get_db()
        self.cardinality = self.db.execute("select count(*) from cases").fetchone()[0]
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
        # logger.debug("limit: %s, %s" % (start, end))
        db = get_db()
        search_case_sql = 'SELECT case_id, predict, validate, case_date, case_cover, bug_cover, author_id, username FROM cases c JOIN user u ON c.author_id = u.id ORDER BY case_date DESC limit %s offset %s' % (length, start)
        # logger.debug("search_case_sql: %s" % search_case_sql)
        cases_list = []
        for row in db.execute(search_case_sql).fetchall():
            cases_list.append(dict(row))
        # logger.debug("cases_list: %s" % cases_list)
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
