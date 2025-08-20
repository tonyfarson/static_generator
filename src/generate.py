# src/generate.py
import os
from markdown import markdown_to_html_node


def extract_title(markdown: str) -> str:
    """
    Return the first level-1 heading text from the markdown (line starting with "# ").
    Raise an Exception if none exists.
    """
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No h1 header found in markdown")


def _apply_basepath(html: str, basepath: str) -> str:
    """
    Prefix root-relative href/src (starting with /) with the provided basepath.
    Examples:
      href="/x" -> href="{basepath}x"
      src="/y"  -> src="{basepath}y"
    External links like https://... are unaffected.
    """
    if not basepath.endswith("/"):
        basepath = basepath + "/"
    # Avoid double slashes when we join basepath + path
    # We only replace attributes that literally start with "/"
    html = html.replace('href="/', f'href="{basepath}')
    html = html.replace('src="/', f'src="{basepath}')
    return html


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str = "/") -> None:
    """
    Render a single markdown file using the HTML template into a destination .html file.
    basepath is used to prefix root-relative href/src attributes for GitHub Pages.
    """
    print(f"[page] Generating {dest_path} from {from_path} using {template_path} (basepath={basepath})")

    # Read markdown source
    with open(from_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Read template
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # Convert markdown -> HTML
    root_node = markdown_to_html_node(md_text)
    content_html = root_node.to_html()

    # Extract title
    title = extract_title(md_text)

    # Fill template placeholders
    html = template.replace("{{ Title }}", title).replace("{{ Content }}", content_html)

    # Apply basepath rewrites for root-relative links
    html = _apply_basepath(html, basepath)

    # Ensure destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write output
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[done] Wrote {dest_path}")


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str = "/") -> None:
    """
    Crawl every entry in dir_path_content. For each *.md file found, generate a corresponding
    .html file in dest_dir_path with the same relative structure.

    Examples:
      content/index.md                -> docs/index.html
      content/blog/tom/index.md       -> docs/blog/tom/index.html
      content/notes/about.md          -> docs/notes/about.html
    """
    for root, _dirs, files in os.walk(dir_path_content):
        for filename in files:
            if not filename.lower().endswith(".md"):
                continue

            src_md = os.path.join(root, filename)

            # Compute relative directory under content/
            rel_dir = os.path.relpath(root, dir_path_content)
            rel_dir = "" if rel_dir == "." else rel_dir

            # Map filename.md -> filename.html
            base = filename[:-3]  # strip ".md"
            dest_subdir = os.path.join(dest_dir_path, rel_dir) if rel_dir else dest_dir_path
            dest_html = os.path.join(dest_subdir, f"{base}.html")

            generate_page(src_md, template_path, dest_html, basepath=basepath)
