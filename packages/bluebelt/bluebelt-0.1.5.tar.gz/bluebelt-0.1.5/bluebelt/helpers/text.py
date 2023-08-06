import re
import math

def get_nice_list(the_list):
    if len(the_list) == 1:
        return the_list[0]
    else:
        return ", ".join(the_list[:-1])+" and "+the_list[-1]

def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

def format_digits(x, digits=6):
    if isinstance(x, list):
        return max([format_digits(i, digits=digits) for i in x])
    elif x == 0 or not math.isfinite(x):
        return x
    else:
        prtd = max(digits, math.ceil(math.log10(abs(x))))
        prtd -= math.ceil(math.log10(abs(x)))
        prtd = min(digits, prtd)
        return f'1.{prtd}f'

def get_h0_equal_means(columns):
    if len(columns) == 1:
        return ''
    elif len(columns) > 4:
        return f'$H_0: \\bar{{X}}_{{{columns[0]}}} = \\bar{{X}}_{{{columns[1]}}} = \\bar{{X}}_{{...}} = \\bar{{X}}_{{{columns[-1]}}}$'
    else:
        result = f'$H_0: \\bar{{X}}_{{{columns[0]}}}$'
        for col in columns[1:]:
            result += f'$ = \\bar{{X}}_{{{col}}}$'
        return result
    