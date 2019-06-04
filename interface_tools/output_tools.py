def show_weak_warning(args):
    print('\033[38;2;255;255;0mWeak warning:\033[38;2;255;255;255m ', end='')
    print(args)


def show_warning(args):
    print('\033[38;2;255;127;0m     Warning:\033[38;2;255;255;255m ', end='')
    print(args)


def show_error(args):
    print('\033[38;2;255;0;0m       Error:\033[38;2;255;255;255m ', end='')
    print(args)