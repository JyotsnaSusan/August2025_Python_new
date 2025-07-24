import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel("GDM_Python_Aug2025.xlsx")
df = data.copy()

st.title("Delivery Method Dashboard")
# Chart 1
st.subheader("Patient Distribution by History of GDM")


# Count and relabel
history_gdm = df['PreviousGDM10 V1'].value_counts().rename({0: 'No History of GDM', 1: 'Past History of GDM'})

# Plot
fig, ax = plt.subplots()
ax.pie(
    history_gdm,
    labels=history_gdm.index,
    autopct='%1.1f%%',
    startangle=90,
    colors=['lightcoral', 'blue']
)
#ax.set_title("Patient Distribution by History of GDM")

# Display in Streamlit
st.pyplot(fig)
##############################
# Chart 2
st.subheader("Delivery Method - Proportions by GDM Status")

# Step 1: Clean your data
df_clean = df[(df['GDM Diagonised'] != 'NR') & (df['Caesarean'] != 'NR')]

# Step 2: Calculate proportions within each GDM group
proportions = (
    df_clean.groupby('GDM Diagonised')['Caesarean']
    .value_counts(normalize=True)
    .unstack()
    .fillna(0) * 100
).round(1)

# Step 3: Prepare plot data
plot_data = pd.DataFrame({
    'GDM Diagonised': proportions.index,
    'Cesarean (%)': proportions[1],
    'Vaginal (%)': proportions[0]
})

# Step 4: Plot
fig, ax = plt.subplots(figsize=(7, 5))
bar_width = 0.4
x = range(len(plot_data))

# Bars
ax.bar(x, plot_data['Cesarean (%)'], width=bar_width, label='Cesarean', color='salmon')
ax.bar([i + bar_width for i in x], plot_data['Vaginal (%)'], width=bar_width, label='Vaginal', color='lightblue')

# Styling
ax.set_xticks([i + bar_width / 2 for i in x])
ax.set_xticklabels(plot_data['GDM Diagonised'])
ax.set_ylabel('Delivery Method Proportion (%)')
#ax.set_title('Delivery Method Proportions by GDM Status')
ax.legend()

# Annotate bars
for i in x:
    ax.text(i, plot_data['Cesarean (%)'].iloc[i] + 1,
             f"{plot_data['Cesarean (%)'].iloc[i]}%", ha='center')
    ax.text(i + bar_width, plot_data['Vaginal (%)'].iloc[i] + 1,
             f"{plot_data['Vaginal (%)'].iloc[i]}%", ha='center')

fig.tight_layout()

# Display in Streamlit
st.pyplot(fig)
########
#Chart 3
#Delivery Distribution
label_map = {0.0: 'Normal', 1.0: 'Cesarean', 'NR': 'NR'}
df['delivery_type_label'] = df['Caesarean'].map(label_map)

# Streamlit app layout
#st.title("Delivery Type Distribution")
st.subheader("Pie Chart of Delivery Methods")

# Plotting pie chart
fig, ax = plt.subplots(figsize=(6, 6))
df['delivery_type_label'].value_counts().plot(
    kind='pie',
    autopct='%1.1f%%',
    ax=ax)
ax.set_ylabel('')  # Hide y-axis label

# Show in Streamlit
st.pyplot(fig)
#############
# Chart 4
st.subheader("Histogram of Gestational Age at Delivery")

# 📊 Histogram
fig, ax = plt.subplots(figsize=(10, 6))
df['GA at delivery'].plot(
    kind='hist',
    bins=15,
    color='orchid',
    edgecolor='black',
    ax=ax
)
#ax.set_title("Histogram of Gestational Age at Delivery")
ax.set_xlabel("Gestational Age (Weeks)")
ax.set_ylabel("Frequency")
ax.grid(True)
plt.tight_layout()

# Display plot
st.pyplot(fig)

# 🧠 Categorize gestational age
def categorize_ga(ga_weeks):
    if ga_weeks < 28:
        return 'Extremely preterm'
    elif ga_weeks < 32:
        return 'Very preterm'
    elif ga_weeks < 37:
        return 'Moderate to late preterm'
    else:
        return 'Full term or later'

df['GA Category'] = df['GA at delivery'].apply(categorize_ga)

# 📋 Display counts per category
st.subheader("Categorized Gestational Age Distribution")
st.write(df['GA Category'].value_counts())