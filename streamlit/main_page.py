import streamlit as st
import matplotlib.pyplot as plt
import yaml
from io import BytesIO

import utils

TITLE = "Himars Deployment"
st.set_page_config(
    page_title = TITLE,
    page_icon = "🚀",
    layout = "wide"
)
st.title(f"🚀 {TITLE} 🚀")
st.text("Use UTM Grids with Prefix. Example: 312302 123423")

### DATA
data = yaml.load(open("data_model.yaml","r"), Loader=yaml.FullLoader)
dof = None
cola, colb = st.columns([0.1,0.90])
with cola:
    if st.button("Demo"):
        data = yaml.load(open("demo.yaml","r"), Loader=yaml.FullLoader)
        dof = "2300"
with colb:
    if st.button("Clear"):
        data = yaml.load(open("data_model.yaml","r"), Loader=yaml.FullLoader)

#### FRONTEND ####
st.markdown("### HQ CSS")
colw, colx, coly, colz = st.columns(4)
with colw:  
    dof = st.text_input("DOF", value= utils.empty_or_None(dof))
with colx:  data["hq"]["brv"] = st.text_input("BRV", value=utils.empty_or_None(data["hq"]["brv"]))
with coly:  data["hq"]["bcp"] = st.text_input("BCP", value=utils.empty_or_None(data["hq"]["bcp"]))
with colz:  data["hq"]["css_ha"] = st.text_input("CSS_HA", value=utils.empty_or_None(data["hq"]["css_ha"]))

hq = []
for plt_element, grid  in data["hq"].items():
    if not grid: continue
    easting, northing = utils.get_easting_northing(grid)
    hq.append((easting, northing, plt_element))

plt1_tab, plt2_tab, bty_tab = st.tabs(["Platoon1", "Platoon2", "Battery"])

with plt1_tab:
    ### Front End
    st.markdown("### Platoon1")
    to_expand = False
    col1, col2, col3, col4 = st.columns(4)
    cola, colb, colc, cold = st.columns([0.15,0.3,0.3,0.3])

    with col1:  data["plt1"]["plt1_prv"] = st.text_input("PRV", key="plt1_prv", value=utils.empty_or_None(data["plt1"]["plt1_prv"]))
    with col2:  data["plt1"]["plt1_pcp"] = st.text_input("PCP", key="plt1_pcp", value=utils.empty_or_None(data["plt1"]["plt1_pcp"]))
    with col3:  data["plt1"]["plt1_rp1"] = st.text_input("RP1", key="plt1_rp1", value=utils.empty_or_None(data["plt1"]["plt1_rp1"]))
    with col4:  data["plt1"]["plt1_rp2"] = st.text_input("RP2", key="plt1_rp2", value=utils.empty_or_None(data["plt1"]["plt1_rp2"]))

    with cola:
        if st.button("Expand"): to_expand = True
        if st.button("Collaspe"): to_expand = False
    with colb:
        with st.expander("Launcher 1", expanded=to_expand):
            data["plt1"]["t1_fp1"] = st.text_input("FP1", key="t1_fp1", value=utils.empty_or_None(data["plt1"]["t1_fp1"]))
            data["plt1"]["t1_fp2"] = st.text_input("FP2", key="t1_fp2", value=utils.empty_or_None(data["plt1"]["t1_fp2"]))
            data["plt1"]["t1_hp1"] = st.text_input("HP1", key="t1_hp1", value=utils.empty_or_None(data["plt1"]["t1_hp1"]))
            data["plt1"]["t1_hp2"] = st.text_input("HP2", key="t1_hp2", value=utils.empty_or_None(data["plt1"]["t1_hp2"]))
    with colc:
        with st.expander("Launcher 2", expanded=to_expand):
            data["plt1"]["t2_fp1"] = st.text_input("FP1",  key="t2_fp1", value=utils.empty_or_None(data["plt1"]["t2_fp1"]))
            data["plt1"]["t2_fp2"] = st.text_input("FP2",  key="t2_fp2", value=utils.empty_or_None(data["plt1"]["t2_fp2"]))
            data["plt1"]["t2_hp1"] = st.text_input("HP1",  key="t2_hp1", value=utils.empty_or_None(data["plt1"]["t2_hp1"]))
            data["plt1"]["t2_hp2"] = st.text_input("HP2",  key="t2_hp2", value=utils.empty_or_None(data["plt1"]["t2_hp2"]))
    with cold:
        with st.expander("Launcher 3", expanded=to_expand):
            data["plt1"]["t3_fp1"] = st.text_input("FP1",  key="t3_fp1",  value=utils.empty_or_None(data["plt1"]["t3_fp1"]))
            data["plt1"]["t3_fp2"] = st.text_input("FP2",  key="t3_fp2",  value=utils.empty_or_None(data["plt1"]["t3_fp2"]))
            data["plt1"]["t3_hp1"] = st.text_input("HP1",  key="t3_hp1",  value=utils.empty_or_None(data["plt1"]["t3_hp1"]))
            data["plt1"]["t3_hp2"] = st.text_input("HP2",  key="t3_hp2",  value=utils.empty_or_None(data["plt1"]["t3_hp2"]))
    
    ### Data Processing
    plt1 = []
    plt1_fp = []
    for plt_element, grid  in data["plt1"].items():
        if not grid: continue
        easting, northing = utils.get_easting_northing(grid)

        if "fp" in plt_element:
            plt1_fp.append((easting, northing, plt_element))
        else:
            plt1.append((easting, northing, plt_element))

    ### Plot
    fig, ax = plt.subplots(figsize=(5,5))
    ax.set_title(f'Platoon Deployment: DOF {dof}')
    ax.set_xlabel('Easting')
    ax.set_ylabel('Northing')
    ax.grid(which="both", linestyle=":", linewidth=0.5, color='gray')
    ax.tick_params(axis='both', which='major', labelsize=6)

    if any(plt1):
        plt1_easting, plt1_northing, _ = utils.unzip(plt1)
        ax.scatter(plt1_easting, plt1_northing, color="blue",marker="s")
        for point in plt1:
            ax.annotate(point[2],(point[0],point[1]),size=6,ha="right",va="bottom")
    
    if any(plt1_fp):
        plt1_fp_easting, plt1_fp_northing, _ = utils.unzip(plt1_fp)
        ax.scatter(plt1_fp_easting, plt1_fp_northing, color="red",marker="x")
        for point in plt1_fp:
            ax.annotate(point[2],(point[0],point[1]),size=6,ha="right",va="bottom")

    # TODO: Draw DOF Arrow

    buf = BytesIO()
    plt.tight_layout()
    plt.axis('equal')
    fig.savefig(buf, format="png")
    st.image(buf)

    # TODO: Range Table, Mils Table with Violations


