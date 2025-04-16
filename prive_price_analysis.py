import streamlit as st
import pandas as pd

st.title("CSV File Uploader with Filters")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)

    # Columns to remove
    columns_to_remove = [
        "Street Name", "Type of Area", "Nett Price($)",
        "Property Type", "Number of Units", "Tenure", "Market Segment"
    ]

    # Drop those columns if they exist
    df_display = df.drop(columns=[col for col in columns_to_remove if col in df.columns])

    st.write("### Original Data (Filtered Columns)")
    st.dataframe(df_display)

    # Check if required columns exist
    if "Area (SQM)" in df.columns and "Floor Level" in df.columns:
        st.write("### Filters")

        # Filter for Area (SQM) using numeric inputs
        min_area = float(df["Area (SQM)"].min())
        max_area = float(df["Area (SQM)"].max())

        area_min_input = st.number_input("Minimum Area (SQM)", value=min_area, min_value=min_area, max_value=max_area)
        area_max_input = st.number_input("Maximum Area (SQM)", value=max_area, min_value=min_area, max_value=max_area)

        # Ensure min is not greater than max
        if area_min_input > area_max_input:
            st.warning("Minimum area cannot be greater than maximum area.")

        # Filter for Floor Level
        floor_levels = df["Floor Level"].dropna().unique()
        selected_floors = st.multiselect("Select Floor Level(s)", options=sorted(floor_levels), default=sorted(floor_levels))

        # Apply filters
        filtered_df = df[
            (df["Area (SQM)"] >= area_min_input) &
            (df["Area (SQM)"] <= area_max_input) &
            (df["Floor Level"].isin(selected_floors))
        ]

        # Drop unwanted columns again for filtered view
        filtered_df_display = filtered_df.drop(columns=[col for col in columns_to_remove if col in filtered_df.columns])

        st.write("### Filtered Data")
        st.dataframe(filtered_df_display)
    else:
        st.warning("The required columns 'Area (SQM)' and/or 'Floor Level' are not present in the uploaded file.")
else:
    st.info("Please upload a CSV file to proceed.")
