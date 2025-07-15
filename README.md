# Aave Credit Scoring

This project builds a credit score system (0–1000) for wallets interacting with the Aave V2 protocol based on raw transaction data.

## 📊 Features Used
- Total deposits, borrows
- Repayment ratio
- Liquidation count
- Token diversity
- Transaction count
- Activity frequency

## ⚙️ How to Run

1. Place `user_transactions.json` in the `data/` folder.
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the main script:
    ```bash
    python main.py
    ```

## 📁 Outputs
- `outputs/scores.csv`: Wallet-level scores
- `outputs/score_distribution.png`: Score distribution plot
