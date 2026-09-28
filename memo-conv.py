import streamlit as st
import cv2 as cv
import pandas as pd
import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import io
from io import BytesIO
from streamlit_image_zoom import image_zoom
import base64
from datetime import datetime

# custom functions
# ------------------------------------------------------------
def prac_viewer(img, height=700, max_zoom_ratio=4.0, key="osd_viewer"):
    if isinstance(img, Image.Image):
        pil_img = img
    else:
        pil_img = Image.open(img)

    buffered = BytesIO()
    if pil_img.mode in ("RGB", "P"):
        pil_img = pil_img.convert("RGB")

    pil_img.save(buffered, format="JPEG", quality=95)
    img_b64 = base64.b64encode(buffered.getvalue()).decode()

    # openseadragon
    html_osd = f"""
    <!DOCTYPE html>
    <html style="height:100%">
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/openseadragon/4.1.0/openseadragon.min.js"></script>
        <style>
            body {{
    margin: 0;
    padding: 0;
    background-color: #0e1117;
    height: 100%;
    width: 100%;
    overflow: hidden;}}
            #openseadragon-container {{
                width: 100vw;
                height: 100vh;
                background: #111827;
                border: 10px solid #374151;
                border-radius: 8px;
    box-sizing: border-box;
            }}
        </style>
    </head>
    <body>
        <div id="openseadragon-container"></div>
        <script type="text/javascript">
            var viewer = OpenSeadragon({{
                id: "openseadragon-container",
                prefixUrl: "https://cdnjs.cloudflare.com/ajax/libs/openseadragon/4.1.0/images/",
                tileSources: {{
                    type: 'image',
                    url:  'data:image/jpeg;base64,{img_b64}'
                }},
                // Performance and Zoom configuration
                maxZoomPixelRatio: {max_zoom_ratio},
                minZoomImageRatio: 0.8,
                visibilityRatio: 0.8,
                constrainDuringPan: true,
                
                // Controls setup
                showNavigationControl: true,
                navigationControlAnchor: OpenSeadragon.ControlAnchor.TOP_LEFT,
                showRotationControl: false,
                showFullPageControl: true,
                showHomeControl: true,
                
                // Smooth interaction tuning
                animationTime: 0.3,
                bllendTime: 0.1,
                springStiffness: 10
            }});
        </script>
    </body>
    </html>
    """
    st.components.v1.html(html_osd, height=height, scrolling=False)

# ------------------------------------------------------------
def grade_submission():
    # grade q1a
    lat_1_a_decimal = st.session_state["one_a_lat"]
    lon_1_a_decimal = st.session_state["one_a_lon"]
    


# ------------------------------------------------------------
    
st.set_page_config(layout="wide")
    
st.title("Practical 1 — Converting Coordinates")

st.markdown("""
### Instructions
1. Enter your details in the provided field.
2. Load the student submission.
3. Verify that the name on the submission matches the name of the file.
4. **DON't** use commas for decimal marks. Please use a full-stop.
""")

# load class list and submission
grader = st.text_input("Name of grader", key = "graderName")
image = st.file_uploader("Select the student submission", type = ["png", "jpg"])

