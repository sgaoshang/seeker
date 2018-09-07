import requests, json, datetime
from bs4 import BeautifulSoup
from seeker.logger import logger
from seeker.naivebayes import classifier

# python2
# import HTMLParser
# python3
# from html.parser import HTMLParser
# python3.4
# import html
# sax module
from xml.sax.saxutils import unescape


class CPCaseScraper(object):

    def scrape_cases(self, max_pages=1):
        cases = []
        # https://access.redhat.com/rs/cases?redhat_client=Red Hat Customer Portal 1.3.34&
        # account_number=477931&query=virt\-who AND case_status:Closed*&sort=case_createdDate DESC&start=0&limit=50&newSearch=true&partnerSearch=false
        # https://access.redhat.com/rs/cases?redhat_client=Red Hat Customer Portal 1.3.34&
        # account_number=477931&query=virt\-who AND case_status:*&sort=case_lastModifiedDate DESC&start=0&limit=50&newSearch=true&partnerSearch=false

        # <case casenumber="02143542">
        # <createdby>Gnoc Team</createdby>
        # <createddate>2018-07-18T08:41:52Z</createddate>
        # <lastmodifiedby>GNOC TEAM</lastmodifiedby>
        # <lastmodifieddate>2018-07-19T04:56:28Z</lastmodifieddate>
        # <id>500A000000bTarhIAC</id>
        # <uri>https://api.access.redhat.com/rs/cases/02143542</uri>
        # <summary>Cann't able to register any Virtual machine into satellite</summary>
        # <status>Closed</status>
        # <product>Red Hat Satellite or Proxy</product>
        # <version>6.2</version>
        # <accountnumber>5632860</accountnumber>
        # <contactname>Gnoc Team</contactname>
        # <owner>Prajeesh Kunnumbreth</owner>
        # <severity>3 (Normal)</severity>
        # <lastpublicupdateat>2018-07-19T04:56:27Z</lastpublicupdateat>
        # <lastpublicupdateby>GNOC TEAM</lastpublicupdateby>
        # </case>

        search_request = {
            "account_number":   "477931",
            "limit":            "10",
            "newSearch":        "true",
            "partnerSearch":    "false",
            "query":            "virt\-who AND case_status:Closed",
            "redhat_client":    "Red Hat Customer Portal 1.3.64",
            "sort":             "case_createdDate DESC",
            "start":            "0"
        }
        pageno = 0
        search_request['start'] = pageno

        while pageno < max_pages:
            r = requests.get(
                url='https://access.redhat.com/rs/cases',
                params=search_request,
                auth=self.get_auth(),
            )
            # print r.url
            s = BeautifulSoup(r.content, "lxml")
            # print s.find("totalcount").string
            for case in s.findAll("case"):
                # https://access.redhat.com/support/cases/#/case/00037785\
                case_dict = {}
                case_dict["casenumber"] = case.attrs["casenumber"]
                case_dict["createddate"] = case.createddate.text
                case_dict["lastmodifieddate"] = case.createddate.text
                case_dict["summary"] = case.summary.text
                case_dict["status"] = case.status.text
                cases.append(case_dict)
            # Next page
            pageno += 1
            search_request['start'] = pageno
        return cases

    def scrape_cases_id_via_date(self, search_date="2018-08-21"):
        cases_id_list = []
        search_request = {
            "account_number":   "477931",
            "limit":            "50",
            "newSearch":        "true",
            "partnerSearch":    "false",
            "query":            "virt\-who AND case_status:*",
            "redhat_client":    "Red Hat Customer Portal 1.3.64",
            "sort":             "case_createdDate DESC",
            "start":            "0"
        }
        search_start = 0
        search_request['start'] = search_start

        while search_start < 100000:
            r = requests.get(
                url='https://access.redhat.com/rs/cases',
                params=search_request,
                auth=self.get_auth(),
            )
            s = BeautifulSoup(r.content, "lxml")
            for case in s.findAll("case"):
                created_date = case.createddate.text[0:10]
                if datetime.datetime.strptime(created_date, '%Y-%m-%d') > datetime.datetime.strptime(search_date, '%Y-%m-%d'):
                    case_id = case.attrs["casenumber"]
                    logger.debug("scraped case: %s" % case_id)
                    cases_id_list.append(case_id)
                else:
                    logger.debug("exceeded date limit")
                    # need to check whether case missed
                    return cases_id_list
            # Next page
            search_start += int(search_request['limit'])
            search_request['start'] = search_start

        min_date = ""
        for case in cases_id_list:
            if self.db.execute('SELECT * FROM cases WHERE case_id="%s"' % (case["case_id"])).fetchone() is not None:
                logger.debug("case already exist: %s" % case)
                cases_id_list.remove(case)
            else:
                if min_date == "" or datetime.datetime.strptime(min_date, '%Y-%m-%d') > datetime.datetime.strptime(case["case_date"], '%Y-%m-%d'):
                    min_date = case["case_date"]
        if datetime.datetime.strptime(min_date, '%Y-%m-%d') > datetime.datetime.strptime(search_date, '%Y-%m-%d'):
            logger.debug("update search date to: %s" % min_date)
            # update_search_date("2018-08-20")
        return cases_id_list

    def scrape_cases_via_date(self, date_limit="2018-08-21"):
        cases_list = []
        search_request = {
            "account_number":   "477931",
            "limit":            "50",
            "newSearch":        "true",
            "partnerSearch":    "false",
            "query":            "virt\-who AND case_status:*",
            "redhat_client":    "Red Hat Customer Portal 1.3.64",
            "sort":             "case_createdDate DESC",
            "start":            "0"
        }
        search_start = 0
        search_request['start'] = search_start

        while search_start < 100000:
            r = requests.get(
                url='https://access.redhat.com/rs/cases',
                params=search_request,
                auth=self.get_auth(),
            )
            # print r.url
            s = BeautifulSoup(r.content, "lxml")
            # print s.find("totalcount").string
            for case in s.findAll("case"):
                case_dict = {}
                created_date = case.createddate.text[0:10]
                # logger.debug(created_date)
                if datetime.datetime.strptime(created_date, '%Y-%m-%d') > datetime.datetime.strptime(date_limit, '%Y-%m-%d'):
                    # logger.debug("no exceeded date limit")
                    case_dict["case_date"] = created_date
                else:
                    logger.debug("exceeded date limit")
                    # need to check whether case missed
                    return cases_list
                case_id = case.attrs["casenumber"]
                case_dict["case_id"] = case_id
                # case_dict["lastmodifieddate"] = case.createddate.text
                # case_dict["summary"] = case.summary.text
                case_dict["status"] = case.status.text
