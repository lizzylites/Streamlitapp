import streamlit as st
import pandas as pd
import openpyxl

st.subheader("Winnability Index: Social Determinant Scoring")

# Tableau Public URL for the view
tableau_url = "https://public.tableau.com/views/IowaSocialDeterminantScoring/SummaryMap"

# HTML code to embed Tableau with dynamic sizing
tableau_html = f"""
    <div class='tableauPlaceholder' id='viz1727391933235' style='position: relative'>
        <noscript>
            <a href='#'>
                <img alt='Iowa Social Determinant Issue Scoring' 
                src='https://public.tableau.com/static/images/Io/IowaSocialDeterminantScoring/SummaryMap/1_rss.png' 
                style='border: none' />
            </a>
        </noscript>
        <object class='tableauViz' style='display:none;'>
            <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> 
            <param name='embed_code_version' value='3' /> 
            <param name='site_root' value='' />
            <param name='name' value='IowaSocialDeterminantScoring/SummaryMap' />
            <param name='tabs' value='no' />
            <param name='toolbar' value='yes' />
            <param name='static_image' value='https://public.tableau.com/static/images/Io/IowaSocialDeterminantScoring/SummaryMap/1.png' />
            <param name='animate_transition' value='yes' />
            <param name='display_static_image' value='yes' />
            <param name='display_spinner' value='yes' />
            <param name='display_overlay' value='yes' />
            <param name='display_count' value='yes' />
            <param name='language' value='en-US' />
        </object>
    </div>
    <script type='text/javascript'>
        var divElement = document.getElementById('viz1727391933235');                    
        var vizElement = divElement.getElementsByTagName('object')[0];                    
        vizElement.style.width='100%'; 
        vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    
        var scriptElement = document.createElement('script');                    
        scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    
        vizElement.parentNode.insertBefore(scriptElement, vizElement);
    </script>
"""

# Embed the Tableau visualization using HTML
st.components.v1.html(tableau_html, height=800)

# Create a two-column layout for the DataFrames
col1, col2 = st.columns([1, 1])  # Adjust column widths if needed

# Load the Excel file
file_path = '/Users/elizabethlites/Desktop/Vscode Practice/SD Scoring Final .xlsx'
sheets_dict = pd.read_excel(file_path, sheet_name=None)

# Create a dropdown menu to select a sheet in the left column
with col1:
    sheet_names = list(sheets_dict.keys())
    selected_sheet = st.selectbox("Select a DataFrame to view:", sheet_names)

    # Get the selected DataFrame
    df = sheets_dict[selected_sheet]

    # Remove the 99th row if the sheet is not 'Allscores' or 'Longdata'
    if selected_sheet not in ['Allscores', 'Longdata'] and len(df) > 99:
        df = df.drop(99)  # 99th row has index 98 since index is 0-based

    # Create a text input for filtering by county
    county_filter = st.text_input("Enter county name to filter:")

    # Filter the DataFrame based on the county input
    if county_filter:
        filtered_df = df[df['COUNTY'].str.contains(county_filter, case=False, na=False)]  # Adjust 'COUNTY' to your actual column name
    else:
        filtered_df = df

    # Display the filtered DataFrame
    st.dataframe(filtered_df.style.set_properties(**{'min-width': '150px'}), use_container_width=True)

# Display top 10 lowest Composite_Score in the right column
with col2:
    if 'Composite_Score' in filtered_df.columns:
        lowest_scores = filtered_df.nsmallest(10, 'Composite_Score')
        st.write(f"Top 10 Lowest Scoring Counties for '{selected_sheet}':")
        st.dataframe(lowest_scores[['COUNTY', 'Composite_Score']], use_container_width=True)
    else:
        st.write("Composite_Score column not found in this DataFrame.")

# Create a row for metrics below the two DataFrames
st.subheader("Category Metrics:")
excluded_keywords = ["Quantile", "Score", "quantile", "score", "COUNTY", "Category", "Region"]
filtered_columns = [col for col in df.columns if not any(keyword in col for keyword in excluded_keywords)]

# Display metrics in a horizontal format
if filtered_columns:
    metrics_list = "<ul style='list-style-type: none; padding: 0;'>" + "".join(f"<li style='display: inline; margin-right: 15px;'>{col}</li>" for col in filtered_columns) + "</ul>"
    st.markdown(metrics_list, unsafe_allow_html=True)
else:
    st.write("No metrics to display.")

# Create a hyperlink
st.subheader("Social Determinant County Scoring Iowa Map")
st.markdown("[View](https://public.tableau.com/shared/B6JQ6BSB3?:display_count=n&:origin=viz_share_link)")
