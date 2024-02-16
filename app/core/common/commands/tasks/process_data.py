import re
from paver.easy import task, cmdopts
from app.core.common.commands.console.process_data_command import ProcessData
from app.core.exceptions import PaverCommandException

@task
@cmdopts([
    ('file_date=', 's', 'Date of the file to be processed, %Y-%M-%D format')
])
def process_data(options):
    ''' Command to execute the process of adding CDMX wifi information '''
    try:
        if hasattr(options, 'file_date'):
            file_date = options.file_date
            if re.match(r'^\d{4}-\d{2}-\d{2}$', file_date):
                ProcessData.process_data(file_date)
                print(f'{file_date} done!')
            else:
                raise PaverCommandException("Invalid 'file_date' format. Please use YYYY-MM-DD.")
        else:
            raise PaverCommandException("Missing 'file_date' argument.")
    except Exception as e:
        print(e)        
