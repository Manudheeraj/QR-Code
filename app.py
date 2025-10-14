import io
import streamlit as st
from backend import QRCodeGenerator

# Page configs
st.set_page_config(
    page_title="QR Code Generator Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional Custom CSS
st.markdown("""
<style>
    /* Import Professional Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
     
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Background */
    .main {
        background: linear-gradient(135deg, #1a1c2e 0%, #2d1b4e 50%, #1a1c2e 100%);
        padding: 2rem;
    }
    
    /* Content Container */
    .block-container {
        background: rgba(30, 33, 54, 0.95);
        border-radius: 24px;
        padding: 3rem 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.5);
        max-width: 1400px;
        margin: 0 auto;
        border: 1px solid rgba(139, 92, 246, 0.2);
    }
    
    /* Title Styling */
    h1 {
        font-weight: 800 !important;
        font-size: 3.5rem !important;
        background: linear-gradient(135deg, #a78bfa 0%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem !important;
        letter-spacing: -2px;
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #a1a1aa;
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 3rem;
    }
    
    /* Section Headers */
    h2, h3 {
        font-weight: 700 !important;
        color: #e4e4e7 !important;
        letter-spacing: -0.5px;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: rgba(17, 24, 39, 0.6);
        padding: 8px;
        border-radius: 16px;
        border: 1px solid rgba(139, 92, 246, 0.3);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        border-radius: 12px;
        padding: 0 32px;
        font-weight: 700;
        font-size: 1rem;
        color: #a1a1aa;
        background-color: transparent;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%);
        color: white !important;
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.5);
    }
    
    /* Input Fields */
    .stTextArea textarea {
        border-radius: 12px !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        background: rgba(17, 24, 39, 0.6) !important;
        color: #e4e4e7 !important;
        font-size: 1rem !important;
        padding: 16px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: #8b5cf6 !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2) !important;
        background: rgba(17, 24, 39, 0.8) !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #71717a !important;
    }
    
    /* Input Labels */
    .stTextArea label, .stFileUploader label {
        color: #d4d4d8 !important;
        font-weight: 600 !important;
    }
    
    /* File Uploader */
    .stFileUploader {
        border: 2px dashed rgba(139, 92, 246, 0.4);
        border-radius: 16px;
        padding: 2rem;
        background: rgba(17, 24, 39, 0.6);
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: #8b5cf6;
        background: rgba(17, 24, 39, 0.8);
    }
    
    .stFileUploader label {
        color: #d4d4d8 !important;
    }
    
    .stFileUploader [data-testid="stFileUploaderDropzone"] {
        background: rgba(30, 33, 54, 0.8);
        border: 2px dashed rgba(139, 92, 246, 0.4);
        border-radius: 12px;
    }
    
    .stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] {
        color: #a1a1aa !important;
    }
    
    .stFileUploader button {
        background: rgba(139, 92, 246, 0.2) !important;
        color: #e4e4e7 !important;
        border: 1px solid rgba(139, 92, 246, 0.4) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    
    .stFileUploader button:hover {
        background: rgba(139, 92, 246, 0.3) !important;
        border-color: #8b5cf6 !important;
    }
    
    /* Color Picker Labels */
    .stColorPicker label {
        font-weight: 700 !important;
        color: #e4e4e7 !important;
        font-size: 0.95rem !important;
    }
    
    .stColorPicker > div {
        background: rgba(17, 24, 39, 0.6) !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        border-radius: 8px !important;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%);
        color: white;
        border-radius: 14px;
        border: none;
        padding: 18px 48px;
        font-weight: 700;
        font-size: 1.1rem;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 8px 24px rgba(139, 92, 246, 0.4);
        width: 100%;
        text-transform: uppercase;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 32px rgba(139, 92, 246, 0.6);
        background: linear-gradient(135deg, #7c3aed 0%, #9333ea 100%);
    }
    
    .stButton>button:active {
        transform: translateY(-1px);
    }
    
    /* Download Button */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border-radius: 14px;
        border: none;
        padding: 18px 48px;
        font-weight: 700;
        font-size: 1.1rem;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 8px 24px rgba(16, 185, 129, 0.4);
        width: 100%;
    }
    
    .stDownloadButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 32px rgba(16, 185, 129, 0.6);
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
    }
    
    /* Success/Warning/Error Messages */
    .stSuccess, .stWarning, .stError, .stInfo {
        border-radius: 12px;
        padding: 16px 20px;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    
    .stSuccess {
        background: rgba(16, 185, 129, 0.15) !important;
        color: #6ee7b7 !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
    }
    
    .stInfo {
        background: rgba(59, 130, 246, 0.15) !important;
        color: #93c5fd !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
    }
    
    .stWarning {
        background: rgba(245, 158, 11, 0.15) !important;
        color: #fcd34d !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.15) !important;
        color: #fca5a5 !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
    }
    
    /* QR Code Display Area */
    .qr-display {
        background: rgba(17, 24, 39, 0.6);
        border-radius: 20px;
        padding: 2rem;
        border: 2px solid rgba(139, 92, 246, 0.3);
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
        min-height: 400px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        font-weight: 700 !important;
        background: rgba(17, 24, 39, 0.6);
        border-radius: 12px;
        padding: 12px 20px;
        border: 1px solid rgba(139, 92, 246, 0.3);
        color: #e4e4e7 !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(17, 24, 39, 0.4);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 0 0 12px 12px;
    }
    
    /* Code blocks */
    code {
        background: rgba(17, 24, 39, 0.8) !important;
        color: #a78bfa !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
    }
    
    pre {
        background: rgba(17, 24, 39, 0.8) !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        border-radius: 8px !important;
    }
    
    pre code {
        color: #c4b5fd !important;
    }
    
    /* Caption Text */
    .stCaption {
        font-weight: 500 !important;
        color: #a1a1aa !important;
        font-size: 0.9rem !important;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Column Spacing */
    [data-testid="column"] {
        padding: 0 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize backend generator
if 'qr_generator' not in st.session_state:
    st.session_state.qr_generator = QRCodeGenerator()

# Initialize session state for generated QR codes
if 'qr_image' not in st.session_state:
    st.session_state.qr_image = None
if 'upload_info' not in st.session_state:
    st.session_state.upload_info = None

# Title and Subtitle
st.markdown("<h1>⚡ QR CODE GENERATOR PRO</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Create stunning QR codes instantly • Share files with permanent links • Professional quality</p>", unsafe_allow_html=True)

# Create two columns for the left and right sections
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    # Use tabs for Text/URL and File Upload
    tab1, tab2 = st.tabs(["📝 TEXT / URL", "📁 FILE UPLOAD"])

    with tab1:
        st.markdown("### Enter Your Content")
        text_input = st.text_area(
            "Text or URL:",
            placeholder="https://example.com or any text you want to encode...",
            height=120,
            key="text_input",
            label_visibility="collapsed"
        )

        st.markdown("### Customize Colors")
        # Color pickers for text QR
        col_fg, col_bg = st.columns(2)
        with col_fg:
            text_fg_color = st.color_picker(
                "🎨 QR Color", "#000000", key="text_fg")
        with col_bg:
            text_bg_color = st.color_picker(
                "🎨 Background", "#FFFFFF", key="text_bg")

        st.markdown("")  # Spacing

        # Generate button for text/URL
        if st.button("🚀 GENERATE QR CODE", key="text_btn"):
            if text_input.strip():
                with st.spinner("⚡ Generating your QR code..."):
                    try:
                        # Generate QR code from text
                        qr_buffer = st.session_state.qr_generator.generate_qr_code(
                            text_input.strip(),
                            fill_color=text_fg_color,
                            back_color=text_bg_color
                        )

                        # Store in session state
                        st.session_state.qr_image = qr_buffer
                        st.session_state.upload_info = None
                        st.success("✅ *QR code generated successfully!*")

                    except Exception as e:
                        st.error(f"❌ *Error:* {str(e)}")
            else:
                st.warning("⚠ *Please enter some text or URL first*")

    with tab2:
        st.markdown("### Upload Your File")
        st.caption(
            "📦 *Supported:* PDF • Images • Videos • Documents • Audio • Archives • And more!")

        uploaded_file = st.file_uploader(
            "Choose a file to upload",
            type=None,  # Allow all file types
            key="file_uploader",
            label_visibility="collapsed"
        )

        if uploaded_file:
            file_size = len(uploaded_file.getvalue()) / 1024
            if file_size > 1024:
                file_size_display = f"{file_size/1024:.2f} MB"
            else:
                file_size_display = f"{file_size:.2f} KB"

            # Show file icon based on type
            file_ext = uploaded_file.name.split('.')[-1].lower()
            file_icons = {
                'pdf': '📄', 'doc': '📄', 'docx': '📄', 'txt': '📄',
                'jpg': '🖼', 'jpeg': '🖼', 'png': '🖼', 'gif': '🖼', 'svg': '🖼',
                'mp4': '🎥', 'avi': '🎥', 'mov': '🎥', 'mkv': '🎥', 'webm': '🎥',
                'mp3': '🎵', 'wav': '🎵', 'flac': '🎵', 'ogg': '🎵',
                'zip': '📦', 'rar': '📦', '7z': '📦', 'tar': '📦',
                'xlsx': '📊', 'xls': '📊', 'csv': '📊',
                'pptx': '📽', 'ppt': '📽'
            }
            icon = file_icons.get(file_ext, '📎')

            st.success(f"{icon} {uploaded_file.name}** • {file_size_display}")

        st.markdown("### Customize Colors")
        # Color pickers for file QR
        col_fg2, col_bg2 = st.columns(2)
        with col_fg2:
            file_fg_color = st.color_picker(
                "🎨 QR Color", "#000000", key="file_fg")
        with col_bg2:
            file_bg_color = st.color_picker(
                "🎨 Background", "#FFFFFF", key="file_bg")

        st.markdown("")  # Spacing

        # Generate button for file
        if st.button("🚀 UPLOAD & GENERATE", key="file_btn"):
            if uploaded_file:
                with st.spinner("⚡ Uploading file and generating QR code..."):
                    try:
                        # Upload file and generate QR from link
                        qr_buffer, upload_result = st.session_state.qr_generator.generate_qr_from_file(
                            uploaded_file.getvalue(),
                            uploaded_file.name,
                            fill_color=file_fg_color,
                            back_color=file_bg_color
                        )

                        # Store in session state
                        st.session_state.qr_image = qr_buffer
                        st.session_state.upload_info = upload_result
                        st.success("✅ *QR code generated successfully!*")

                    except Exception as e:
                        st.error(f"❌ *Upload failed:* {str(e)}")
            else:
                st.warning("⚠ *Please upload a file first*")

with col_right:
    st.markdown("### Generated QR Code")

    # Display QR code if available
    if st.session_state.qr_image:
        # Display the QR code
        st.image(st.session_state.qr_image, use_container_width=True)

        # If this was from a file upload, show upload info
        if st.session_state.upload_info:
            st.info(
                f"📡 Hosting Service:** {st.session_state.upload_info['service']}")
            st.success(f"{st.session_state.upload_info['message']}")

            with st.expander("🔗 *View Direct Link*"):
                st.code(st.session_state.upload_info['url'], language=None)

        st.markdown("")  # Spacing

        # Download button
        st.session_state.qr_image.seek(0)
        st.download_button(
            label="⬇ DOWNLOAD QR CODE",
            data=st.session_state.qr_image.read(),
            file_name="qr_code.png",
            mime="image/png",
            use_container_width=True
        )
    else:
        # Placeholder with professional styling
        st.markdown("""
        <div style='background: rgba(17, 24, 39, 0.6); 
                    border-radius: 20px; 
                    padding: 4rem 2rem; 
                    text-align: center;
                    border: 2px dashed rgba(139, 92, 246, 0.4);
                    min-height: 400px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;'>
            <div style='font-size: 4rem; margin-bottom: 1rem;'>📱</div>
            <div style='font-size: 1.3rem; font-weight: 700; color: #e4e4e7; margin-bottom: 0.5rem;'>
                Your QR Code Will Appear Here
            </div>
            <div style='font-size: 1rem; font-weight: 500; color: #a1a1aa;'>
                Generate a QR code from text or file to get started
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #a1a1aa; font-weight: 600; padding: 2rem 0;'>
    <p style='margin: 0;'>⚡ Built with Streamlit • Powered by Multiple Hosting Services</p>
    <p style='margin: 0.5rem 0 0 0; font-size: 0.9rem;'>Professional QR Code Generation Tool</p>
</div>
""", unsafe_allow_html=True)
