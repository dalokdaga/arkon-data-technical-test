from paver.easy import task, cmdopts
from app.core.common.commands.console.process_data_command import ProcessData


@task
@cmdopts([
    ('file_date=', 's', 'Date of the file to be processed, %Y-%M-%D format')
])
def process_data(options):
    ''' Command to execute the process of adding CDMX wifi information '''
    try:
        ProcessData.process_data(options.file_date)
        print(f'{options.file_date} done!')
    except Exception as err:
        print(err)
