# AppendixD

This Python code allows you to convert the contents of a specified directory into a single appendix document.


## Features

-   **Selective Conversion**: Converts text-based files while skipping over binary and image files (e.g., `.exe`, `.db`, `.png`, `.jpg`, `.gif`, `.pdf`, `.pyc`).


## Usage

To use the script, navigate to the directory
```bash

python appendixd.py --folder <path_to_folder> [--skip-folder <folder_to_skip>] [--output <output_filename>]

```

### Parameters:

-   `--folder`: The path to the folder containing the files you want to convert. (Required)
-
-   `--skip-folder`: Skip any folder (Optional)
-   `--output`: The name of the output file. (Optional, Default=`appendix.txt` )

### Example:

```bash

python appendixd.py --folder ./my_project --skip-folder temp --output my_project_appendix.txt

```

## Todo

- Add support for other languages, this too focused on python

- Minmalist and Sleek GUI


