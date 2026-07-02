import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data.csv')

df['size_delta_kb'] = df['target_size_kb'] - df['encoded_size_kb']
df['jpeg_variant'] = df['jpeg_variant'].str.upper().str.replace('J2K', 'JPEG2000')
df = df.rename(columns={'jpeg_variant': 'Format'})

g = sns.catplot(data=df, kind='box', col='Format', col_wrap=3, col_order=['JPEG', 'JPEG2000', 'JXL', 'JXR', 'JAI'],
            x='target_size_kb', y='size_delta_kb')

g.set_axis_labels(
    x_var="Target Size (KB)", 
    y_var="Size Δ (KB)", 
    fontsize=12,
)

g.map(plt.axhline, y=0, color="red", linestyle=":", linewidth=1)

plt.savefig('size_delta_plot.pdf')