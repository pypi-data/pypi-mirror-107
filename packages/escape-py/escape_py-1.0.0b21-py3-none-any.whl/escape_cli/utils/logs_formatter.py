"""The formatter that will be passed to loguru."""


def format_logs(record):
    """Format loguru records properly."""
    if record['level'].name == 'SUCCESS':
        return """<bold><blue>escape</blue></bold> | <bold><green>{level}</green></bold> | <green>{message}</green>
"""
    if record['level'].name == 'WARNING':
        return """<bold><blue>escape</blue></bold> | <bold><yellow>{level}</yellow></bold> | <yellow>{message}</yellow>
"""
    if record['level'].name == 'ERROR':
        return """<bold><blue>escape</blue></bold> | <bold><red>{level}</red></bold> | <red>{message}</red>
"""
    return (
        '<bold><blue>escape</blue></bold> | <bold><blue>{level}</blue></bold> | {message}\n'
        )
