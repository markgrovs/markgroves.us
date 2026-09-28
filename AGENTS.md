# Repository Guidelines

## Project Structure & Module Organization

This repository contains the markgroves.us Hugo blog. Markdown articles live in `content/posts/`, link posts in `content/links/`, and content templates in `archetypes/`. Site-specific Hugo templates and rendering hooks live in `layouts/`. Images, icons, and the CMS interface live in `static/`; webmention records live in `data/webmentions/`.

Shared configuration is in `config/_default/config.toml`, with environment overrides under `config/development/` and `config/production/`. The `themes/hello-friend-ng/` theme is a Git submodule. Prefer site overrides in `layouts/` for local customizations. Generated `public/` and `resources/` directories are ignored; do not commit them.

## Build, Test, and Development Commands

Use Hugo Extended; `netlify.toml` currently pins version `0.165.0`.

- `git submodule update --init --recursive`: initialize the theme after cloning.
- `hugo server -D`: serve locally at `http://localhost:1313/`, including drafts.
- `hugo new content/posts/my-new-post.md`: create an article from the default archetype.
- `hugo --environment production`: build the production site into `public/`.
- `hugo --buildFuture --buildDrafts`: check content included in Netlify previews.

Netlify deploys the main branch automatically. Preview and branch builds include draft and future-dated content.

## Coding Style & Naming Conventions

Match surrounding formatting: local HTML templates generally use four-space indentation; nested TOML settings commonly use two spaces. Write articles in Markdown with YAML front matter containing `title`, `date`, and `draft`. Link posts also use `type: "link"` and `link`.

Prefer descriptive, hyphenated filenames for new content, such as `my-new-post.md`. Preserve existing URLs: article permalinks include the date and title. No repository-wide formatter or linter is configured; avoid unrelated formatting changes.

## Testing Guidelines

No dedicated test framework, test naming convention, or coverage threshold is configured. Run a production build, then inspect affected pages locally. Check navigation, images, links, RSS output, and mobile layout when relevant. Confirm draft visibility in both production and preview builds.

## Commit & Pull Request Guidelines

History includes `chore:` and `fix:` prefixes alongside automated publishing commits. Use short, descriptive commit subjects; follow those prefixes where appropriate.

For pull requests, describe the change, link any relevant issue, and record build and manual validation results. Include screenshots for visual changes. Call out permalink, configuration, or theme submodule changes explicitly.