#                 case_dict["predict"] = 1
                logger.debug("classify case: %s" % case_id)
                case_dict["predict"] = classifier.classify(self.scrape_case_messages(case_id))
                cases_list.append(case_dict)
            # Next page
            search_start += int(search_request['limit'])
            search_request['start'] = search_start
        return cases_list

    def scrape_cases_via_period(self, date_start="2018-08-01", date_end="2018-09-01"):
        cases_list = []
        search_request = {
            "account_number":   "477931",
            "limit":            "50",
            "newSearch":        "true",
            "partnerSearch":    "false",
            "query":            "virt\-who AND case_status:*",
            "redhat_client":    "Red Hat Customer Portal 1.3.64",
            "sort":             "case_createdDate DESC",
            "start":            "0"
        }
        search_start = 0
        search_request['start'] = search_start

        while search_start < 100000:
            r = requests.get(
                url='https://access.redhat.com/rs/cases',
                params=search_request,
                auth=self.get_auth(),
            )
            s = BeautifulSoup(r.content, "lxml")
            for case in s.findAll("case"):
                case_dict = {}
                created_date = case.createddate.text[0:10]
                logger.debug(created_date)
                if datetime.datetime.strptime(created_date, '%Y-%m-%d') > datetime.datetime.strptime(date_end, '%Y-%m-%d'):
                    logger.debug("new than date_end, do nothing...")
                    continue
                if datetime.datetime.strptime(date_start, '%Y-%m-%d') > datetime.datetime.strptime(created_date, '%Y-%m-%d'):
                    logger.debug("old than date_start, stop...")
                    return cases_list
                logger.debug("add case ...")
                # need to check whether case missed
                case_dict["case_date"] = created_date
                case_id = case.attrs["casenumber"]
                case_dict["case_id"] = case_id
                # case_dict["lastmodifieddate"] = case.createddate.text
                # case_dict["summary"] = case.summary.text
                case_dict["status"] = case.status.text
                case_dict["predict"] = 1
                logger.debug("classify case: %s" % case_id)
