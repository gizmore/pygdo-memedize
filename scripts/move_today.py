"""Move images last modified today from the legacy archive to today's folder."""

import argparse
import os
from datetime import date, datetime
from pathlib import Path


def move_today(root, today, apply=False):
    root = root.resolve(strict=True)
    source = root / '2023-09-23'
    target = root / today.isoformat()
    if source.is_symlink() or not source.is_dir() or target.is_symlink():
        raise ValueError('Source and destination must be real directories')
    if target == source:
        raise ValueError('Destination is the legacy archive')
    if target.exists() and not target.is_dir():
        raise ValueError('Destination is not a directory')
    images = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
    files = [p for p in source.iterdir() if not p.is_symlink() and p.is_file()
             and p.suffix.lower() in images and datetime.fromtimestamp(p.stat().st_mtime).date() == today]
    if any((target / p.name).exists() or (target / p.name).is_symlink() for p in files):
        raise ValueError('Destination filename collision; no files moved')
    if apply and files:
        target.mkdir(exist_ok=True)
        for path in files:
            destination = target / path.name
            os.link(path, destination, follow_symlinks=False)
            try:
                if not os.path.samestat(path.stat(), destination.stat()):
                    raise RuntimeError('Source changed during move')
                path.unlink()
            except Exception:
                destination.unlink()
                raise
    return len(files)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    folder = Path(__file__).resolve().parent.parent / 'memes'
    print(f'{move_today(folder, date.today(), args.apply)} images {"moved" if args.apply else "would be moved"}')
