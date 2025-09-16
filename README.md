# Bitvavo to Parqet CSV Converter

A Python script that fetches your Bitvavo trades (specifically BTC-EUR) via the official API and converts them into a CSV file that is ready for import into Parqet.

## Features

- Fetches trade history for one or more cryptocurrencies (e.g., BTC, ETH) against EUR.
- Fetches EUR cash deposit history.
- Formats all data according to Parqet's CSV import requirements.
- Uses a secure `.env` file to handle API credentials and configuration.
- Includes a simple `run.sh` script to automate the process.

## Requirements

- Python 3.x

## Setup & Installation

1.  **Clone the Repository**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-directory>
    ```

2.  **Create and Activate Virtual Environment**
    This project requires a virtual environment to manage dependencies without affecting your system's Python installation.

    ```bash
    # Create the virtual environment
    python3 -m venv .venv

    # Activate it (you'll need to do this every time you work on the project)
    source .venv/bin/activate
    ```

3.  **Install Dependencies**
    With the virtual environment active, install the required Python libraries.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure API Credentials & Holding ID**
    The script reads your Bitvavo API credentials and your Parqet Holding ID from an `.env` file.

    - Create a file named `.env` in the project root.
    - Add your credentials and ID in the following format:

      ```
      BITVAVO_API_KEY=your_64_character_api_key
      BITVAVO_API_SECRET=your_api_secret
      PARQET_HOLDING_ID=your_parqet_cash_account_holding_id
      CRYPTO_SYMBOLS=BTC,ETH,SOL
      ```
    - **`CRYPTO_SYMBOLS` (Optional):** A comma-separated list of crypto symbols you want to export. If you don't add this line, it will default to `BTC`.

    - **Important:** Ensure your Bitvavo API key has the "View Information" permission.
    - **Finding your Parqet Holding ID:**
        1. In Parqet, navigate to your cash account (e.g., "Verrechnungskonto").
        2. Copy the URL from your browser. It will look like this: `https://app.parqet.com/p/.../h/hld_68a9c778d99c5d158e5900d6`.
        3. The Holding ID is the complete string **after** `/h/`, including the `hld_` prefix. In the example, it's `hld_68a9c778d99c5d158e5900d6`.

## Usage

1.  **Make the Run Script Executable**
    You only need to do this once.
    ```bash
    chmod +x run.sh
    ```

2.  **Run the Script**
    Execute the `run.sh` script. It will automatically activate the virtual environment and run the Python script for you.
    ```bash
    ./run.sh
    ```

## Output

After the script runs successfully, you will find a `parqet.csv` file in the project directory. This file can be directly uploaded to Parqet.
