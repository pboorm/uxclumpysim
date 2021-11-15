"""
Streamlit app to show AGN spectrum as function of logNH
Copyright: Peter Boorman (2021)
"""

import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np

## pre-load cmap plasma_r
cmap_cols = [np.array([0.940015, 0.975158, 0.131326, 1.      ]), np.array([0.944152, 0.961916, 0.146861, 1.      ]), np.array([0.951726, 0.941671, 0.152925, 1.      ]), np.array([0.956808, 0.928152, 0.152409, 1.      ]), np.array([0.964021, 0.90795 , 0.14937 , 1.      ]), np.array([0.968443, 0.894564, 0.147014, 1.      ]), np.array([0.974443, 0.874622, 0.144061, 1.      ]), np.array([0.977995, 0.861432, 0.142808, 1.      ]), np.array([0.982653, 0.841812, 0.142303, 1.      ]), np.array([0.986509, 0.822401, 0.143557, 1.      ]), np.array([0.988648, 0.809579, 0.145357, 1.      ]), np.array([0.991209, 0.790537, 0.149377, 1.      ]), np.array([0.992505, 0.777967, 0.152855, 1.      ]), np.array([0.993851, 0.759304, 0.159092, 1.      ]), np.array([0.994355, 0.746995, 0.163821, 1.      ]), np.array([0.994553, 0.728728, 0.171622, 1.      ]), np.array([0.994324, 0.716681, 0.177208, 1.      ]), np.array([0.993456, 0.69881 , 0.186041, 1.      ]), np.array([0.991985, 0.681179, 0.195295, 1.      ]), np.array([0.990681, 0.669558, 0.201642, 1.      ]), np.array([0.98826 , 0.652325, 0.211364, 1.      ]), np.array([0.986345, 0.640969, 0.217948, 1.      ]), np.array([0.983041, 0.624131, 0.227937, 1.      ]), np.array([0.980556, 0.613039, 0.234646, 1.      ]), np.array([0.976428, 0.596595, 0.244767, 1.      ]), np.array([0.971835, 0.580382, 0.254931, 1.      ]), np.array([0.968526, 0.5697  , 0.261721, 1.      ]), np.array([0.963203, 0.553865, 0.271909, 1.      ]), np.array([0.959424, 0.543431, 0.278701, 1.      ]), np.array([0.953428, 0.52796 , 0.288883, 1.      ]), np.array([0.949217, 0.517763, 0.295662, 1.      ]), np.array([0.942598, 0.502639, 0.305816, 1.      ]), np.array([0.93799 , 0.492667, 0.312575, 1.      ]), np.array([0.930798, 0.477867, 0.322697, 1.      ]), np.array([0.923287, 0.463251, 0.332801, 1.      ]), np.array([0.918109, 0.453603, 0.339529, 1.      ]), np.array([0.910098, 0.439268, 0.34961 , 1.      ]), np.array([0.904601, 0.429797, 0.356329, 1.      ]), np.array([0.896131, 0.415712, 0.366407, 1.      ]), np.array([0.89034 , 0.406398, 0.37313 , 1.      ]), np.array([0.881443, 0.392529, 0.383229, 1.      ]), np.array([0.875376, 0.383347, 0.389976, 1.      ]), np.array([0.866078, 0.36966 , 0.400126, 1.      ]), np.array([0.856547, 0.356066, 0.410322, 1.      ]), np.array([0.850066, 0.347048, 0.417153, 1.      ]), np.array([0.840155, 0.33358 , 0.427455, 1.      ]), np.array([0.833422, 0.324635, 0.434366, 1.      ]), np.array([0.823132, 0.311261, 0.444806, 1.      ]), np.array([0.816144, 0.302368, 0.451816, 1.      ]), np.array([0.805467, 0.289057, 0.462415, 1.      ]), np.array([0.794549, 0.27577 , 0.473117, 1.      ]), np.array([0.787133, 0.266922, 0.480307, 1.      ]), np.array([0.775796, 0.253658, 0.491171, 1.      ]), np.array([0.76809 , 0.244817, 0.498465, 1.      ]), np.array([0.756304, 0.231555, 0.509468, 1.      ]), np.array([0.748289, 0.222711, 0.516834, 1.      ]), np.array([0.736019, 0.209439, 0.527908, 1.      ]), np.array([0.72767 , 0.200586, 0.535293, 1.      ]), np.array([0.714883, 0.187299, 0.546338, 1.      ]), np.array([0.701769, 0.174005, 0.557296, 1.      ]), np.array([0.69284 , 0.165141, 0.564522, 1.      ]), np.array([0.67916 , 0.151848, 0.575189, 1.      ]), np.array([0.669845, 0.142992, 0.582154, 1.      ]), np.array([0.65558 , 0.129725, 0.592317, 1.      ]), np.array([0.645872, 0.120898, 0.598867, 1.      ]), np.array([0.631017, 0.107699, 0.608287, 1.      ]), np.array([0.620919, 0.098934, 0.614257, 1.      ]), np.array([0.605485, 0.085854, 0.622686, 1.      ]), np.array([0.589719, 0.072878, 0.630408, 1.      ]), np.array([0.579029, 0.064296, 0.635126, 1.      ]), np.array([0.562738, 0.051545, 0.641509, 1.      ]), np.array([0.551715, 0.043136, 0.645277, 1.      ]), np.array([0.534952, 0.031217, 0.650165, 1.      ]), np.array([0.523633, 0.024532, 0.652901, 1.      ]), np.array([0.506454, 0.016333, 0.656202, 1.      ]), np.array([0.489055, 0.010127, 0.658534, 1.      ]), np.array([0.477344, 0.00698 , 0.659549, 1.      ]), np.array([0.459623, 0.003574, 0.660277, 1.      ]), np.array([0.447714, 0.00208 , 0.66024 , 1.      ]), np.array([4.29719e-01, 8.31000e-04, 6.59425e-01, 1.00000e+00]), np.array([4.17642e-01, 5.64000e-04, 6.58390e-01, 1.00000e+00]), np.array([3.99411e-01, 8.59000e-04, 6.56133e-01, 1.00000e+00]), np.array([0.387183, 0.001434, 0.654177, 1.      ]), np.array([0.368733, 0.002724, 0.650601, 1.      ]), np.array([0.35015 , 0.004382, 0.646298, 1.      ]), np.array([0.337683, 0.005618, 0.643049, 1.      ]), np.array([0.318856, 0.007576, 0.63764 , 1.      ]), np.array([0.30621 , 0.008902, 0.633694, 1.      ]), np.array([0.287076, 0.010855, 0.627295, 1.      ]), np.array([0.274191, 0.012109, 0.622722, 1.      ]), np.array([0.254627, 0.013882, 0.615419, 1.      ]), np.array([0.241396, 0.014979, 0.610259, 1.      ]), np.array([0.221197, 0.016497, 0.602083, 1.      ]), np.array([0.200445, 0.017902, 0.593364, 1.      ]), np.array([0.186213, 0.018803, 0.587228, 1.      ]), np.array([0.16407 , 0.020171, 0.577478, 1.      ]), np.array([0.148607, 0.021154, 0.570562, 1.      ]), np.array([0.123903, 0.022878, 0.559423, 1.      ]), np.array([0.10598 , 0.024309, 0.551368, 1.      ]), np.array([0.075353, 0.027206, 0.538007, 1.      ])]

