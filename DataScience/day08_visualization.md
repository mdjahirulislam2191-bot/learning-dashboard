# Day 08: ডেটা ভিজুয়ালাইজেশন (Matplotlib & Seaborn)
## Data Visualization with Matplotlib & Seaborn

### ভিজুয়ালাইজেশন কেন গুরুত্বপূর্ণ?
ডেটা ভিজুয়ালাইজেশন জটিল ডেটাকে সহজে বোধগম্য করে তোলে। এটি প্যাটার্ন, ট্রেন্ড এবং আউটলায়ার দ্রুত শনাক্ত করতে সাহায্য করে।

```python
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import numpy as np
import pandas as pd

# কনফিগারেশন
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 12
sns.set_style('whitegrid')
sns.set_palette('husl')

print(f"Matplotlib: {mpl.__version__}")
print(f"Seaborn: {sns.__version__}")
```

### Matplotlib বেসিক:
```python
# বেসিক লাইন প্লট
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

plt.figure(figsize=(10, 5))
plt.plot(x, y1, 'b-', linewidth=2, label='sin(x)')
plt.plot(x, y2, 'r--', linewidth=2, label='cos(x)')
plt.xlabel('X Values')
plt.ylabel('Y Values')
plt.title('Sine and Cosine Waves')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Multiple subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Line plot
axes[0, 0].plot(x, np.sin(x), 'b-')
axes[0, 0].set_title('Sine Wave')
axes[0, 0].grid(True, alpha=0.3)

# Scatter plot
x_scatter = np.random.randn(100)
y_scatter = np.random.randn(100)
axes[0, 1].scatter(x_scatter, y_scatter, alpha=0.6, c='red', edgecolors='black')
axes[0, 1].set_title('Random Scatter')

# Bar plot
categories = ['A', 'B', 'C', 'D', 'E']
values = np.random.randint(10, 50, 5)
axes[1, 0].bar(categories, values, color='steelblue', edgecolor='black')
axes[1, 0].set_title('Bar Chart')

# Histogram
data = np.random.randn(1000)
axes[1, 1].hist(data, bins=30, edgecolor='black', alpha=0.7, color='green')
axes[1, 1].set_title('Histogram')

plt.tight_layout()
plt.show()
```

### Seaborn স্টাইলিং ও থিম:
```python
# Seaborn স্টাইল
sns.set_theme()

# বিভিন্ন Seaborn থিম
themes = ['whitegrid', 'darkgrid', 'white', 'dark', 'ticks']

fig, axes = plt.subplots(2, 3, figsize=(15, 8))
axes = axes.flatten()

for idx, theme in enumerate(themes):
    with sns.axes_style(theme):
        ax = axes[idx]
        sns.histplot(np.random.randn(500), kde=True, ax=ax, color='steelblue')
        ax.set_title(f"Style: {theme}")

# Remove last subplot
axes[-1].axis('off')
plt.tight_layout()
plt.show()
```

### ডিস্ট্রিবিউশন প্লট:
```python
np.random.seed(42)
df = pd.DataFrame({
    'বেতন': np.random.normal(60000, 15000, 500),
    'বয়স': np.random.normal(35, 10, 500),
    'বিভাগ': np.random.choice(['IT', 'HR', 'Sales', 'Marketing'], 500)
})

# Distribution plots
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Histogram with KDE
sns.histplot(df['বেতন'], kde=True, bins=30, ax=axes[0, 0], color='steelblue')
axes[0, 0].set_title('Salary Distribution')

# KDE plot
sns.kdeplot(df['বেতন'], fill=True, ax=axes[0, 1], color='purple')
axes[0, 1].set_title('Salary KDE')

# Box plot
sns.boxplot(y=df['বেতন'], ax=axes[0, 2], color='lightgreen')
axes[0, 2].set_title('Salary Box Plot')

# Violin plot
sns.violinplot(y=df['বেতন'], ax=axes[1, 0], color='orange')
axes[1, 0].set_title('Salary Violin Plot')

# ECDF plot
sns.ecdfplot(df['বেতন'], ax=axes[1, 1], color='red')
axes[1, 1].set_title('ECDF Plot')

# Rug plot
sns.rugplot(df['বেতন'], ax=axes[1, 2], color='black', height=0.1)
sns.kdeplot(df['বেতন'], fill=True, ax=axes[1, 2], alpha=0.3)
axes[1, 2].set_title('KDE with Rug')

plt.tight_layout()
plt.show()
```