with plt2_tab:
    st.markdown("### Platoon2")
    to_expand = False
    col1, col2, col3, col4 = st.columns(4)
    cola, colb, colc, cold = st.columns([0.15,0.3,0.3,0.3])

    with col1:  data["plt2"]["plt2_prv"] = st.text_input("PRV", key="plt2_prv",  value=utils.empty_or_None(data["plt2"]["plt2_prv"]))
    with col2:  data["plt2"]["plt2_pcp"] = st.text_input("PCP", key="plt2_pcp",  value=utils.empty_or_None(data["plt2"]["plt2_pcp"]))
    with col3:  data["plt2"]["plt2_rp1"] = st.text_input("RP1", key="plt2_rp1",  value=utils.empty_or_None(data["plt2"]["plt2_rp1"]))
    with col4:  data["plt2"]["plt2_rp2"] = st.text_input("RP2", key="plt2_rp2",  value=utils.empty_or_None(data["plt2"]["plt2_rp2"]))

    with cola:
        if st.button("Expand", key="Expand2"): to_expand = True
        if st.button("Collaspe", key="Collaspe2"): to_expand = False
    with colb:
        with st.expander("Launcher 4", expanded=to_expand):
            data["plt2"]["t4_fp1"] = st.text_input("FP1", key="t4_fp1", value=utils.empty_or_None(data["plt2"]["t4_fp1"]))
            data["plt2"]["t4_fp2"] = st.text_input("FP2", key="t4_fp2", value=utils.empty_or_None(data["plt2"]["t4_fp2"]))
            data["plt2"]["t4_hp1"] = st.text_input("HP1", key="t4_hp1", value=utils.empty_or_None(data["plt2"]["t4_hp1"]))
            data["plt2"]["t4_hp2"] = st.text_input("HP2", key="t4_hp2", value=utils.empty_or_None(data["plt2"]["t4_hp2"]))
    with colc:
        with st.expander("Launcher 5", expanded=to_expand):
            data["plt2"]["t5_fp1"] = st.text_input("FP1",  key="t5_fp1", value=utils.empty_or_None(data["plt2"]["t5_fp1"]))
            data["plt2"]["t5_fp2"] = st.text_input("FP2",  key="t5_fp2", value=utils.empty_or_None(data["plt2"]["t5_fp2"]))
            data["plt2"]["t5_hp1"] = st.text_input("HP1",  key="t5_hp1", value=utils.empty_or_None(data["plt2"]["t5_hp1"]))
            data["plt2"]["t5_hp2"] = st.text_input("HP2",  key="t5_hp2", value=utils.empty_or_None(data["plt2"]["t5_hp2"]))
    with cold:
        with st.expander("Launcher 6", expanded=to_expand):
            data["plt2"]["t6_fp1"] = st.text_input("FP1",  key="t6_fp1", value=utils.empty_or_None(data["plt2"]["t6_fp1"]))
            data["plt2"]["t6_fp2"] = st.text_input("FP2",  key="t6_fp2", value=utils.empty_or_None(data["plt2"]["t6_fp2"]))
            data["plt2"]["t6_hp1"] = st.text_input("HP1",  key="t6_hp1", value=utils.empty_or_None(data["plt2"]["t6_hp1"]))
            data["plt2"]["t6_hp2"] = st.text_input("HP2",  key="t6_hp2", value=utils.empty_or_None(data["plt2"]["t6_hp2"]))

    plt2 = []
    plt2_fp = []
    for plt_element, grid  in data["plt2"].items():
        if not grid: continue
        easting, northing = utils.get_easting_northing(grid)

        if "fp" in plt_element:
            plt2_fp.append((easting, northing, plt_element))
        else:
            plt2.append((easting, northing, plt_element))

    # PLT 2
    fig, ax = plt.subplots(figsize=(5,5))
    ax.set_title(f'Platoon Deployment: DOF {dof}')
    ax.set_xlabel('Easting')
    ax.set_ylabel('Northing')
    ax.grid(which="both", linestyle=":", linewidth=0.5, color='gray')
    ax.tick_params(axis='both', which='major', labelsize=6)

    if any(plt2):
        plt2_easting, plt2_northing, _ = utils.unzip(plt2)
        ax.scatter(plt2_easting, plt2_northing, color="blue",marker="s")
        for point in plt2:
            ax.annotate(point[2],(point[0],point[1]),size=6,ha="right",va="bottom")
    
    if any(plt2_fp):
        plt2_fp_easting, plt2_fp_northing, _ = utils.unzip(plt2_fp)
        ax.scatter(plt2_fp_easting, plt2_fp_northing, color="red",marker="x")
        for point in plt2_fp:
            ax.annotate(point[2],(point[0],point[1]),size=6,ha="right",va="bottom")
    
    plt.tight_layout()
    plt.axis('equal')
    fig.savefig(buf, format="png")
    st.image(buf)

