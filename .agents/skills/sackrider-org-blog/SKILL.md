---
name: sackrider-org-blog
title: Authoring & Archiving for sackrider.org
description: Author, format, review, and publish family blog posts, milestones, photo journals, and memories for the Sackrider family blog at sackrider.org. Use when drafting new family updates, organizing archive entries, formatting Astro markdown frontmatter, managing media, and deploying to Cloudflare.
version: 1.0.0
author: Dale & Stephanie Sackrider
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Family-Archive, Personal-Blogging, Memories, Photo-Journal, Sackrider-Family, Astro]
    category: domain
    requires_toolsets: []
---

# Authoring & Archiving for sackrider.org

## Overview
This skill guides agents in writing, formatting, archiving, and publishing family updates, memories, and photos for the **Sackrider family blog** at [sackrider.org](https://sackrider.org).

The site is built with **Astro**, version-controlled in Git, and hosted on **Cloudflare Edge**.

---

## 👨‍👩‍👧‍👦 Voice & Tone Guidelines

### Purpose & Audience
* **Context:** The ongoing digital memory album and personal journal of the Sackrider family (Dale, Stephanie, and kids), spanning from 2004 to present.
* **Audience:** Family members, friends, future generations, and fellow Sackriders discovering the family site.
* **Tone:** Warm, candid, celebratory, reflective, down-to-earth, and personal.

### Content Types
1. **Family Milestones:** Birthdays, graduations, family trips, holidays, new additions, and career/life transitions.
2. **Everyday Reflections:** Humorous kid quotes, funny moments at home, hobbies, pets, and weekend adventures.
3. **Photo Entries:** Visual journals with captioned photos stored in `public/wp-content/uploads/`.
4. **Historical Retrospectives:** Looking back at older memories from the 2000s and 2010s archive.

---

## 📁 Repository & File Structure

* **Project Root:** `/Users/skippy/repos/sackrider-org`
* **Content Directory:** `/Users/skippy/repos/sackrider-org/src/content/blog/`
* **Media Directory:** `/Users/skippy/repos/sackrider-org/public/wp-content/uploads/`
* **GitHub Repository:** `https://github.com/dsackr/sackrider-org`
* **Live Site:** `https://sackrider.org`

---

## 📝 Post Format Specification

Every post is a Markdown file located at `/Users/skippy/repos/sackrider-org/src/content/blog/<slug>.md`.

### Frontmatter Schema
```yaml
---
title: "Title of the Family Post"
description: "A short 1-2 sentence preview for search and summary cards."
pubDate: "YYYY-MM-DD"
draft: false
tags: ["family", "photos", "milestones"]
---
```

### Media Guidelines
* Reference images using relative paths: `/wp-content/uploads/YYYY/MM/filename.jpg`.
* Use markdown image syntax: `![Caption or Description](/wp-content/uploads/2026/09/family-photo.jpg)`.

---

## 🚀 Step-by-Step Publishing Workflow

### 1. Draft the Post
Create `/Users/skippy/repos/sackrider-org/src/content/blog/<slug>.md` with frontmatter and Markdown body.

### 2. Verify Build Locally
```bash
cd /Users/skippy/repos/sackrider-org
npm run build
```

### 3. Deploy to Cloudflare Edge
```bash
cd /Users/skippy/repos/sackrider-org
npx wrangler deploy
```

### 4. Commit and Push to GitHub
```bash
cd /Users/skippy/repos/sackrider-org
git add .
git commit -m "Publish: <Title of Post>"
git push origin main
```

---

## 🔍 Quality Checklist Before Publishing
- [ ] Is the title warm, descriptive, and personal?
- [ ] Is `pubDate` set correctly in `YYYY-MM-DD` format?
- [ ] Are all embedded image paths pointing to valid `/wp-content/uploads/...` paths?
- [ ] Did `npm run build` build all 540+ pages with 0 errors?
- [ ] Is the post visible on https://sackrider.org and in the `/archive` timeline?
