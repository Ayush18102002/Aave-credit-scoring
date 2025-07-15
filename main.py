import pandas as pd
from src.process_data import load_json
from src.feature_generator import generate_features
from src.model import score_wallet
import matplotlib.pyplot as plt
import seaborn as sns

def categorize(score):
    if score >= 90:
        return 'Low Risk'
    elif score >= 50:
        return 'Medium Risk'
    else:
        return 'High Risk'
def main():
    df  = load_json('data/user-wallet-transactions.json')
    feature = generate_features(df)
    scores = score_wallet(feature)

        # Bucket logic
    bucket_labels = ["0–100", "100–300", "300–600", "600–900", "900–1000"]
    bucket_ranges = [0, 100, 300, 600, 900, 1000]

    scores['score_bucket'] = pd.cut(scores['score'], bins=bucket_ranges, labels=bucket_labels, right=True)
    bucket_counts = scores['score_bucket'].value_counts(sort=False).reset_index()
    bucket_counts.columns = ['Score Range', 'Wallet Count']

    print(bucket_counts.to_markdown(index=False))


    scores['risk_category'] = scores['score'].apply(categorize)

    scores.to_csv('outputs/scores.csv',index = False)   # saving the scores data

    high_risk = scores[scores['risk_category'] == 'High Risk']
    print("\n High-risk wallets:")
    print(high_risk[['wallet', 'score']].to_string(index=False))
          
    sns.histplot(scores['score'],bins =10)
    plt.title("Wallet Credit Score Distribution")
    plt.xlabel("Score")
    plt.ylabel("Number of Wallets")
    plt.savefig('outputs/score_distribution.png')
    plt.close()

if __name__=="__main__": 
    main()
