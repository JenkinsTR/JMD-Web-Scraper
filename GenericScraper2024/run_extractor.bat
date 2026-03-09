@echo off

set "SCRIPT_PATH=K:\GitHub\JMD-Web-Scraper\GenericScraper2024\extract_links.py"
set "INPUT_FILE_PATH=K:\GitHub\JMD-Web-Scraper\GenericScraper2024\urls.txt"
set "OUTPUT_FILE_PATH=K:\GitHub\JMD-Web-Scraper\GenericScraper2024\extracted_links.txt"

python "%SCRIPT_PATH%" "%INPUT_FILE_PATH%" "%OUTPUT_FILE_PATH%"
pause
