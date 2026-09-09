#!/usr/bin/env python3
import subprocess
import os
import re
import html
import yaml
from collections import defaultdict

DB_CONTAINER = "sackrider-org-db-1"
DB_USER = "wp_user"
DB_PASS = "KNFcW&ijC=t]%LIbliuOVKg}vuMJBLgh"
DB_NAME = "wordpress"
OUTPUT_DIR = "/Users/skippy/repos/sackrider-org/src/content/blog"

def run_query(sql):
    cmd = [
        "docker", "exec", DB_CONTAINER,
        "mariadb", "-u", DB_USER, f"-p{DB_PASS}", DB_NAME,
        "-sN", "-e", sql
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Query error: {res.stderr}")
    return res.stdout

def unhex(h):
    if not h or h == "NULL":
        return ""
    try:
        raw = bytes.fromhex(h)
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError:
            return raw.decode("latin1")
    except Exception:
        return ""

def fix_encoding_artifacts(text):
    if not text:
        return ""
    replacements = {
        'â€™': "'",
        'â€˜': "'",
        'â€œ': '"',
        'â€ ': '"',
        'â€“': '–',
        'â€”': '—',
        'â€¦': '...',
        'Â ': ' ',
        'Â': '',
        'Ã©': 'é',
        'Ã¡': 'á',
        'Ã­': 'í',
        'Ã³': 'ó',
        'Ãº': 'ú',
        'Ã±': 'ñ',
        'Ã ': 'à',
        'Ã¨': 'è',
        'Ã¬': 'ì',
        'Ã²': 'ò',
        'Ã¹': 'ù',
        '˜': '"',
        '\r\n': '\n',
        '\r': '\n',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def clean_html_and_shortcodes(content):
    if not content:
        return ""
    
    # Replace absolute URLs to local uploads
    content = re.sub(r'https?://(?:www\.)?sackrider\.org/wp-content/uploads/', '/wp-content/uploads/', content)
    content = re.sub(r'https?://(?:www\.)?dalesackrider\.com/wp-content/uploads/', '/wp-content/uploads/', content)
    
    # Strip Gutenberg block comments e.g. <!-- wp:paragraph -->
    content = re.sub(r'<!--\s*/?wp:[^>]*-->', '', content)
    # Strip <!--more-->
    content = re.sub(r'<!--more-->', '', content)
    
    # Clean Facebook paste artifacts
    content = re.sub(r'<span class="text_exposed_hide">.*?</span>', '', content, flags=re.DOTALL)
    
    # Strip div, span, font wrapper tags
    content = re.sub(r'</?(?:div|span|font)[^>]*>', '', content)
    
    # Convert WordPress caption shortcodes:
    def replace_caption(match):
        inner = match.group(1).strip()
        return f"\n\n{inner}\n\n"
    
    content = re.sub(r'\[caption[^\]]*\](.*?)\[/caption\]', replace_caption, content, flags=re.DOTALL)
    
    # Convert [embed]url[/embed] to url
    content = re.sub(r'\[embed\](.*?)\[/embed\]', r'\1', content, flags=re.DOTALL)
    
    # Fix encoding artifacts
    content = fix_encoding_artifacts(content)
    
    # Trim excessive blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content.strip()

def extract_description(content, excerpt=""):
    if excerpt:
        cleaned = fix_encoding_artifacts(excerpt.strip())
        cleaned = re.sub(r'<[^>]+>', '', cleaned)
        cleaned = html.unescape(cleaned).strip()
        if len(cleaned) > 10:
            return cleaned[:200]
    
    # Derive from content
    plain = re.sub(r'<[^>]+>', ' ', content)
    plain = re.sub(r'\[[^\]]+\]', ' ', plain)
    plain = html.unescape(plain)
    plain = re.sub(r'\s+', ' ', plain).strip()
    
    if not plain:
        return ""
    
    if len(plain) <= 160:
        return plain
    truncated = plain[:160]
    last_space = truncated.rfind(' ')
    if last_space > 80:
        return truncated[:last_space] + '...'
    return truncated + '...'

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-')

def main():
    # Remove existing exported files to prevent stale files
    if os.path.exists(OUTPUT_DIR):
        for f in os.listdir(OUTPUT_DIR):
            if f.endswith('.md'):
                os.remove(os.path.join(OUTPUT_DIR, f))
    else:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("Fetching taxonomy...")
    tax_sql = "SELECT tr.object_id, HEX(t.name), tt.taxonomy FROM wp_kq5vj3_term_relationships tr JOIN wp_kq5vj3_term_taxonomy tt ON tr.term_taxonomy_id = tt.term_taxonomy_id JOIN wp_kq5vj3_terms t ON tt.term_id = t.term_id;"
    tax_out = run_query(tax_sql)
    terms = defaultdict(lambda: {'categories': [], 'tags': []})
    for line in tax_out.strip().split('\n'):
        if not line:
            continue
        parts = line.split('\t')
        if len(parts) >= 3:
            oid = int(parts[0])
            name = unhex(parts[1])
            tax = parts[2]
            if tax == 'category' and name.lower() != 'uncategorized':
                terms[oid]['categories'].append(name)
            elif tax == 'post_tag':
                terms[oid]['tags'].append(name)

    print("Fetching posts from MariaDB...")
    posts_sql = """
    SELECT ID, HEX(post_title), HEX(post_name), post_date, post_status, post_type, HEX(post_content), HEX(post_excerpt)
    FROM wp_kq5vj3_posts
    WHERE post_type IN ('post', 'page')
      AND post_status IN ('publish', 'private', 'draft')
    ORDER BY post_date DESC;
    """
    posts_out = run_query(posts_sql)
    
    lines = posts_out.strip().split('\n')
    print(f"Total post rows fetched: {len(lines)}")
    
    exported_count = 0
    used_slugs = set()
    
    for line in lines:
        if not line:
            continue
        parts = line.rstrip('\r\n').split('\t')
        if len(parts) < 6:
            continue
        
        pid = int(parts[0])
        raw_title = unhex(parts[1])
        raw_slug = unhex(parts[2])
        post_date = parts[3]
        post_status = parts[4]
        post_type = parts[5]
        raw_content = unhex(parts[6]) if len(parts) > 6 else ""
        raw_excerpt = unhex(parts[7]) if len(parts) > 7 else ""
        
        # Skip completely empty posts with no title and no content
        if not raw_title.strip() and not raw_content.strip():
            continue
        
        title = fix_encoding_artifacts(raw_title).strip()
        if not title:
            title = f"Post {pid}"
            
        slug = raw_slug.strip()
        if not slug:
            slug = slugify(title)
        if not slug:
            slug = f"post-{pid}"
            
        # Ensure unique slug
        base_slug = slug
        counter = 1
        while slug in used_slugs:
            counter += 1
            slug = f"{base_slug}-{counter}"
        used_slugs.add(slug)
        
        # Format date (YYYY-MM-DD)
        date_str = post_date.split(' ')[0] if post_date and post_date != '0000-00-00 00:00:00' else '2000-01-01'
        
        # Status
        is_draft = (post_status != 'publish')
        
        # Content & Description
        cleaned_content = clean_html_and_shortcodes(raw_content)
        description = extract_description(cleaned_content, raw_excerpt)
        if not description:
            description = title
            
        # Tags & Categories
        post_terms = terms.get(pid, {'categories': [], 'tags': []})
        all_tags = sorted(list(set(post_terms['categories'] + post_terms['tags'])))
        
        # Frontmatter
        frontmatter = {
            'title': title,
            'description': description,
            'pubDate': date_str,
            'draft': is_draft,
        }
        if all_tags:
            frontmatter['tags'] = all_tags
            
        # Look for a hero image in content if any
        img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', cleaned_content)
        if not img_match:
            img_match = re.search(r'!\[.*?\]\((.*?)\)', cleaned_content)
        if img_match:
            img_url = img_match.group(1)
            if img_url.startswith('/wp-content/uploads/'):
                frontmatter['heroImage'] = img_url
        
        # Format YAML
        yaml_str = yaml.dump(frontmatter, allow_unicode=True, default_flow_style=False, sort_keys=False).strip()
        
        full_file_content = f"---\n{yaml_str}\n---\n\n{cleaned_content}\n"
        
        file_path = os.path.join(OUTPUT_DIR, f"{slug}.md")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(full_file_content)
            
        exported_count += 1

    print(f"Successfully exported {exported_count} posts to {OUTPUT_DIR}")

if __name__ == '__main__':
    main()
