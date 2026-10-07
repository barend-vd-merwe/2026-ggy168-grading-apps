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
def submission_viewer(
    img_uri: str,
    height: int = 700,
    max_zoom_ratio: float = 4.0,
    key: str = "osd_viewer",
):
    html_template = """
    <!DOCTYPE html>
    <html style="height:100%">
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/openseadragon/4.1.0/openseadragon.min.js"></script>
        <style>
            body {
                margin: 0;
                padding: 0;
                background-color: #F5F5DC;
                height: 100%;
                width: 100%;
                overflow: hidden;
            }
            #openseadragon-container {
                width: 100vw;
                height: 100vh;
                background: #F5F5DC;
                border: 10px solid #374151;
                border-radius: 8px;
                box-sizing: border-box;
            }
        </style>
    </head>
    <body>
        <div id="openseadragon-container"></div>
        <script type="text/javascript">
            var viewer = OpenSeadragon({
                id: "openseadragon-container",
                prefixUrl: "https://cdnjs.cloudflare.com/ajax/libs/openseadragon/4.1.0/images/",
                tileSources: {
                    type: 'image',
                    url: '__IMAGE_URI__'
                },
                // Performance and Zoom configuration
                maxZoomPixelRatio: __MAX_ZOOM__,
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
                blendTime: 0.1,
                springStiffness: 10
            });

            // Zoom to question block once viewer finishes opening
            viewer.addHandler('open', function() {
                var answer_block = new OpenSeadragon.Rect(0.065396,0.108961, 0.199762, 0.311153);
                viewer.viewport.fitBounds(answer_block, true);
            });
        </script>
    </body>
    </html>
    """

    html_osd = html_template.replace("__IMAGE_URI__", img_uri).replace(
        "__MAX_ZOOM__", str(max_zoom_ratio)
    )

    st.components.v1.html(html_osd, height=height, scrolling=False)

    st.set_page_config(layout="wide")

def clear_files():
     st.session_state["uploader_key"] += 1
     del st.session_state["script_index"]

def next_submission():
    st.session_state["script_index"] += 1
    st.session_state["emplid"] = ""
    st.session_state["surname_field"] = ""
    st.session_state["name_field"] = ""
    st.rerun()

st.title("Submission Renaming Tool")

if "script_index" not in st.session_state:
    st.session_state["script_index"] = 0

if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = 0

with st.sidebar:
    gc = st.file_uploader("Select the class list CSV file", type = "csv")
    uploaded_files = st.file_uploader("Select the student submission",
                         type = ["png"],
                         accept_multiple_files = True,
                                      key = str(st.session_state["uploader_key"]))

    st.button("Clear", on_click = clear_files)

if uploaded_files:
    total_scripts = len(uploaded_files)
    image = uploaded_files[st.session_state["script_index"]]
    filename = image.name
    img = Image.open(image)

    # store the submission in memory as cv2 object
    img_bytes = np.frombuffer(image.getvalue(), dtype=np.uint8)
    cv_img = cv.imdecode(img_bytes, cv.IMREAD_COLOR)

    # prepare values for detector
    aruco_dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_50)
    parameters = cv.aruco.DetectorParameters()
    
    # instantiate detector
    detector = cv.aruco.ArucoDetector(aruco_dictionary, parameters)

    col1, col2 = st.columns(2)
    
    try:
        # use detector to detect aruco markers
        corners, ids, _ = detector.detectMarkers(cv_img)

        # get the coordinates of the points to maximise scanned area
        ids = ids.flatten().tolist()
        aruco_0_index = ids.index(0)
        aruco_0_corners = corners[aruco_0_index]
        aruco_0_corners = aruco_0_corners.squeeze()
        top_left = aruco_0_corners[0]

        aruco_1_index = ids.index(1)
        aruco_1_corners = corners[aruco_1_index]
        aruco_1_corners = aruco_1_corners.squeeze()
        top_right = aruco_1_corners[1]

        aruco_2_index = ids.index(2)
        aruco_2_corners = corners[aruco_2_index]
        aruco_2_corners = aruco_2_corners.squeeze()
        bottom_left = aruco_2_corners[3]

        aruco_3_index = ids.index(3)
        aruco_3_corners = corners[aruco_3_index]
        aruco_3_corners = aruco_3_corners.squeeze()
        bottom_right = aruco_3_corners[2]

        # Prepare the image for warping
        current_coords = np.float32([[top_left[0], top_left[1]],
                                     [top_right[0], top_right[1]],
                                     [bottom_right[0], bottom_right[1]],
                                     [bottom_left[0], bottom_left[1]]])
        target_coords = np.float32([[177,177],
                                    [2303,177],
                                    [2303,3330],
                                    [177,3330]])
        transformation_matrix = cv.getPerspectiveTransform(current_coords,
                                                           target_coords)

        # transform the image
        warped_img = cv.warpPerspective(cv_img,
                                        transformation_matrix,
                                        (2480,3508),
                                        borderMode=cv.BORDER_CONSTANT,
                                        borderValue=(255, 255, 255))

        st.session_state["submission"] = warped_img

        processed_img = cv.imencode(".png",warped_img)[1]
        b64_str = base64.b64encode(processed_img).decode("utf-8")
        img_url = f"data:image/png;base64,{b64_str}"

        with col1:
            submission_viewer(img_url)

    except:
        st.error("Can't process submission.")
    
    with col2:
        snumber = st.text_input("Student Number", key="emplid")
        if st.button("Load Details"):
            df = pd.read_csv(gc, encoding = "latin1")
            surname, name = df.loc[df["emplid"] == snumber, ["surname", "name"]].iloc[0]
            sname = st.text_input("Surname", value=surname, key="surname_field")
            fname = st.text_input("Initials", value=name, key="name_field")
            filename = f"{surname}_{name}_{snumber}.png"
            final_img_rgb = cv.cvtColor(st.session_state["submission"], cv.COLOR_BGR2RGB)
            final_img_pil = Image.fromarray(final_img_rgb)
            buffer = io.BytesIO()
            final_img_pil.save(buffer, format="PNG")
            st.download_button(label=f"Download {filename}", data=buffer, file_name=filename, mime="image/png")

        if st.button("Unknown student"):
            filename = f"unknown_{st.session_state["script_index"]}.png"
            final_img_rgb = cv.cvtColor(st.session_state["submission"], cv.COLOR_BGR2RGB)
            final_img_pil = Image.fromarray(final_img_rgb)
            buffer = io.BytesIO()
            final_img_pil.save(buffer, format="PNG")
            st.download_button(label=f"Download {filename}", data=buffer, file_name=filename, mime="image/png")

        if st.session_state["script_index"] < len(uploaded_files) - 1:
            st.button("Next Submission", on_click = next_submission)
