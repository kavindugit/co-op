import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="ගම්මාන දත්ත පද්ධතිය",
    page_icon="🏘️",
    layout="wide"
)


# 2. Load Data Function
@st.cache_data
def load_data():
    try:
        # Load the CSV file
        df = pd.read_csv("data_coop.csv", encoding='utf-8')

        # --- DATA CLEANING ---
        if 'Village' in df.columns:
            df['Village'] = df['Village'].astype(str).str.strip()

        if 'SirialNo' in df.columns:
            df['SirialNo'] = df['SirialNo'].astype(str).str.replace(r'\.0$', '', regex=True)

        df = df.fillna("")
        return df

    except FileNotFoundError:
        st.error("⚠️ 'data_coop.csv' ගොනුව හමු නොවීය.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"දත්ත ලබා ගැනීමේ දෝෂයක්: {e}")
        return pd.DataFrame()


# Load the data
df = load_data()

# 3. Main App Layout
if not df.empty:
    st.title("🏘️ සාමාජික තොරතුරු")

    # --- SIDEBAR CONTROLS ---
    with st.sidebar:
        st.header("සැකසුම් (Settings)")

        # --- MODE SWITCHER ---
        mode = st.radio(
            "ක්‍රමවේදය තෝරන්න (Select Mode):",
            ["තනි (Single)", "බහු (Multi)"],
            index=0,
            horizontal=True
        )

        st.write("---")

        # Get list of villages
        village_list = sorted(df['Village'].unique().tolist())

        # Initialize variables
        selected_single = None
        selected_multi = []

        # --- CONDITIONAL INPUTS ---
        if mode == "තනි (Single)":
            # SINGLE MODE
            placeholder_text = "--- තෝරන්න (Select) ---"
            village_list_with_ph = [placeholder_text] + village_list

            selected_single = st.selectbox(
                "ගම්මානය:",
                options=village_list_with_ph,
                index=0
            )
        else:
            # MULTI MODE
            selected_multi = st.multiselect(
                "ගම්මාන (Villages):",
                options=village_list,
                placeholder="ගම්මාන එකතු කරන්න..."
            )

            if len(selected_multi) > 0:
                if st.button("තේරීම් ඉවත් කරන්න (Clear)"):
                    selected_multi = []

        st.write("---")
        st.caption("Developed by **Kavindu Herath**")
        st.caption("For Co-op Data Management")

    # --- MAIN CONTENT LOGIC ---

    # 1. LOGIC: SINGLE MODE
    if mode == "තනි (Single)":
        if selected_single == placeholder_text:
            st.info("👈 **ආරම්භ කිරීමට:**")
            st.markdown("""
            **ජංගම දුරකථන (Mobile):** ඉහළ වම් කෙළවරේ ඇති ඊතලය **( > )** ඔබා මෙනුවෙන් **ගම්මානයක්** තෝරන්න.
            """)
            st.metric(label="මුළු සාමාජිකයින් (System Total)", value=len(df))
        else:
            filtered_data = df[df['Village'] == selected_single]

            st.subheader(f"📍 {selected_single}")
            st.caption(f"සාමාජිකයින් ගණන: {len(filtered_data)}")

            st.dataframe(
                filtered_data,
                use_container_width=True,
                hide_index=True,
                height=500,
                column_config={
                    "SirialNo": st.column_config.TextColumn("අංකය", width="small"),
                    "MemberNo": st.column_config.TextColumn("සා.අංකය", width="small"),
                    "NIC": "ජා.හැ. අංකය",
                    "Name": "නම",
                    "Address": "ලිපිනය",
                    "Gender": "ස්ත්‍රී/පුරු",
                    "Village": None
                }
            )

    # 2. LOGIC: MULTI MODE (UPDATED)
    else:
        if not selected_multi:
            st.info("👈 **බහු-තේරීම් (Multi Mode):**")
            st.write("මෙනුවෙන් (Sidebar) ඔබට අවශ්‍ය **ගම්මාන කිහිපයක්** එකතු කරගන්න.")
            st.metric(label="මුළු සාමාජිකයින් (System Total)", value=len(df))
        else:
            # Filter Data
            filtered_data = df[df['Village'].isin(selected_multi)]

            # --- NEW: Calculate Individual Counts ---
            # This creates a count of how many members in each selected village
            village_counts = filtered_data['Village'].value_counts()

            # 1. Show Grand Total Prominently
            st.subheader(f"📊 මුළු එකතුව (Total Sum): {len(filtered_data)}")

            # 2. Show Breakdown (List of Counts)
            # using an expander keeps it clean on mobile, but 'expanded=True' keeps it open
            with st.expander("විස්තරාත්මක ගණන් බැලීම් (View Counts)", expanded=True):
                for village in selected_multi:
                    # Get count safely, default to 0 if empty
                    count = village_counts.get(village, 0)
                    st.write(f"🔹 **{village}**: {count}")

            st.markdown("---")

            # Table
            st.dataframe(
                filtered_data,
                use_container_width=True,
                hide_index=True,
                height=500,
                column_config={
                    "SirialNo": st.column_config.TextColumn("අංකය", width="small"),
                    "MemberNo": st.column_config.TextColumn("සා.අංකය", width="small"),
                    "NIC": "ජා.හැ. අංකය",
                    "Name": "නම",
                    "Address": "ලිපිනය",
                    "Gender": "ස්ත්‍රී/පුරු",
                    "Village": st.column_config.TextColumn("ගම්මානය", width="medium")
                }
            )

else:
    st.info("දත්ත පූරණය වෙමින් පවතී... (Waiting for data)")
