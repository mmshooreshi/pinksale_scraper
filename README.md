# ⚡️ Supercharged Pinksale Scraper ⚡️
---

Welcome to the **Ultimate Pinksale Scraper**. 🕷️ This project automates the collection of data from Pinksale's web pages using Selenium and undetected-chromedriver. It gathers detailed information about various tokens on the Pinksale platform and stores this information in structured CSV files for easy analysis.


```plaintext
                (
                 )
                (
          /\  .-"""-.  /\
         //\\/  ,,,  \//\\
         |/\| ,;;;;;, |/\|
         //\\\;-"""-;///\\
        //  \/   .   \/  \\
       (| ,-_| \ | / |_-, |)
         //`__\.-=-./__`\\
        // /.-(() ())-.\ \\
       (\ |)   '---'   (| /)
        ` (|           |) `
          \)           (/

```

---

This is a hobby project, as a help to my friend.

---

## 📁 Project Structure

- `INPUTS/`: Input data for the base URL scraper, including lists of URLs to scrape.
- `OUTPUTS/`: Output data from the final scraper.
- `README.md`: Project documentation.
- `requirements.txt`: Dependencies required by the project.
- `scrape_new.py`: Main script for scraping individual token pages.
- `scrape_urls.py`: Script for processing the `/leaderboards` page to generate a list of URLs.

---

## 🚀 Quickstart Guide

### Prerequisites
- **Python 3.10**
- **Chrome WebDriver**

---

### 📜 Installation

Clone the repository:
```sh
git clone https://github.com/mmshooreshi/pinksale-scraper.git
cd pinksale-scraper
```

Install dependencies:
```sh
pip install -r requirements.txt
```

Set up a virtual environment:
```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

---

### 🖥️ Usage on Windows PowerShell

1. **Activate Virtual Environment**:
    ```powershell
    Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
    .\venv\Scripts\Activate.ps1
    ```

2. **Run the Scraper**:
    ```powershell
    .\run_pinksale_scraper.ps1
    ```

3. **Follow the Prompts**: Enter the weeks to process when prompted.

---

### 🐧 Usage on Linux / macOS

1. **Activate Virtual Environment**:
    ```sh
    source venv/bin/activate
    ```

2. **Run the Scraper**:
    ```sh
    ./run_pinksale_scraper.sh
    ```

3. **Follow the Prompts**: Enter the weeks to process when prompted.

---

### 🐳 Docker Setup

1. **Build Docker Image**:
    ```sh
    docker-compose build
    ```

2. **Run Docker Container**:
    ```sh
    docker-compose up
    ```

---

### ⚙️ How it Works

- **`scrape_urls.py`**: Gathers URLs for specified weeks.
- **`scrape_new.py`**: Extracts detailed data from each URL.
- **Shell and PowerShell Scripts**: Automate the workflow.

### Detailed Usage

#### Generating URLs for Scraping

Run the following command to process the `/leaderboards` page and generate a list of URLs:
```bash
python scrape_urls.py <comma-separated-weeks>
```
This will create two types of CSV files in the `INPUTS/` directory:
- `Week-XX-YYYY.csv`: Basic token data including IDs, names, symbols, total raised, finish time, and URLs.
- `Week-XX-YYYY_links.csv`: Only the URLs for each token.

#### Extracting Detailed Token Data

To scrape detailed data for each URL found in the `_links.csv` files, use:
```bash
python scrape_new.py
```
This script processes each URL and saves detailed token and pool data to `OUTPUTS/Week-XX-YYYY_links_extracted_data.csv`.

---

## 🏗️ Contributing

Contributions are welcome! Clone, create a branch, and open a PR. Let's make this the best scraper ever!

---

## 📜 License

Released under [CC0 License](LICENSE).

Feel free to reach out for any questions or suggestions!
