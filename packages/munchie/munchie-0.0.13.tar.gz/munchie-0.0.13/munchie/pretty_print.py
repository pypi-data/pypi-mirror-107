# import libraries
from rich import box
from rich.console import Console
from rich.progress import BarColumn, Progress, TextColumn, TimeElapsedColumn, TimeRemainingColumn
from rich.table import Table


CONSOLE = Console()


def console_log(message_text: str, message_type: str = 'success') -> None:
    '''
    Print a message to the screen in pretty colors.

    Args:
        message_text (str): message to print

    Optional Args:
        message_type (str): log level of the message; defaults to success (green)
    '''

    message_color = {
        'success': 'green',
        'warning': 'yellow',
        'informational': 'blue',
        'error': 'red',
    }.get(message_type, message_type)

    CONSOLE.print(message_text, style=f'bold {message_color}')


def task_processing(task_name: str) -> object:
    '''
    Display spinner wheel while processing a task.

    Args:
        task_name (str): text to display while processing

    Returns:
        status (object): status object with a spinner while processing
    '''

    return CONSOLE.status(f'[bold blue]{task_name}')


def task_progress_bar() -> 'Progress':
    '''
    Display progress bar while processing a task.

    Returns:
        progress_bar (class): instantiated progress bar object
    '''

    progress_bar = Progress(
        '[progress.descripion]{task.description}',
        BarColumn(),
        '[progress.percentage]{task.percentage:>3.0f}%',
        TextColumn('[progress.percentage]{task.completed}/{task.total}'),
        TimeRemainingColumn(),
        TimeElapsedColumn()
    )

    return progress_bar


def add_table_columns(table: 'Table', headers: list) -> None:
    '''
    Add columns to the Table object.

    Args:
        table (class): instantiated Table object
        headers (list): list of header fields
    '''

    for header in headers:
        table.add_column(header.replace('_', ' ').title(), justify='left')


# add rows to output table
def add_table_rows(table: 'Table', data: tuple) -> None:
    '''
    Add rows to the Table object.

    Args:
        table (class): instantiated Table object
        data (tuple): single data record
    '''

    table.add_row(*data)


def print_table(contents: list, headers: list, total_count: int) -> None:
    '''
    Format output into Table object and print results to console.

    Args:
        contents (list): list of contents to print to the Table
        headers (list): list of header fields
        total_count (int): count of table results
    '''

    table = Table(show_header=True, header_style='bold magenta', box=box.HORIZONTALS)
    add_table_columns(table, headers)

    for content in contents:
        add_table_rows(table, content)

    CONSOLE.print(table)
    console_log(f'Total count: {total_count}', 'success')
