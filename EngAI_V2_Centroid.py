import streamlit as st
import time
from datetime import timedelta
import math

st.set_page_config(page_title="STATICS Method — Centroids", page_icon="🎯", layout="centered")

# ==========================================
# 1. PROBLEM DEFINITION & DIAGRAM
# ==========================================
st.title("Locate the Centroid of the Plane Area")

# Replace this URL with your local file path or hosted image link
PROBLEM_IMAGE_URL = "https://i.imgur.com/hsLsIHl.png"

try:
    st.image(PROBLEM_IMAGE_URL, caption="Problem 5.5 Diagram", use_container_width=True)
except Exception:
    st.error("Could not load image. Please check the PROBLEM_IMAGE_URL variable in the code.")

st.info("📄 **Reference:** Refer to the diagram showing the plate with dimensions 8 in. by 12 in. and two cutouts.")

PROBLEM_TEXT = (
    "**The Scenario:**\n"
    "You need to find the exact center of mass (centroid) of the given 2D plane area. "
    "This shape is not a standard rectangle or circle, so you must use the method of composite areas.\n\n"
    "**The System Specs:**\n"
    "* **Overall Base:** $8$ in.\n"
    "* **Overall Height:** $12$ in.\n"
    "* **Cutouts:** Two quarter-circles of radius $r = 4$ in. removed from the top-right and bottom-right corners.\n"
    "* **Origin:** The coordinate system $(0,0)$ is placed exactly at the bottom-left corner of the shape.\n\n"
    "**The Objective:**\n"
    "1. Break the complex shape down into standard geometric parts.\n"
    "2. Determine the area and local centroid coordinates for each individual part.\n"
    "3. Apply the composite area formulas to find the global centroid $(\\bar{X}, \\bar{Y})$."
)
st.markdown(PROBLEM_TEXT)
st.divider()

