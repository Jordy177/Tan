import pandas as pd
import numpy as np

class read_table:
    def __init__(self, filename):
        self._filename = filename

    def _read_internal(self):
        with open(self._filename, 'r') as f:
            data = f.readlines()

        return data

    def read(self):
        txt = ''
        for line in self._read_internal():
            txt += line

        return txt

    def clean(self):
        txt = self.read()
        clean_txt = txt.split('WITH')
        print(clean_txt[0])

    def read_column_names(self):
        raw_table = self.read()

        # Find opening in table
        r = raw_table.find('CREATE TABLE') + 12
        begin = raw_table.find('(', r) + 1

        # Find end in table
        r = raw_table.find('WITH')
        end = raw_table.rfind(')', 0, r)

        t = raw_table[begin:end].replace('\n', '').replace('\t', '').split(',')
        n = []
        for line in t:
            line_dict = {'column_name': line.strip().split(' ')[0], 'column_type': line.strip(
            ).split(' ')[1].upper(), 'null-type': line.strip().split(' ')[2].upper()}
            n.append(line_dict)

        return list(n)


class compare_table(read_table):
    def __init__(self, old_table, new_table):
        self._old_table = old_table
        self._new_table = new_table

    def compare_table(self):
        old_table = read_table(self._old_table).read_column_names()
        new_table = read_table(self._new_table).read_column_names()

        # Change dictionary to dataframe
        df_old = pd.DataFrame.from_dict(old_table).reset_index(drop=True)
        df_new = pd.DataFrame.from_dict(new_table).reset_index(drop=True)
        

        df_remove = pd.merge(df_old, df_new, on=['column_name'], how='left')
        df_remove_filtered = df_remove[df_remove['column_type_y'].isnull()]
        df_add = pd.merge(df_new, df_old, on=['column_name'], how='left')
        df_add_filtered = df_add[df_add['column_type_y'].isnull()]
        df_diff = pd.merge(df_new, df_old, on=['column_name'], how='inner')



        print(df_remove_filtered['column_name'].tolist())

        print(df_add_filtered['column_name'].tolist())

        print(df_diff[['column_name', 'column_type_y', 'null-type_y']].values.tolist())