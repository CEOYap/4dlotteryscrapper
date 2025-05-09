## Description
A python script which uses `Playwright` for asynchronous web scraping of previous `Grand Dragon 4D` lottery results from `check4d.org` and outputs an .xlsx. The excel sheet can be further imported into Postgres for further analysis or processing via postgres.py.
## Key Features

- Uses `Playwright` for asynchronous\parallel scraping and processing
- Extracts Grand Dragon 4D past results  from check4d.org
- Easily configurable for other companies in check4d.org by replacing `id` 
- `postgres.py` allows import of xlsx to your Postgres database
## Requirements

- Python 3.x
- [`pandas` library](https://pandas.pydata.org/)
- [`openpyxl` library](https://pypi.org/project/openpyxl/)
- [`playwright`library](https://playwright.dev/python/)
- [`psycopg`  library](https://www.psycopg.org/psycopg3/)

## Usage

1. Download repo as a zip file and extract files. (You can also easily run the script with [Google Colab](https://colab.research.google.com/) with `main_googlecolab.ipynb`)
2. **Install Libraries:**
```bash
pip install pandas pandas openpyxl playwright psycopg
```
3. Followed with:
```bash
playwright install
```
4.  Open main.py with your favourite editor and configure it your liking
```bash
BASE_URL = "https://www.check4d.org/past-results/"
START_DATE = date(2020, 5, 4)  #Extract from which date
END_DATE = date.today() #Extract until wwhich date
EXCEL_FILENAME = "check4d_pastresults_GD4D.xlsx" #Output name
PAGE_LOAD_TIMEOUT = 45000 # Max amount of time to wait for page to load completely, if page doesn't load it will throw an error
ACTION_TIMEOUT = 15000 # Max amount of time to wait for actions to be done (i.e finding class id or element)
DELAY_BETWEEN_REQUESTS = 3.0 # Adds delay between next  requests to prevent server overload or being flagged as a bot
COMPANY_NAME = "Grand Dragon 4D" #Serves as organising purpose on excel output
MAX_CONCURRENT_REQUESTS = 5 #How many dates can it process in a single time. Adjust based on your PC capabilities
```
5. Run python script
```bash
python main.py
```
6. Output will look as follows:
   ![[example.jpg]]
7. From here you can do all sorts of analysis or simulation you want:
    - Heatmaps
    - Winning digit position weighting
    - Machine Learning
    - [Martingale simulation](https://en.wikipedia.org/wiki/Martingale_(betting_system))
8. (OPTIONAL) Import .xlsx (Store them in `input_docs` folder) to Postgres by running postgres.py. Adjust the following to your configuration.
```bash
DB_HOST = "localhost"
DB_NAME = "lottery_db"
DB_USER = "yourusername"
DB_PASSWORD = "yourpassword"
DB_PORT = 5432
```
## Limitations

-  **Limited to Grand Dragon 4D**: Scraping data for other companies requires significant changes to the code. As the first 3 companies in check4d.org (Magnum4D, Da Ma Cai, and Sports Toto4D) uses class-based selectors (`resulttop`, `resultbottom`)
- **No Data Deduplication**: Script does not check for any duplicated data before saving
## License

Released under the [MIT License](https://opensource.org/licenses/MIT).