##

df = pd.read_csv("streamlit_uxclumpy.csv")
x_range = [np.log10(0.3), np.log10(350.)]
y_range = [np.log10(2.e-4), np.log10(9.)]

st.subheader("${\\tt UXCLUMPY}$ log $N_{\\rm H}$")

## controller
logNH_c = st.slider(
        "",
        min_value=21.,
        max_value=25.95,
        value = 24.,
        step=0.05,
        format="%.2f",
        key="",
    )

fig = px.line(
    df,
    x=df["E_keV"],
    y=df["lognh_%.2f" %(logNH_c)],
    log_x=True,
    log_y=True,
    width=1000,
    height=500,
    labels=dict(Flux="EFE / keV s-1 cm-2", Energy="Energy / keV"),
)

colour = "rgba(%s)" %(",".join(["%.5f" %(f) for f in cmap_cols[df.columns.get_loc("lognh_%.2f" %(logNH_c)) - 1]]))

## more info: https://plotly.com/python/axes/
fig.update_xaxes(ticks="inside", tickwidth = 2.5, ticklen = 10., linewidth = 2.5, linecolor = "black", mirror = True, gridcolor = "LightGray")
fig.update_yaxes(ticks="inside", tickwidth = 2.5, ticklen = 10., linewidth = 2.5, linecolor = "black", mirror = True, gridcolor = "LightGray")

fig.update_traces(line=dict(color=colour, width=4.))

fig.update_layout(plot_bgcolor = "rgba(0, 0, 0, 0)",
                  legend=dict(yanchor="top",
                              y=0.99,
                              xanchor="left",
                              x=0.01),
                  yaxis=dict(range=y_range,
                             title_text="EF<sub>E</sub> / arb.",
                             tickfont = dict(size=20),
                             tickvals=[1.e-3, 1.e-2, 1.e-1, 1.e0],
                             tickmode="array",
                             mirror="allticks",
                             side="top",
                             titlefont=dict(size=30)), 
                  xaxis=dict(range=x_range,
                             title_text="E / keV",
                             tickfont = dict(size=20),
                             tickvals=[1., 10., 100.],
                             tickmode="array",
                             mirror="allticks",
                             side="top",
                             titlefont=dict(size=30)))

## more here: https://plotly.com/python/configuration-options/
config = {'staticPlot': True}
st.plotly_chart(fig, use_container_width=True, config=config)
    

# st.sidebar.markdown("### Model outputs")
if st.checkbox("Show Table", False):
    st.subheader("Raw Data Table")
    st.write(df[["E_keV", "lognh_%.2f" %(logNH_c)]], index=False)

# Some advertising
st.markdown("[UXCLUMPY](https://github.com/JohannesBuchner/xars/blob/master/doc/uxclumpy.rst) [(Buchner et al., 2019)](https://ui.adsabs.harvard.edu/abs/2019A%26A...629A..16B/abstract), &copy; [Dr. Peter Boorman](https://www.peterboorman.com) & [Dr. Adam Hill](https://www.adambenhill.com)")
