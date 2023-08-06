class memoize_one(object):
    def __init__(self, func):
        self.func = func
        self.last_args = None
        self.last_kwargs = None

    def __call__(self, *args, **kwargs):
        if (self.last_args != args or self.last_kwargs != kwargs
                or not hasattr(self, 'last_value')):

            self.last_args = args
            self.last_kwargs = kwargs
            self.last_value = self.func(*args, **kwargs)

        return self.last_value


def get_chapter_writer(directory):
    """
    """

    get_current_fd = memoize_one(partial(get_fd, path=directory))
    return partial(writer_base, file_finder_function=get_current_fd)
