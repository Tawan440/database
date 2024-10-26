@dataclass
class Commands:
    start = '/start'
    help = '/help'
    beginning = '/beginning'
    bookmarks = '/bookmarks'
    continu = '/continu'
def get_menu_args() -> list[dict]:
    _commands = Commands()
    return [
        {'command': _commands.beginning, 'description': 'to da brgin'},
        {'command': _commands.contin, 'description': 'reading'},
        {'command': _commands.bookmarks, 'description': 'my bookmark'},
        {'command': _commands.help, 'description': 'see ho bot do'},
    ]