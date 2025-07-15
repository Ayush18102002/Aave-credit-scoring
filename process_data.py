import json 
import pandas as pd

def load_json(filepath):
              with open(filepath, 'r') as f:
                data = json.load(f)
                return pd.DataFrame(data)
              
