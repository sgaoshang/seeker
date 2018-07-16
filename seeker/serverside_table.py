import re
from seeker.logger import logger
from seeker.db import get_db


class serverside_table(object):

    def __init__(self, request):
        self.table_data = None
        self.db = get_db()
        self.cardinality = self.db.execute("select count(*) from cases").fetchone()[0]
        logger.debug("cardinality: %s" % self.cardinality)
        self.request_values = request.values
        self.table_data = self._pagination()

    def _pagination(self):
        start = int(self.request_values['iDisplayStart'])
        length = int(self.request_values['iDisplayLength'])
        if self.cardinality <= length:
            # display only one page
            limit_start = 0
            length = self.cardinality
        else:
            limit_start = start
            limit_end = start + length
            if limit_end >= self.cardinality:
                # display last page
                length = self.cardinality - start
        # logger.debug("limit: %s, %s" % (limit_start, limit_end))
        db = get_db()
        search_case_sql = 'SELECT case_id, predict, validate, case_date, case_cover, bug_cover, author_id, username FROM cases c JOIN user u ON c.author_id = u.id ORDER BY case_date DESC limit %s offset %s' % (length, limit_start)
        logger.debug("search_case_sql: %s" % search_case_sql)
        cases_row = []
        for row in db.execute(search_case_sql).fetchall():
            cases_row.append(list(row))
        return cases_row

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
