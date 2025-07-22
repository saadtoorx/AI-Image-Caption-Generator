#Importing necessary libraries
import streamlit as st
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
import io

# Configure page with wide layout
st.set_page_config(
    page_title="AI Caption Generator",
    page_icon="🖼️",
    layout="wide"  # This allows more control over layout
)

#Custom CSS for better styling
st.markdown("""
<style>
    /* Main container padding */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Center the title */
    .main-title {
        text-align: center;
        padding-bottom: 1rem;
    }
    
    /* Add some spacing between sections */
    .stHeader {
        padding-top: 1rem;
    }
    
    /* Style the upload area */
    .uploadedFile {
        border-radius: 10px;
    }
    
    /* Add some breathing room to columns */
    .stColumn {
        padding: 0 1rem;
    }
    
    /* Center content in columns */
    .center-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    
    /* Style for the caption display */
    .caption-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 1rem;
        border-left: 4px solid #ff6b6b;
    }
    
    /* Responsive design for smaller screens */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Cache the model loading to avoid reloading on every interaction
@st.cache_resource

#Function to load the pretrained BLIP Model and Processor
def load_model():
    """Load the BLIP model and processor"""
    try:
        #Loading the pretrained BLIP Processor
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")

        #Loading the pretrained BLIP Model
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

        return processor, model

    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None, None

#Function to generate caption using BLIP Model and Processor
def generate_caption(image_bytes: bytes, max_length: int):
    processor, model = load_model()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    inputs = processor(image, return_tensors="pt")

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_length=max_length,
            min_length=max(5, max_length // 2),  # Encourage longer captions
            num_beams=5,
            early_stopping=True,
            no_repeat_ngram_size=2
        )

    caption = processor.decode(output[0], skip_special_tokens=True)
    return caption

#Main Function
def main():
    # Centered title with custom styling
    st.markdown('<h1 class="main-title">🖼️ AI Caption Generator</h1>', unsafe_allow_html=True)
    
    # Centered subtitle
    st.markdown(
        '<p style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 2rem;">'
        'Upload an image and get an AI-generated caption instantly!</p>', 
        unsafe_allow_html=True
    )
    
    # Sidebar with better styling
    with st.sidebar:
        st.markdown("### 📋 About")
        st.info(
            "This app uses the BLIP (Bootstrapping Language-Image Pre-training) "
            "model to generate captions for images."
        )
        
        with st.expander("📖 How to use", expanded=True):
            st.write("1. 📤 Upload an image (JPG, JPEG, PNG)")
            st.write("2. ⏳ Wait for the model to process")
            st.write("3. ✨ View the generated caption!")
        
        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        max_length = st.slider(
            "Maximum caption length", 
            min_value=20, 
            max_value=100, 
            value=50,
            help="Longer values generate more detailed captions"
        )
        
        # Add a button to force regeneration
        if st.button("🔄 Generate New Caption", help="Click to regenerate caption with current settings"):
            # Clear the cache to force regeneration
            generate_caption.clear()
            st.rerun()  # Trigger a rerun to regenerate
        
        # Add some extra info
        st.markdown("---")
        st.markdown("### 🎯 Tips")
        st.success("📸 Clear, well-lit images work best!")
        st.info("🔄 Try different caption lengths for variety")
    
    # Add some vertical space
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Main content with improved spacing - use 3-column layout for better centering
    left_spacer, main_col1, center_spacer, main_col2, right_spacer = st.columns([0.5, 3, 0.5, 3, 0.5])
    
    with main_col1:
        st.markdown("### 📤 Upload Your Image")
        
        uploaded_file = st.file_uploader(
            "Choose an image file", 
            type=['png', 'jpg', 'jpeg'],
            help="Upload a PNG, JPG, or JPEG image (max 200MB)"
        )
        
        if uploaded_file is not None:
            # Display the uploaded image with better styling
            image = Image.open(uploaded_file)
            st.image(
                image, 
                caption=f"📁 {uploaded_file.name}", 
                use_container_width=True,
                clamp=True  # This prevents huge images from breaking the layout
            )
            
            # Show image details
            st.markdown("**Image Details:**")
            st.write(f"• **Size:** {image.size[0]} × {image.size[1]} pixels")
            st.write(f"• **Format:** {image.format}")
            st.write(f"• **Mode:** {image.mode}")
    
    with main_col2:
        st.markdown("### ✨ Generated Caption")
        
        if uploaded_file is not None:
            # Load model with better progress indication
            with st.spinner("🤖 Loading AI model..."):
                processor, model = load_model()
            
            if processor is not None and model is not None:
                # Create a unique hash for the image to help with caching
                import hashlib
                img_bytes = io.BytesIO()
                image.save(img_bytes, format='PNG')
                img_hash = hashlib.md5(img_bytes.getvalue()).hexdigest()
                
                # Generate caption with progress
                with st.spinner("🔮 Generating caption..."):
                    img_bytes = io.BytesIO()
                    image.save(img_bytes, format='PNG')
                    image_bytes = img_bytes.getvalue()

                    caption = generate_caption(
                        image_bytes=image_bytes,
                        max_length=max_length
                        )

                
                # Display result with custom styling
                st.success("🎉 Caption generated successfully!")
                
                # Custom styled caption box
                st.markdown(
                    f'<div class="caption-box">'
                    f'<h4 style="margin-top: 0; color: #333;">📝 Your Caption:</h4>'
                    f'<p style="font-size: 1.1rem; font-style: italic; margin-bottom: 0; line-height: 1.5; color: black;">'
                    f'"{caption}"</p>'
                    f'</div>', 
                    unsafe_allow_html=True
                )
                
                # Copy-friendly version
                st.markdown("**📋 Copy-ready version:**")
                st.code(caption, language=None)
                
                # Add download option for the caption
                st.download_button(
                    label="💾 Download Caption as Text",
                    data=caption,
                    file_name=f"caption_{uploaded_file.name.split('.')[0]}.txt",
                    mime="text/plain"
                )
                
            else:
                st.error("❌ Failed to load the AI model. Please refresh and try again.")
        else:
            # Placeholder with better styling
            st.markdown(
                '<div style="text-align: center; padding: 3rem 1rem; '
                'background-color: #f8f9fa; border-radius: 10px; '
                'border: 2px dashed #ddd;">'
                '<h3 style="color: #999; margin-bottom: 1rem;">👆 Upload an image to get started</h3>'
                '<p style="color: #666;">Your AI-generated caption will appear here</p>'
                '</div>', 
                unsafe_allow_html=True
            )
    
    # Add some vertical space before footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Footer with better styling
    st.markdown("---")
    footer_col1, footer_col2, footer_col3 = st.columns([1, 2, 1])
    with footer_col2:
        st.markdown(
            '<p style="text-align: center; color: #666;">'
            'Made by <strong>Saad Toor</strong> aka <strong>saadtoorx</strong>'
            '</p>', 
            unsafe_allow_html=True
        )

#Calling Main Function
if __name__ == "__main__":
    main()
