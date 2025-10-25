import numpy as np
from scipy.stats import chi2_contingency, chi2, norm

ai_names = ['default', 'beginner', 'intermediate', 'expert', 'worse']

# Data for each run [successes, failures]
runs = {
    'Run 1': np.array([
        [521, 1000-521],  # default
        [590, 1000-590],  # beginner
        [552, 1000-552],  # intermediate
        [532, 1000-523],  # expert
        [560, 1000-560]   # worse
    ]),
    'Run 2': np.array([
        [483, 1000-483],
        [551, 1000-551],
        [519, 1000-519],
        [507, 1000-507],
        [519, 1000-519]
    ]),
    'Run 3': np.array([
        [515, 1000-515],
        [579, 1000-579],
        [548, 1000-548],
        [561, 1000-561],
        [545, 1000-545]
    ]),
    'Run 4': np.array([
        [517, 1000-517],
        [568, 1000-568],
        [553, 1000-553],
        [520, 1000-520],
        [530, 1000-530]
    ]),
    'Run 5': np.array([
        [508, 1000-508],
        [572, 1000-572],
        [554, 1000-554],
        [524, 1000-524],
        [538, 1000-538]
    ])
}

# Store p-values for Fisher's method
p_values = []

# Perform chi-square test for each run
for run_name, contingency in runs.items():
    chi2_stat, p_value, dof, expected = chi2_contingency(contingency)
    p_values.append(p_value)
    print(f"\n{run_name}:")
    print(f"Chi-square statistic: {chi2_stat:.2f}")
    print(f"p-value: {p_value:.6f}")
    print(f"Degrees of freedom: {dof}")

# Fisher's method
chi_square = -2 * sum(np.log(p_values))
df = 2 * len(p_values)  # degrees of freedom = 2k
combined_p = chi2.sf(chi_square, df)

print(f"\nFisher's Combined Results:")
print(f"Combined Chi-square: {chi_square:.4f}")
print(f"Degrees of freedom: {df}")
print(f"Combined p-value: {combined_p:.8f}")

z_scores = norm.ppf(1 - np.array(p_values))  # Using 1-p because we want right-tail p-values
z_combined = sum(z_scores) / np.sqrt(len(z_scores))
stouffer_p = 1 - norm.cdf(z_combined)

print(f"\nStouffer's Combined Results:")
print(f"Combined Z-score: {z_combined:.4f}")
print(f"Combined p-value: {stouffer_p:.8f}")

# print sorted leaderboard
print("\nLeaderboard:")
for i, ai in enumerate(ai_names):
    print(f"{i+1}. {ai}")