# ----------------------------
# 2. STATE MANAGEMENT
# ----------------------------
def init_state():
    defaults = {
        "step_idx": 0,
        "start_time": None,
        "timer_finished": False,
        "parts_correct": False,
        "geom_correct": False,
        "area_correct": False
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()
STUDY_DURATION = 180 

# ----------------------------
# 3. SIDEBAR RESET
# ----------------------------
if st.sidebar.button("🔄 Reset Problem"):
    st.session_state.clear()
    st.rerun()

# ----------------------------
# STEP 0: START
# ----------------------------
if st.session_state.step_idx == 0:
    if st.button("▶️ Begin S.T.A.T.I.C.S. Method"):
        st.session_state.step_idx = 1
        st.session_state.start_time = time.time()
        st.rerun()
    st.stop()

# ======================================================
# S — STUDY (Step 1)
# ======================================================
if st.session_state.step_idx >= 1:
    st.header("S — Study the Problem")
    st.caption("Read carefully and identify the best composite strategy.")
    
    timer_placeholder = st.empty()
    if not st.session_state.timer_finished:
        elapsed = time.time() - st.session_state.start_time
        remaining = STUDY_DURATION - int(elapsed)
        if remaining <= 0:
            st.session_state.timer_finished = True
            st.rerun()
        timer_placeholder.warning(f"⏳ **Focus Period:** {str(timedelta(seconds=remaining))[2:7]} remaining.")
        if st.button("⏭️ Skip Timer"):
            st.session_state.timer_finished = True
            st.rerun()
        time.sleep(1)
        st.rerun()
    else:
        timer_placeholder.success("✅ Study time complete!")

    st.write("#### System Mechanics Check")
    st.write("There are two ways to solve composite areas: Additive (adding pieces together) or Subtractive (starting with a big piece and subtracting holes).")
    
    q_method = st.selectbox("Which strategy is most efficient for this specific geometry?", 
                          ["Select...", 
                           "Additive: A left rectangle + a middle square + two spandrels", 
                           "Subtractive: One large rectangle minus two quarter-circles"])

    if st.session_state.step_idx == 1 and st.session_state.timer_finished:
        if st.button("Check Strategy & Continue"):
            if "Subtractive" in q_method:
                st.success("Correct! The subtractive method requires tracking fewer parts and uses standard quarter-circles rather than obscure 'spandrel' formulas.")
                st.session_state.step_idx = 2
                st.rerun()
            else:
                st.error("While the additive method *works*, finding the centroid of a 'spandrel' (the sharp pointy bit left over) is much harder than just subtracting a quarter circle. Try the other method.")

# ======================================================
# T — TRANSLATE TO COMPOSITE PARTS (Step 2)
# ======================================================
if st.session_state.step_idx >= 2:
    st.divider()
    st.header("T — Translate to Composite Parts")
    st.caption("Identify the distinct shapes you will use for your subtractive method.")

    st.write("Check the three geometric parts that will make up your composite table:")
    
    c1 = st.checkbox("Part 1: A solid rectangular plate (8 in. wide by 12 in. tall).")
    c2 = st.checkbox("Part 2: A quarter-circle cutout (r = 4 in.) located at the bottom-right.")
    c3 = st.checkbox("Part 3: A quarter-circle cutout (r = 4 in.) located at the top-right.")
    c4 = st.checkbox("Part 4: A triangle located at the origin.")
    
    if st.button("Verify Parts"):
        if c1 and c2 and c3 and not c4:
            st.success("Correct. We will start with the large rectangle and subtract the two corner cutouts.")
            st.session_state.step_idx = 3
            st.rerun()
        else:
            st.error("Carefully review the required shapes. You only need the base rectangle and the two specific circular cutouts.")

# ======================================================
# A — ASSIGN (Step 3: Coordinates)
# ======================================================
if st.session_state.step_idx >= 3:
    st.divider()
    st.header("A — Assign Coordinates")
    
    st.write("The origin $(0,0)$ is explicitly given at the bottom-left corner. We must acknowledge how this affects our centroid coordinates.")
    
    st.markdown("**Assumption Strategy:**")
    st.info("Because the cutouts are on the right side of the shape, their local 'x' centroids will be located by starting at the right edge ($x=8$) and subtracting the local quarter-circle centroid distance. You cannot just use the quarter-circle formula directly from 0!")
    
    if st.button("Acknowledge Coordinate System"):
        st.session_state.step_idx = 4
        st.rerun()

# ======================================================
# T — TRANSLATE TO COMPONENTS (Step 4: Geometry)
# ======================================================
if st.session_state.step_idx >= 4:
    st.divider()
    st.header("T — Translate to Components (Geometry)")
    st.caption("Calculate the raw geometric properties of a quarter circle before building your table.")
    
    st.write("Look up or recall the geometric centroid formulas for a standard quarter circle.")

    with st.expander("Need a hint?"):
        st.write("The area of a full circle is $\\pi r^2$. A quarter circle is exactly 1/4 of that.")
        st.write("Check the inside cover or the appendix of your Statics textbook for the centroid location of a quarter-circular area. The formula involves the radius $r$ and $\\pi$.")

    q_area = st.number_input("What is the area of ONE of the quarter-circle cutouts? (in²):", min_value=0.0, step=1.0)
    q_dist = st.number_input("What is the perpendicular distance from the straight edge (the radius) to the local centroid of the quarter-circle? (in):", min_value=0.0, step=0.1)

    if st.button("Verify Quarter-Circle Geometry"):
        if abs(q_area - 12.57) < 0.2 and abs(q_dist - 1.70) < 0.1:
            st.success("Correct! Area ≈ $12.57$ in², and the local centroid offset is ≈ $1.70$ in. You are ready to build your composite table.")
            st.session_state.geom_correct = True
            st.session_state.step_idx = 5
            st.rerun()
        else:
            st.error("Check your textbook formulas and use $r = 4$.")

# ======================================================
# I — IMPLEMENT (Step 5: Composite Equations)
# ======================================================
if st.session_state.step_idx >= 5:
    st.divider()
    st.header("I — Implement Composite Equations")
    st.caption("Map out your strategy for the composite table.")
    
    st.write("To find the global centroid, we use weighted averages:")
    st.write("$\\bar{X} = \\frac{\\sum (\\bar{x}_i A_i)}{\\sum A_i}$")
    st.write("$\\bar{Y} = \\frac{\\sum (\\bar{y}_i A_i)}{\\sum A_i}$")
    
    st.markdown("#### Table Logic Check")
    chk_signs = st.checkbox("I must enter the Area of the two cutouts as **NEGATIVE** numbers in my calculations.")
    chk_xbar = st.checkbox("To find the global $\\bar{x}$ of the cutouts, I must subtract their $1.70$ in. offset from the total width of $8$ in. ($\\bar{x} = 8 - 1.70$).")
    chk_ybar = st.checkbox("To find the global $\\bar{y}$ of the top cutout, I must subtract its $1.70$ in. offset from the total height of $12$ in. ($\\bar{y} = 12 - 1.70$).")
    
    if st.button("Validate Table Logic"):
        if chk_signs and chk_xbar and chk_ybar:
            st.success("Excellent! You understand how to translate local shape properties into the global $(0,0)$ coordinate system.")
            st.session_state.step_idx = 6
            st.rerun()
        else:
            st.warning("Please acknowledge all three principles. Signs and global coordinate offsets are the #1 cause of errors in centroid problems.")

# ======================================================
# C — COMPUTE (Step 6: Guided Math)
# ======================================================
if st.session_state.step_idx >= 6:
    st.divider()
    st.header("C — Compute Results")
    st.caption("Solve algebraically for the global properties.")

    st.write("**Step A: Total Area**")
    with st.expander("Need a hint for Area?"):
        st.write("Total Area = Area of Rectangle ($8 \\times 12$) MINUS the Area of Cutout 1 MINUS the Area of Cutout 2.")
    area_val = st.number_input("Calculate Total Area $\\sum A$ (in²):", min_value=0.0, format="%.2f")
    
    st.write("**Step B: Global $\\bar{X}$**")
    with st.expander("Need a hint for X-bar?"):
        st.write("Calculate $\\sum \\bar{x}A$.")
        st.write("1. Rectangle: Area = $96$, $\\bar{x} = 4$.")
        st.write("2. Cutouts: Area = $-12.57$, $\\bar{x} = (8 - 1.70) = 6.30$.")
        st.write("Sum them up, then divide by your Total Area.")
    x_val = st.number_input("Calculate Global $\\bar{X}$ (in):", min_value=0.0, format="%.2f")

    st.write("**Step C: Global $\\bar{Y}$**")
    with st.expander("Need a hint for Y-bar?"):
        st.write("Look closely at the overall shape. Is there a line of symmetry? If the top half mirrors the bottom half perfectly, you don't even need to do the math for $\\bar{Y}$!")
    y_val = st.number_input("Calculate Global $\\bar{Y}$ (in):", min_value=0.0, format="%.2f")
    
    if st.button("Check Centroids and Finish"):
        ok_area = abs(area_val - 70.87) < 0.5
        ok_x = abs(x_val - 3.18) < 0.1
        ok_y = abs(y_val - 6.0) < 0.1
        
        if ok_area and ok_x and ok_y:
            st.balloons()
            st.session_state.step_idx = 7
            st.rerun()
        else:
            if not ok_area:
                st.error("Check Total Area. $96 - 12.57 - 12.57$.")
            if not ok_x:
                st.error("Check $\\bar{X}$. Verify your $\\sum \\bar{x}A$ calculation. Did you remember to make the cutout areas negative when multiplying by their positive x-coordinates?")
            if not ok_y:
                st.error("Check $\\bar{Y}$. The total height is 12. Where is the exact vertical middle?")

# ======================================================
# S — SANITY CHECK (Step 7)
# ======================================================
if st.session_state.step_idx >= 7:
    st.divider()
    st.header("S — Sanity Check")
    
    st.success("Calculations Complete!")
    
    st.markdown("### Final Global Centroid:")
    st.write("- **Total Area**: $70.87$ in²")
    st.write("- **$\\bar{X}$**: $3.18$ in")
    st.write("- **$\\bar{Y}$**: $6.00$ in")
    
    st.markdown("### Reflection")
    st.write("Think about your final results and check the boxes if they make physical sense:")
    
    check1 = st.checkbox("The value for $\\bar{Y} = 6.0$ makes perfect sense because the shape is horizontally symmetrical. The 'pull' of the top half perfectly balances the 'pull' of the bottom half.")
    check2 = st.checkbox("If the shape were a solid rectangle, $\\bar{X}$ would be exactly $4.0$. Because mass (the cutouts) was removed from the RIGHT side, the 'balance point' naturally shifts to the LEFT to compensate.")
    check3 = st.checkbox("Therefore, $\\bar{X} = 3.18$ in. (being slightly to the left of the middle) logically verifies our math.")
    
    if check1 and check2 and check3:
        st.info("You have successfully applied the S.T.A.T.I.C.S. approach to a composite area problem. Excellent logical verification!")
        
        if st.button("Start New Problem"):
            st.session_state.clear()
            st.rerun()