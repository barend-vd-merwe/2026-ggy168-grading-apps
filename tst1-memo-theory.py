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
def submission_viewer(img_url, height=700, max_zoom_ratio=4.0, key="osd_viewer"):
    if isinstance(img, Image.Image):
        pil_img = img
    else:
        pil_img = Image.open(img)

    buffered = BytesIO()
    if pil_img.mode in ("RGB", "P"):
        pil_img = pil_img.convert("RGB")

    pil_img.save(buffered, format="PNG", quality=95)
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
    background-color: #F5F5DC;
    height: 100%;
    width: 100%;
    overflow: hidden;}}
            #openseadragon-container {{
                width: 100vw;
                height: 100vh;
                background: #F5F5DC;
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
                    url:  '{img_url}'
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
        "mem_val"  : [869.9621],
        "mem_unit" : ["mm/yr"],
        "fc_U"     : [869.9622],
        "fc_L"     : [869.9620],
        "pc_U"     : [869.9623],
        "pc_L"     : [869.9619],
        "sub_val"  : [float(st.session_state["q1_velocity"])],
        "sub_unit" : [st.session_state["q1_units"]],
        "grade"    : [0.0]
    }

    q1 = pd.DataFrame(q1)
    q1_val_fc = q1["sub_val"].between(q1["fc_L"], q1["fc_U"])
    q1_val_pc = q1["sub_val"].between(q1["pc_L"], q1["pc_U"])
    q1_val_opt = [q1_val_fc, q1_val_pc]
    q1_val_grd = [1.0, 0.5]
    q1["grade"] += np.select(q1_val_opt, q1_val_grd, default = 0.0)
    q1_unit_fc = q1["sub_unit"] == q1["mem_unit"]
    q1_unit_nc = q1["sub_unit"] != q1["mem_unit"]
    q1_unit_opt = [q1_unit_fc, q1_unit_nc]
    q1_unit_grd = [1.0, 0.0]
    q1["grade"] += np.select(q1_unit_opt, q1_unit_grd, default = 0.0)

    # ==============================
    q2 = {
        "mem"   : ["Transform"],
        "sub"   : [st.session_state["q2_boundary"]],
        "grade" : [0.0]
    }

    q2 = pd.DataFrame(q2)
    q2_fc = q2["sub"] == q2["mem"]
    q2_nc = q2["sub"] != q2["mem"]
    q2_opt = [q2_fc, q2_nc]
    q2_grd = [1.0, 0.0]
    q2["grade"] += np.select(q2_opt, q2_grd, default = 0.0)

    # ==============================
    q3 = {
        "mem_val"  : [306.25],
        "mem_unit" : ["°C"],
        "fc_U"     : [306.26],
        "fc_L"     : [306.24],
        "pc_U"     : [306.27],
        "pc_L"     : [306.23],
        "sub_val"  : [float(st.session_state["q3_temperature"])],
        "sub_unit" : [st.session_state["q3_units"]],
        "grade"    : [0.0]
    }

    q3 = pd.DataFrame(q3)
    q3_val_fc = q3["sub_val"].between(q3["fc_L"], q3["fc_U"])
    q3_val_pc = q3["sub_val"].between(q3["pc_L"], q3["pc_U"])
    q3_val_opt = [q3_val_fc, q3_val_pc]
    q3_val_grd = [1.0, 0.5]
    q3["grade"] += np.select(q3_val_opt, q3_val_grd, default = 0.0)
    q3_unit_fc = q3["sub_unit"] == q3["mem_unit"]
    q3_unit_nc = q3["sub_unit"] != q3["mem_unit"]
    q3_unit_opt = [q3_unit_fc, q3_unit_nc]
    q3_unit_grd = [1.0, 0.0]
    q3["grade"] += np.select(q3_unit_opt, q3_unit_grd, default = 0.0)

    # ==============================
    q4 = {
        "mem_val"  : [128.8],
        "mem_unit" : ["Megapascals"],
        "fc_U"     : [128.8 + 0.0001],
        "fc_L"     : [128.8 - 0.0001],
        "pc_U"     : [128.8 + 0.0002],
        "pc_L"     : [128.8 - 0.0002],
        "sub_val"  : [float(st.session_state["q4_pressure"])],
        "sub_unit" : [st.session_state["q4_units"]],
        "grade"    : [0.0]
    }

    q4 = pd.DataFrame(q4)
    q4_val_fc = q4["sub_val"].between(q4["fc_L"], q4["fc_U"])
    q4_val_pc = q4["sub_val"].between(q4["pc_L"], q4["pc_U"])
    q4_val_opt = [q4_val_fc, q4_val_pc]
    q4_val_grd = [1.0, 0.0]
    q4["grade"] += np.select(q4_val_opt, q4_val_grd, default = 0.0)
    q4_unit_fc = q4["sub_unit"] == q4["mem_unit"]
    q4_unit_nc = q4["sub_unit"] != q4["mem_unit"]
    q4_unit_opt = [q4_unit_fc, q4_unit_nc]
    q4_unit_grd = [1.0, 0.0]
    q4["grade"] += np.select(q4_unit_opt, q4_unit_grd, default = 0.0)

    # ==============================
    q5 = {
        "mem_ans" : ["A"],
        "sub_ans" : [st.session_state["q5_state"]],
        "grade"   : [0.0]
    }

    q5 = pd.DataFrame(q5)
    q5_fc = q5["sub_ans"] == q5["mem_ans"]
    q5_nc = q5["sub_ans"] != q5["mem_ans"]
    q5_opt = [q5_fc, q5_nc]
    q5_grd = [1.0, 0.0]
    q5["grade"] += np.select(q5_opt, q5_grd, default = 0.0)

    # ==============================
    q6 = {
        "mem_val"  : [0.9175],
        "fc_U"     : [0.9175 + 0.0001034921],
        "fc_L"     : [0.9175 - 0.0001034921],
        "pc_U"     : [0.9175 + 0.0002069841],
        "pc_L"     : [0.9175 - 0.0002069841],
        "mem_unit" : ["Years"],
        "sub_val"  : [float(st.session_state["q6_cooling_time"])],
        "sub_unit" : [st.session_state["q6_units"]],
        "grade"    : [0.0]
    }

    q6 = pd.DataFrame(q6)
    q6_val_fc = q6["sub_val"].between(q6["fc_L"], q6["fc_U"])
    q6_val_pc = q6["sub_val"].between(q6["pc_L"], q6["pc_U"])
    q6_val_opt = [q6_val_fc, q6_val_pc]
    q6_val_grd = [1.0, 0.5]
    q6["grade"] += np.select(q6_val_opt, q6_val_grd, default = 0.0)
    q6_unit_fc = q6["sub_unit"] == q6["mem_unit"]
    q6_unit_nc = q6["sub_unit"] != q6["mem_unit"]
    q6_unit_opt = [q6_unit_fc, q6_unit_nc]
    q6_unit_grd = [1.0, 0.0]
    q6["grade"] += np.select(q6_unit_opt, q6_unit_grd, default = 0.0)

    # ==============================
    q7 = {
        "mem_ans" : ["A"],
        "mem_mot" : ["fc"],
        "sub_ans" : [st.session_state["q7_crystal"]],
        "sub_mot" : [st.session_state["q7_motivation"]],
        "grade"   : [0.0]
    }

    q7 = pd.DataFrame(q7)
    q7_ans_fc = q7["sub_ans"] == q7["mem_ans"]
    q7_ans_nc = q7["sub_ans"] != q7["mem_ans"]
    q7_ans_opt = [q7_ans_fc, q7_ans_nc]
    q7_ans_grd = [1.0, 0.0]
    q7["grade"] += np.select(q7_ans_opt, q7_ans_grd, default = 0.0)
    q7_mot_fc = q7["sub_mot"] == "fc"
    q7_mot_pc = q7["sub_mot"] == "pc"
    q7_mot_nc = q7["sub_mot"] == "nc"
    q7_mot_opt = [q7_mot_fc, q7_mot_pc, q7_mot_nc]
    q7_mot_grd = [2.0, 1.0, 0.0]
    q7["grade"] += np.select(q7_mot_opt, q7_mot_grd, default = 0.0)

    # ==============================
    q8 = {
        "mem"   : ["Aetherite"],
        "sub"   : [st.session_state["q8_stable"]],
        "grade" : [0.0]
    }

    q8 = pd.DataFrame(q8)
    q8_fc = q8["sub"] == q8["mem"]
    q8_nc = q8["sub"] != q8["mem"]
    q8_opt = [q8_fc, q8_nc]
    q8_grd = [1.0, 0.0]
    q8["grade"] += np.select(q8_opt, q8_grd, default = 0.0)

    # ==============================
    q9 = {
        "mem_por"      : [17.99],
        "por_fc_U"     : [17.99 + 0.01077999],
        "por_fc_L"     : [17.99 - 0.01077999],
        "por_pc_U"     : [17.99 + 0.02155998],
        "por_pc_L"     : [17.99 - 0.02155998],
        "por_unit"     : ["%"],
        "mem_mic"      : [41.94],
        "mic_fc_U"     : [41.94 + 0.01277578],
        "mic_fc_L"     : [41.94 - 0.01277578],
        "mic_pc_U"     : [41.94 + 0.02555157],
        "mic_pc_L"     : [41.94 - 0.02555157],
        "mic_unit"     : ["%"],
        "sub_por"      : [float(st.session_state["q9_porosity"])],
        "sub_por_unit" : [st.session_state["q9a_units"]],
        "sub_mic"      : [float(st.session_state["q9_microporosity"])],
        "sub_mic_unit" : [st.session_state["q9b_units"]],
        "grade"        : [0.0]
    }

    q9 = pd.DataFrame(q9)
    q9_por_fc = q9["sub_por"].between(q9["por_fc_L"], q9["por_fc_U"])
    q9_por_pc = q9["sub_por"].between(q9["por_pc_L"], q9["por_pc_U"])
    q9_por_opt = [q9_por_fc, q9_por_pc]
    q9_por_grd = [1.0, 0.5]
    q9["grade"] += np.select(q9_por_opt, q9_por_grd, default = 0.0)
    q9_por_unit_fc = q9["sub_por_unit"] == q9["por_unit"]
    q9_por_unit_nc = q9["sub_por_unit"] != q9["por_unit"]
    q9_por_unit_opt = [q9_por_unit_fc, q9_por_unit_nc]
    q9_por_unit_grd = [1.0, 0.0]
    q9["grade"] += np.select(q9_por_unit_opt, q9_por_unit_grd, default = 0.0)
    q9_mic_fc = q9["sub_mic"].between(q9["mic_fc_L"], q9["mic_fc_U"])
    q9_mic_pc = q9["sub_mic"].between(q9["mic_pc_L"], q9["mic_pc_U"])
    q9_mic_opt = [q9_mic_fc, q9_mic_pc]
    q9_mic_grd = [1.0, 0.5]
    q9["grade"] += np.select(q9_mic_opt, q9_mic_grd, default = 0.0)
    q9_mic_unit_fc = q9["sub_mic_unit"] == q9["mic_unit"]
    q9_mic_unit_nc = q9["sub_mic_unit"] != q9["mic_unit"]
    q9_mic_unit_opt = [q9_mic_unit_fc, q9_mic_unit_nc]
    q9_mic_unit_grd = [1.0, 0.0]
    q9["grade"] += np.select(q9_mic_unit_opt, q9_mic_unit_grd, default = 0.0)

    # ==============================
    q10 = {
        "mem_ans" : ["Neither"],
        "sub_ans" : [st.session_state["q10_salt"]],
        "mem_mot" : ["fc"],
        "sub_mot" : [st.session_state["q10_motivation"]],
        "grade"   : [0.0]
    }

    q10 = pd.DataFrame(q10)
    q10_ans_fc = q10["sub_ans"] == q10["mem_ans"]
    q10_ans_nc = q10["sub_ans"] != q10["mem_ans"]
    q10_ans_opt = [q10_ans_fc, q10_ans_nc]
    q10_ans_grd = [1.0, 0.0]
    q10["grade"] += np.select(q10_ans_opt, q10_ans_grd, default = 0.0)
    q10_mot_fc = q10["sub_mot"] == "fc"
    q10_mot_pc = q10["sub_mot"] == "pc"
    q10_mot_nc = q10["sub_mot"] == "nc"
    q10_mot_opt = [q10_mot_fc, q10_mot_pc, q10_mot_nc]
    q10_mot_grd = [2.0, 1.0, 0.0]
    q10["grade"] += np.select(q10_mot_opt, q10_mot_grd, default = 0.0)

    # ==============================
    q11 = {
        "mem_ans" : ["Na2CO3"],
        "sub_ans" : [st.session_state["q11_salt"]],
        "mem_mot" : ["fc"],
        "sub_mot" : [st.session_state["q11_motivation"]],
        "grade"   : [0.0]
    }

    q11 = pd.DataFrame(q11)
    q11_ans_fc = q11["sub_ans"] == q11["mem_ans"]
    q11_ans_nc = q11["sub_ans"] != q11["mem_ans"]
    q11_ans_opt = [q11_ans_fc, q11_ans_nc]
    q11_ans_grd = [1.0, 0.0]
    q11["grade"] += np.select(q11_ans_opt, q11_ans_grd, default = 0.0)
    q11_mot_fc = q11["sub_mot"] == "fc"
    q11_mot_pc = q11["sub_mot"] == "pc"
    q11_mot_nc = q11["sub_mot"] == "nc"
    q11_mot_opt = [q11_mot_fc, q11_mot_pc, q11_mot_nc]
    q11_mot_grd = [3.0, 1.5, 0.0]
    q11["grade"] += np.select(q11_mot_opt, q11_mot_grd, default = 0.0)

    # calculate total
    questions = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11]
    total = sum(question["grade"].sum() for question in questions)

    # metadatafor png
    st.session_state["final_grade"] = str(total)
    st.session_state["q1_grade"]    = str(q1["grade"].item())
    st.session_state["q2_grade"]    = str(q2["grade"].item())
    st.session_state["q3_grade"]    = str(q3["grade"].item())
    st.session_state["q4_grade"]    = str(q4["grade"].item())
    st.session_state["q5_grade"]    = str(q5["grade"].item())
    st.session_state["q6_grade"]    = str(q6["grade"].item())
    st.session_state["q7_grade"]    = str(q7["grade"].item())
    st.session_state["q8_grade"]    = str(q8["grade"].item())
    st.session_state["q9_grade"]    = str(q9["grade"].item())
    st.session_state["q10_grade"]   = str(q10["grade"].item())
    st.session_state["q11_grade"]   = str(q11["grade"].item())

    # add results to submission
    cv.putText(warped_img, str(total), (850,455), cv.FONT_HERSHEY_SIMPLEX, 3.0, (0,0,255), 1)
    cv.putText(warped_img, student_id, (303,199), cv.FONT_HERSHEY_SIMPLEX, 2.0, (0,0,255), 1)
    cv.putText(warped_img, st.session_state["q1_grade"], (2257,421), cv.FONT_HERSHEY_SIMPLEX, 2.0, (0,0,255), 1)
    cv.putText(warped_img, st.session_state["q2_grade"], (2257,546), cv.FONT_HERSHEY_SIMPLEX, 2.0, (0,0,255), 1)
    cv.putText(warped_img, st.session_state["q3_grade"], (2257,671), cv.FONT_HERSHEY_SIMPLEX, 2.0, (0,0,255), 1)
    cv.putText(warped_img, st.session_state["q4_grade"], (2257,796), cv.FONT_HERSHEY_SIMPLEX, 2.0, (0,0,255), 1)
    cv.putText(warped_img, st.session_state["q5_grade"], (2257,914), cv.FONT_HERSHEY_SIMPLEX, 2.0, (0,0,255), 1)
    cv.putText(warped_img, st.session_state["q6_grade"], (2257,1039), cv.FONT_HERSHEY_SIMPLEX, 2.0, (0,0,255), 1)
    cv.putText(warped_img, st.session_state["q7_grade"], (2354,1281), cv.FONT_HERSHEY_SIMPLEX, 2.0, (0,0,255), 1)
    cv.putText(warped_img, st.session_state["q8_grade"], (2264,1714), cv.FONT_HERSHEY_SIMPLEX, 2.0, (0,0,255), 1)
    cv.putText(warped_img, st.session_state["q9_grade"], (2354,1914), cv.FONT_HERSHEY_SIMPLEX, 2.0, (0,0,255), 1)
    cv.putText(warped_img, st.session_state["q10_grade"], (2354,2321), cv.FONT_HERSHEY_SIMPLEX, 2.0, (0,0,255), 1)
    cv.putText(warped_img, st.session_state["q11_grade"], (2354,2908), cv.FONT_HERSHEY_SIMPLEX, 2.0, (0,0,255), 1)

    st.session_state["graded_submission"] = warped_img
    

