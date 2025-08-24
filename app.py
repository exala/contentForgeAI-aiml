import streamlit as st
import pandas as pd
import os

# --- Import Your Existing Modules ---
from modules import prompt_orchestrator, generate_content, post_processor, article_storage_manager, generate_image
from modules.wordpress_publisher import create_wordpress_post, upload_image_to_wordpress

# --- Page Configuration ---
st.set_page_config(
    page_title="ContentForgeAI",
    page_icon="🤖",
    layout="wide"
)

# --- Main Application ---
st.title("🤖 ContentForgeAI")
st.markdown("Your AI-powered content creation and publishing assistant.")

# --- Welcome Popup Logic ---
if 'show_instructions' not in st.session_state:
    st.session_state.show_instructions = True


@st.dialog("Welcome to ContentForgeAI!", width="large")
def show_welcome_message():
    # ... (dialog code remains the same)
    st.markdown("### Quick Start Guide")
    st.markdown("""
    This application helps you generate and publish AI-written articles in just a few clicks. Here's how to get started:

    **1. Set Your Credentials (in the Sidebar):**
    - **AI/ML API Key**: Your personal API key for the content and image generation service. (Get your API KEYS from https://aimlapi.com)
    - **WordPress Details**: Your site URL, username, and an **Application Password**. 
      *(Note: You must generate an Application Password from your WordPress profile page under "Users" -> "Profile")*.

    **2. Configure Your Article (in the Sidebar):**
    - **Choose a Model**: Select the AI model you want to use.
    - **Set Word Count**: Define the target length for your article.
    - **Generate Image**: Check this box if you want an AI-generated featured image.

    **3. Generate Content:**
    - **Single Topic**: Use the first tab to enter a topic and click "Generate".
    - **Bulk Processing**: Use the second tab to upload an Excel file with a list of topics.

    Ready to go? Just click the button below to close this guide.
    """)
    if st.button("Got it! Let's Start", type="primary"):
        st.session_state.show_instructions = False
        st.rerun()


if st.session_state.show_instructions:
    show_welcome_message()

# --- Sidebar ---
with st.sidebar:
    # --- NEW: Add Logo to the top of the sidebar ---
    logo_url = "https://raw.githubusercontent.com/exala/ContentForgeAI/main/Logo.png"
    st.image(logo_url, width=250)
    st.markdown("---")
    # --- END of new section ---

    st.header("Model Settings")
    model_options = [
        "openai/gpt-5-chat-latest",
        "openai/gpt-5-nano-2025-08-07",
        "openai/gpt-5-mini-2025-08-07",
        "openai/gpt-5-2025-08-07"
    ]
    selected_model = st.selectbox("Choose a content generation model:", model_options)
    word_count = st.number_input(
        "Set Target Word Count:",
        min_value=100,
        max_value=2000,
        value=800,
        step=50
    )

    generate_featured_image = st.checkbox("Generate a featured image")
    st.markdown("---")

    st.header("Credentials")
    st.markdown("Enter your credentials here for the current session.")

    api_key = st.text_input("AIML API Key", type="password", key="api_key")
    wp_url = st.text_input("WordPress URL", key="wp_url", placeholder="https://yourdomain.com")
    wp_user = st.text_input("WordPress Username", key="wp_user")
    wp_password = st.text_input("WordPress Password", type="password", key="wp_password")

    # Set all credentials and settings as environment variables
    if selected_model:
        os.environ['SELECTED_MODEL'] = selected_model
    if api_key:
        os.environ['AIML_API_KEY'] = api_key
    if wp_url:
        os.environ['WP_URL'] = wp_url
    if wp_user:
        os.environ['WP_USER'] = wp_user
    if wp_password:
        os.environ['WP_PASSWORD'] = wp_password

    st.markdown("---")

    st.header("Export Data")
    db_file_path = 'articles.db'
    if os.path.exists(db_file_path):
        with open(db_file_path, 'rb') as f:
            db_bytes = f.read()
        st.download_button(
            label="Download articles.db",
            data=db_bytes,
            file_name="articles.db",
            mime="application/octet-stream"
        )
    else:
        st.info("No database file found. Generate an article first to create it.")

# --- Main Content Area with Tabs ---
tab1, tab2 = st.tabs(["Single Topic Generation", "Excel Bulk Processing"])