#                 case_dict["predict"] = classifier.classify(self.scrape_case_messages(case_id))
                cases_list.append(case_dict)
            # Next page
            search_start += int(search_request['limit'])
            search_request['start'] = search_start
        return cases_list

    def scrape_case_messages(self, case_number):
        messages = []
        # https://access.redhat.com/rs/cases/00037785?redhat_client=Red Hat Customer Portal 1.3.34&account_number=477931
        case_url = 'https://access.redhat.com/rs/cases/%s' % case_number
        r = requests.get(
            url=case_url,
            # url='https://access.redhat.com/rs/cases/%s' % case_number,
            params={"account_number":"477931", "redhat_client":"Red Hat Customer Portal 1.3.34"},
            auth=self.get_auth(),
        )
        s = BeautifulSoup(r.content, "lxml")
        description = s.findAll("description")
        for message in s.findAll("text"):
            messages.append(message)
        messages.append(description)
        messages.reverse()
        # logger.debug(len(messages))
        return unescape(str(messages).replace("\\n", "<br>"))

    def scrape_case_dict(self, case_number):
        case_dict = {}
        messages = []
        case_url = 'https://access.redhat.com/rs/cases/%s' % case_number
        r = requests.get(
            url=case_url,
            params={"account_number":"477931", "redhat_client":"Red Hat Customer Portal 1.3.34"},
            auth=self.get_auth(),
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
        logger.debug("classify case: %s" % case_number)
        #case_dict["predict"] = 1
        case_dict["predict"] = classifier.classify(messages_string)
        return case_dict

    def scrape_his_data(self):
        valid_cases = []
        invalid_cases = []
        handler = open("history.xml").read()
        # handler = open("test.xml").read()
        s = BeautifulSoup(handler, "lxml")
        for case in s.findAll("case"):
            if case.qe_valid.text == "Yes":
                valid_cases.append(case.attrs["casenumber"])
            elif case.qe_valid.text == "N/A":
                invalid_cases.append(case.attrs["casenumber"])
        print "Valide case: %s" % len(valid_cases)
        print "Invalide case: %s" % len(invalid_cases)
#         for case in valid_cases:
#             file_content = self.scrape_case_messages(case)
#             file_path = "../bayesian/file_train/pos/%s.txt" % case
#             self.write_file(file_path, file_content)
#         for case in invalid_cases:
#             file_content = self.scrape_case_messages(case)
#             file_path = "../bayesian/file_train/neg/%s.txt" % case
#             self.write_file(file_path, file_content)

        file_path = "../naivebayes/virtwho/virtwho_sample.txt"
        for case in valid_cases[0:50]:
            message = "spam" + "\t" + self.scrape_case_messages(case) + "\n"
            self.write_file(file_path, message)
        for case in invalid_cases[0:50]:
            message = "ham" + "\t" + self.scrape_case_messages(case) + "\n"
            self.write_file(file_path, message)

#         file_path = "../naivebayes/virtwho/virtwho_test.txt"
#         for case in valid_cases[300:350]:
#             message = "spam" + "\t" + self.scrape_case_messages(case) + "\n"
#             self.write_file(file_path, message)
#         for case in invalid_cases[300:350]:
#             message = "ham" + "\t" + self.scrape_case_messages(case) + "\n"
#             self.write_file(file_path, message)

        # print case.attrs["casenumber"]
        # print case.qe_valid
        # print case.qe_cases
        # print case.bugzilla

    def get_auth(self):
        with open("seeker/scraper/auth.json", 'r') as f:
#         with open("auth.json", 'r') as f:
            auth = json.load(f)
        return tuple(auth)

    def write_file(self, file_path, file_content):
        with open(file_path, 'a') as f:
            f.write(file_content)
            f.close()


if __name__ == '__main__':
    scraper = CPCaseScraper()
#     print scraper.scrape_cases_via_date()
#     scraper.scrape_cases_via_period()
    print scraper.scrape_case_dict("01322510")
#     for item in scraper.scrape_case_messages("dd"):
#         print item
#     import time
#     start = time.time()
#     scraper.scrape_his_data()
#     end = time.time()
#     print end - start
# Valide case: 631
# Invalide case: 589
# 300X2 case: 1348.37533808
# 50X2 case: 211.432296038
