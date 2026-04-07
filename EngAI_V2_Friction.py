import streamlit as st
import time
from datetime import timedelta

# Try to import drawable canvas
try:
    from streamlit_drawable_canvas import st_canvas
    _canvas_ok = True
except ImportError:
    _canvas_ok = False

st.set_page_config(page_title="STATICS Method — Incline Friction", page_icon="📐", layout="centered")

# ==========================================
# 1. PROBLEM DEFINITION & DIAGRAM
# ==========================================
st.title("Minimum Force on an Incline")

# Replace this URL with your local file path or hosted image link for image_199a62.png
PROBLEM_IMAGE_URL = "https://i.imgur.com/a9nylti.png"

try:
    st.image(PROBLEM_IMAGE_URL, caption="Problem Diagram", use_container_width=True)
except Exception:
    st.error("Could not load image. Please check the PROBLEM_IMAGE_URL variable in the code.")

st.info("📄 **Reference:** Refer to the diagram of the pipe being pulled up the incline.")

PROBLEM_TEXT = (
    "**The Scenario:**\n"
    "Determine the angle $\\phi$ at which the applied force $P$ should act on the pipe so that $P$ is as small as possible for pulling the pipe up the incline. "
    "What is the corresponding value of $P$?\n\n"
    "**The System Specs:**\n"
    "* The pipe weighs $W$.\n"
    "* The slope angle $\\alpha$ is known.\n"
    "* Express the answer in terms of the angle of kinetic friction, $\\theta = \\tan^{-1}(\\mu_k)$.\n\n"
    "**The Objective:**\n"
    "1. Derive the algebraic expression for $P$ required to move the pipe.\n"
    "2. Use trigonometric properties to minimize the value of $P$.\n"
    "3. Find the optimal angle $\\phi$ and the minimum force $P_{min}$."
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
        "comp_correct": False,
        "eq_correct": False,
        "deriv1_correct": False,
        "deriv2_correct": False
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
    st.caption("Read carefully and identify the unique nature of this problem.")
    
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
    st.write("This is a symbolic problem. We are not plugging in numbers; we are deriving formulas. Let's identify the variables.")
    
    q_goal = st.selectbox("What mathematical condition represents 'P is as small as possible'?", 
                          ["Select...", "Set P = 0", "Find the minimum of the function P(φ)", "Set friction to zero", "Make the angle φ equal to α"])

    if st.session_state.step_idx == 1 and st.session_state.timer_finished:
        if st.button("Check Mechanics & Continue"):
            if q_goal == "Find the minimum of the function P(φ)":
                st.success("Correct! We must write an equation for $P$ in terms of $\\phi$, and then find what value of $\\phi$ minimizes $P$.")
                st.session_state.step_idx = 2
                st.rerun()
            else:
                st.error("Review the objective. We can't change the friction or weight, but we can change the angle of our pull to optimize the force required.")

# ======================================================
# T — TRANSLATE TO DIAGRAM (Step 2: FBD)
# ======================================================
if st.session_state.step_idx >= 2:
    st.divider()
    st.header("T — Translate to a Diagram (FBD)")

    st.write("Visualize all the forces acting on the pipe.")
    
    with st.expander("Need a hint?"):
        st.write("There are 4 main forces acting on the pipe: its weight, the pulling force, the surface pushing back up, and the surface resisting the sliding motion.")
    
    st.info("Using the canvas toolbar, sketch the FBD of the pipe on the incline.")
    st.caption("Draw the pipe. Add the Weight (W), Normal Force (N), Friction Force (F), and applied Force (P) at their correct relative angles.")
    
    if _canvas_ok:
        canvas_fbd = st_canvas(
            stroke_width=3, stroke_color="#000", background_color="#fff",
            height=300, width=500, drawing_mode="line", display_toolbar=True, key="canvas_fbd_pipe"
        )

        if st.button("Check FBD"):
            num_lines = len(canvas_fbd.json_data["objects"]) if canvas_fbd.json_data else 0
            if num_lines >= 4:
                st.success("FBD looks populated. You should have W, N, F, and P. Proceed.")
                st.session_state.step_idx = 3
                st.rerun()
            else:
                st.error(f"Detected {num_lines} lines. Think about the 4 specific forces acting on a body sliding on a rough surface.")

# ======================================================
# A — ASSIGN (Step 3: Coordinates)
# ======================================================
if st.session_state.step_idx >= 3:
    st.divider()
    st.header("A — Assign Coordinates")
    
    st.write("Choosing the right coordinate system makes the algebra much easier.")
    
    coord_choice = st.radio("Which coordinate system is most efficient for a block on an incline?",
                            ["Standard: +X is horizontal, +Y is vertical",
                             "Tilted: +X is parallel to the incline (upward), +Y is perpendicular to the incline"])
    
    if st.button("Confirm Coordinates"):
        if "Tilted" in coord_choice:
            st.success("Correct! Tilting the axes means the Normal force and Friction force perfectly align with the Y and X axes, respectively. Only W and P need to be broken into components.")
            st.session_state.step_idx = 4
            st.rerun()
        else:
            st.error("If you use standard axes, N, F, and P will ALL be at strange angles, requiring complicated trig for every single force. Try the other way.")

# ======================================================
# T — TRANSLATE TO COMPONENTS (Step 4)
# ======================================================
if st.session_state.step_idx >= 4:
    st.divider()
    st.header("T — Translate Forces to Components")
    st.caption("Break the forces into components based on your tilted X-Y axes.")
    
    st.write("Match the force to its correct components. Remember, X is along the ramp, Y is perpendicular to the ramp.")

    with st.expander("Need a hint?"):
        st.write("Look at the angle $\\alpha$ for the weight. The weight points straight down. Geometry tells us the angle between the Weight vector and the negative Y-axis is exactly $\\alpha$.")
        st.write("For $P$, the angle $\\phi$ is measured directly from the X-axis (the incline).")

    q_weight_x = st.selectbox("X-component of Weight ($W_x$):", ["Select...", "W", "-W * sin(α)", "-W * cos(α)", "0"])
    q_weight_y = st.selectbox("Y-component of Weight ($W_y$):", ["Select...", "-W", "-W * sin(α)", "-W * cos(α)", "0"])
    q_pull_y = st.selectbox("Y-component of Pulling Force ($P_y$):", ["Select...", "P * cos(φ)", "P * sin(φ)", "P", "0"])

    if st.button("Verify Components"):
        if q_weight_x == "-W * sin(α)" and q_weight_y == "-W * cos(α)" and q_pull_y == "P * sin(φ)":
            st.success("Correct! The weight pulls down and backwards. The pull P has an upward Y-component that will help relieve the normal force.")
            st.session_state.comp_correct = True
            st.session_state.step_idx = 5
            st.rerun()
        else:
            st.error("Check your trigonometry. If the ramp is almost flat ($\\alpha$ ≈ 0), $W_y$ should be almost all of W, and $W_x$ should be almost 0. Which trig functions match that logic?")

# ======================================================
# I — IMPLEMENT (Step 5: Equilibrium Equations)
# ======================================================
if st.session_state.step_idx >= 5:
    st.divider()
    st.header("I — Implement Equilibrium Equations")
    st.caption("Write out the algebraic equations before trying to solve them.")
    
    st.markdown("#### Acknowledge the Required Equations")
    st.write("Since the pipe is just barely moving up the incline at a constant rate, it is in equilibrium.")
    
    chk_fx = st.checkbox("$\\sum F_x = 0$ (Forces parallel to the ramp must balance: Pull vs. Gravity + Friction)")
    chk_fy = st.checkbox("$\\sum F_y = 0$ (Forces perpendicular to the ramp must balance: Normal + Pull vs. Gravity)")
    chk_fric = st.checkbox("Kinetic Friction Equation ($F = \\mu_k N$) must be substituted into the X equation.")
    
    if st.button("Validate Logic & Equations"):
        if chk_fx and chk_fy and chk_fric:
            st.success("Excellent! You have the complete set of algebraic tools to isolate P.")
            st.session_state.step_idx = 6
            st.rerun()
        else:
            st.warning("Please acknowledge all three principles required to solve this system.")

# ======================================================
# C — COMPUTE (Step 6: Guided Derivation)
# ======================================================
if st.session_state.step_idx >= 6:
    st.divider()
    st.header("C — Compute Results")
    st.caption("Let's derive the formula for $P$ step-by-step.")

    # --- Part 1: Normal Force ---
    st.subheader("Part 1: Find the Normal Force (N)")
    st.write("Using $\\sum F_y = 0$, isolate the Normal Force ($N$).")
    
    with st.expander("Need a hint?"):
        st.write("The forces in the Y direction are: Normal Force ($N$, up), Y-component of Pull ($P \\sin\\phi$, up), and Y-component of Weight ($-W \\cos\\alpha$, down).")

    q_normal = st.radio("Which expression correctly represents $N$?", 
                        ["N = W * cos(α)", 
                         "N = W * cos(α) + P * sin(φ)", 
                         "N = W * cos(α) - P * sin(φ)"])
    
    if st.button("Check Normal Force"):
        if q_normal == "N = W * cos(α) - P * sin(φ)":
            st.success("Correct! Pulling upward at an angle *reduces* the normal force pressing into the ground.")
            st.session_state.deriv1_correct = True
        else:
            st.error("Write out $\\sum F_y = 0 \\Rightarrow N + P_y - W_y = 0$. Solve for N.")

    # --- Part 2: Simplify with Friction Angle ---
    if st.session_state.get("deriv1_correct"):
        st.divider()
        st.subheader("Part 2: Isolate $P$ and use the Friction Angle $\\theta$")
        st.write("Substitute $N$ into $\\sum F_x = 0$ and isolate $P$. Then, use the given relation $\\mu_k = \\tan\\theta = \\frac{\\sin\\theta}{\\cos\\theta}$.")
        
        with st.expander("Need a heavy hint for the algebra?"):
            st.write("1. $\\sum F_x = P \\cos\\phi - W \\sin\\alpha - \\mu_k N = 0$")
            st.write("2. Substitute N: $P \\cos\\phi - W \\sin\\alpha - \\mu_k(W \\cos\\alpha - P \\sin\\phi) = 0$")
            st.write("3. Group the $P$ terms: $P(\\cos\\phi + \\mu_k \\sin\\phi) = W(\\sin\\alpha + \\mu_k \\cos\\alpha)$")
            st.write("4. Substitute $\\mu_k = \\frac{\\sin\\theta}{\\cos\\theta}$ and multiply the top and bottom by $\\cos\\theta$.")
            st.write("5. You will get terms like $\\cos\\phi\\cos\\theta + \\sin\\phi\\sin\\theta$. Use trig angle difference identities!")

        q_trig = st.radio("Using the trigonometric identity $\\cos(A-B) = \\cos A \\cos B + \\sin A \\sin B$, what does the denominator $(\\cos\\phi + \\mu_k \\sin\\phi)$ simplify to after introducing $\\theta$?",
                          ["cos(φ + θ)", "cos(φ - θ)", "sin(φ - θ)"])
        
        if st.button("Check Trig Identity"):
            if q_trig == "cos(φ - θ)":
                st.success("Brilliant! The full equation simplifies elegantly to:  $P = \\frac{W \\sin(\\alpha + \\theta)}{\\cos(\\phi - \\theta)}$")
                st.session_state.deriv2_correct = True
            else:
                st.error("Look closely at the sign in the trig identity expansion.")

    # --- Part 3: Minimization ---
    if st.session_state.get("deriv2_correct"):
        st.divider()
        st.subheader("Part 3: Minimize $P$")
        st.write("You derived the equation: $P = \\frac{W \\sin(\\alpha + \\theta)}{\\cos(\\phi - \\theta)}$")
        st.write("To make $P$ as **small as possible**, what must be true about the denominator?")
        
        with st.expander("Need a hint?"):
            st.write("If you want the smallest possible fraction, you need the *largest* possible denominator. What is the maximum possible value for a cosine function? At what angle does cosine reach that maximum?")

        q_phi = st.radio("To minimize P, what must the angle $\\phi$ equal?", ["0", "α", "θ", "90 degrees"])
        
        if st.button("Check Minimization & Finish"):
            if q_phi == "θ":
                st.balloons()
                st.session_state.step_idx = 7
                st.rerun()
            else:
                st.error("To maximize $\\cos(\\phi - \\theta)$, the inside of the cosine must be $0$. So, $\\phi - \\theta = 0$. Solve for $\\phi$.")

# ======================================================
# S — SANITY CHECK (Step 7)
# ======================================================
if st.session_state.step_idx >= 7:
    st.divider()
    st.header("S — Sanity Check")
    
    st.success("Calculations Complete!")
    
    st.markdown("### Final Theoretical Results:")
    st.write(r"- **Optimal Pulling Angle ($\phi$)**: $\theta$ (The angle of kinetic friction)")
    st.write(r"- **Minimum Force required ($P_{min}$)**: $W \sin(\alpha + \theta)$")
    
    st.markdown("### Reflection")
    st.write("Think about your final results and check the boxes if they make physical sense:")
    
    check1 = st.checkbox("If I pull perfectly parallel to the ramp ($\\phi = 0$), I maximize my pulling effort along the ramp, but I don't help lift the pipe at all, so friction stays high.")
    check2 = st.checkbox("If I pull too far upward, I reduce friction nicely, but I waste a lot of my force trying to lift the pipe instead of pulling it forward.")
    check3 = st.checkbox("The math proves there is a 'sweet spot' exactly equal to the friction angle $\\theta$. At this angle, the tradeoff between reducing friction and pulling forward is perfectly optimized!")
    
    if check1 and check2 and check3:
        st.info("You have successfully applied the S.T.A.T.I.C.S. approach to a complex algebraic derivation! Great job.")
        
        if st.button("Start New Problem"):
            st.session_state.clear()
            st.rerun()