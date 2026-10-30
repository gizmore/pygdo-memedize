# pygdo-memedize
A (lost) Meme picture collection from the gdo creator. See TikTok for more memes :)

# Memedize (For Humans)

Welcome to more MayMay! Browse the local meme images; click one to open the
original file. In text chat, the overview returns the website link instead.

## Methods

- `Memedize.Overview` displays an information panel and the image gallery.

## GDTs

- Uses the existing information panel and HTML rendering components.

## GDOs

- No database records; images come from `memes/`.

# Memedize (For ALs)

## Methods

- `memedize.overview` is public and reads regular PNG, JPEG, GIF and WebP
  images from the module's `memes/` folder in deterministic filename order.
  HTML displays escaped clickable image links; textual modes return only the
  absolute overview URL. Filenames with Unicode and spaces remain clickable.
  Other files, including archives, are never listed.

## GDTs

- Reuse existing panel, container and HTML GDTs.

## GDOs

- None.
