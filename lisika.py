import streamlit as st
import joblib
import pandas as pd
df1 = pd.read_csv('business_data.csv')
df2 = pd.read_csv('education_data.csv')
df3 = pd.read_csv('entertainment_data.csv')
df4 = pd.read_csv('sports_data.csv')
df5 = pd.read_csv('technology_data.csv')
df = pd.concat([df1,df2,df3,df4,df5],ignore_index=True)
print(df)

# Get all unique categories for reference
all_categories = df['category'].unique()

# Streamlit UI
st.title("Find Indian Express Articles news by Category")

# User input: either select or type
user_input = st.text_input("Enter a category (e.g., business, sports, technology,education,entertainment):")

# Filter articles on button click
if st.button("Search"):
    user_input = user_input.lower().strip()
    matching_articles = df[df['category'].str.lower() == user_input]

    if matching_articles.empty:
        st.warning("No articles found for that category. Check spelling or try another.")
    else:
        st.success(f"Found {len(matching_articles)} articles in category '{user_input}'")
        for i, row in matching_articles.iterrows():
            st.markdown(f"### {row['headlines']}")
            st.write(row['description'])
            st.markdown(f"[Read more]({row['url']})")
            st.markdown("---")
