import streamlit as str
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# 🎨 Slide-Matching Aesthetic Page Config
str.set_page_config(page_title="IMMUTO 4.0 - SIR Simulator", layout="wide")

str.title("🧬 IMMUTO 4.0: Infectious Disease Epidemic Simulator")
str.markdown("### Computational Biology Framework for Predicting Human Health Risks")
str.write("---")

# 🎛️ Sidebar Controls (Sourced directly from your presentation script variables)
str.sidebar.header("🕹️ Real-Time Parameters")

# Variable 1: Vaccination Rate & Immunity
vaccination_rate = str.sidebar.slider("Variable 1: Vaccination Rate (%)", min_value=0, max_value=100, value=0, step=5) / 100.0

# Variable 2: Population Density (Simulating crowded urban environments vs rural)
pop_density = str.sidebar.slider("Variable 2: Population Density (People/sq km)", min_value=50, max_value=1000, value=200, step=50)

# Variable 3: Interventions (Mask-wearing, social distancing multiplier)
intervention = str.sidebar.select_slider(
    "Variable 3: Public Health Interventions",
    options=["None", "Mask Wearing", "Social Distancing", "Full Lockdown"],
    value="None"
)

# 🧮 Mathematical S-I-R Core Logic
# Baseline parameters
base_beta = 0.3   # Core transmission rate
gamma = 0.1       # Recovery rate (1 / days to recover)

# Adjust beta based on Population Density
density_multiplier = pop_density / 200.0  # Normalized around 200 people/sq km
beta = base_beta * density_multiplier

# Adjust beta based on Interventions
if intervention == "Mask Wearing":
    beta *= 0.7  # 30% reduction in transmission
elif intervention == "Social Distancing":
    beta *= 0.5  # 50% reduction in transmission
elif intervention == "Full Lockdown":
    beta *= 0.2  # 80% reduction in transmission

# Population Setup
Total_Population = 100000
# If population is vaccinated, they move straight to the Recovered/Immune group
Initial_Recovered = Total_Population * vaccination_rate
Initial_Infected = 10  # Start with 10 patient zeros
Initial_Susceptible = Total_Population - Initial_Infected - Initial_Recovered

# S-I-R Differential Equation Formulas
def S_I_R_deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

# Timeline array (160 simulation days)
t = np.linspace(0, 160, 160)
y0 = [Initial_Susceptible, Initial_Infected, Initial_Recovered]

# Integrate equations over time
ret = odeint(S_I_R_deriv, y0, t, args=(Total_Population, beta, gamma))
S, I, R = ret.T

# 📊 Render Modern Aesthetic Graphs
fig, ax = plt.subplots(figsize=(10, 5), facecolor='#0e1117')
ax.set_facecolor('#0e1117')

# Plot population curves with high contrast styling
ax.plot(t, S, 'cyan', alpha=0.8, lw=3, label='Susceptible [S]')
ax.plot(t, I, 'red', alpha=0.9, lw=4, label='Infected [I] (Epidemic Curve)')
ax.plot(t, R, 'limegreen', alpha=0.8, lw=3, label='Recovered/Immune [R]')

# Healthcare System Capacity Line
healthcare_threshold = Total_Population * 0.15
ax.axhline(healthcare_threshold, color='orange', linestyle='--', lw=2, label='Healthcare Capacity Line')

# Style Customizations
ax.set_title("Epidemic Progression Tracking Matrix", color='white', fontsize=14, pad=15)
ax.set_xlabel('Days Simulated', color='white')
ax.set_ylabel('Number of People', color='white')
ax.tick_params(colors='white')
ax.grid(color='#333333', linestyle=':', alpha=0.5)

# Dynamic legend text color matching dark mode canvas
legend = ax.legend(facecolor='#0e1117', edgecolor='#333333')
for text in legend.get_texts():
    text.set_color('white')

# Display variables in columns for clear visual presentation
col1, col2 = str.columns([3, 1])

with col1:
    str.pyplot(fig)

with col2:
    str.metric("Peak Active Infections", f"{int(max(I)):,}")
    
    # Live alert system to impress judges based on slider selections
    if max(I) > healthcare_threshold:
        str.error("❌ CRITICAL RISK: Epidemic curve breaches healthcare infrastructure threshold limits.")
    else:
        str.success("✅ STABLE: Curve flattens below crisis capabilities.")
