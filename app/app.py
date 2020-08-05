from table_operations import read_table as rt
from table_operations import compare_table as ct
from output_operations import create_output as co
import config as conf

old = rt(conf.old_table)
old.get_table_name()

compare = ct(conf.old_table, conf.new_table)

output = co(compare.compare_table())

output.alter_table_script(compare.get_table_name())

print('ALTER TABLE Script successfully created!')