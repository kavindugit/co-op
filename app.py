import streamlit as st
import pandas as pd

# 1. Page Configuration
# layout="wide" is crucial for mobile to use the full screen width
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
        # Ensure 'Village' column exists and clean it
        if 'Village' in df.columns:
            df['Village'] = df['Village'].astype(str).str.strip()

        # Fix formatting for Serial Numbers
        if 'SirialNo' in df.columns:
            df['SirialNo'] = df['SirialNo'].astype(str).str.replace(r'\.0$', '', regex=True)

        # Fill missing values
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
    # App Title
    st.title("🏘️ සාමාජික තොරතුරු")

    # --- SIDEBAR: VILLAGE SELECTION ---
    with st.sidebar:
        st.header("තේරීම් කරන්න")

        # Get unique, sorted list of villages
        village_list = sorted(df['Village'].unique().tolist())

        # Placeholder option
        placeholder_text = "--- තෝරන්න (Select) ---"
        village_list.insert(0, placeholder_text)

        # Selectbox
        selected_village = st.selectbox(
            "ගම්මානය (Village):",
            options=village_list,
            index=0
        )

        st.write("---")
        st.caption("Developed for Co-op Data Management")

    # --- MAIN CONTENT LOGIC ---

    # Check if a village is selected
    if selected_village == placeholder_text:
        # --- MOBILE FRIENDLY INSTRUCTION ---
        # On mobile, the sidebar is hidden. We must tell them to open it.
        st.info("👈 **ආරම්භ කිරීමට:**")
        st.markdown("""
        1. ** ජංගම දුරකථන (Mobile):** ඉහළ වම් කෙළවරේ ඇති ඊතලය **( > )** ඔබා මෙනුව ලබාගන්න.
        2. ** පරිගණක (Laptop):** වම්පස මෙනුවෙන් ගම්මානය තෝරන්න.
        """)

        # Show total count as a quick stat
        st.metric(label="මුළු සාමාජිකයින් (All Members)", value=len(df))

    else:
        # Filter Data
        filtered_data = df[df['Village'] == selected_village]

        # Use columns to stack nicely on mobile
        # On mobile, these will appear one after another
        st.markdown("---")
        st.subheader(f"📍 {selected_village}")
        st.caption(f"සාමාජිකයින් ගණන: {len(filtered_data)}")

        # --- MOBILE OPTIMIZED TABLE ---
        # use_container_width=True ensures it fills the phone screen
        # Users can scroll horizontally to see Address/NIC
        st.dataframe(
            filtered_data,
            use_container_width=True,
            hide_index=True,
            height=500,  # Fixed height makes scrolling easier on mobile
            column_config={
                "SirialNo": st.column_config.TextColumn("අංකය", width="small"),
                "MemberNo": st.column_config.TextColumn("සා.අංකය", width="small"),
                "NIC": "ජා.හැ. අංකය",
                "Name": "නම",
                "Address": "ලිපිනය",
                "Gender": "ස්ත්‍රී/පුරු",
                "Village": None  # Hide Village as it's repetitive
            }
        )

else:
    st.info("දත්ත පූරණය වෙමින් පවතී... (Waiting for data)")