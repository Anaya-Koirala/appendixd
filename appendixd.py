import argparse
import os
import fnmatch


def is_included(file, included_extensions):
    return any(file.endswith(ext) for ext in included_extensions)


def get_all_files(start_dir, auto_skip_folders):
    for root, dirs, files in os.walk(start_dir, topdown=True):
        dirs[:] = [d for d in dirs if d not in auto_skip_folders]
        for file in files:
            yield os.path.join(root, file)


def get_files_default(start_dir, auto_skip_folders, included_extensions):
    for file_path in get_all_files(start_dir, auto_skip_folders):
        if is_included(file_path, included_extensions):
            yield file_path


def get_files_all(start_dir, auto_skip_folders):
    yield from get_all_files(start_dir, auto_skip_folders)


def get_files_ignore(start_dir, auto_skip_folders, ignore_patterns):
    for file_path in get_all_files(start_dir, auto_skip_folders):
        if any(fnmatch.fnmatch(file_path, pat) for pat in ignore_patterns):
            continue
        yield file_path


def get_files_manual(files):
    for file_path in files:
        if os.path.isfile(file_path):
            yield file_path


def copy_contents_to_appendix(start_dir, output_file, user_skip_folder, mode, ignore_patterns=None, manual_files=None):
    included_extensions = [
        ".py", ".js", ".ts", ".java", ".cpp", ".c", ".h", ".hpp", ".cs",
        ".html", ".css", ".json", ".xml", ".yml", ".yaml", ".sh", ".bat",
        ".rb", ".php", ".go", ".rs", ".swift", ".kt", ".m", ".pl", ".sql",
        ".md", ".ini", ".cfg", ".toml", ".dart", ".scala", ".vue", ".jsx", ".tsx"
    ]
    auto_skip_folders = ["venv", "__pycache__", ".git", user_skip_folder]

    if mode == "default":
        files_iter = get_files_default(start_dir, auto_skip_folders, included_extensions)
    elif mode == "all":
        files_iter = get_files_all(start_dir, auto_skip_folders)
    elif mode == "ignore":
        files_iter = get_files_ignore(start_dir, auto_skip_folders, ignore_patterns or [])
    elif mode == "manual":
        files_iter = get_files_manual(manual_files or [])
    else:
        raise ValueError(f"Unknown mode: {mode}")

    with open(output_file, "w", encoding="utf-8") as output_txt:
        for file_path in files_iter:
            file = os.path.basename(file_path)
            try:
                with open(file_path, "r", encoding="utf-8") as infile:
                    content = infile.read()
                    output_txt.write(f"File: {file}\n\n{content}\n\n\n")
            except UnicodeDecodeError:
                print(f"Skipping file due to encoding issue: {file_path}")
            except Exception as e:
                print(f"Skipping file {file_path} due to error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert your code into an appendix. Modes: default (auto-detect), all (all files), ignore (ignore patterns), manual (manual file list).\nNote: This is converted to .txt for editing before you convert it to pdf.\nEditing before converting highly recommended as there might be bugs"
    )
    parser.add_argument("--folder", type=str, help="Folder to Convert", required=True)
    parser.add_argument("--skip-folder", type=str, help="Folder to Skip", default="")
    parser.add_argument("--output", type=str, help="Output filename", default="appendix.txt")
    parser.add_argument("--mode", type=str, choices=["default", "all", "ignore", "manual"], default="default", help="Mode of file selection")
    parser.add_argument("--ignore", type=str, nargs="*", help="Ignore patterns (wildcards supported, only for ignore mode)")
    parser.add_argument("--files", type=str, nargs="*", help="Manual file list (only for manual mode)")
    args = parser.parse_args()

    output_file = args.output
    copy_contents_to_appendix(
        args.folder,
        output_file,
        args.skip_folder,
        args.mode,
        ignore_patterns=args.ignore,
        manual_files=args.files
    )
    print("\n**Success**\n\n")
    print(
        "WARNING: This is in .txt for editing before you convert it to pdf.\nEditing before converting highly recommended as there might be bugs"
    )


if __name__ == "__main__":
    main()
