# SuperOpsImport

To Import a local Directory filled with .html files to your SuperOps IT Documentation
Ideally for Confluence

# STATUS: Upload works, parsers don't

# How to use
## Requirements
* Directory of html formatted files
* SuperOps.ai API Token
* customer subdomain
* typeId of ItDocumentationCategory
* client accountId
* siteId
* WIP: Content Host (Webserver)

## Optional
html title tags for automatic Document Title in Super Ops

## Expected Directory Structure
<pre>
./
├── style/
│   └──  site.css
├── images/
│   └── icons/
│       └── emoticons/
├── attachments/
│   ├── thumbnails
│   └── ...
└── ...
</pre>
