import os


def redirect(file, fd, open_mode):
    new_fd = os.open(file, open_mode)
    os.dup2(new_fd, fd)
    os.close(new_fd)


def redirect_input(file, fd):
    redirect(file, fd, os.O_RDONLY)


def redirect_output(file, fd, start_time):
    if os.path.isfile(file):
        mtime = os.path.getmtime(file)
        if mtime < start_time:
            # Old stale version; truncate.
            redirect(file, fd, os.O_WRONLY | os.O_TRUNC | os.O_CREAT)
        else:
            # A new invocation of the same job instance; append putput
            redirect(file, fd, os.O_APPEND)
    else:
        redirect(file, fd, os.O_WRONLY | os.O_TRUNC | os.O_CREAT)


def cond_unlink(file):
    if os.path.exists(file):
        os.unlink(file)


def assert_file_executable(fname):
    """The function raises an IOError if the given file is either not a file or
    not an executable.

    If the given file name is an absolute path, its functionality is straight
    forward. When given a relative path it will look for the given file in the
    current directory as well as all locations specified by the environment
    path.

    """
    if not fname:
        raise IOError('No executable provided!')
    fname = os.path.expanduser(fname)

    potential_executables = [os.path.abspath(fname)]
    if not os.path.isabs(fname):
        potential_executables = (potential_executables +
                                 [
                                     os.path.join(location, fname)
                                     for location in os.environ["PATH"]
                                            .split(os.pathsep)
                                 ])

    if not any(map(os.path.isfile, potential_executables)):
        raise IOError("{} is not a file!".format(fname))

    if not any([os.access(fn, os.X_OK) for fn in potential_executables]):
        raise IOError("%s is not an executable!" % fname)
