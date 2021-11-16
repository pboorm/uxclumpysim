"""
Streamlit app to show AGN spectrum as function of logNH
Copyright: Peter Boorman (2021)
"""

import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np
from matplotlib.pyplot import get_cmap
from matplotlib.colors import Normalize, rgb2hex
import cmasher as cmr

df = pd.read_csv("streamlit_uxclumpy.csv")
x_range = [np.log10(0.3), np.log10(250.)]
y_range = [np.log10(2.e-4), np.log10(0.99)]

test_df = (df.set_index("E_keV")
                  .unstack()
                  .reset_index()
                  .rename(columns={"level_0": "log N(H)", 0: "EFE"}))

test_df["log N(H)"] = test_df["log N(H)"].map(lambda x: float(x.split("_")[-1]))

y_range_lin = [10 ** v for v in y_range]
x_range_lin = [10 ** v for v in x_range]

cmap = get_cmap('cmr.cosmic_r')
norm = Normalize(vmin = 19., vmax = 26.)
cmap_cols = cmap(norm(test_df["log N(H)"]))
color_discrete_map = {lognh: rgb2hex(cmap_cols[i]) for i, lognh in enumerate(test_df["log N(H)"].values)}

## for line with colourscale: https://community.plotly.com/t/plotly-express-line-chart-color/27333/4
fig = px.line(test_df, x="E_keV",
              y="EFE",
              animation_frame="log N(H)",
              color="log N(H)",
              color_discrete_map=color_discrete_map,
              log_x = True,
              log_y=True,
              range_x=x_range_lin,
              range_y=y_range_lin,
              width=1000,
              height=600,
              )

st.subheader("${\\tt UXCLUMPY}$ log $N_{\\rm H}$")

## more info: https://plotly.com/python/axes/
fig.update_xaxes(ticks="inside", tickwidth = 2.5, ticklen = 10., linewidth = 2.5, linecolor = "black", mirror = True, gridcolor = "LightGray")
fig.update_yaxes(ticks="inside", tickwidth = 2.5, ticklen = 10., linewidth = 2.5, linecolor = "black", mirror = True, gridcolor = "LightGray")

fig.update_traces(line=dict(
                  width=4.))

fig.update_layout(
                  showlegend=False,
                  plot_bgcolor = "rgba(0, 0, 0, 0)",
                  legend=dict(yanchor="top",
                              y=0.99,
                              xanchor="left",
                              x=0.01),
                  yaxis=dict(
                             title_text="EF<sub>E</sub> / arb.",
                             tickfont = dict(size=20),
                             tickvals=[1.e-3, 1.e-2, 1.e-1],
                             tickmode="array",
                             mirror="allticks",
                             side="top",
                             titlefont=dict(size=30)), 
                  xaxis=dict(
                             title_text="E / keV",
                             tickfont = dict(size=20),
                             tickvals=[1., 10., 100.],
                             tickmode="array",
                             mirror="allticks",
                             side="top",
                             titlefont=dict(size=30)))

fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 30
fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 5

## more here: https://plotly.com/python/configuration-options/
config = {}#'staticPlot': True}
st.plotly_chart(fig, use_container_width=True, config=config)
    

# st.sidebar.markdown("### Model outputs")
# if st.checkbox("Show Table", False):
#     st.subheader("Raw Data Table")
    # st.write(df[["E_keV", "lognh_%.2f" %(logNH_c)]], index=False)

# Some advertising
st.markdown("[UXCLUMPY](https://github.com/JohannesBuchner/xars/blob/master/doc/uxclumpy.rst) [(Buchner et al., 2019)](https://ui.adsabs.harvard.edu/abs/2019A%26A...629A..16B/abstract), &copy; [Dr. Peter Boorman](https://www.peterboorman.com) & [Dr. Adam Hill](https://www.adambenhill.com)")
