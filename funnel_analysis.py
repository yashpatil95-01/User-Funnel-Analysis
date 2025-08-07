import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = r"E:\PythonProjects\datasets\funnel_data.csv"
df = pd.read_csv(file_path)

# Calculate funnel counts
visit_count = len(df)
signup_count = df['signed_up'].sum()
add_to_cart_count = df['added_to_cart'].sum()
checkout_count = df['initiated_checkout'].sum()
purchase_count = df['purchased'].sum()

# Print funnel conversion counts
print("Funnel Counts:")
print(f"Visits: {visit_count}")
print(f"Sign Ups: {signup_count}")
print(f"Added to Cart: {add_to_cart_count}")
print(f"Initiated Checkout: {checkout_count}")
print(f"Purchases: {purchase_count}")

# Calculate conversion rates
conversion_rates = {
    "Visit → Sign Up": signup_count / visit_count,
    "Sign Up → Add to Cart": add_to_cart_count / signup_count,
    "Add to Cart → Checkout": checkout_count / add_to_cart_count,
    "Checkout → Purchase": purchase_count / checkout_count
}

print("\nConversion Rates:")
for step, rate in conversion_rates.items():
    print(f"{step}: {rate:.2%}")
