# 🤖 ContentForgeAI

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/)

<div align="center">
  <img src="https://raw.githubusercontent.com/exala/ContentForgeAI/main/Logo.png" alt="ContentForgeAI Logo" width="400">
</div>

ContentForgeAI is a powerful, all-in-one content creation pipeline that leverages AI to automate the entire process of writing, generating images for, and publishing articles directly to WordPress. This intuitive Streamlit application provides a user-friendly interface for both single-article generation and bulk processing from an Excel file.

## ✨ Features

-   **AI-Powered Content Generation**: Utilizes powerful language models to create high-quality, SEO-friendly articles on any topic. Specifically designed for AI/ML API. (https://aimlapi.com)
-   **Bulk Processing**: Upload an Excel file with a list of topics to generate dozens of articles in a single run.
-   **AI Featured Image Generation**: Automatically create a relevant, high-quality featured image for each article.
-   **Direct WordPress Publishing**: Seamlessly publish generated content and images directly to your WordPress site.
-   **Interactive UI**: A clean, modern web interface built with Streamlit for an easy user experience.
-   **Full Customization**:
    -   Select from multiple AI models.
    -   Set a target word count for articles.
    -   Toggle image generation and WordPress publishing on or off.
-   **Local Database Storage**: All generated articles are automatically saved to a local SQLite database.
-   **Data Export**: Download the entire article database with a single click from the sidebar.

## 🖼️ Application Preview

![ContentForgeAI Screenshot](https://github.com/exala/contentForgeAI-aiml/blob/main/Screenshot.PNG)

## 🛠️ Tech Stack

-   **Framework**: Streamlit
-   **Core Libraries**: Python, Pandas
-   **AI Services**: AIMLAPI (for text and image generation)
-   **Database**: SQLite

## 🚀 Getting Started

Follow these instructions to set up and run ContentForgeAI on your local machine.

### 1. Clone the Repository

First, clone the repository to your local machine using Git.

```bash
git clone https://github.com/exala/ContentForgeAI.git
cd ContentForgeAI
```

### 2. Clone the Repository

Create and Activate a Virtual Environment
It is highly recommended to use a virtual environment to manage project dependencies.

**Create the environment:**
```bash
python -m venv venv
```

**Activate the environment:**

- **On Windows:**
```bash
.\venv\Scripts\activate
```

- **On macOS & Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

Install all the required packages from the `requirements.txt` file using pip.

```bash
pip install -r requirements.txt
```

### 4. Run the Application

You are now ready to launch the Streamlit app!

```bash
streamlit run app.py
```

The application will automatically open in a new tab in your web browser. A welcome popup will guide you.

### 5. Configure Credentials in the App

Once the app is running, **all settings and credentials are managed in the sidebar on the left**. You will need to enter:
- **AIML API Key:** Your key for content and image generation.
- **WordPress URL:** The full URL to your WordPress site.
- **WordPress Username:** Your admin username.
- **WordPress Password:** IMPORTANT: This must be an Application Password, not your main user password. You can generate one from your WordPress admin dashboard under `Users > Profile > Application Passwords`.

## 📄 License
This project is licensed under the MIT License.

**MIT License**

Copyright (c) 2025 exala


Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:


The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.


THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
