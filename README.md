# markgroves.us

Mark Groves’s Hugo site. Hugo Extended 0.166.0 is pinned in `netlify.toml` and used for local validation.

## Theme and local preview

Commonplace is the default theme and a separate Git submodule under `themes/commonplace/`, sourced from [its GitHub repository](https://github.com/markgrovs/commonplace). The original `hello-friend-ng` theme remains available for rollback. After a fresh clone, run `git submodule update --init --recursive`.

```sh
hugo server -D
hugo --environment production
hugo --environment legacy
```

The default configuration uses `commonplace-overrides/` for site templates, leaving the legacy root `layouts/` in place. To roll back, build with `hugo --environment legacy`, or set `theme = "hello-friend-ng"` and `layoutDir = "layouts"` in `config/_default/config.toml`.

Theme changes are committed inside `themes/commonplace/`, pushed to its own remote, and then recorded in the blog with `git add themes/commonplace`. Blog configuration, content, archetypes, and `commonplace-overrides/` stay in the blog repository.

Author names, the footer email URL, the commit-link base URL, and IndieAuth/Webmention discovery endpoints live in `config/_default/config.toml`. Hugo adds a revision link to tracked writing when Git history is available; new untracked drafts do not show one.

## Writing and privacy

Only deliberately approved public excerpts belong in this repository. Netlify previews include drafts and future-dated content, so `draft: true` is an editorial marker, not privacy protection. Keep private journal originals and private attachments outside the repository.

Create one public log entry per date with `hugo new content --kind log logs/YYYY-MM-DD/index.md`, or write `content/logs/YYYY-MM-DD.md`, and set its front matter date to match. A date-only Log title is treated as an untitled note in IndieWeb markup; a meaningful title is marked as its name. Create new essays with `hugo new content --kind essay essays/my-essay/index.md`. The singular `log.md` and `essay.md` archetypes set `type: log` and `type: essay` and start as drafts; `--kind` selects them for the plural content folders. Section `_index.md` files describe the lists and do not need an entry type. Existing articles remain in `content/posts/`, and automated publishing to that directory can continue; Essays lists both older posts and new essays. Legacy images under `content/posts/assets/` retain their existing URLs. For new photos, place the files in the page bundle, supply meaningful alt text, and add an optional Markdown image title for a caption. Existing photographs with empty alt text need author review.

## Validation

```sh
hugo --environment legacy --destination public/validation/baseline
hugo --environment production --cleanDestinationDir --destination public/validation/commonplace
python3 scripts/check_site.py public/validation/commonplace --baseline public/validation/baseline
python3 scripts/check_indieweb.py public/validation/commonplace
hugo --buildFuture --buildDrafts --destination public/validation/commonplace-preview
python3 scripts/check_indieweb.py public/validation/commonplace-preview
```

The checkers compare generated routes, feed GUIDs, local references, and each writing type’s IndieWeb markup. The legacy and new builds leave generated files under ignored `public/`.

The `/admin/` interface and Bridgy redirects remain in the blog repository. Public pages in Commonplace omit the old GoatCounter and Netlify Identity scripts; verify admin invitation and recovery callbacks after the theme change.
