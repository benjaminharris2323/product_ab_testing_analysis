import pandas as pd
import numpy as np
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "ab_test_data.csv"

np.random.seed(42)

n = 1000

data = pd.DataFrame({
    "user_id": range(1, n + 1),
    "group": np.random.choice(["A", "B"], size=n),
    "device": np.random.choice(["mobile", "desktop"], size=n),
    "country": np.random.choice(["US", "CA", "UK"], size=n)
})

# Simulate conversion
def simulate_conversion(row):
    base_rate = 0.10  # 10% baseline

    if row["group"] == "B":
        base_rate += 0.03  # treatment improves conversion

    if row["device"] == "mobile":
        base_rate -= 0.02

    return np.random.rand() < base_rate

data["converted"] = data.apply(simulate_conversion, axis=1).astype(int)

data.to_csv(DATA_PATH, index=False)

print(f"Dataset saved to: {DATA_PATH}")