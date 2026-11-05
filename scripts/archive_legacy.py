"""Move legacy root/month files into the archive without URL aliases."""

import argparse
import os
import re
from pathlib import Path


def archive(root, apply=False):
    root = root.resolve(strict=True)
    target = root / '2023-09-23'
    if target.is_symlink() or (target.exists() and not target.is_dir()):
        raise ValueError('Archive destination must be a real directory')
    sources = [p for p in root.iterdir() if p.is_file() and not p.is_symlink()]
    for directory in root.iterdir():
        if directory.is_symlink() or not directory.is_dir() or not re.fullmatch(r'\d{4}-\d{2}', directory.name):
            continue
        sources.extend(p for p in directory.iterdir() if p.is_file() and not p.is_symlink())
    names = [p.name for p in sources]
    if len(set(names)) != len(names):
        raise ValueError('Duplicate legacy filenames; no files moved')
    if any((target / name).exists() or (target / name).is_symlink() for name in names):
        raise ValueError('Archive destination contains conflicting names; no files moved')
    if not apply:
        return len(sources)
    target.mkdir(exist_ok=True)
    for source in sources:
        destination = target / source.name
        # Create without overwriting, then remove the old directory entry.
        os.link(source, destination, follow_symlinks=False)
        try:
            if not os.path.samestat(source.stat(), destination.stat()):
                raise RuntimeError('Source changed during archive')
            source.unlink()
        except Exception:
            destination.unlink()
            raise
    return len(sources)


def remove_legacy_links(root, apply=False):
    """Remove only aliases pointing to matching regular files in the archive."""
    root = root.resolve(strict=True)
    target = (root / '2023-09-23').resolve(strict=True)
    if target != root / '2023-09-23' or not target.is_dir():
        raise ValueError('Archive must be a real directory')
    parents = [root] + [p for p in root.iterdir() if not p.is_symlink() and p.is_dir()
                        and re.fullmatch(r'\d{4}-\d{2}', p.name)]
    links = []
    for parent in parents:
        for path in parent.iterdir():
            expected = target / path.name
            if path.is_symlink() and expected.is_file() and not expected.is_symlink() and path.resolve() == expected:
                links.append(path)
    if apply:
        for path in links:
            path.unlink()
    return len(links)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--remove-legacy-links', action='store_true')
    args = parser.parse_args()
    folder = Path(__file__).resolve().parent.parent / 'memes'
    if args.remove_legacy_links:
        print(f'{remove_legacy_links(folder, args.apply)} legacy links {"removed" if args.apply else "would be removed"}')
    else:
        print(f'{archive(folder, args.apply)} legacy files {"archived" if args.apply else "would be archived"}')
