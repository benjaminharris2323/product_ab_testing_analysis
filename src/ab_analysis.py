import pandas as pd
from pathlib import Path
from statsmodels.stats.proportion import proportions_ztest
import matplotlib.pyplot as plt

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "ab_test_data.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

df = pd.read_csv(DATA_PATH)

# ----------------------------
# Overall Conversion Rates
# ----------------------------
summary = df.groupby("group")["converted"].agg(["sum", "count"])
summary["conversion_rate"] = summary["sum"] / summary["count"]

print("\nConversion Rates:")
print(summary)

# ----------------------------
# A/B Test
# ----------------------------
successes = summary["sum"].values
samples = summary["count"].values

z_stat, p_value = proportions_ztest(successes, samples)

print("\nA/B Test Results:")
print(f"Z-statistic: {z_stat:.4f}")
print(f"P-value: {p_value:.4f}")

# Absolute lift (percentage points)
lift = summary.loc["B", "conversion_rate"] - summary.loc["A", "conversion_rate"]

# Relative lift (percent improvement over control)
relative_lift = lift / summary.loc["A", "conversion_rate"]

print(f"\nLift (B - A): {lift:.2%}")
print(f"Relative Lift: {relative_lift:.2%}")

if p_value < 0.05:
    print("Result: Statistically significant improvement → Recommend rollout")
else:
    print("Result: No statistically significant difference → Do not roll out")

# ----------------------------
# Segment Analysis
# ----------------------------
print("\nConversion by Device:")
device_summary = df.groupby(["device", "group"])["converted"].mean().unstack()
print(device_summary)

print("\nDevice-Level Lift (B vs A):")
device_lift = device_summary["B"] - device_summary["A"]
device_relative_lift = device_lift / device_summary["A"]

device_results = pd.DataFrame({
    "absolute_lift": device_lift,
    "relative_lift": device_relative_lift
})

print(device_results)

# ----------------------------
# Visualization
# ----------------------------
OUTPUT_DIR.mkdir(exist_ok=True)

labels = ["Control (A)", "Treatment (B)"]
rates = [
    summary.loc["A", "conversion_rate"],
    summary.loc["B", "conversion_rate"]
]

plt.figure()
plt.bar(labels, rates)
plt.title("Conversion Rate by Group")
plt.ylabel("Conversion Rate")

file_path = OUTPUT_DIR / "conversion_rate_comparison.png"
plt.savefig(file_path)
plt.close()

print(f"\nChart saved to: {file_path}")