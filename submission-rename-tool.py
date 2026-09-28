import streamlit as st
import cv2 as cv
import pandas as pd
import numpy as np
from PIL import Image
import io
from io import BytesIO
from streamlit_image_zoom import image_zoom
import base64

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


gc = st.file_uploader("Select the grades CSV file", type = "csv")
image = st.file_uploader("Select the student submission", type = ["png", "jpg"])
if image and gc is not None:
    filename = image.name
    img_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
    img = cv.imdecode(img_bytes, 1)
    snumber = st.text_input("Student Number")
    prac_viewer(img=image)
    if st.button("Load Details"):
        df = pd.read_csv(gc, encoding = "latin1")
        surname, name = df.loc[df["emplid"] == snumber, ["surname", "name"]].iloc[0]
        sname = st.text_input("Surname", value=surname)
        fname = st.text_input("Initials", value=name)
        filename = f"{surname}_{name}_{snumber}.png"
        final_img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        final_img_pil = Image.fromarray(final_img_rgb)
        buffer = io.BytesIO()
        final_img_pil.save(buffer, format="PNG")
        st.download_button(label=f"Download {filename}", data=buffer, file_name=filename, mime="image/png")
