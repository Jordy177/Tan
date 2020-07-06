import config as conf


class create_output:
    def __init__(self, column_list: dict):
        self._column_list = column_list

    def print_proc(self):
        print(conf.stored_procedure_txt.format(procedure_name='tst'))

    def alter_table_script(self, table_name):
        with open(conf.out_file, 'w') as f:

            f.write('--Dropped columns\n')
            for column in self._column_list['drop']:
                f.write('ALTER TABLE {table_name} DROP COLUMN {column} \n'.format(
                    table_name=table_name, column=column))
            f.write('\n')

            f.write('--Added columns\n')
            for column, type, null_type in self._column_list['add']:
                f.write('ALTER TABLE {table_name} ADD COLUMN {column} {type} {null_type} \n'.format(
                    table_name=table_name, column=column, type=type, null_type=null_type))
            f.write('\n')

            f.write('--Added columns\n')
            for column, type, null_type in self._column_list['alter']:
                f.write('ALTER TABLE {table_name} ALTER COLUMN {column} {type} {null_type} \n'.format(
                    table_name=table_name, column=column, type=type, null_type=null_type))
            f.write('\n')
