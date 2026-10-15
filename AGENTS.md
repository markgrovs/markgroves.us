# Repository Guidelines

## Project Structure & Module Organization

This repository contains the markgroves.us Hugo blog. Existing articles live in `content/posts/`, new essays in `content/essays/`, daily logs in `content/logs/`, link posts in `content/links/`, and content templates in `archetypes/`. Site-specific Hugo template overrides belong in `commonplace-overrides/`, the configured `layoutDir`. Images, icons, and the CMS interface live in `static/`; webmention records live in `data/webmentions/`.

Shared configuration is in `config/_default/config.toml`, with environment overrides under `config/`. The `themes/commonplace/` theme is a separate Git submodule. Keep site-specific changes in this repository; reusable theme changes belong in the theme repository, followed by a submodule pointer update here. Generated `public/` and `resources/` directories are ignored; do not commit them.

## Build, Test, and Development Commands

Use Hugo Extended; `netlify.toml` currently pins version `0.166.0`.

- `git submodule update --init --recursive`: initialize the theme after cloning.
- `hugo server -D`: serve locally at `http://localhost:1313/`, including drafts.
- `hugo new content/posts/my-new-post.md`: create an article from the default archetype.
- `hugo new content --kind log logs/YYYY-MM-DD/index.md`: create a daily log bundle.
- `hugo new content --kind essay essays/my-essay/index.md`: create an essay bundle.
- `hugo new content --kind link links/my-reference.md`: create a link post.
- `hugo --environment production`: build the production site into `public/`.
- `hugo --buildFuture --buildDrafts`: check content included in Netlify previews.

Netlify's production branch and build command are managed in hosting settings, not established by this repository. In `netlify.toml`, deploy previews include future-dated content; branch builds include drafts and future-dated content. Only approved public writing and attachments belong here; draft status is not access control. Do not modify the external publishing daemon or private vault as part of site changes.

## Coding Style & Naming Conventions

Match surrounding formatting: local HTML templates generally use four-space indentation; nested TOML settings commonly use two spaces. Write articles in Markdown with YAML front matter containing `title`, `date`, and `draft`. Use the singular archetypes `log`, `essay`, and `link` for their plural sections; they set matching singular `type` values and default to drafts. Link posts also require `link` for the original source URL.

Prefer descriptive, hyphenated filenames for new content, such as `my-new-post.md`. Preserve existing URLs: article permalinks include the date and title. No repository-wide formatter or linter is configured; avoid unrelated formatting changes.

## Testing Guidelines

Run production and draft/future builds into separate, clean output directories, then inspect affected pages locally. Use `scripts/check_site.py` for production links, assets, fragments, and feeds, and `scripts/check_indieweb.py` for production and preview markup; see README.md for commands. An optional pre-change production build passed with `--baseline` checks route and root-feed GUID preservation. Check navigation, images, RSS output, and mobile layout when relevant. Confirm draft visibility in both production and preview builds. No dedicated test framework or coverage threshold is configured.

## Commit & Pull Request Guidelines

History includes `chore:` and `fix:` prefixes alongside automated publishing commits. Use short, descriptive commit subjects; follow those prefixes where appropriate.

For pull requests, describe the change, link any relevant issue, and record build and manual validation results. Include screenshots for visual changes. Call out permalink, configuration, or theme submodule changes explicitly.
