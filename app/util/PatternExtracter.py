import re
from collections import defaultdict
from app.util.ConfigparserHelper import ConfigparserHelper
from app.util.ElaspeDecorator import elapse_decorator
import multiprocessing as mp

class PatternExtracter:
    def __init__(self, strList):
        self.strList = strList
    def str_to_regex(self, id):
        x = re.escape(id)
        ch = ConfigparserHelper()
        delimiter = ch.getValue('regx', 'delimiter')
        # replace delimiter with (delimiter)
        x = re.sub(r'([^a-zA-Z0-9]+['+ delimiter +']*[\s]*)', r'(\1)', x)
        # replace words with [a-zA-Z]+
        x = re.sub(r'[a-zA-Z]+', r'([A-Z]+)', x)
        # replace digits with [0-9]+
        x = re.sub(r'[0-9]+', r'([0-9]+)', x)
        return '^' + x + '$'
    @elapse_decorator
    def determineRegex(self):
        global patterns_global
        patterns_global = defaultdict(list)
        PROCESSOR_COUNT = mp.cpu_count() // 2
        pool = mp.Pool(PROCESSOR_COUNT)

        for i in range(PROCESSOR_COUNT):
            data_shard = self.sharding_data(i, len(self.strList) // PROCESSOR_COUNT)
            pool.apply_async(self.single_process_task, args=(data_shard, ), callback=self.multi_process_call_back)

        pool.close()
        pool.join()

        return patterns_global

    def single_process_task(self, data_shard):
        patterns = defaultdict(list)
        for id in data_shard:
            pattern = self.str_to_regex(id)
            patterns[pattern].append(id)
        return patterns

    def multi_process_call_back(self, result):
        global patterns_global
        for key in result.keys():
            patterns_global[key].extend(result.get(key))

    def sharding_data(self, i, size):
        if (i+1) * size > len(self.strList):
            return self.strList[i*size:]
        else:
            return self.strList[i*size:(i+1)*size]
