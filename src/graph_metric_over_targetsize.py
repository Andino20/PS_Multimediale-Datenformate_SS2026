import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

IQMS = ['brisque', 'niqe', 'nima', 'clip']

df = pd.read_csv('data.csv')

df['jpeg_variant'] = df['jpeg_variant'].str.upper().str.replace('J2K', 'JPEG2000')
df = df.rename(columns={'jpeg_variant': 'Format'})

for iqm in IQMS:
    g = sns.relplot(data=df, kind='line',
                x='target_size_kb', y=iqm,
                hue='Format', style='Format')
    
    g.set_axis_labels(
        x_var="Target Size (KB)", 
        y_var=iqm.upper(), 
        fontsize=12, 
        fontweight='bold'
    )

    plt.savefig(f'{iqm}_over_targetsize.pdf')
