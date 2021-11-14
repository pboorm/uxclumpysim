"""
Streamlit app to show AGN spectrum as function of logNH
Copyright: Peter Boorman (2021)
"""

import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np

def find_nearest_ID(array, value):
    """
    Find nearest float in a numpy array of floats
    """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def gen_obscured_df(fd, logNH_chosen):
    """
    Function to return the obscured spectrum as a df with E_keV and spec as columns
    """
    fd["parameters"] = np.array([float(c.split("_")[-1]) for c in fd["cols"]])
    logNH_par = find_nearest_ID(fd["parameters"], logNH_chosen)

    df_new = fd["df"][["E_keV", fd["cols"][logNH_par]]]
    return df_new
    
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)

# DEGREE_SYMBOL = "\N{DEGREE SIGN}"

# units_choice = st.sidebar.selectbox('Choose y-axis units', ('uxclumpy', 'mytorus[coupled]', 'borus02', 'pexrav (R17B1)'))

# import matplotlib.pyplot as plt


fd = {}

fd["df"] = pd.read_csv("./uxclumpy_var_NH_v19.csv")
fd["cols"] = [c for c in fd["df"].columns if "E_keV" not in c]
fd["x_range"] = [np.log10(0.5), np.log10(350.)]
fd["y_range"] = [np.log10(2.e-4), np.log10(9.)]
# fd["y_label"] = r"$E$\,F$_{E}$\ $\longrightarrow$"#E$^{2}n({\rm E})\,/\,$keV$^{2}$\,s$^{-1}$\,cm$^{-2}$\,keV$^{-1}$"
# fd["x_label"] = r"E\,/\,keV\ $\longrightarrow$"
fd["vmin"] = 21.
fd["vmax"] = 26.
# fd["cmap"] = plt.get_cmap('PuOr_r')

# mod_df = fd["df"].melt(
#         id_vars=["E_keV"], value_vars=fd["cols"]
#     )

# print(mod_df)

# mod_df = mod_df.rename(columns={"variable": "lognh", "value": "spec"})
# fig_bkg = px.line(
#     mod_df,
#     x="E_keV",
#     y="spec",
#     color=,
#     log_x=True,
#     log_y=True,
#     width=1000,
#     height=700,
#     labels=dict(Flux="EFE / keV s-1 cm-2", Energy="Energy / keV"),
# )
# fig_bkg.update_layout(legend=dict(yanchor="top",
#                               y=0.99,
#                               xanchor="left",
#                               x=0.01),
#                   yaxis=dict(range=fd["y_range"]), 
#                   xaxis=dict(range=fd["x_range"]))

# st.plotly_chart(fig_bkg)


# st.sidebar.title("Parameters")

st.title("${\\tt uxclumpy}$ X-ray Simulator")

st.subheader("log $N_{\\rm H}$")
## controller
logNHtor_c = st.slider(
        "",
        min_value=21.,
        max_value=26.,
        value = 24.,
        step=0.1,
        format="%.1f",
        key="",
    )

df = gen_obscured_df(fd, logNHtor_c)

df_columns = df.columns
fig = px.line(
    df,
    x=df_columns[0],
    y=df_columns[1],
    log_x=True,
    log_y=True,
    width=775,
    height=680,
    labels=dict(Flux="EFE / keV s-1 cm-2", Energy="Energy / keV"),
)

## more info: https://plotly.com/python/axes/
fig.update_xaxes(ticks="inside", tickwidth = 2.5, ticklen = 10., linewidth = 2.5, linecolor = "black", mirror = True, gridcolor = "LightGray")
fig.update_yaxes(ticks="inside", tickwidth = 2.5, ticklen = 10., linewidth = 2.5, linecolor = "black", mirror = True, gridcolor = "LightGray")

fig.update_traces(line=dict(color="dodgerblue", width=4.))

fig.update_layout(plot_bgcolor = "rgba(0, 0, 0, 0)",
                  legend=dict(yanchor="top",
                              y=0.99,
                              xanchor="left",
                              x=0.01),
                  yaxis=dict(range=fd["y_range"],
                             title_text="EFE / arb.",
                             tickfont = dict(size=20),
                             tickvals=[1.e-3, 1.e-2, 1.e-1, 1.e0],
                             tickmode="array",
                             mirror="allticks",
                             side="top",
                             titlefont=dict(size=30)), 
                  xaxis=dict(range=fd["x_range"],
                             title_text="E / keV",
                             tickfont = dict(size=20),
                             tickvals=[1., 10., 100.],
                             tickmode="array",
                             mirror="allticks",
                             side="top",
                             titlefont=dict(size=30)))

st.plotly_chart(fig, use_container_width=True)
    

# st.sidebar.markdown("### Model outputs")
if st.checkbox("Show Table", False):
    st.subheader("Raw Data Table")
    st.write(df, index=False)

# Some advertising
st.markdown("[uxclumpy](https://github.com/JohannesBuchner/xars/blob/master/doc/uxclumpy.rst): [Buchner et al., (2019)](https://ui.adsabs.harvard.edu/abs/2019A%26A...629A..16B/abstract)")
st.markdown("App designed by: [Dr. Peter Boorman](https://www.peterboorman.com) & [Dr. Adam Hill](https://www.adambenhill.com)")