# ... (The rest of your code for tab1 and tab2 remains exactly the same) ...
with tab1:
    st.header("Generate a Single Article")
    topic = st.text_input("Enter a keyword or topic", placeholder="e.g., 'Benefits of Solar Energy'")
    publish_to_wp = st.checkbox("Publish to WordPress", key="single_publish")
    generate_button = st.button("Generate Article")

    if generate_button and topic:
        if (publish_to_wp and not all([wp_url, wp_user, wp_password])) or not api_key:
            st.error("Please provide all API and WordPress credentials in the sidebar.")
        else:
            try:
                # 1. Generate Content
                with st.spinner(f"Generating content with `{selected_model}`..."):
                    prompt = prompt_orchestrator(topic, word_count)
                    raw_content = generate_content(prompt)
                    title, html_content = post_processor(raw_content)

                article_storage_manager(title, html_content, topic)
                st.success("Article generated and stored in the database!")

                # 2. Generate Image (if requested)
                generated_image_url = None
                if generate_featured_image:
                    with st.spinner("Generating featured image..."):
                        generated_image_url = generate_image(title)
                        if generated_image_url:
                            st.success("Image generated successfully!")
                        else:
                            st.warning("Could not generate an image.")

                # 3. Display Results
                with st.container(border=True):
                    st.subheader(title)
                    if generated_image_url:
                        st.image(generated_image_url, caption="Generated Featured Image")
                    st.markdown(html_content, unsafe_allow_html=True)
                    st.caption(f"Word Count: {len(html_content.split())}")

                # 4. Publish to WordPress (if requested)
                if publish_to_wp:
                    with st.spinner("Publishing to WordPress..."):
                        featured_media_id = None
                        if generated_image_url:
                            featured_media_id = upload_image_to_wordpress(generated_image_url, title)

                        success = create_wordpress_post(title, html_content, "publish", featured_media_id)
                        if success:
                            st.success("✅ Successfully published to WordPress!")
                        else:
                            st.error("❌ Failed to publish to WordPress.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

with tab2:
    st.header("Generate Articles in Bulk from Excel")
    uploaded_file = st.file_uploader("Upload an Excel file (.xlsx, .xls)", type=["xlsx", "xls"])

    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            st.success(f"Successfully uploaded `{uploaded_file.name}` with {len(df)} rows.")
            with st.expander("Preview Data", expanded=True):
                st.dataframe(df.head())

            column_name = st.selectbox("Select the column containing the topics:", df.columns)
            publish_bulk_to_wp = st.checkbox("Publish all articles to WordPress", key="bulk_publish")
            process_button = st.button("Generate All Articles from Excel")

            if process_button:
                if (publish_bulk_to_wp and not all([wp_url, wp_user, wp_password])) or not api_key:
                    st.error("Please provide all API and WordPress credentials in the sidebar.")
                else:
                    topics = df[column_name].dropna().tolist()
                    st.info(f"Starting to process {len(topics)} topics using `{selected_model}`...")
                    results_container = st.container(border=True)
                    progress_bar = st.progress(0)

                    for i, topic in enumerate(topics):
                        try:
                            results_container.write(f"---")
                            results_container.write(f"Processing topic ({i + 1}/{len(topics)}): **{topic}**")

                            # 1. Generate Content
                            prompt = prompt_orchestrator(topic, word_count)
                            raw_content = generate_content(prompt)
                            title, html_content = post_processor(raw_content)
                            article_storage_manager(title, html_content, topic)
                            result_msg = f"✅ **{topic}**: Generated '{title}' ({len(html_content.split())} words)."

                            # 2. Generate Image
                            generated_image_url = None
                            if generate_featured_image:
                                results_container.write("   - Generating image...")
                                generated_image_url = generate_image(title)
                                result_msg += " 🖼️ Image generated." if generated_image_url else " ⚠️ Image failed."

                            # 3. Publish to WordPress
                            if publish_bulk_to_wp:
                                featured_media_id = None
                                if generated_image_url:
                                    results_container.write("   - Uploading image to WordPress...")
                                    featured_media_id = upload_image_to_wordpress(generated_image_url, title)

                                results_container.write("   - Publishing post to WordPress...")
                                success = create_wordpress_post(title, html_content, "publish", featured_media_id)
                                result_msg += " 📝 Published." if success else " ❌ WP Post failed."

                            results_container.markdown(result_msg)

                        except Exception as e:
                            results_container.error(f"❌ **{topic}**: Failed with error - {e}")

                        # Update progress bar
                        progress_bar.progress((i + 1) / len(topics))
        except Exception as e:
            st.error(f"Error processing Excel file: {e}")