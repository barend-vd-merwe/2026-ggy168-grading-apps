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
    # memo q1
    q1 = {
        "q" : ["a","b","c","d"],
        "mem_lat" : [42.5725, 51.2419, 72.2795, 15.1430],
        "fc_lat_U" : [42.5727, 51.2421, 72.2797, 15.1432],
        "fc_lat_L" : [42.5723, 51.2417, 72.2793, 15.1428],
        "pc_lat_U" : [42.5729, 51.2423, 72.2799, 15.1434],
        "pc_lat_L" : [42.5721, 51.2415, 72.2791, 15.1426],
        "sub_lat" : [float(st.session_state["one_a_lat"]),
                     float(st.session_state["one_b_lat"]),
                     float(st.session_state["one_c_lat"]),
                     float(st.session_state["one_d_lat"])],
        "mem_lon" : [47.2889, 40.5508, 115.3131, 112.3586],
        "fc_lon_U" : [47.2891, 40.551, 115.3133, 112.3588],
        "fc_lon_L" : [47.2887, 40.5506, 115.3129, 112.3584],
        "pc_lon_U" : [47.2893, 40.5512, 115.3135, 112.359],
        "pc_lon_L" : [47.2885, 40.5504, 115.3127, 112.3582],
        "sub_lon" : [float(st.session_state["one_a_lon"]),
                     float(st.session_state["one_b_lon"]),
                     float(st.session_state["one_c_lon"]),
                     float(st.session_state["one_d_lon"])],
        "mem_lat_card" : ["S", "S", "N", "N"],
        "sub_lat_card" : [st.session_state["one_a_lat_dir"],
                          st.session_state["one_b_lat_dir"],
                          st.session_state["one_c_lat_dir"],
                          st.session_state["one_d_lat_dir"]],
        "mem_lon_card" : ["E", "W", "E", "W"],
        "sub_lon_card" : [st.session_state["one_a_lon_dir"],
                          st.session_state["one_b_lon_dir"],
                          st.session_state["one_c_lon_dir"],
                          st.session_state["one_d_lon_dir"]],
        "grade" : [0.0, 0.0, 0.0, 0.0]
    }

    q2 = {
        "q" : ["a", "b", "c", "d"],
        "mem_lat_deg" : [5, 74, 42, 49],
        "mem_lat_min" : [1, 1, 42, 34],
        "mem_lat_sec" : [18, 46, 34, 43],
        "fc_lat_U"    : [19, 47, 35, 44],
        "fc_lat_L"    : [17, 45, 33, 42],
        "pc_lat_U"    : [20, 48, 36, 45],
        "pc_lat_L"    : [16, 44, 32, 41],
        "mem_lat_card": ["S", "S", "N", "N"],
        "mem_lon_deg" : [137, 121, 106, 96],
        "mem_lon_min" : [24, 38, 37, 10],
        "mem_lon_sec" : [49, 2, 12, 9],
        "fc_lon_U"    : [50, 3, 13, 10],
        "fc_lon_L"    : [48, 1, 11, 8],
        "pc_lon_U"    : [51, 4, 14, 11],
        "pc_lon_L"    : [47, 0, 10, 7],
        "mem_lon_card": ["E", "W", "E", "W"],
        "sub_lat_deg" : [float(st.session_state["two_a_lat_deg"]),
                         float(st.session_state["two_b_lat_deg"]),
                         float(st.session_state["two_c_lat_deg"]),
                         float(st.session_state["two_d_lat_deg"])],
        "sub_lat_min" : [float(st.session_state["two_a_lat_min"]),
                         float(st.session_state["two_b_lat_min"]),
                         float(st.session_state["two_c_lat_min"]),
                         float(st.session_state["two_d_lat_min"])],
        "sub_lat_sec" : [float(st.session_state["two_a_lat_sec"]),
                         float(st.session_state["two_b_lat_sec"]),
                         float(st.session_state["two_c_lat_sec"]),
                         float(st.session_state["two_d_lat_sec"])],
        "sub_lat_card": [st.session_state["two_a_lat_dir"],
                         st.session_state["two_b_lat_dir"],
                         st.session_state["two_c_lat_dir"],
                         st.session_state["two_d_lat_dir"]],
        "sub_lon_deg" : [float(st.session_state["two_a_lon_deg"]),
                         float(st.session_state["two_b_lon_deg"]),
                         float(st.session_state["two_c_lon_deg"]),
                         float(st.session_state["two_d_lon_deg"])],
        "sub_lon_min" : [float(st.session_state["two_a_lon_min"]),
                         float(st.session_state["two_b_lon_min"]),
                         float(st.session_state["two_c_lon_min"]),
                         float(st.session_state["two_d_lon_min"])],
        "sub_lon_sec" : [float(st.session_state["two_a_lon_sec"]),
                         float(st.session_state["two_b_lon_sec"]),
                         float(st.session_state["two_c_lon_sec"]),
                         float(st.session_state["two_d_lon_sec"])],
        "sub_lon_card": [st.session_state["two_a_lon_dir"],
                         st.session_state["two_b_lon_dir"],
                         st.session_state["two_c_lon_dir"],
                         st.session_state["two_d_lon_dir"]],
        "grade"       : [0.0, 0.0, 0.0, 0.0]
    }

    q1 = pd.DataFrame(q1)
    q2 = pd.DataFrame(q2)

    # Question 1
    # latitude
    lat_fc = q1["sub_lat"].between(q1["fc_lat_L"], q1["fc_lat_U"])
    lat_pc = q1["sub_lat"].between(q1["pc_lat_L"], q1["pc_lat_U"])

    lat_opt = [lat_fc, lat_pc]
    lat_grd = [1.0, 0.5]
    q1["grade"] += np.select(lat_opt, lat_grd, default = 0.0)

    # longitude
    lon_fc = q1["sub_lon"].between(q1["fc_lon_L"], q1["fc_lon_U"])
    lon_pc = q1["sub_lon"].between(q1["pc_lon_L"], q1["pc_lon_U"])
    lon_opt = [lon_fc, lon_pc]
    lon_grd = [1.0, 0.5]
    q1["grade"] += np.select(lon_opt, lon_grd, default = 0.0)

    # cardinal direction
    lat_card_fc = q1["sub_lat_card"] == q1["mem_lat_card"]
    lat_card_nc = q1["sub_lat_card"] != q1["mem_lat_card"]
    lat_card_opt = [lat_card_fc, lat_card_nc]
    lat_card_grd = [1.0, 0.0]
    q1["grade"] += np.select(lat_card_opt, lat_card_grd, default = 0.0)

    # cardinal direction
    lon_card_fc = q1["sub_lon_card"] == q1["mem_lon_card"]
    lon_card_nc = q1["sub_lon_card"] != q1["mem_lon_card"]
    lon_card_opt = [lon_card_fc, lon_card_nc]
    lon_card_grd = [1.0, 0.0]
    q1["grade"] += np.select(lon_card_opt, lon_card_grd, default = 0.0)

    # question 2
    # latitude
    fc_lat_deg = q2["sub_lat_deg"] == q2["mem_lat_deg"]
    nc_lat_deg = q2["sub_lat_deg"] != q2["sub_lat_deg"]
    lat_deg_opt = [fc_lat_deg, nc_lat_deg]
    lat_deg_grd = [1.0, 0.0]
    lat_degree = np.select(lat_deg_opt, lat_deg_grd, default=0.0)

    fc_lat_min = q2["sub_lat_min"] == q2["mem_lat_min"]
    nc_lat_min = q2["sub_lat_min"] != q2["mem_lat_min"]
    lat_min_opt = [fc_lat_min, nc_lat_min]
    lat_min_grd = [1.0, 0.0]
    lat_minute = np.select(lat_min_opt, lat_min_grd, default = 0.0)

    fc_lat_sec = q2["sub_lat_sec"].between(q2["fc_lat_L"], q2["fc_lat_U"])
    pc_lat_sec = q2["sub_lat_sec"].between(q2["pc_lat_L"], q2["pc_lat_U"])
    lat_sec_opt = [fc_lat_sec, pc_lat_sec]
    lat_sec_grd = [1.0, 0.5]
    q2["grade"] += np.select(lat_sec_opt, lat_sec_grd, default=0.0) * lat_degree * lat_minute

    fc_lat_card = q2["sub_lat_card"] == q2["mem_lat_card"]
    nc_lat_card = q2["sub_lat_card"] != q2["mem_lat_card"]
    lat_card_opt = [fc_lat_card, nc_lat_card]
    lat_card_grd = [1.0, 0.0]
    q2["grade"] += np.select(lat_card_opt, lat_card_grd, default=0.0)

    # Longitude
    fc_lon_deg = q2["sub_lon_deg"] == q2["mem_lon_deg"]
    nc_lon_deg = q2["sub_lon_deg"] != q2["sub_lon_deg"]
    lon_deg_opt = [fc_lon_deg, nc_lon_deg]
    lon_deg_grd = [1.0, 0.0]
    lon_degree = np.select(lon_deg_opt, lon_deg_grd, default=0.0)

    fc_lon_min = q2["sub_lon_min"] == q2["mem_lon_min"]
    nc_lon_min = q2["sub_lon_min"] != q2["mem_lon_min"]
    lon_min_opt = [fc_lon_min, nc_lon_min]
    lon_min_grd = [1.0, 0.0]
    lon_minute = np.select(lon_min_opt, lon_min_grd, default = 0.0)

    fc_lon_sec = q2["sub_lon_sec"].between(q2["fc_lon_L"], q2["fc_lon_U"])
    pc_lon_sec = q2["sub_lon_sec"].between(q2["pc_lon_L"], q2["pc_lon_U"])
    lon_sec_opt = [fc_lon_sec, pc_lon_sec]
    lon_sec_grd = [1.0, 0.5]
    q2["grade"] += np.select(lon_sec_opt, lon_sec_grd, default=0.0) * lon_degree * lon_minute

    fc_lon_card = q2["sub_lon_card"] == q2["mem_lon_card"]
    nc_lon_card = q2["sub_lon_card"] != q2["mem_lon_card"]
    lon_card_opt = [fc_lon_card, nc_lon_card]
    lon_card_grd = [1.0, 0.0]
    q2["grade"] += np.select(lon_card_opt, lon_card_grd, default=0.0)

    # assignment total
    total = float(q1["grade"].sum() + q2["grade"].sum())
    st.session_state["q1"] = str(float(q1["grade"].sum()))
    st.session_state["q2"] = str(float(q2["grade"].sum()))
    st.session_state["grade"] = str(total)

    # student details
    student_id = name + " " + surname + " (" + emplid + ")"
    
    # add text to image
    graded_script = cv.putText(warped_img, str(total), (824,446), cv.FONT_HERSHEY_SIMPLEX, 3.0, (0,0,255), 1)
    graded_script = cv.putText(warped_img, student_id, (1150,442), cv.FONT_HERSHEY_SIMPLEX, 2.0, (0,0,255), 1)
    graded_script = cv.putText(warped_img, f"Q1a: {str(q1.loc[q1.index[0], 'grade'])}", (1150,517), cv.FONT_HERSHEY_SIMPLEX, 2.0, (0,0,255), 1)
    graded_script = cv.putText(warped_img, f"Q1b: {str(q1.loc[q1.index[1], 'grade'])}", (1150,592), cv.FONT_HERSHEY_SIMPLEX, 2.0, (0,0,255), 1)
    graded_script = cv.putText(warped_img, f"Q1c: {str(q1.loc[q1.index[2], 'grade'])}", (1150,667), cv.FONT_HERSHEY_SIMPLEX, 2.0, (0,0,255), 1)
    graded_script = cv.putText(warped_img, f"Q1d: {str(q1.loc[q1.index[3], 'grade'])}", (1150,742), cv.FONT_HERSHEY_SIMPLEX, 2.0, (0,0,255), 1)

    graded_script = cv.putText(warped_img, f"Q2a: {str(q2.loc[q1.index[0], 'grade'])}", (1150,817), cv.FONT_HERSHEY_SIMPLEX, 2.0, (0,0,255), 1)
    graded_script = cv.putText(warped_img, f"Q2b: {str(q2.loc[q1.index[1], 'grade'])}", (1150,892), cv.FONT_HERSHEY_SIMPLEX, 2.0, (0,0,255), 1)
    graded_script = cv.putText(warped_img, f"Q2c: {str(q2.loc[q1.index[2], 'grade'])}", (1150,967), cv.FONT_HERSHEY_SIMPLEX, 2.0, (0,0,255), 1)
    graded_script = cv.putText(warped_img, f"Q2d: {str(q2.loc[q1.index[3], 'grade'])}", (1150,1042), cv.FONT_HERSHEY_SIMPLEX, 2.0, (0,0,255), 1)

    st.session_state["graded_submission"] = graded_script

 

    

