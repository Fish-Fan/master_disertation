from collections import defaultdict
import pandas as pd
import re
from collections import OrderedDict
from difflib import SequenceMatcher
from app.util.PatternExtracter import PatternExtracter
from app.util.ConfigparserHelper import ConfigparserHelper
from app.util.ElaspeDecorator import elapse_decorator
import multiprocessing as mp
import numpy as np

class DelimiterExtracter:
    def __init__(self, strList):
        self.strList = strList

    def _determineDelimiter_(self, counters):
        regList = counters.keys()
        delimiterSet = []

        for s in regList:
            s = re.sub(r'\\', '', s)
            ch = ConfigparserHelper()
            d = ch.getValue('regx', 'delimiter')
            arr = re.findall(r'[(]{1}(['+ d +']{1}|[\s]+)[)]{1}', s)
            for delimiter in arr:
                delimiterSet.append(delimiter)
        return set(delimiterSet)

    @elapse_decorator
    def extractDelimiterSet(self):
        pattern_extracter = PatternExtracter(self.strList)
        counters = pattern_extracter.determineRegex()
        delimiterSet = self._determineDelimiter_(counters)
        score_dict = {}
        for delimiter in delimiterSet:
            max_count_split_columns = 0
            score_arr = []
            for row in counters.keys():
                if delimiter == '-':
                    row = re.sub(r'\\-', '^', row)
                    delimiter = '^'
                row = re.sub(r'\\', '', row)
                row = re.sub(r'[()+]', '', row)[1:-1]
                split_arr = row.split(delimiter)
                max_count_split_columns = max(max_count_split_columns, len(split_arr))
                ratio_arr = []
                for i in range(len(split_arr) - 1):
                    r1, r2 = pattern_extracter.str_to_regex(split_arr[i]), pattern_extracter.str_to_regex(
                        split_arr[i + 1])
                    ratio_arr.append(self._similiar_(r1, r2))
                if ratio_arr:
                    score_arr.append(sum(ratio_arr) / len(ratio_arr))
                else:
                    score_arr.append(1.0)
            meanScore = pd.Series(score_arr).mean()
            if delimiter == '^':
                delimiter = '-'
            score_dict[delimiter] = {'max_split_column_count': max_count_split_columns, 'score': meanScore}

            # global score_count_arr
            # score_count_arr = []
            # PROCESS_COUNT = mp.cpu_count() // 2
            # pool = mp.Pool(PROCESS_COUNT)
            #
            # for i in range(PROCESS_COUNT):
            #     data_shard = self.sharding_data(i, len(self.strList) // PROCESS_COUNT)
            #     pool.apply_async(self.single_processor_task, args=(delimiter, pattern_extracter, data_shard), callback=self.multi_process_call_back)
            #
            # pool.close()
            # pool.join()
            #
            #
            # tmpDf = pd.DataFrame(np.array(score_count_arr), columns=['score', 'region_count'])
            # meanScore = tmpDf['score'].mean()
            # max_count_split_columns = tmpDf['region_count'].max()
            # score_dict[delimiter] = {'max_split_column_count': max_count_split_columns, 'score': meanScore}
        d = OrderedDict(sorted(score_dict.items(), key=lambda t: t[1]['score'], reverse=True))
        ans = []
        for key, value in d.items():
            ans_item = {}
            ans_item['delimiter'] = key
            ans_item['score'] = value['score']
            ans_item['max_count'] = value['max_split_column_count']
            ans.append(ans_item)
        ans.sort(key=lambda x: x['score'], reverse=True)
        return ans

    def single_processor_task(self, delimiter, pattern_extracter, counters):
        arr = []
        for row in counters.keys():
            split_arr = row.split(delimiter)
            ratio_arr = []
            for i in range(len(split_arr) - 1):
                r1, r2 = pattern_extracter.str_to_regex(split_arr[i]), pattern_extracter.str_to_regex(split_arr[i + 1])
                ratio_arr.append(self._similiar_(r1, r2))
            if ratio_arr:
                arr.append([sum(ratio_arr) / len(ratio_arr), len(split_arr)])
            else:
                arr.append([1.0, len(split_arr)])
        return arr


    def extractBestDelimiter(self):
        pass

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


    de = DelimiterExtracter(phone_samples)
    delimiterSet = de.extractBestDelimiter()
    print(delimiterSet)


    pe = PatternExtracter(email_samples)
    ans = pe.determineRegex()
    print(ans)