if image is not None and grader.strip():
    # extract student details from img filename
    filename = image.name
    filename = filename.replace(".png","")
    surname, name, emplid = filename.split("_")

    # display student details
    
    st.markdown(f"""
    - *Name*: **{name}**
    - *Surname*: **{surname}**
    - *Student Number*: **{emplid}**
    """)
    
    # read and display image
    img = Image.open(image)

    # display submission and grading tools in two cols
    col1, col2 = st.columns(2)
    
    with col1:    
        prac_viewer(img=img)

    with col2:
        with st.expander("Question 1", expanded=False):
            q1_col1, q1_col2, q1_col3, q1_col4 = st.columns(4)

            with q1_col1:
                st.text_input("(a) — Latitude", key="one_a_lat")
                st.text_input("(b) — Latitude", key="one_b_lat")
                st.text_input("(c) — Latitude", key="one_c_lat")
                st.text_input("(d) — Latitude", key="one_d_lat")

            with q1_col2:
                st.selectbox("Dir", ("N", "E", "S", "W"), key="one_a_lat_dir")
                st.selectbox("Dir", ("N", "E", "S", "W"), key="one_b_lat_dir")
                st.selectbox("Dir", ("N", "E", "S", "W"), key="one_c_lat_dir")
                st.selectbox("Dir", ("N", "E", "S", "W"), key="one_d_lat_dir")

            with q1_col3:
                st.text_input("(a) — Longitude", key="one_a_lon")
                st.text_input("(b) — Longitude", key="one_b_lon")
                st.text_input("(c) — Longitude", key="one_c_lon")
                st.text_input("(d) — Longitude", key="one_d_lon")

            with q1_col4:
                st.selectbox("Dir", ("N", "E", "S", "W"), key="one_a_lon_dir")
                st.selectbox("Dir", ("N", "E", "S", "W"), key="one_b_lon_dir")
                st.selectbox("Dir", ("N", "E", "S", "W"), key="one_c_lon_dir")
                st.selectbox("Dir", ("N", "E", "S", "W"), key="one_d_lon_dir")

            pass

        with st.expander("Question 2", expanded=False):
            with st.expander("2(a) and 2(b)", expanded=False):
                st.markdown("""
                #### 2(a) Latitude (TOP) and Longitude (BOTTOM)
                """)
                q2a_col1, q2a_col2, q2a_col3, q2a_col4 = st.columns(4)

                with q2a_col1:
                    st.text_input("Deg — Latitude", key="two_a_lat_deg")
                    st.text_input("Deg — Longitude", key="two_a_lon_deg")

                with q2a_col2:
                    st.text_input("Min — Latitude", key="two_a_lat_min")
                    st.text_input("Min — Longitude", key="two_a_lon_min")

                with q2a_col3:
                    st.text_input("Sec — Latitude", key="two_a_lat_sec")
                    st.text_input("Sec — Longitude", key="two_a_lon_sec")

                with q2a_col4:
                    st.selectbox("Dir — Latitude", ("N", "E", "S", "W"), key="two_a_lat_dir")
                    st.selectbox("Dir — Longitude", ("N", "E", "S", "W"), key="two_a_lon_dir")

                st.markdown("""
                #### 2(b) Latitude (TOP) and Longitude (BOTTOM)
                """)
                q2b_col1, q2b_col2, q2b_col3, q2b_col4 = st.columns(4)

                with q2b_col1:
                    st.text_input("Deg — Latitude", key="two_b_lat_deg")
                    st.text_input("Deg — Longitude", key="two_b_lon_deg")

                with q2b_col2:
                    st.text_input("Min — Latitude", key="two_b_lat_min")
                    st.text_input("Min — Longitude", key="two_b_lon_min")

                with q2b_col3:
                    st.text_input("Sec — Latitude", key="two_b_lat_sec")
                    st.text_input("Sec — Longitude", key="two_b_lon_sec")

                with q2b_col4:
                    st.selectbox("Dir — Latitude", ("N", "E", "S", "W"), key="two_b_lat_dir")
                    st.selectbox("Dir — Longitude", ("N", "E", "S", "W"), key="two_b_lon_dir")

                pass

            with st.expander("2(c) and 2(d)", expanded=False):
                st.markdown("""
                #### 2(c) Latitude (TOP) and Longitude (BOTTOM)
                """)
                q2c_col1, q2c_col2, q2c_col3, q2c_col4 = st.columns(4)

                with q2c_col1:
                    st.text_input("Deg — Latitude", key="two_c_lat_deg")
                    st.text_input("Deg — Longitude", key="two_c_lon_deg")

                with q2c_col2:
                    st.text_input("Min — Latitude", key="two_c_lat_min")
                    st.text_input("Min — Longitude", key="two_c_lon_min")

                with q2c_col3:
                    st.text_input("Sec — Latitude", key="two_c_lat_sec")
                    st.text_input("Sec — Longitude", key="two_c_lon_sec")

                with q2c_col4:
                    st.selectbox("Dir — Latitude", ("N", "E", "S", "W"), key="two_c_lat_dir")
                    st.selectbox("Dir — Longitude", ("N", "E", "S", "W"), key="two_c_lon_dir")

                st.markdown("""
                #### 2(d) Latitude (TOP) and Longitude (BOTTOM)
                """)
                q2d_col1, q2d_col2, q2d_col3, q2d_col4 = st.columns(4)

                with q2d_col1:
                    st.text_input("Deg — Latitude", key="two_d_lat_deg")
                    st.text_input("Deg — Longitude", key="two_d_lon_deg")

                with q2d_col2:
                    st.text_input("Min — Latitude", key="two_d_lat_min")
                    st.text_input("Min — Longitude", key="two_d_lon_min")

                with q2d_col3:
                    st.text_input("Sec — Latitude", key="two_d_lat_sec")
                    st.text_input("Sec — Longitude", key="two_d_lon_sec")

                with q2d_col4:
                    st.selectbox("Dir — Latitude", ("N", "E", "S", "W"), key="two_d_lat_dir")
                    st.selectbox("Dir — Longitude", ("N", "E", "S", "W"), key="two_d_lon_dir")
        
    st.button("Grade", on_click=grade_submission)
    
