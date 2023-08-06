import inspect
import sys
import os


def _clean(it):
    return it.split('#')[0].strip('"\'() ')


def compact(*_, dirty=False, default=None):
    this = inspect.stack()[0][3] + '('

    _frame = inspect.currentframe()
    caller_data = _frame.f_back.f_locals

    # inspect names
    caller_frame = inspect.getouterframes(_frame)[1][0]

    f_info = inspect.getframeinfo(caller_frame)
    _ctx = f_info.code_context
    if not _ctx:
        raise NotImplementedError('compact is not available in the interactive prompt.')
    string = _ctx[0]
    if ')' not in string or '(' not in string:
        # multiline

        _lne = caller_frame.f_lineno

        full_contents = open(f_info.filename).readlines()
        cur = string

        string += full_contents[_lne].strip()

        # which line is _line depends on python version: https://bugs.python.org/issue38283
        if ')' not in string:
            # look forward
            _lne += 1
            while ')' not in cur:
                # look for compact( start
                _lne += 1
                cur = full_contents[_lne].strip()
                string = string + cur
        else:
            # look back
            _lne -= 1
            while this not in cur:
                # look for compact( start
                _lne -= 1
                cur = full_contents[_lne].strip()
                string = cur + string

    string = string.replace('\n', '')

    # get the different arguments
    names = [_clean(s) for s in string[string.find(this) + len(this):-1].split(',') if '=' not in s]

    if dirty:
        # none on missing
        return {f: caller_data.get(f, default) for f in names}
    else:
        # error on missing
        return {f: caller_data[f] for f in names}


def main(d):
    # demo
    a = '1'
    b = '2'
    c = 'b'

    comp = compact(
        'a',
        'b',
        c,
        dirty=True
    )  # oop

    print(comp)


if __name__ == '__main__':
    # demo
    a = 2
    b = 3
    c = 5
    main(d=123)
