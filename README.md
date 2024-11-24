# Lightspeed Categorization Tool

## Overview

A Python CLI tool for querying domain categorizations via the Lightspeed Systems API. Supports both single and bulk domain queries, as well as filtering domains by category, stored in `ls.json`.

## Features

- Fetch domain categories from Lightspeed's API.
- Query single domains or process bulk domains via `links.txt`.
- Filter domains by category using predefined mappings.
- Clean and user-friendly CLI with `rich` formatting.

## Installation

1. Clone the repository and navigate to it:

   ```bash
   git clone https://github.com/your-username/lightspeed-categorization-tool.git
   cd lightspeed-categorization-tool
   ```
3. Install required dependencies:

   ```bash
   pip install requirements.txt
   ```
## Usage
Run with `python main.py` for the CLI. This project also supports the following arguments:
```
usage: python main.py [-h] [--bulk-cr] [-d DOMAIN] [-filter CATEGORY_NAME]

A tool for domain categorization and filtering.

options:
  -h, --help            Show this help message and exit.
  --bulk-cr             Bulk query: Check categories for all domains in 'links.txt'.
  -d DOMAIN, --d DOMAIN
                        Query a single domain (e.g., 'example.com').
  -filter CATEGORY_NAME
                        Filter domains by category (e.g., 'security.proxy').

```



## License
This project is Licensed under the MIT License. See [LICENSE](https://github.com/silentsparrows/lightspeed-categorization-tool/blob/main/LICENSE) for details.
