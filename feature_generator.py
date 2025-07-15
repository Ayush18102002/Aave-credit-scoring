import pandas as pd
import json 
def generate_features(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    
    # Convert actionData to dictionary if it's a string
    def parse_action_data(x):
        if isinstance(x, dict):
            return x
        elif isinstance(x, str):
            try:
                return json.loads(x)
            except json.JSONDecodeError:
                return {}
        else:
            return {}

    df['actionData'] = df['actionData'].apply(parse_action_data)

    # Now safely extract amount and token
    df['amount'] = df['actionData'].apply(lambda x: x.get('amount', 0))
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0)
    df['token'] = df['actionData'].apply(lambda x: x.get('token', None))
    grouped = df.groupby('userWallet')

    features = []

    for wallet, group in grouped:
        deposits = group[group['action'] == 'deposit']['amount'].sum()
        borrows = group[group['action'] == 'borrow']['amount'].sum()
        repays = group[group['action'] == 'repay']['amount'].sum()
        liquidations = group[group['action'] == 'liquidationcall'].shape[0]

        tx_count = group.shape[0]
        unique_tokens = group['token'].nunique()
        active_days = group['timestamp'].dt.date.nunique()
        last_seen = (pd.Timestamp.now() - group['timestamp'].max()).days

        repayment_ratio = repays / borrows if borrows else 1
        deposit_to_borrow_ratio = deposits / borrows if borrows else 1


        features.append({
            'wallet': wallet,
            'total_deposits': deposits,
            'total_borrows': borrows,
            'repayment_ratio': repayment_ratio,
            'deposit_to_borrow_ratio': deposit_to_borrow_ratio,
            'num_liquidations': liquidations,
            'tx_count': tx_count,
            'unique_tokens': unique_tokens,
            'active_days': active_days,
            'days_since_last_tx': last_seen
        })

    return pd.DataFrame(features)