with bty_tab:
    # BTY
    fig, ax = plt.subplots(figsize=(5,5))
    ax.set_title(f'Platoon Deployment: DOF {dof}')
    ax.set_xlabel('Easting')
    ax.set_ylabel('Northing')
    ax.grid(which="both", linestyle=":", linewidth=0.5, color='gray')
    ax.tick_params(axis='both', which='major', labelsize=6)

    if any(plt1):
        plt1_easting, plt1_northing, _ = utils.unzip(plt1)
        ax.scatter(plt1_easting, plt1_northing, color="blue",marker="s")
        for point in plt1:
            ax.annotate(point[2],(point[0],point[1]),size=6,ha="right",va="bottom")
    
    if any(plt1_fp):
        plt1_fp_easting, plt1_fp_northing, _ = utils.unzip(plt1_fp)
        ax.scatter(plt1_fp_easting, plt1_fp_northing, color="red",marker="x")
        for point in plt1_fp:
            ax.annotate(point[2],(point[0],point[1]),size=6,ha="right",va="bottom")

    if any(plt2):
        plt2_easting, plt2_northing, _ = utils.unzip(plt2)
        ax.scatter(plt2_easting, plt2_northing, color="blue",marker="s")
        for point in plt2:
            ax.annotate(point[2],(point[0],point[1]),size=6,ha="right",va="bottom")
    
    if any(plt2_fp):
        plt2_fp_easting, plt2_fp_northing, _ = utils.unzip(plt2_fp)
        ax.scatter(plt2_fp_easting, plt2_fp_northing, color="red",marker="x")
        for point in plt2_fp:
            ax.annotate(point[2],(point[0],point[1]),size=6,ha="right",va="bottom")

    if any(hq):
        hq_easting, hq_northing, _ = utils.unzip(hq)
        ax.scatter(hq_easting, hq_northing, color="black",marker="^")
        for point in hq:
            ax.annotate(point[2],(point[0],point[1]),size=6,ha="right",va="bottom")
    
    plt.tight_layout()
    plt.axis('equal')
    fig.savefig(buf, format="png")
    st.image(buf)