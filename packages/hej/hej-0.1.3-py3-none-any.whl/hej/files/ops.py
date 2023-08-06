import shutil
from pathlib import Path


def difference(a, b, out=None, suffixes=None, flatten=False):
    a, b = Path(a), Path(b)

    if out is None:
        out = f"{str(a)}_diff"

    out = Path(out)

    shutil.rmtree(out, ignore_errors=True)

    rm_list = set([f.name for f in b.glob("**/*.*")])

    src_list = [f for f in a.glob("**/*.*") if f.name not in rm_list]

    if isinstance(suffixes, str):
        suffixes = set(suffixes.split(","))
        src_list = [f for f in src_list if f.suffix in suffixes]

    if flatten:
        dst_list = [out / f.name for f in src_list]
    else:
        dst_list = [out / f.relative_to(a) for f in src_list]

    for fpath in sorted(set([f.parent for f in dst_list])):
        fpath.mkdir(parents=True, exist_ok=True)

    for src, dst in zip(src_list, dst_list):
        shutil.copyfile(src, dst)

    return f"copy {len(src_list)} file to {out}"
