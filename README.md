# markgroves.us

[![Netlify Status](https://api.netlify.com/api/v1/badges/c78e0951-b7fb-4ba8-8ff6-3a2d4414ea7a/deploy-status)](https://app.netlify.com/sites/markgroves/deploys)

Mark Groves’s Hugo site. Hugo Extended 0.166.0 is pinned in `netlify.toml` and used for local validation.

## Theme and local preview

Commonplace is the site's theme and a separate Git submodule under `themes/commonplace/`, sourced from [its GitHub repository](https://github.com/markgrovs/commonplace). After a fresh clone, run `git submodule update --init --recursive`.

```sh
hugo server -D
hugo --environment production
```

Shared configuration lives in `config/_default/config.toml`, with environment overrides under `config/`. The configured `layoutDir` is `commonplace-overrides/`; put site-specific template overrides there rather than in a root `layouts/` directory.

Theme changes are committed inside `themes/commonplace/`, pushed to its own remote, and then recorded in the blog with `git add themes/commonplace`. Blog configuration, content, archetypes, and `commonplace-overrides/` stay in the blog repository.

Author names, the footer email URL, the commit-link base URL, and IndieAuth/Webmention discovery endpoints live in `config/_default/config.toml`. Hugo adds a revision link to tracked writing when Git history is available; new untracked drafts do not show one.

The Follow page subscribes to production even in local and deploy previews. Its `rss-subscribe` shortcode combines `params.productionBaseURL` with the homepage RSS output's actual path. Keep this production base URL aligned with `baseURL` if the site's address changes; preview `--baseURL` overrides only normal site navigation and feed discovery.

## Writing and privacy

Only deliberately approved public excerpts belong in this repository. Netlify deploy previews include future-dated content; branch builds include drafts and future-dated content. `draft: true` is an editorial marker, not privacy protection. Keep private journal originals and private attachments outside the repository.

Create one public log entry per date with `hugo new content --kind log logs/YYYY-MM-DD/index.md`, or write `content/logs/YYYY-MM-DD.md`, and set its front matter date to match. A date-only Log title is treated as an untitled note in IndieWeb markup; a meaningful title is marked as its name. Create new essays with `hugo new content --kind essay essays/my-essay/index.md`. The singular `log.md` and `essay.md` archetypes set `type: log` and `type: essay` and start as drafts; `--kind` selects them for the plural content folders. Section `_index.md` files describe the lists and do not need an entry type. Existing articles remain in `content/posts/`, and automated publishing to that directory can continue; Essays lists both older posts and new essays. Legacy images under `content/posts/assets/` retain their existing URLs. For new photos, place the files in the page bundle, supply meaningful alt text, and add an optional Markdown image title for a caption. Existing photographs with empty alt text need author review.

Create a link post with `hugo new content --kind link links/my-reference.md`. Keep its existing `type: link` and set `link` to the original source URL, then add your observations in Markdown. The Links archive and RSS keep older references; the homepage's Recent links section includes only published entries from the preceding 30 days at build time. New automatic link publishing would need to write this format to `content/links/`; the external publisher's mapping is not maintained in this repository.

## Validation

```sh
hugo --environment production --cleanDestinationDir --destination public/validation/production
python3 scripts/check_site.py public/validation/production
python3 scripts/check_indieweb.py public/validation/production
hugo --buildFuture --buildDrafts --cleanDestinationDir --destination public/validation/preview
python3 scripts/check_indieweb.py public/validation/preview
```

The checkers validate local links, assets, fragments, feed membership, and each writing type's IndieWeb markup. To check route and root-feed GUID preservation across a change, save a production build before editing and pass its output directory to `check_site.py --baseline PATH`. Use separate, clean output directories to avoid stale generated files. Validation output under `public/` is ignored.

The `/admin/` interface and Bridgy redirects remain in the blog repository. Public pages omit GoatCounter and Netlify Identity scripts; the admin interface retains Identity. Admin invitation and recovery callbacks still require interactive verification.