### রিলেশনাল প্লট:
```python
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Scatter plot
sns.scatterplot(x='বয়স', y='বেতন', data=df, ax=axes[0, 0], alpha=0.6)
axes[0, 0].set_title('Age vs Salary')

# Scatter with hue
sns.scatterplot(x='বয়স', y='বেতন', hue='বিভাগ', data=df, ax=axes[0, 1], alpha=0.6)
axes[0, 1].set_title('Age vs Salary by Department')

# Joint plot তৈরি করে ফিগারে দেখানো যাবে না, স্ক্যাটার দিয়ে
sns.regplot(x='বয়স', y='বেতন', data=df, ax=axes[0, 2], scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
axes[0, 2].set_title('Regression Plot')

# Pairwise scatter
# Hexbin
hb = axes[1, 0].hexbin(df['বয়স'], df['বেতন'], gridsize=20, cmap='Blues')
axes[1, 0].set_title('Hexbin Plot')
plt.colorbar(hb, ax=axes[1, 0])

# kde contour plot
sns.kdeplot(x='বয়স', y='বেতন', data=df, ax=axes[1, 1], cmap='viridis', fill=True)
axes[1, 1].set_title('2D KDE Contour')

# kde with contours
sns.kdeplot(x='বয়স', y='বেতন', data=df, ax=axes[1, 2], cmap='viridis', levels=5)
axes[1, 2].set_title('KDE Contour Levels')

plt.tight_layout()
plt.show()
```

### ক্যাটেগোরিকাল প্লট:
```python
# ক্যাটেগোরিকাল ডেটা ভিজুয়ালাইজেশন
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Bar plot
sns.countplot(x='বিভাগ', data=df, ax=axes[0, 0], palette='Set2')
axes[0, 0].set_title('Department Count')

# Point plot
sns.pointplot(x='বিভাগ', y='বেতন', data=df, ax=axes[0, 1], palette='Set2')
axes[0, 1].set_title('Average Salary by Department')

# Box plot
sns.boxplot(x='বিভাগ', y='বেতন', data=df, ax=axes[0, 2], palette='Set2')
axes[0, 2].set_title('Salary Distribution by Department')

# Violin plot
sns.violinplot(x='বিভাগ', y='বেতন', data=df, ax=axes[1, 0], palette='Set2')
axes[1, 0].set_title('Salary Violin by Department')

# Swarm plot (সাব-স্যাম্পল)
df_sample = df.sample(100)
sns.swarmplot(x='বিভাগ', y='বেতন', data=df_sample, ax=axes[1, 1], palette='Set2')
axes[1, 1].set_title('Salary Swarm (sample)')

# Boxen plot
sns.boxenplot(x='বিভাগ', y='বেতন', data=df, ax=axes[1, 2], palette='Set2')
axes[1, 2].set_title('Salary Boxen Plot')

plt.tight_layout()
plt.show()
```

### হিটম্যাপ ও কোরিলেশন ম্যাট্রিক্স:
```python
# Correlation heatmap
np.random.seed(42)
n = 200
df_corr = pd.DataFrame({
    'Feature_A': np.random.randn(n),
    'Feature_B': np.random.randn(n) * 0.5 + 0.3,
    'Feature_C': np.random.randn(n) * 0.8,
    'Feature_D': np.random.randn(n) * 0.3 + 0.7,
    'Feature_E': np.random.randn(n) * 0.6 - 0.2,
    'Target': np.random.randn(n) * 1.5
})

# Correlation matrix
corr = df_corr.corr()

plt.figure(figsize=(10, 8))

# Heatmap
sns.heatmap(corr, annot=True, cmap='RdBu_r', center=0, 
            square=True, linewidths=1, cbar_kws={"shrink": 0.8},
            fmt='.2f', annot_kws={'size': 10})
plt.title('Feature Correlation Heatmap', fontsize=14)
plt.tight_layout()
plt.show()

# Clustered heatmap
sns.clustermap(corr, annot=True, cmap='RdBu_r', center=0, 
               square=True, linewidths=1, fmt='.2f',
               figsize=(10, 8))
plt.suptitle('Clustered Correlation Heatmap', y=1.02)
plt.show()
```

