import pandas as pd
import numpy as np
from database_operations import Db


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

    def get_table_name(self):
        raw_table = self.read()

        begin = raw_table.find('CREATE TABLE') + 12
        end = raw_table.find('(', begin)

        return raw_table[begin:end].strip()

    def clean(self):
        txt = self.read()
        clean_txt = txt.split('WITH')
        print(clean_txt[0])

    def read_column_names(self, create: bool):
        raw_table = self.read()

        # Find opening in table
        r = raw_table.find('CREATE TABLE') + 12
        begin = raw_table.find('(', r) + 1

        # Find end in table
        r = raw_table.find('WITH')
        end = raw_table.rfind(')', 0, r)

        t = raw_table[begin:end].replace('\n', '').replace('\t', '').split(',')
        u = raw_table[:end+1]

        n = []
        for line in t:
            line_dict = {'column_name': line.strip().split(' ')[0], 'column_type': line.strip(
            ).split(' ')[1].upper(), 'null-type': line.strip().split(' ')[2].upper()}
            n.append(line_dict)

        if create:
            with Db() as d:
                d.create_table(str(u))

        return list(n)


class compare_table(read_table):
    def __init__(self, old_table, new_table):
        self._old_table = old_table
        self._new_table = new_table
        self._table_name = None

    def get_table_name(self):
        return self._table_name

    def compare_table(self):
        obj_old_table = read_table(self._old_table)
        obj_new_table = read_table(self._new_table)

        # Check if table names are equal
        if obj_old_table.get_table_name() == obj_new_table.get_table_name():
            self._table_name = obj_new_table.get_table_name()
        else:
            print('Table names are not the same!')
            exit()
        old_table = obj_old_table.read_column_names(True)
        new_table = obj_new_table.read_column_names(False)

        # Change dictionary to dataframe
        df_old = pd.DataFrame.from_dict(old_table).reset_index(drop=True)
        df_new = pd.DataFrame.from_dict(new_table).reset_index(drop=True)

        df_remove = pd.merge(df_old, df_new, on=['column_name'], how='left')
        df_remove_filtered = df_remove[df_remove['column_type_y'].isnull()]
        df_add = pd.merge(df_new, df_old, on=['column_name'], how='left')
        df_add_filtered = df_add[df_add['column_type_y'].isnull()]
        df_diff = pd.merge(df_new, df_old, on=['column_name'], how='inner')

        output_dict = {'drop': df_remove_filtered['column_name'].tolist(),
                       'add': df_add_filtered[['column_name', 'column_type_x', 'null-type_x']].values.tolist(),
                       'alter': df_diff[['column_name', 'column_type_y', 'null-type_y']].values.tolist()}

        return output_dict