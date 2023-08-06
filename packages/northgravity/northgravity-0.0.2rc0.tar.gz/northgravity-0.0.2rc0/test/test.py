import northgravity_python_sdk.northgravity as ng
import logging; log=logging.getLogger()
import time
import pandas as pd
import io

#--------------
import northgravity as ng

# Instantiate the Datalake Handler
dh = ng.DatalakeHandler()

# read file from data lake by its ID
# it returns a BytesIO object
fileIO = dh.download_by_id(file_id='b343048a-dafc-4cf1-9cb4-0bded0766b5c',
                            dest_file_name=None,
                            save=False,
                            unzip=False)

# read the object as pandas DataFrame
df = pd.read_csv(fileIO)




#-----------------#
print('-' * 110)
# DatalakeHandler
dh = ng.DatalakeHandler()

# search
print(dh.search_file(file_name='prepared_data.csv', file_type='SOURCE', group_name='Tests_Damien'))
print(dh.search_file(file_name='Concord Copper.csv', file_type=None, group_name='Tests_Damien'))
print(dh.search_file(file_name='prepared_data.csv', file_type='SOURCE', group_name=None))


print(dh.get_info_from_id(file_id='1bcfd8e9-a954-45b4-b5bf-c0755dfb0efd'))

print(dh.download_by_id(file_id='1bcfd8e9-a954-45b4-b5bf-c0755dfb0efd', dest_file_name='test/test.csv', save=True))
print(dh.download_by_id(file_id='1bcfd8e9-a954-45b4-b5bf-c0755dfb0efd', dest_file_name='test/test.csv', save=False))

print(dh.download_by_name(file_name='prepared_data.csv', group_name='Tests_Damien',
                          file_type='SOURCE', dest_file_name='test/test.csv', save=True))
print(dh.download_by_name(file_name='prepared_data.csv', group_name='Tests_Damien',
                          file_type='SOURCE', dest_file_name='test/test.csv', save=False))

print(dh.upload_file(file='test/test.csv', group_name='Tests_Damien', file_upload_name='test_sdk.csv', file_type='SOURCE'))

iodf = io.BytesIO(pd.read_csv('test/test.csv').to_csv(index=False).encode())
print(dh.upload_file(file=iodf, group_name='Tests_Damien', file_upload_name='test_sdk.csv', file_type='SOURCE'))


#-----------------#
# Status Handler
print('-' * 110)
sth = ng.StatusHandler()

sth.info('TEST SDK')
time.sleep(10)

sth.warn('TEST SDK')
time.sleep(10)

sth.error('TEST SDK')
time.sleep(10)
sth.info('TEST SDK')


#----------#
# TaskHandler
print('-' * 110)
sh = ng.TaskHandler()

print(sh.read_task_parameter_value(arg_name='First Dataset'))

print(sh.download_from_input_parameter(arg_name='First Dataset', dest_file_name=None, save=False))
print(sh.download_from_input_parameter(arg_name='First Dataset', dest_file_name=None, save=True))
print(sh.download_from_input_parameter(arg_name='First Dataset', dest_file_name='test/test.csv', save=True))

print(sh.write_task_parameter_value(output_name='Output', value='test'))

print(sh.upload_to_output_parameter(output_name='First Dataset', file='test/test.csv', group_name='Tests_Damien', file_type='SOURCE'))
print(sh.upload_to_output_parameter(output_name='First Dataset', file=iodf, group_name='Tests_Damien', file_upload_name='TEST.csv', file_type='SOURCE'))

#----------#
# Time Series Handler
print('-' * 110)
ts = ng.Timeseries()


symbols = {'Symbol': "CUA"}
columns = 'Open'

ts.retrieve_data_as_csv(file_name='ts_test.csv',
                        symbols=symbols,
                        columns=columns,
                        group_name='Concord History',
                        start_date='2021-01-04',
                        end_date='2021-02-05'
                        )