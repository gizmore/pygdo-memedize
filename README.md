# pygdo-memedize
A (lost) Meme picture collection from the gdo creator. See TikTok for more memes :)

# Memedize (For Humans)

Welcome to more MayMay! Hover over a meme for a small zoom and click it for a
larger preview, with a link to the original file. In text chat, the overview
returns the website link instead.

## Ideas

- Add **Lost & Found** to the left menu: a shared place to find and collect
  memes and videos. An entry can start with a link or a description of a
  half-remembered item. People discuss it and add links; a found item becomes
  a collection entry with its title, tags and context.
- Let people submit their favorite memes and videos for a shared collection,
  linking to releases on established platforms. Memedize is the community
  around them, not a replacement publishing platform.
- Let people describe a half-remembered meme or video in a forum discussion so
  others can help find it.
- Rate archived favorites and explore the community's discoveries.
- Subscribe to meme releases. Add per-user support; the exact subscription
  scope, delivery channels and user-specific features remain open.
- Planned chat flow: `$memedize.create <idea>` requests a meme from Mira's
  `$meme` skill. Once created, `$memedize.neu` announces the release to
  channels that explicitly opted in through `$memedize.abbo`. Channels are
  unsubscribed by default. A create request costs 100 credits by default;
  release announcements require staff. The local create and release methods
  are prepared but not yet deployed. For now creation is restricted to staff
  and charges nothing; atomic charging, failure handling, opening requests to
  others and per-user subscriptions remain open.

These features are planned ideas, not implemented yet. Submission, forum
integration, and rating rules are open for design.

## Methods

- `Memedize.Overview` displays an information panel and the image gallery.

## GDTs

- Uses the existing information panel and HTML rendering components.

## GDOs

- No database records; images come from `memes/`.

# Memedize (For ALs)

## Methods

- `memedize.overview` is public and displays one `YYYY-MM-DD` directory per
  page, newest first, with a choice of days, links to older/newer days and to browse the directory.
  A day with many images is split into pages of 24; page links retain the day.
  It reads regular PNG, JPEG, GIF and WebP images in deterministic filename order.
  HTML displays escaped clickable image links, enhanced with a hover zoom and
  a dismissible click preview; without JavaScript the link opens the original.
  Textual modes return only the
  absolute overview URL. Filenames with Unicode and spaces remain clickable.
  Other files, including archives, are never listed.
- New memes are saved under the local creation date. Legacy files are archived
  in `2023-09-23`.

## GDTs

- Reuse existing panel, container and HTML GDTs.

## GDOs

- None.
