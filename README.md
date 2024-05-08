# Pinksale Scraping Project

This project automates the extraction of data from Pinksale's web pages using Selenium and undetected-chromedriver. The primary goal is to collect detailed information about various tokens listed on the Pinksale platform, including their launchpad data, and store this information in structured CSV files for further analysis or reporting.

## Project Structure

- `INPUTS/`: Contains input data for the base URL scraper, including lists of URLs to scrape.
- `OUTPUTS/`: Stores output data from the final scraper.
- `README.md`: Documentation for the project.
- `requirements.txt`: Lists all dependencies required by the project.
- `scrape_new.py`: Main Python script for scraping operations on individual token pages.
- `scrape_urls.py`: Python script that handles processing the `/leaderboards` page to generate a list of URLs for further extraction.

## Prerequisites

Before running the project, ensure that Python and pip are installed on your machine. It is recommended to use a virtual environment to manage dependencies.

### Setup Instructions

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Generating URLs for Scraping

Run the following command to process the `/leaderboards` page and generate a list of URLs:
```bash
python scrape_urls.py
```
This will create two types of CSV files in the `INPUTS/` directory:
- `Week-XX-YYYY.csv`: Contains basic token data including IDs, names, symbols, total raised, finish time, and URLs.
- `Week-XX-YYYY_links.csv`: Contains only the URLs for each token.

### Extracting Detailed Token Data

To scrape detailed data for each URL found in the `_links.csv` files, use:
```bash
python scrape_new.py
```
This script processes each URL and saves detailed token and pool data to `OUTPUTS/Week-XX-YYYY_links_extracted_data.csv`, structured as follows:

**Columns:**
- Audits, Token Address, Token Name, Symbol, Decimals, Total Supply
- Pool Address, Tokens for Presale, Tokens for Liquidity, Softcap
- Start Time, End Time, Listing on, Liquidity Percent, Liquidity Lockup Time
- Liquidity Unlocked Time, Status, Sale Type, Min Buy, Max Buy
- Current Rate, Current Raised, Total Contributors, Claim Time, Hard Cap Per User

## Contributing

Contributions are welcome. Please fork the repository and submit a pull request with your changes or improvements.

## License

This project is open-sourced under the MIT License.

## Contact

For any questions or feedback regarding this project, please feel free to contact me.