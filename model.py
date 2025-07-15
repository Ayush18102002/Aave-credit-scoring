def score_wallet(features_df):
    def score_row(row):
        score = 100
        if row['num_liquidations'] > 0:
            score -= 200
        if row['repayment_ratio'] < 0.5:
            score -=300
        if row['deposit_to_borrow_ratio'] < 1:
            score -= 150
        if row['active_days'] < 3:
            score -= 100
        if row['days_since_last_tx'] > 180:
            score -= 50

        score += min(row['unique_tokens']*5,50)
        score += min(row['tx_count'],100)

        return max(0,min(1000,int(score)))
    
    features_df['score'] = features_df.apply(score_row,axis=1)
    return features_df[['wallet','score']]
