import streamlit as st
import pandas as pd
import numpy as np


st.title("Custom Kaya Identity for Urban Transport Emissions")

st.markdown("### Equation 1:")
st.latex(r"""
\frac{\text{CO₂}}{\text{Population}} =
\frac{\text{CO₂}}{\text{GDP}} \times
\frac{\text{GDP}}{\text{Area}} \times
\frac{\text{Area}}{\text{VKT}_{\text{public}}} \times
\frac{\text{VKT}_{\text{public}}}{\text{VKT}_{\text{private}}} \times
\frac{\text{VKT}_{\text{private}}}{\text{Fuel}} \times
\frac{\text{Fuel}}{\text{Population}}
""")

st.markdown("""
**Term Explanations:**

- $\dfrac{\\text{CO₂}}{\\text{GDP}}$ : CO₂ emissions per unit of GDP (carbon intensity of the economy).

- $\dfrac{\\text{GDP}}{\\text{Area}}$ : Economic output per unit area (urban economic density).

- $\dfrac{\\text{Area}}{\\text{VKT}_{\\text{public}}}$ : Public transport VKT per unit area (inverse) (public transport coverage efficiency).

- $\dfrac{\\text{VKT}_{\\text{public}}}{\\text{VKT}_{\\text{private}}}$ : Ratio of public to private transport usage (public transport share).

- $\dfrac{\\text{VKT}_{\\text{private}}}{\\text{Fuel}}$ : Private vehicle fuel efficiency.

- $\dfrac{\\text{Fuel}}{\\text{Population}}$ : Fuel consumption per capita.
""")

# separation line
st.markdown("---")

st.markdown("### Equation 2:")
st.latex(r"""
\frac{\text{CO₂}}{\text{Population}} =
\frac{\text{CO₂congestion}}{\text{GDP}}
\times \frac{\text{GDP}}{\text{Area}}
\times \frac{\text{Area}}{\text{VKT}_{\text{public}}}
""")
st.latex(r"""
\times \frac{\text{VKT}_{\text{public}}}{\text{VKT}_{\text{private}}}
\times \frac{\text{VKT}_{\text{private}}}{\text{Fuel}}
\times \frac{\text{Fuel}}{\text{Population}}
\times \alpha
\times \text{Gini}_{\text{CO₂}}
""")

# write the explanation
st.markdown("""**Term Explanations:**

- $\dfrac{\\text{CO₂congestion}}{\\text{GDP}}$ : CO₂ congestion emissions per unit of GDP.

- $\\alpha$ : A factor representing the impact of congestion on emissions.

- $\\text{Gini}_{\\text{CO₂}}$ : Gini coefficient for CO₂ emissions, representing inequality in emissions distribution.

Additionally, $\\alpha \\times \\text{Gini}_{\\text{CO₂}} = \\dfrac{\\text{CO₂}}{\\text{CO₂congestion}}$

            alpha is estimated using the ratio of total CO₂
            emissions to congestion-related CO₂ emissions.
""")