---
title: "Adding Webmentions to a static site via GitHub"
date: 2019-08-24 23:14:34
draft: false
type: "post"
tags: ['meta','indieweb', 'hugo']
toc: false
---

Over the last several weeks, I decided to build my site from the ground up using [Hugo][1], a static site generator. My main goal in rebuilding my website is to get back into writing while having a place on the web that is my own. 

I am adding features of the IndieWeb to my site along the way. 

My latest IndieWeb support is implementing Webmentions. With the help from posts by [Vincent Pickering][2], [Keith Grant][3], and [Max Böck][4] I was able to add initial support for Webmentions to my Hugo based site.

## What are Webmentions?

[Webmentions][5] is a W3C recommendation that enables site owners to send and receive notifications for reactions posted from other sites. A Webmention reaction can be when someone posts a blog post linking to one of your posts. Or, using services such as [Bridgy][6] your site can receive likes and re-posts from services such as Twitter.

## Challenge without JavaScript

The main benefits of using static site generators, such as Hugo or Jekyll, is the performance of only needing to serve up HTML and CSS. Adding significant logic in JavaScript defeats these benefits, in my opinion.

Posts on this site use a git-based flow, that starts with a merge into the master branch on GitHub. This merge kicks off a build within [Netlify][7] that host this site. 

The challenge of using a GitHub-to-Netlify deployment flow is that the site doesn't change unless something has changed within the git repository. Figuring out how to get data from a new Webmention to change my git repository was what I needed to figure out.

## Solution

Vincent's post got me pretty far down the line of figuring out a solution to this problem. In his post, he outlines how to use Jekyll data files and a server he calls [Mastr-Cntrl][8] to post to his git repository. Since Hugo also has [data files][9], I knew I was on to something. But, I was hoping I didn't need to stand up a server to listen for Webmentions.

To get this to work without the need for a running server, I set off to find a solution that would look more like a serverless function. The workflow I wanted looked like this:

```
webmetion.io > webhook > create data file > pull request > merge > build > deploy
```

1. Webmention notifications would first go to [webmentions.io][10] by adding my site's Webmention endpoint to the HTML header.

```html
<link rel="webmention" href="https://webmention.io/markgroves.us/webmention" />
<link rel="pingback" href="https://webmention.io/markgroves.us/xmlrpc" />
```

2. Next, I needed something to listen for [webhook events][11] from webmentions.io.
   
The [Integromat][12] service came to the rescue. Integromat is similar to Zapier or IFTTT, but, it supports creating a webhook endpoint, and also has an integration to GitHub that supports creating files within your git repository.

3. Parse Webmention JSON within Integromat and save a file to /data/webmention folder.

![webhook to JSON to GitHub](/images/Integration_Webhooks__JSON___Integromat.png)

Now, each time a webmentions.io picks up a Webmention for one of my posts, Integromat will create a new file within a git branch using the wm-id from the JSON send over in the webhook.
![GitHub configuration detail](/images/Integration_Webhooks__JSON___Integromat_details.png)

### Leveraging GitHub pull requests

One of the benefits of using GitHub for managing your web site is that you have complete control on when changes get deployed. Since I want to make sure the Webmentions I am going to add to my site are appropriate, I decided to leverage pull-requests within GitHub. 

By posting the Webmention JSON file into a separate branch, I can review the changes before merging them with the master branch and ultimately publishing publicly.

### Automating Git check-ins - Integromat

At this point, Integromat is an experiment. I don't expect enough traffic on my site to need to upgrade to a paid plan. But, even at $9 a month, if this solution continues to work, it will be worth it.

## Formatting Webmentions using Hugo

At this point, the remaining work is to pull the data from the data files into the matching posts. I added a partial template to my Hugo theme named [webmentions.html][13]. For each reaction type, I format the reaction to match my theme:

```html
<div class="pagination__title">
        <span class="pagination__title-h">Replies</span>
        <hr/>
    </div>
    {{ range .Site.Data.webmentions }}
        {{ range . }}
            {{ if isset . "wm-property" }} 
                {{ if eq (index . "wm-property") "in-reply-to" }}

                    <div class="u-comment h-cite">
                        <a class="u-author h-card" {{- if .author.url -}} href="{{ .author.url }}" {{ end }}>            
                            {{ .author.name | humanize }}
                        </a>
                    </p>
                        <p class="e-content e-name">
                            {{- .content.html | safeHTML }}
                        </p>
                        <a class="u-url" href="{{ .url }}">
                            {{ .url }}
                        </a>
                        &nbsp;@
                        <time class="dt-published">{{ if .published }}{{ dateFormat $.Site.Params.dateformNumTime .published }}{{ end }}</time>  
                    </div>
                    <hr/>
                {{ end }}
            {{ end }}
        {{ end }}
    {{ end }}
```

## Conclusion

Although I don't expect to have significant traffic on my site, I wanted a process that fit my goals of having a static website with low maintenance.

Getting this to work was a bit complex, but I learned a good bit about how Hugo works along the way. Feel free to contact me if you have any questions.

[1]:https://gohugo.io
[2]:https://vincentp.me/articles/2018/11/14/20-00/
[3]:https://keithjgrant.com/posts/2019/02/adding-webmention-support-to-a-static-site/
[4]:https://mxb.dev/blog/using-webmentions-on-static-sites/
[5]:https://webmention.net/draft/
[6]:https://brid.gy/
[7]:https://netlify.com
[8]:https://github.com/vipickering/mastr-cntrl
[9]:https://gohugo.io/templates/data-templates/
[10]:https://webmentions.io
[11]:https://webmention.io/settings/webhooks
[12]:https://www.integromat.com
[13]:https://github.com/markgrovs/hugo-theme-hello-friend-ng/blob/master/layouts/partials/webmentions.html
