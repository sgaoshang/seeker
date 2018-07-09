import requests, json
from bs4 import BeautifulSoup


class CPCaseScraper(object):

    def scrape_cases(self, max_pages=1):
        cases = []
        # https://access.redhat.com/rs/cases?redhat_client=Red Hat Customer Portal 1.3.34&
        # account_number=477931&query=virt\-who AND case_status:Closed*&sort=case_createdDate DESC&start=0&limit=50&newSearch=true&partnerSearch=false
        # https://access.redhat.com/rs/cases?redhat_client=Red Hat Customer Portal 1.3.34&
        # account_number=477931&query=virt\-who AND case_status:*&sort=case_lastModifiedDate DESC&start=0&limit=50&newSearch=true&partnerSearch=false
        search_request = {
            "account_number":   "477931",
            "limit":            "10",
            "newSearch":        "true",
            "partnerSearch":    "false",
            "query":            "virt\-who AND case_status:Closed",
            "redhat_client":    "Red Hat Customer Portal 1.3.34",
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
            # print s
            # print s.find("totalcount").string
            for case in s.findAll("case"):
                # https://access.redhat.com/support/cases/#/case/00037785
                cases.append(case.attrs["casenumber"])
            # Next page
            pageno += 1
            search_request['start'] = pageno
        return cases

    def scrape_case_messages(self, case_number):
        messages = []
        # https://access.redhat.com/rs/cases/00037785?redhat_client=Red Hat Customer Portal 1.3.34&account_number=477931
        r = requests.get(
            # url='https://access.redhat.com/rs/cases/00037785',
            url='https://access.redhat.com/rs/cases/%s' % case_number,
            params={"account_number":"477931", "redhat_client":"Red Hat Customer Portal 1.3.34"},
            auth=self.get_auth(),
        )
        s = BeautifulSoup(r.content, "lxml")
        description = s.findAll("description")
        for message in s.findAll("text"):
            messages.append(message)
        messages.append(description)
        messages.reverse()
        return str(messages)

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
        file_path = "../naivebayes/virtwho/virtwho_test.txt"
        for case in valid_cases[0:50]:
            message = "spam" + "\t" + self.scrape_case_messages(case) + "\n"
            self.write_file(file_path, message)
        for case in invalid_cases[0:50]:
            message = "ham" + "\t" + self.scrape_case_messages(case) + "\n"
            self.write_file(file_path, message)

        # print case.attrs["casenumber"]
        # print case.qe_valid
        # print case.qe_cases
        # print case.bugzilla

    def get_auth(self):
        with open("auth.json", 'r') as f:
            auth = json.load(f)
        return tuple(auth)

    def write_file(self, file_path, file_content):
        with open(file_path, 'a') as f:
            f.write(file_content)
            f.close()


if __name__ == '__main__':
    scraper = CPCaseScraper()
#     print scraper.scrape_cases()
#     print scraper.scrape_case_messages("01322510")
#     for item in scraper.scrape_case_messages("dd"):
#         print item
    import time
    start = time.time()
    scraper.scrape_his_data()
    end = time.time()
    print end - start