# ------------------------------------------------------------
    
st.set_page_config(layout="wide")
    
st.title("Semester Test 1 — Theory")

st.markdown("""
### Instructions
1. Enter your name in the provided space.
2. Load the student submission.
3. If there is an error during loading, refresh your browser window and try again.
4. If it still doesn't work, send me an email with the student's details and move on to the next submission.
5. Verify that the name on the submission matches the name of the file.
6. Transfer the answers on the submission to the spaces provided.
7. **DON'T** use commas for decimal marks. Please use a full-stop.
8. If they didn't add the cardinal direction, select the "NA" option from the drop-down menu.
9. When you are done, press the grade button.
10. Download the graded submission and store it in a separate folder. **DON'T** change the filename.
""")

# load class list and submission
grader = st.text_input("Name of grader", key="graderName")
image = st.file_uploader("Select the student submission", type = ["png", "jpg"])

if image is not None and grader.strip():
    # extract student details from img filename
    filename = image.name
    filename = filename.replace(".png","")
    surname, name, emplid = filename.split("_")
    student_id = f"{name} {surname} ({emplid})"

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

        # for pt, col in zip([top_left, top_right, bottom_right, bottom_left], 
        #             [(255,0,0), (0,255,0), (0,0,255), (255,255,0)]):
        #     cv.circle(cv_img, (int(pt[0]), int(pt[1])), 15, col, -1)

        # Prepare the image for warping
        current_coords = np.float32([[top_left[0], top_left[1]],
                                     [top_right[0], top_right[1]],
                                     [bottom_right[0], bottom_right[1]],
                                     [bottom_left[0], bottom_left[1]]])
        target_coords = np.float32([[177,177],
                                    [2303,177],
                                    [2303,3331],
                                    [177,3331]])
        transformation_matrix = cv.getPerspectiveTransform(current_coords,
                                                           target_coords)

        tm_inverted = np.linalg.inv(transformation_matrix)

        template_corners = np.array([[0,0],
                                     [2480,0],
                                     [2480,3508],
                                     [0,3508]], dtype=np.float32).reshape(-1,1,2)

        src_corners = cv.perspectiveTransform(template_corners, tm_inverted).squeeze()

        img_h, img_w = cv_img.shape[:2]
        src_corners[:, 0] = np.clip(src_corners[:, 0], 0, img_w - 1)
        src_corners[:, 1] = np.clip(src_corners[:, 1], 0, img_h - 1)

        final_matrix = cv.getPerspectiveTransform(src_corners,
                                                  np.float32([[0, 0], [2480, 0], [2480, 3508], [0, 3508]]))

        # transform the image
        warped_img = cv.warpPerspective(cv_img,
                                        final_matrix,
                                        (2480,3508))

        processed_img = cv.imencode(".png",warped_img)[1]
        b64_str = base64.b64encode(processed_img).decode("utf-8")
        img_url = f"data:image/png;base64,{b64_str}"


    except:
        st.error("Can't process submission.")

    

    # display submission and grading tools in two cols
    col1, col2 = st.columns(2)
    
    with col1:    
        submission_viewer(img_url)

    with col2:
        with st.expander("Question 1 to 5", expanded = False):
            with st.expander("Question 1", expanded = False):
                col_q1_1, col_q1_2 = st.columns(2)

                with col_q1_1:
                    st.text_input("Plate velocity", key = "q1_velocity")

                with col_q1_2:
                    st.selectbox("Units",
                                 ("mm/yr", "Other"),
                                 index = None,
                                 placeholder = "Select units...",
                                 key = "q1_units")
                pass

            #==============================
            with st.expander("Question 2", expanded = False):
                st.selectbox("Type of boundary",
                             ("Transform", "Other"),
                             index = None,
                             placeholder = "Select boundary...",
                             key = "q2_boundary")
                pass

            # ==============================
            with st.expander("Question 3", expanded = False):
                col_q3_1, col_q3_2 = st.columns(2)

                with col_q3_1:
                    st.text_input("Temperature", key = "q3_temperature")

                with col_q3_2:
                    st.selectbox("Units",
                                 ("°C", "Other"),
                                 index = None,
                                 placeholder = "Select units...",
                                 key = "q3_units")
                pass

            # ==============================
            with st.expander("Question 4", expanded = False):
                col_q4_1, col_q4_2 = st.columns(2)

                with col_q4_1:
                    st.text_input("Pressure", key = "q4_pressure")

                with col_q4_2:
                    st.selectbox("Units",
                                 ("Megapascals", "Other"),
                                 index = None,
                                 placeholder = "Select units...",
                                 key = "q4_units")
                pass

            # ==============================
            with st.expander("Question 5", expanded = False):
                st.selectbox("Completely solid state",
                             ("A", "Other"),
                             index = None,
                             placeholder = "Make a selection ...",
                             key = "q5_state")
                pass

            pass
        
        with st.expander("Question 6 to 11", expanded = False):
            with st.expander("Question 6", expanded = False):
                col_q6_1, col_q6_2 = st.columns(2)

                with col_q6_1:
                    st.text_input("Cooling time", key = "q6_cooling_time")

                with col_q6_2:
                    st.selectbox("Units",
                                 ("Years", "Other"),
                                 index = None,
                                 placeholder = "Select units ...",
                                 key = "q6_units")
                pass
        
            # ==============================
            with st.expander("Question 7", expanded = False):
                q7_col_1, q7_col_2 = st.columns(2)

                with q7_col_1:
                    st.selectbox("Largest crystals",
                                 ("A", "Other"),
                                 index = None,
                                 placeholder = "Make a selection ...",
                                 key = "q7_crystal")

                with q7_col_2:
                    st.selectbox("Motivation",
                                 ("fc", "pc", "nc"),
                                 index = None,
                                 placeholder = "Make a selection ...",
                                 key = "q7_motivation")

                pass

            # ==============================
            with st.expander("Question 8", expanded = False):
                st.selectbox("Stable phase",
                             ("Aetherite", "Other"),
                             index = None,
                             placeholder = "Make a selection ...",
                             key = "q8_stable")
                pass

            # ==============================
            with st.expander("Question 9", expanded = False):
                q9_col_1, q9_col_2 = st.columns(2)

                with q9_col_1:
                    st.text_input("9a) Porosity", key = "q9_porosity")
                    st.text_input("9b) Microporosity", key = "q9_microporosity")

                with q9_col_2:
                    st.selectbox("Units",
                                 ("%", "Other"),
                                 index = None,
                                 placeholder = "Select units ...",
                                 key = "q9a_units")
                    st.selectbox("Units",
                                 ("%", "Other"),
                                 index = None,
                                 placeholder = "Make a selection ...",
                                 key = "q9b_units")

                pass

            # ==============================
            with st.expander("Question 10", expanded = False):
                q10_col_1, q10_col_2 = st.columns(2)

                with q10_col_1:
                    st.selectbox("Answer",
                                 ("Neither", "Other"),
                                 index = None,
                                 placeholder = "Make a selection ...",
                                 key = "q10_salt")

                with q10_col_2:
                    st.selectbox("Motivation",
                                 ("fc", "pc", "nc"),
                                 index = None,
                                 placeholder = "Make a selection ...",
                                 key = "q10_motivation")

                pass
            # ==============================
            with st.expander("Question 11", expanded = False):
                q11_col_1, q11_col_2 = st.columns(2)

                with q11_col_1:
                    st.selectbox("Answer",
                                 ("Na2CO3", "Other"),
                                 index = None,
                                 placeholder = "Make a selection ...",
                                 key = "q11_salt")

                with q11_col_2:
                    st.selectbox("Motivation",
                                 ("fc", "pc", "nc"),
                                 index = None,
                                 placeholder = "Make a selection ...",
                                 key = "q11_motivation")

                pass

            pass

        
    st.button("Grade", on_click=grade_submission)

    if "graded_submission" in st.session_state:
        st.image(st.session_state["graded_submission"])

        final_img_rgb = cv.cvtColor(st.session_state["graded_submission"], cv.COLOR_BGR2RGB)
        final_img_pil = Image.fromarray(final_img_rgb)

        filename = filename + ".png"
        grader_timestamp = datetime.now().isoformat()
        meta_info = PngInfo()
        meta_info.add_text("Grader", grader.strip())
        meta_info.add_text("GradedAt", grader_timestamp)
        meta_info.add_text("final", st.session_state["final_grade"])
        meta_info.add_text("q1", st.session_state["q1_grade"])
        meta_info.add_text("q2", st.session_state["q2_grade"])  
        meta_info.add_text("q3", st.session_state["q3_grade"])  
        meta_info.add_text("q4", st.session_state["q4_grade"])  
        meta_info.add_text("q5", st.session_state["q5_grade"])  
        meta_info.add_text("q6", st.session_state["q6_grade"])  
        meta_info.add_text("q7", st.session_state["q7_grade"])  
        meta_info.add_text("q8", st.session_state["q8_grade"])  
        meta_info.add_text("q9", st.session_state["q9_grade"])  
        meta_info.add_text("q10", st.session_state["q10_grade"])  
        meta_info.add_text("q11", st.session_state["q11_grade"]) 
        buffer = io.BytesIO()
        final_img_pil.save(buffer, format="PNG", pnginfo=meta_info)
        st.download_button(label=f"Download {filename}", data=buffer, file_name=filename, mime="image/png")

