import re


async def reformat_name(name: str, query: str) -> str:
    name = re.sub(r"[-|~]", " ", name)

    low_name, spl_name = name.lower(), name.split()
    low_q, spl_q = query.lower(), query.split()

    try:
        idx_max = low_name.split().index(low_q.split()[-1])
    except ValueError:
        return name

    if (len(spl_name) - len(spl_q)) > 1:
        res = " ".join(spl_name[: idx_max + 3])
    elif (len(spl_name) - len(spl_q)) > 0:
        res = " ".join(spl_name[: idx_max + 2])
    else:
        res = " ".join(spl_name[: idx_max + 1])
    return res
