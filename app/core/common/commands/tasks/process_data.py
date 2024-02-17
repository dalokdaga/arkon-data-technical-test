import re
from paver.easy import task, cmdopts
from app.core.common.commands.console.process_data_command import ProcessDataConsole
from app.core.exceptions import PaverCommandException
from config.logging import setup_logging

logger = setup_logging()


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
                ProcessDataConsole.process_data(file_date)
                print(f'{file_date} done!')
            else:
                raise PaverCommandException("Invalid 'file_date' format. Please use YYYY-MM-DD.")
        else:
            raise PaverCommandException("Missing 'file_date' argument.")
        logger.info(f"Paver - Message: {file_date} done!")
    except Exception as e:
        logger.error(f"Paver - Message: {e}")
        print(e)        
