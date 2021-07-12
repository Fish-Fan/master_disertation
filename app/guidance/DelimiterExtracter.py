from collections import defaultdict
import pandas as pd
import re
from collections import OrderedDict
from difflib import SequenceMatcher

class DelimiterExtracter:
    def __init__(self, strList):
        self.strList = strList

    def _id_to_regex_(self, id):
        x = re.escape(id)
        x = re.sub(r'([^a-zA-Z0-9]+[~+!@#$%^&*./-]*[\s]*)', r'(\1)', x)
        x = re.sub(r'[a-zA-Z]+', r'([A-Z)]+)', x)
        x = re.sub(r'[0-9]+', r'([0-9]+)', x)
        return '^' + x + '$'

    def _determineRegex_(self, identifiers):
        patterns = defaultdict(set)
        for id in identifiers:
            pattern = self._id_to_regex_(id)
            patterns[pattern].add(id)

        return patterns

    def _determineDelimiter_(self, counters):
        regList = counters.keys()
        delimiterSet = []

        for s in regList:
            s = re.sub(r'\\', '', s)
            arr = re.findall(r'[(]{1}([~+!@#$%^&*./-]{1}|[\s]+)[)]{1}', s)
            for delimiter in arr:
                delimiterSet.append(delimiter)
        return set(delimiterSet)

    def extractDelimiterSet(self):
        counters = self._determineRegex_(self.strList)
        delimiterSet = self._determineDelimiter_(counters)
        return delimiterSet

    def extractBestDelimiter(self):
        delimiterSet = self.extractDelimiterSet()
        score_dict = {}
        for delimiter in delimiterSet:
            score_arr = []
            for row in self.strList:
                split_arr = row.split(delimiter)
                ratio_arr = []
                for i in range(len(split_arr) - 1):
                    r1, r2 = self._id_to_regex_(split_arr[i]), self._id_to_regex_(split_arr[i + 1])
                    ratio_arr.append(self._similiar_(r1, r2))
                if ratio_arr:
                    score_arr.append(sum(ratio_arr) / len(ratio_arr))
                else:
                    score_arr.append(1.0)
            meanScore = pd.Series(score_arr).mean()
            score_dict[delimiter] = meanScore
        d = OrderedDict(sorted(score_dict.items(), key=lambda t: t[1], reverse=True))
        ans = {}
        for key, value in d.items():
            ans['delimiter'] = key
            ans['score'] = value
            break
        return ans

    def _similiar_(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

if __name__ == '__main__':
    email_samples = ["atomkiewicz@hotmail.com",
               "evan.zigomalas@gmail.com",
               "france.andrade@hotmail.com",
               "ulysses@hotmail.com",
               "tyisha.veness@hotmail.com",
               "erampy@rampy.co.uk",
               "marg@hotmail.com",
               "laquita@yahoo.com",
               "lura@hotmail.com",
               "yuette.klapec@klapec.co.uk",
               "fernanda@writer.co.uk",
               "charlesetta_erm@gmail.com",
               "corrinne_jaret@gmail.com",
               "niesha.bruch@yahoo.com",
               "rueben_gastellum@gastellum.co.uk",
               "mthrossell@throssell.co.uk"]

    phone_samples = ["01944-369967",
                    "01937-864715",
                    "01347-368222",
                    "01912-771311,01302-601380",
                    "01547-429341",
                    "01969-886290,01545-817375",
                    "01865-582516",
                    "01746-394243",
                    "01907-538509",
                    "01903-649460",
                    "01630-202053",
                    "01276-816806",
                    "01625-932209",
                    "01874-856950,01342-793603"]

    name_samples = ["Aleshia Tomkiewicz",
                    "Evan Zigomalas",
                    "France Andrade",
                    "Tyisha Veness",
                    "Eric Rampy",
                    "Marg Grasmick",
                    "Laquita Hisaw",
                    "Lura Manzella",
                    "Yuette Klapec"]


    date_samples = ["1997/12/13",
                    "1998/12/11",
                    "2009/10/09",
                    "2008/09/01",
                    "2020/01/02"]


    de = DelimiterExtracter(date_samples)
    delimiterSet = de.extractDelimiter()
    print(delimiterSet)