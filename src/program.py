from table_operations import read_table as rt
from table_operations import compare_table as ct
import config as conf

compare = ct(conf.old_table, conf.new_table)

compare.compare_table()