import requests
import pandas as pd
url = "https://fake-store-api.mock.beeceptor.com/api/products"
response = requests.get(url)
data = response.json()
df = pd.DataFrame(data)
df.to_csv("products.csv", index=False)
print("Data successfully saved to products.csv")