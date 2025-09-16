import csv
from datetime import datetime, timezone
from python_bitvavo_api.bitvavo import Bitvavo
from dotenv import load_dotenv
import os

def main():
    """
    Main function to fetch Bitvavo trades and convert them to a Parqet compatible CSV file.
    """
    load_dotenv()
    api_key = os.getenv('BITVAVO_API_KEY')
    api_secret = os.getenv('BITVAVO_API_SECRET')
    parqet_holding_id = os.getenv('PARQET_HOLDING_ID')
    crypto_symbols_str = os.getenv('CRYPTO_SYMBOLS', 'BTC') # Default to BTC if not set

    if not api_key or not api_secret:
        print("Error: BITVAVO_API_KEY or BITVAVO_API_SECRET not found in .env file.")
        print("Please create a .env file with your API key and secret.")
        print("Example .env file content:")
        print("BITVAVO_API_KEY=your_api_key")
        print("BITVAVO_API_SECRET=your_api_secret")
        return
        
    if not parqet_holding_id:
        print("Error: PARQET_HOLDING_ID not found in .env file.")
        print("Please add your Parqet cash account holding ID to the .env file.")
        print("Example: PARQET_HOLDING_ID=632753972193856f22ee6618")
        return

    bitvavo = Bitvavo({
        'APIKEY': api_key,
        'APISECRET': api_secret
    })

    # --- Fetch Trades ---
    symbols_to_fetch = [symbol.strip().upper() for symbol in crypto_symbols_str.split(',')]
    all_trades = []
    print(f"Fetching trades for the following symbols: {', '.join(symbols_to_fetch)}")

    for symbol in symbols_to_fetch:
        market = f"{symbol}-EUR"
        print(f"Fetching trades for {market}...")
        trades = bitvavo.trades(market, {})
        if 'error' in trades:
            print(f"Could not fetch trades for {market}: {trades['error']}")
            continue
        all_trades.extend(trades)
    
    print(f"Found a total of {len(all_trades)} trades.")


    # --- Fetch Deposits ---
    print("Fetching deposit history for EUR...")
    # Passing no symbol should return all deposits, we will filter for EUR
    deposits = bitvavo.depositHistory({})
    if 'error' in deposits:
        print(f"Could not fetch deposits: {deposits['error']}")
        deposits = []
    
    eur_deposits = [d for d in deposits if d.get('symbol') == 'EUR']
    print(f"Found a total of {len(eur_deposits)} EUR deposits.")

    parqet_data = []

    # --- Process Trades ---
    for trade in all_trades:
        market = trade['market']
        base_currency, quote_currency = market.split('-')
        
        parqet_row = {
            'datetime': datetime.fromtimestamp(trade['timestamp'] / 1000, timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z'),
            'price': str(trade['price']).replace('.', ','),
            'shares': str(trade['amount']).replace('.', ','),
            'tax': '0',
            'fee': str(trade['fee']).replace('.', ','),
            'type': 'Buy' if trade['side'] == 'buy' else 'Sell',
            'assetType': 'Crypto',
            'identifier': base_currency,
            'currency': quote_currency,
            'amount': str(float(trade['price']) * float(trade['amount'])).replace('.', ',')
        }
        parqet_data.append(parqet_row)

    # --- Process Deposits ---
    for deposit in eur_deposits:
        parqet_row = {
            'datetime': datetime.fromtimestamp(deposit['timestamp'] / 1000, timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z'),
            'amount': str(deposit['amount']).replace('.', ','),
            'tax': '0',
            'fee': str(deposit.get('fee', '0')).replace('.', ','),
            'type': 'TransferIn',
            'holding': parqet_holding_id
        }
        parqet_data.append(parqet_row)

    if not parqet_data:
        print("No trades or deposits to export.")
        return

    # Sort all activities by date
    parqet_data.sort(key=lambda x: x['datetime'])

    # Write to CSV
    filename = 'parqet.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        # Superset of all possible columns for both trades and deposits
        fieldnames = ['datetime', 'type', 'identifier', 'shares', 'price', 'amount', 'fee', 'tax', 'currency', 'assetType', 'holding']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';', quoting=csv.QUOTE_ALL, extrasaction='ignore')

        writer.writeheader()
        writer.writerows(parqet_data)
        
    print(f"Successfully exported {len(parqet_data)} activities to {filename}")

if __name__ == '__main__':
    main()
