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
                f.write("--{table_name}\nIF EXISTS (SELECT 1 FROM sys.columns c WHERE c.name = '{column}' AND c.OBJECT_ID = OBJECT_ID('{table_name}', 'U'))\nBEGIN\n\tALTER TABLE {table_name} DROP COLUMN [{column}] \nEND\n".format(
                    table_name=table_name, column=column))
            f.write('\n')

            f.write('--Added columns\n')
            for column, type, null_type in self._column_list['add']:
                f.write("--{table_name}\nIF (OBJECT_ID('{table_name}', 'U') IS NOT NULL) AND NOT EXISTS (SELECT 1 FROM sys.columns c WHERE c.name = '{column}' AND c.OBJECT_ID = OBJECT_ID('{table_name}', 'U'))\nBEGIN\n\tALTER TABLE {table_name} ADD {column} {type} {null_type} \nEND\n".format(
                    table_name=table_name, column=column, type=type, null_type=null_type))
            f.write('\n')

            f.write('--Changed columns\n')
            try:
                for column, type, null_type in self._column_list['alter']:
                    f.write('ALTER TABLE {table_name} ALTER COLUMN {column} {type} {null_type} \n'.format(
                        table_name=table_name, column=column, type=type, null_type=null_type))
                    f.write('\n')
            except: 
                print('No ALTER COLUMN changes found')

            
