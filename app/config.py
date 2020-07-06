#!/usr/bin/env python3
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
base_dir = os.path.dirname(dir_path)

# Input file names
old_table = base_dir + '/input/old_table.sql'
new_table = base_dir + '/input/new_table.sql'

out_file = base_dir + '/output/test.sql'
# Output file names


# SQL Scripts
stored_procedure_txt = '''
CREATE PROCEDURE TST_SCHEMA.{procedure_name} ()
AS
SELECT 1
'''
