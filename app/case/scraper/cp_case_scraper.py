import requests
from datetime import datetime
from bs4 import BeautifulSoup
from xml.sax.saxutils import unescape

from flask import current_app
from app.case.naivebayes import classifier
from app.models import Cases


class CPCaseScraper(object):

    def scrape_cases_id_via_date(self, component, search_date):
        cases_id_list = []
        search_request = {
            "account_number":   "477931",
            "limit":            "50",
            "newSearch":        "true",
            "partnerSearch":    "false",
            "query":            "%s AND case_status:*" % component,
            "redhat_client":    "Red Hat Customer Portal 1.3.64",
            "sort":             "case_createdDate DESC",
            # "startDate":        "%s" % search_start_date,  # do not work
            # "endDate":          "%s" % search_end_date,  # do not work
            "start":            "0"
        }
        search_start = 0
        search_request['start'] = search_start

        search_min_date = ""
        current_app.logger.info("***search_date: %s***" % search_date)
        max_cases = 300
        while search_start < max_cases:
            r = requests.get(
                url='https://access.redhat.com/rs/cases',
                params=search_request,
                auth=(current_app.config['CP_USER'], current_app.config['CP_PASS'])
            )
            if "\"numFound\":0" in r.content:  # MAYBE better solution
                # Re-get page
                search_request['start'] = search_start
                current_app.logger.info("Re-get page, start by %s..." % search_start)
                continue
            s = BeautifulSoup(r.content, "lxml")
            for case in s.findAll("case"):
                created_date = case.createddate.text[0:10]
                current_app.logger.info("created_date: %s" % created_date)  # eg. 10-05
                if datetime.strptime(created_date, '%Y-%m-%d') >= datetime.strptime(search_date, '%Y-%m-%d'):  # eg. 10-05 == 10-05
                    case_id = case.attrs["casenumber"]
                    if Cases.query.filter_by(case_id=case_id, component=component).first() is None:
                        if search_min_date == "" or datetime.strptime(search_min_date, '%Y-%m-%d') >= datetime.strptime(created_date, '%Y-%m-%d'):  # eg. 10-06 >= 10-05
                            search_min_date = created_date  # eg. 10-05
                            cases_id_list.append(case_id)
                    else:
                        current_app.logger.info("case %s already in database..." % case_id)
                else:
                    # need to check whether case missed
                    current_app.logger.info("***%s cases found...***" % len(cases_id_list))
                    return cases_id_list, search_min_date
#             # Next page
            search_start += int(search_request['limit'])
            search_request['start'] = search_start
            current_app.logger.info("search next page, start by %s..." % search_start)

        current_app.logger.info("***more than %s cases found, just return max...***" % max_cases)
        return cases_id_list, search_min_date

    def scrape_case_messages(self, case_id):
        messages = []
        case_url = 'https://access.redhat.com/rs/cases/%s' % case_id
        r = requests.get(
            url=case_url,
            params={"account_number":"477931", "redhat_client":"Red Hat Customer Portal 1.3.34"},
            auth=(current_app.config['CP_USER'], current_app.config['CP_PASS'])
        )
        s = BeautifulSoup(r.content, "lxml")
        description = s.findAll("description")
        for message in s.findAll("text"):
            messages.append(message)
        messages.append(description)
        messages.reverse()
        return unescape(str(messages).replace("\\n", "<br>"))

    def scrape_case_dict(self, component, case_number):
        case_dict = {}
        messages = []
        case_url = 'https://access.redhat.com/rs/cases/%s' % case_number
        r = requests.get(
            url=case_url,
            params={"account_number":"477931", "redhat_client":"Red Hat Customer Portal 1.3.34"},
            auth=(current_app.config['CP_USER'], current_app.config['CP_PASS']),
        )
        s = BeautifulSoup(r.content, "lxml")
        description = s.findAll("description")
        for message in s.findAll("text"):
            messages.append(message)
        messages.append(description)
        messages.reverse()
        messages_string = unescape(str(messages).replace("\\n", "<br>"))

        case_dict["case_id"] = case_number
        case_dict["case_date"] = s.createddate.text[0:10]
        case_dict["summary"] = s.summary.text
        case_dict["status"] = s.status.text
        # case_dict["predict"] = 1
        case_dict["predict"] = classifier.classify(component, messages_string)
        return case_dict
