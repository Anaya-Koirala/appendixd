import argparse
import os


def is_skippable(file, skippable_extensions):
    return any(file.endswith(ext) for ext in skippable_extensions)


def copy_contents_to_appendix(start_dir, output_file, user_skip_folder):
    skippable_extensions = [
        ".exe",
        ".db",
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".pdf",
        ".pyc",
        ".gitignore",
        ".bin",
    ]
    auto_skip_folders = ["venv", "__pycache__", ".git", user_skip_folder]

    with open(output_file, "w", encoding="utf-8") as output_txt:
        for root, dirs, files in os.walk(start_dir, topdown=True):
            dirs[:] = [d for d in dirs if d not in auto_skip_folders]
            for file in files:
                if is_skippable(file, skippable_extensions):
                    print(f"Skipped {file}")
                    continue

                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as infile:
                        content = infile.read()
                        output_txt.write(f"File: {file}\n\n{content}\n\n\n")
                except UnicodeDecodeError:
                    print(f"Skipping file due to encoding issue: {file_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert your code into an appendix.\nNote: This is converted to .txt for editing before you convert it to pdf.\nEditing before converting highly recommended as there might be bugs"
    )
    parser.add_argument("--folder", type=str, help="Folder to Convert", required=True)
    parser.add_argument("--skip-folder", type=str, help="Folder to Skip", default="")

    parser.add_argument(
        "--output", type=str, help="Output filename", default="appendix.txt"
    )
    args = parser.parse_args()

    output_file = args.output
    copy_contents_to_appendix(args.folder, output_file, args.skip_folder)
    print("\n**Success**\n\n")
    print(
        "WARNING: This is in .txt for editing before you convert it to pdf.\nEditing before converting highly recommended as there might be bugs"
    )


if __name__ == "__main__":
    main()
