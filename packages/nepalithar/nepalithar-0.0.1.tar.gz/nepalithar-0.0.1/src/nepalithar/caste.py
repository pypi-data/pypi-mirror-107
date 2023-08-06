from nepalithar.helper import *
import random

class Caste(CASTE_HELPER):
    def is_true(self, str):
        if str:
            str = self._str_process(str)
            if str.upper() in self.GET_CASTE_LIST():
                return True
            else:
                return False
        return False

    def detect(self, str_l):
        index = []
        str = self._change_to_list(str_l)
        for word in str:
            if word.upper() in self.GET_CASTE_LIST():
                if (str.index(word), word) in index:
                    index.append((str.index(word, str.index(word) + 1), word))
                else:
                    index.append((str.index(word), word))
        return index

    def get(self, n=1):
        return self._list_to_title(random.sample(self.GET_CASTE_LIST(), n))

    def get_position(self, str_l):
        caste_in = self.detect(str_l)
        caste_in_list = []
        for position, _ in caste_in:
            caste_in_list.append(position)
        return caste_in_list

    def split_name(self, str_name):
        name_bucket = []
        str_name = self._str_process(str_name)
        raw_name = self._change_to_list(str_name)
        caste_index = self.get_position(str_name)
        total_caste_found = self._get_list_len(caste_index)

        if total_caste_found <= 1:
            name_bucket.append(str_name)
        elif (total_caste_found > 1):
            previous = 0
            for _, index in enumerate(caste_index):
                if index + 1 < len(raw_name) and self.is_true(raw_name[index]) and self.is_true(raw_name[index + 1]):
                    pass
                else:
                    name_bucket.append(self._list_to_str(raw_name[0 if len(name_bucket) == 0 else previous + 1:index + 1]))
                    previous = index
        return (self._list_to_title(name_bucket))