### অ্যাডভান্সড ভিজুয়ালাইজেশন:
```python
# Pairplot
sns.pairplot(df, vars=['বেতন', 'বয়স'], hue='বিভাগ', palette='Set2', diag_kind='kde')
plt.suptitle('Pairplot: Salary and Age by Department', y=1.02)
plt.show()

# FacetGrid
g = sns.FacetGrid(df, col='বিভাগ', height=4, aspect=1.2)
g.map(sns.histplot, 'বেতন', kde=True, color='steelblue')
g.set_titles('{col_name}')
g.set_axis_labels('Salary', 'Count')
plt.suptitle('Salary Distribution by Department', y=1.02)
plt.show()

# Catplot
sns.catplot(x='বিভাগ', y='বেতন', kind='violin', data=df, height=5, aspect=1.5, palette='Set2')
plt.title('Salary Distribution by Department')
plt.tight_layout()
plt.show()
```

### কাস্টমাইজেশন ও ফরম্যাটিং:
```python
# সম্পূর্ণ কাস্টমাইজড প্লট
fig, ax = plt.subplots(figsize=(12, 6))

# ডেটা
categories = ['ঢাকা', 'চট্টগ্রাম', 'খুলনা', 'রাজশাহী', 'সিলেট']
values = [50000, 45000, 35000, 30000, 42000]
errors = [5000, 4000, 3000, 2500, 3500]

# বার প্লট
bars = ax.bar(categories, values, yerr=errors, capsize=5, 
              color=['#2196F3', '#FF5722', '#4CAF50', '#FFC107', '#9C27B0'],
              edgecolor='black', linewidth=1.5, alpha=0.9)

# কাস্টমাইজেশন
ax.set_xlabel('শহর', fontsize=14, fontweight='bold')
ax.set_ylabel('গড় বেতন (টাকা)', fontsize=14, fontweight='bold')
ax.set_title('শহর অনুযায়ী গড় বেতন - ২০২৪', fontsize=16, fontweight='bold', pad=20)
ax.set_ylim(0, 65000)
ax.grid(axis='y', alpha=0.3, linestyle='--')

# ভ্যালু লেবেল
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 1000,
            f'{int(height):,}', ha='center', va='bottom', fontsize=12, fontweight='bold')

# ট্রেন্ড লাইন
ax.plot(categories, values, 'o-', color='red', linewidth=2, markersize=8, label='Trend')
ax.legend()

plt.tight_layout()
plt.show()
```

### সেভিং ও এক্সপোর্ট:
```python
# প্লট সেভ করা
fig, ax = plt.subplots()
ax.plot(x, np.sin(x))
ax.set_title('Sample Plot')

# বিভিন্ন ফরম্যাটে সেভ
plt.savefig('plot.png', dpi=150, bbox_inches='tight')
plt.savefig('plot.pdf', dpi=150, bbox_inches='tight')
plt.savefig('plot.svg', dpi=150, bbox_inches='tight')
print("Plot saved in PNG, PDF, and SVG formats!")
plt.show()
```

### সারসংক্ষেপ:
- Matplotlib বেসিক প্লট (line, scatter, bar, histogram)
- Seaborn ডিস্ট্রিবিউশন প্লট (histogram, KDE, box, violin)
- রিলেশনাল প্লট (scatter, regplot, hexbin)
- ক্যাটেগোরিকাল প্লট (count, boxen, swarm)
- হিটম্যাপ, কোরিলেশন ও ক্লাস্টারিং
- কাস্টমাইজেশন, FacetGrid, Pairplot
- ফিগার সেভ ও এক্সপোর্ট