import ray
import modin.pandas as pd
import numpy as np

ray.init()
s3_path = "s3://<your bucket>/ray_recipe_output"
num_samples = 10000
df = pd.DataFrame({
      'id' : range(num_samples),
      'value' : np.random.randn(num_samples),
     })
result = df[df['value'] > 0]
print(f"Std Dev: {df['value'].std()}")
print(f"Out of {num_samples}, {result.shape[0]} will be saved after filtering")
result.to_parquet(s3_path)
