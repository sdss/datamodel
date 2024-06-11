import pathlib

def generate_markdown_list():
    root = pathlib.Path(__file__).parent.parent
    mdpath = root / 'datamodel/products/md'
    md_files = sorted(mdpath.rglob('*.md'))

    with open('product_files.md', 'w') as f:
        f.write("# Product Files\n\n")
        for md_file in md_files:
            f.write(f"- [{md_file.stem}](../datamodel/products/md/{md_file.name})\n")

if __name__ == "__main__":
    generate_markdown_list()