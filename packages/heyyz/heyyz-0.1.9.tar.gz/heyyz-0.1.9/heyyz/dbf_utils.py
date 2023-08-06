import heyy
import dbfread


def dbf2objs(filename, encoding='gbk', ignore_case=True):
    dbf = dbfread.DBF(filename, encoding)
    objs = [heyy.json2obj(r, ignore_case=ignore_case) for r in dbf.records]
    dbf.unload()
    return objs


def _convert_encoding(s: str, from_encoding: str, to_encoding: str):
    if not isinstance(s, str):
        return s
    try:
        result = s.encode(from_encoding).decode(to_encoding)
    except (UnicodeDecodeError, UnicodeEncodeError):
        result = s
    return result


_FALLBACK_ENCODING = 'latin1'


def try_dbf2objs(filename, encoding='gbk', ignore_case=True):
    try:
        return dbf2objs(filename, encoding, ignore_case)
    except UnicodeDecodeError:
        pass
    latin1_objs = dbf2objs(filename, encoding=_FALLBACK_ENCODING, ignore_case=ignore_case)

    def _convert_obj(obj: heyy.DictObj):
        o = heyy.json2obj(ignore_case=ignore_case)
        for k, v in obj.items():
            k = _convert_encoding(k, _FALLBACK_ENCODING, encoding)
            v = _convert_encoding(v, _FALLBACK_ENCODING, encoding)
            o[k] = v
        return o

    return [_convert_obj(o) for o in latin1_objs]


def str2objs(attrs, string, *, sep='\t', newline='\n', ignore_title_case=False):
    _class = heyy.DictObj if not ignore_title_case else heyy.CaseInsensitiveDictObj
    rows = string.split(newline)
    if not isinstance(attrs, bool):
        def head(): return attrs
    elif attrs:
        title, rows = rows[0].split(sep), rows[1:]
        def head(): return title
    else:
        from itertools import cycle
        def head(): return (f'{v}{i + 1}' for i, v in enumerate(cycle('a')))
    return [_class(zip(head(), s.split(sep))) for s in rows]


def read_fields(dbf_filename, encoding='gbk'):
    dbf = dbfread.DBF(dbf_filename, encoding)
    return dbf.field_names


def split_multiline(string):
    return list(filter(None, string.split('\n')))


def compare_fields(fields_from, fields_to):
    f_order = {v.upper(): i for i, v in enumerate(fields_from)}
    t_order = {v.upper(): i for i, v in enumerate(fields_to)}
    ff = set(s.upper() for s in fields_from)
    ft = set(s.upper() for s in fields_to)
    f_unique = sorted(ff - ft, key=lambda attr: f_order.get(attr))
    t_unique = sorted(ft - ff, key=lambda attr: t_order.get(attr))
    share = sorted(ff & ft, key=lambda attr: (t_order.get(attr), f_order.get(attr)))
    print(f'来源表独特字段为：{f_unique}')
    print(f'目标表独特字段为：{t_unique}')
    print(f'两表共享的字段为：{share}')
