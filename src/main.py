# src/main.py
import os
import sys
import shutil
from generate import generate_pages_recursive

OUT_DIR = "docs"  # GitHub Pages serves from /docs on the main branch by default


def copy_dir_recursive(src: str, dst: str) -> None:
    for entry in os.listdir(src):
        s_path = os.path.join(src, entry)
        d_path = os.path.join(dst, entry)

        if os.path.isdir(s_path):
            os.makedirs(d_path, exist_ok=True)
            print(f"[dir ] {s_path} -> {d_path}")
            copy_dir_recursive(s_path, d_path)
        elif os.path.isfile(s_path):
            shutil.copy2(s_path, d_path)
            print(f"[file] {s_path} -> {d_path}")
        else:
            print(f"[skip] {s_path}")


def copy_static(src: str, dst: str) -> None:
    if os.path.exists(dst):
        print(f"[wipe] Removing existing '{dst}'")
        shutil.rmtree(dst)

    print(f"[mk  ] Creating '{dst}'")
    os.makedirs(dst, exist_ok=True)

    print(f"[copy] {src} -> {dst}")
    copy_dir_recursive(src, dst)
    print("[done] Static assets copied.")


def main() -> None:
    # Basepath from CLI arg (default "/")
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    print(f"[cfg ] basepath = {basepath}")

    # 1) Copy static assets to OUT_DIR
    copy_static("static", OUT_DIR)

    # 2) Generate ALL pages from content/ into OUT_DIR, with basepath
    generate_pages_recursive("content", "template.html", OUT_DIR, basepath=basepath)
    print("[ok  ] Site generation complete")


if __name__ == "__main__":
    main()
