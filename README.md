# markgroves.us

[![Netlify Status](https://api.netlify.com/api/v1/badges/c78e0951-b7fb-4ba8-8ff6-3a2d4414ea7a/deploy-status)](https://app.netlify.com/sites/markgroves/deploys)

Personal blog built with [Hugo](https://gohugo.io/) and deployed on [Netlify](https://www.netlify.com/).

## Prerequisites

- [Hugo](https://gohugo.io/installation/) (Extended version)
- [Git](https://git-scm.com/)

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/markgroves.us.git
cd markgroves.us
```

2. Start the Hugo development server:
```bash
hugo server -D
```

The site will be available at http://localhost:1313/

## Creating New Content

```bash
hugo new content/posts/my-new-post.md
```

## Deployment

This site is automatically deployed to Netlify when changes are pushed to the main branch.

## Project Structure

```
.
├── archetypes/
├── content/
├── layouts/
├── static/
├── themes/
├── config.toml
└── README.md
```

## License

[MIT License](LICENSE)