# ------------------------------------------------------------
    
st.set_page_config(layout="wide")
    
st.title("Practical 1 — Converting Coordinates")

st.markdown("""
### Instructions
1. Enter your name in the provided field.
2. Load the student submission.
3. If there is an error during loading, refresh your browser window and try again.
4. If it still doesn't work, send me an email with the student's details and move on to the next submission.
5. Verify that the name on the submission matches the name of the file.
6. Transfer the answers on the submission to the spaces provided.
7. **DON't** use commas for decimal marks. Please use a full-stop.
8. If they didn't add the cardinal direction, select the "NA" option from the drop-down menu.
9. When you are done, press the grade button.
10. Download the graded submission and store it in a separate folder. **DON'T** change the filename.
""")

# load class list and submission
grader = st.text_input("Name of marker", key = "graderName")
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

    # store the submission in memory as cv2 object
    img_bytes = np.frombuffer(image.getvalue(), dtype=np.uint8)
    cv_img = cv.imdecode(img_bytes, cv.IMREAD_COLOR)

    # prepare values for detector
    aruco_dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_50)
    parameters = cv.aruco.DetectorParameters()
    
    # instantiate detector
    detector = cv.aruco.ArucoDetector(aruco_dictionary, parameters)

    try:
        # use detector to detect aruco markers
        corners, ids, _ = detector.detectMarkers(cv_img)

        # get the coordinates of the points to maximise scanned area
        ids = ids.tolist()
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
                                        (2480,3508))


    except:
        st.error("Can't process submission.")

    

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
                st.selectbox("Dir", ("N", "E", "S", "W", "NA"), key="one_a_lat_dir")
                st.selectbox("Dir", ("N", "E", "S", "W", "NA"), key="one_b_lat_dir")
                st.selectbox("Dir", ("N", "E", "S", "W", "NA"), key="one_c_lat_dir")
                st.selectbox("Dir", ("N", "E", "S", "W", "NA"), key="one_d_lat_dir")

            with q1_col3:
                st.text_input("(a) — Longitude", key="one_a_lon")
                st.text_input("(b) — Longitude", key="one_b_lon")
                st.text_input("(c) — Longitude", key="one_c_lon")
                st.text_input("(d) — Longitude", key="one_d_lon")

            with q1_col4:
                st.selectbox("Dir", ("N", "E", "S", "W", "NA"), key="one_a_lon_dir")
                st.selectbox("Dir", ("N", "E", "S", "W", "NA"), key="one_b_lon_dir")
                st.selectbox("Dir", ("N", "E", "S", "W", "NA"), key="one_c_lon_dir")
                st.selectbox("Dir", ("N", "E", "S", "W", "NA"), key="one_d_lon_dir")

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
                    st.selectbox("Dir — Latitude", ("N", "E", "S", "W", "NA"), key="two_a_lat_dir")
                    st.selectbox("Dir — Longitude", ("N", "E", "S", "W", "NA"), key="two_a_lon_dir")

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
                    st.selectbox("Dir — Latitude", ("N", "E", "S", "W", "NA"), key="two_b_lat_dir")
                    st.selectbox("Dir — Longitude", ("N", "E", "S", "W", "NA"), key="two_b_lon_dir")

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
                    st.selectbox("Dir — Latitude", ("N", "E", "S", "W", "NA"), key="two_c_lat_dir")
                    st.selectbox("Dir — Longitude", ("N", "E", "S", "W", "NA"), key="two_c_lon_dir")

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
                    st.selectbox("Dir — Latitude", ("N", "E", "S", "W", "NA"), key="two_d_lat_dir")
                    st.selectbox("Dir — Longitude", ("N", "E", "S", "W", "NA"), key="two_d_lon_dir")
        
    st.button("Grade", on_click=grade_submission)

    if "graded_submission" in st.session_state:
        st.image(st.session_state["graded_submission"])

        final_img_rgb = cv.cvtColor(st.session_state["graded_submission"], cv.COLOR_BGR2RGB)
        final_img_pil = Image.fromarray(final_img_rgb)

        filename = filename + ".png"
        grader_timestamp = datetime.now().isoformat()
        meta_info = PngInfo()
        meta_info.add_text("Grader:", grader.strip())
        meta_info.add_text("GradedAt:", grader_timestamp)
        meta_info.add_text("Q1:", st.session_state["q1"])
        meta_info.add_text("Q2:", st.session_state["q2"])
        meta_info.add_text("Grade:", st.session_state["grade"])
        buffer = io.BytesIO()
        final_img_pil.save(buffer, format="PNG", pnginfo=meta_info)
        st.download_button(label=f"Download {filename}", data=buffer, file_name=filename, mime="image/png")
    
