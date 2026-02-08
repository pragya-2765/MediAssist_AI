import streamlit as st
import requests
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="MediAssist AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a Professional Medical UI
st.markdown("""
    <style>
        /* Main body styling */
        .main {
            padding: 2rem;
            background-color: #f8fafc;
        }
        
        /* Header styling - Modern Medical Blue */
        .header-container {
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            padding: 2.5rem;
            border-radius: 15px;
            color: white;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }
        
        .header-container h1 {
            margin: 0;
            font-size: 2.8rem;
            font-weight: 800;
            letter-spacing: -0.5px;
        }
        
        .header-container p {
            margin: 0.5rem 0 0 0;
            font-size: 1.2rem;
            opacity: 0.9;
            font-weight: 300;
        }
        
        /* Section styling - Clean & White */
        .section-card {
            background: white;
            padding: 2rem;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            border-top: 5px solid #3b82f6;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
        }
        
        .section-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }
        
        .section-card h2 {
            color: #1e293b;
            margin-top: 0;
            font-size: 1.4rem;
            font-weight: 700;
        }
        
        /* Button styling - High Contrast */
        .stButton button {
            background: #2563eb;
            color: white;
            border: none;
            padding: 0.6rem 2rem;
            border-radius: 8px;
            font-weight: 600;
            width: 100%;
            transition: all 0.2s ease;
        }
        
        .stButton button:hover {
            background: #1d4ed8;
            border: none;
            color: white;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        }

        /* Status badge */
        .status-badge {
            display: inline-block;
            background: #dcfce7;
            color: #166534;
            padding: 0.3rem 0.8rem;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 700;
            border: 1px solid #bbf7d0;
        }
        
        /* Analysis result styling */
        .analysis-result {
            background: #f1f5f9;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 5px solid #0ea5e9;
            margin-top: 1rem;
        }
        
        .analysis-result h4 {
            color: #0369a1;
            margin-top: 0;
            font-weight: 700;
        }
        
        .action-item {
            background: white;
            padding: 1rem;
            margin: 0.6rem 0;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            border-left: 4px solid #3b82f6;
            color: #334155;
        }
        
        /* Sidebar styling */
        .sidebar-info {
            background: #eff6ff;
            padding: 1.2rem;
            border-radius: 10px;
            border: 1px solid #dbeafe;
            margin-bottom: 1rem;
        }
        
        .sidebar-info h4 {
            margin-top: 0;
            color: #1e40af;
        }

        /* Forms */
        .stTextInput input, .stTextArea textarea, .stSelectbox select {
            border: 1px solid #cbd5e1 !important;
            border-radius: 8px !important;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "symptom_id" not in st.session_state:
    st.session_state.symptom_id = None
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

BACKEND_URL = "http://localhost:8000"

# Header
st.markdown("""
    <div class="header-container">
        <h1>🏥 MediAssist AI</h1>
        <p>Your Personal Healthcare Assistant</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar for user information
with st.sidebar:
    st.markdown("### 👤 User Information")
    if st.session_state.user_id:
        st.markdown(f"""
            <div class="sidebar-info">
                <h4>Active User</h4>
                <p><strong>User ID:</strong> {st.session_state.user_id}</p>
                <p><strong>Status:</strong> <span class="status-badge">Logged In</span></p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🚪 Logout", key="logout"):
            st.session_state.user_id = None
            st.session_state.symptom_id = None
            st.session_state.analysis_result = None
            st.rerun()
    else:
        st.markdown(f"""
            <div class="sidebar-info">
                <h4>Status</h4>
                <p>No user logged in yet.</p>
                <p>Please create a user in the main section to get started.</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### ℹ️ About MediAssist AI")
    st.markdown("""
    MediAssist AI is a wellness assistant that provides:
    - General health information
    - Symptom tracking
    - Personal wellness advice
    
    **Important:** This is NOT a substitute for professional medical advice. Always consult a healthcare provider.
    """)

# Main content area
col1, col2 = st.columns([1, 1], gap="medium")

# Left column - User Management
with col1:
    st.markdown("""
    <div class="section-card">
        <h2>👤 User Login / Registration</h2>
    """, unsafe_allow_html=True)
    
    with st.form("user_form", clear_on_submit=True):
        
        name = st.text_input("Full Name", placeholder="Enter your full name (for new users)", key="user_name")
        email = st.text_input("Email Address", placeholder="Enter your email", key="user_email")
        
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            submit_user = st.form_submit_button("✨ Login / Register", use_container_width=True)
        with col1_2:
            if st.form_submit_button("🔄 Clear Form", use_container_width=True):
                st.rerun()
    
    if submit_user:
        if not email:
            st.error("⚠️ Please enter your email address")
        else:
            with st.spinner("Checking user..."):
                try:
                    # First, try to get user by email
                    response = requests.get(f"{BACKEND_URL}/users/", params={"email": email})
                    if response.status_code == 200:
                        users = response.json()
                        existing_user = None
                        for user in users:
                            if user.get("email") == email:
                                existing_user = user
                                break
                        
                        if existing_user:
                            # User exists - log them in
                            st.session_state.user_id = existing_user["id"]
                            st.success(f"✅ Welcome back! User ID: {existing_user['id']}")
                        else:
                            # User doesn't exist - create new one
                            if not name:
                                st.error("⚠️ Please enter your name to create a new account")
                            else:
                                create_response = requests.post(f"{BACKEND_URL}/users/",json={"full_name": name, "email": email})

                                if create_response.status_code == 200:
                                    user_data = create_response.json()
                                    st.session_state.user_id = user_data["id"]
                                    st.success(f"✅ New user created! Your User ID: {user_data['id']}")
                                else:
                                    try:
                                        error_detail = create_response.json().get("detail", create_response.text)
                                    except:
                                        error_detail = create_response.text
                                    st.error(f"❌ Failed to create user: {error_detail}")
                    else:
                        # Try to create user if get fails
                        if not name:
                            st.error("⚠️ User not found. Please enter your name to create an account")
                        else:
                            create_response = requests.post(f"{BACKEND_URL}/users/",json={"full_name": name, "email": email})
                            if create_response.status_code == 200:
                                user_data = create_response.json()
                                st.session_state.user_id = user_data["id"]
                                st.success(f"✅ New user created! Your User ID: {user_data['id']}")
                            else:
                                try:
                                    error_detail = create_response.json().get("detail", create_response.text)
                                except:
                                    error_detail = create_response.text
                                st.error(f"❌ Failed to create user: {error_detail}")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Right column - Quick Stats
with col2:
    st.markdown("""
    <div class="section-card">
        <h2>📊 Your Health Profile</h2>
    """, unsafe_allow_html=True)
    
    if st.session_state.user_id:
        try:
            # Fetch user details
            user_response = requests.get(f"{BACKEND_URL}/users/{st.session_state.user_id}")
            if user_response.status_code == 200:
                user_data = user_response.json()
                
                col_stats1, col_stats2 = st.columns(2)
                with col_stats1:
                    st.metric("User ID", st.session_state.user_id)
                with col_stats2:
                    st.metric("Status", "Active ✓")
                
                st.markdown(f"**Name:** {user_data.get('full_name', 'N/A')}")
                st.markdown(f"**Email:** {user_data.get('email', 'N/A')}")
                
                # Get user's symptoms history
                symptoms_response = requests.get(f"{BACKEND_URL}/symptoms/user/{st.session_state.user_id}")
                if symptoms_response.status_code == 200:
                    symptoms_list = symptoms_response.json()
                    st.markdown(f"**Total Submissions:** {len(symptoms_list)}")
                    
                    if symptoms_list:
                        st.markdown("**Recent Submissions:**")
                        for symptom in symptoms_list[-3:]:  # Show last 3
                            st.markdown(f"- {symptom['severity']} severity (ID: {symptom['id']})")
            else:
                st.metric("Session Status", "Inactive")
        except:
            col_stats1, col_stats2 = st.columns(2)
            with col_stats1:
                st.metric("User ID", st.session_state.user_id)
            with col_stats2:
                st.metric("Status", "Active ✓")
    else:
        st.metric("Session Status", "Inactive")
    
    st.markdown("""
    **Current Time:** """ + datetime.now().strftime("%B %d, %Y %I:%M %p"))
    st.markdown('</div>', unsafe_allow_html=True)

# Symptoms Section
st.markdown("""
<div class="section-card">
    <h2>📝 Submit Your Symptoms</h2>
""", unsafe_allow_html=True)

if st.session_state.user_id:
    with st.form("symptom_form", clear_on_submit=True):
        symptoms = st.text_area("Describe your symptoms in detail", 
                               placeholder="E.g., I have been experiencing headaches for the past 2 days...",
                               height=150)
        
        col_severity1, col_severity2 = st.columns(2)
        with col_severity1:
            severity = st.selectbox("Severity Level", ["Mild", "Moderate", "Severe"])
        with col_severity2:
            st.markdown("<p style='font-size: 0.8rem; color: #666;'>Select how severe your symptoms are</p>", unsafe_allow_html=True)
        
        col_submit1, col_submit2 = st.columns(2)
        with col_submit1:
            submit_symptoms = st.form_submit_button("🩺 Submit Symptoms", use_container_width=True)
        with col_submit2:
            if st.form_submit_button("🔄 Clear Form", use_container_width=True):
                st.rerun()
    
    if submit_symptoms:
        if not symptoms:
            st.error("⚠️ Please describe your symptoms")
        else:
            with st.spinner("Submitting symptoms..."):
                try:
                    response = requests.post(f"{BACKEND_URL}/symptoms/", 
                    json={"user_id": st.session_state.user_id, "description": symptoms, "severity": severity})
                    if response.status_code == 200:
                        symptom_data = response.json()
                        st.session_state.symptom_id = symptom_data["id"]
                        st.success(f"✅ Symptoms submitted successfully!")
                    else:
                        st.error("❌ Failed to submit symptoms")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
else:
    st.info("👤 Please create a user first to submit symptoms.")

st.markdown('</div>', unsafe_allow_html=True)

# AI Analysis Section
st.markdown("---")
st.markdown("""
<div class="section-card">
    <h2>🤖 AI Wellness Analysis</h2>
""", unsafe_allow_html=True)

if st.session_state.user_id:
    # Tab selection for new analysis or previous symptoms
    tab1, tab2 = st.tabs(["📝 New Symptom", "📋 Previous Symptoms"])
    
    with tab1:
        if st.session_state.symptom_id:
            st.markdown("Click the button below to get AI-powered wellness insights based on your symptoms.")
        else:
            st.markdown("Submit symptoms above first to analyze them.")
        col_analyze1, col_analyze2 = st.columns([2, 1])
        
        with col_analyze1:
            pass
        
        with col_analyze2:
            if st.session_state.symptom_id:
                if st.button("🔍 Analyze Symptoms", use_container_width=True, key="analyze_btn"):
                    with st.spinner("Analyzing your symptoms..."):
                        try:
                            response = requests.post(f"{BACKEND_URL}/ai/analysis/{st.session_state.symptom_id}")
                            if response.status_code == 200:
                                analysis = response.json()
                                st.session_state.analysis_result = analysis
                                st.rerun()
                            else:
                                try:
                                    error_detail = response.json().get("detail", response.text)
                                except:
                                    error_detail = response.text
                                st.error(f"❌ Failed to get analysis: {error_detail}")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
    
    with tab2:
        st.markdown("**View and analyze your previous symptom submissions:**")
        try:
            symptoms_response = requests.get(f"{BACKEND_URL}/symptoms/user/{st.session_state.user_id}")
            if symptoms_response.status_code == 200:
                symptoms_list = symptoms_response.json()
                if symptoms_list and len(symptoms_list) > 0:
                    st.success(f"Found {len(symptoms_list)} previous symptom(s)")
                    
                    for idx, symptom in enumerate(symptoms_list):
                        with st.container():
                            col_prev1, col_prev2, col_prev3 = st.columns([2, 1, 1])
                            with col_prev1:
                                severity_emoji = "🟢" if symptom.get('severity') == "Mild" else "🟡" if symptom.get('severity') == "Moderate" else "🔴"
                                symptom_text = symptom.get('description', 'No description')[:60]
                                st.markdown(f"{severity_emoji} **{symptom.get('severity', 'Unknown')}** - {symptom_text}...")
                            with col_prev2:
                                st.caption(f"ID: {symptom.get('id')}")
                            with col_prev3:
                                if st.button("📊 Analyze", key=f"prev_analyze_{symptom.get('id', idx)}", use_container_width=True):
                                    symptom_id = symptom.get('id')
                                    with st.spinner("Analyzing this symptom..."):
                                        try:
                                            analysis_response = requests.post(f"{BACKEND_URL}/ai/analysis/{symptom_id}")
                                            if analysis_response.status_code == 200:
                                                analysis = analysis_response.json()
                                                st.session_state.analysis_result = analysis
                                                st.session_state.symptom_id = symptom_id
                                                st.rerun()
                                            else:
                                                error_msg = analysis_response.json().get("detail", analysis_response.text) if analysis_response.text else "Unknown error"
                                                st.error(f"Failed to analyze: {error_msg}")
                                        except Exception as e:
                                            st.error(f"Error analyzing symptom: {str(e)}")
                            st.divider()
                else:
                    st.info("📭 No previous symptoms found. Submit a new symptom above to get started!")
            elif symptoms_response.status_code == 404:
                st.info("📭 No symptoms found for your account yet.")
            else:
                st.error(f"Failed to load symptoms: Status {symptoms_response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to backend. Please ensure the backend server is running on http://localhost:8000")
        except Exception as e:
            st.error(f"Error loading previous symptoms: {str(e)}")
    
    # Display analysis results OUTSIDE tabs so it shows for both
    if st.session_state.analysis_result:
        st.markdown("---")
        st.markdown("""
        <div class="analysis-result">
            <h4>📋 Analysis Summary</h4>
        """, unsafe_allow_html=True)

        st.markdown(st.session_state.analysis_result['summary'])

        st.markdown("<h4>⚕️ Possible Conditions</h4>", unsafe_allow_html=True)
        for condition in st.session_state.analysis_result['possible_conditions']:
            st.markdown(f"- {condition}")

        st.markdown("<h4>💊 Recommended Actions</h4>", unsafe_allow_html=True)
        for i, action in enumerate(st.session_state.analysis_result['recommended_actions'], 1):
            st.markdown(f"""
            <div class="action-item">
                <strong>{i}. {action}</strong>
            </div>
            """, unsafe_allow_html=True)

        if "disclaimer" in st.session_state.analysis_result:
            st.warning(
            f"⚕️ **Medical Disclaimer:** {st.session_state.analysis_result['disclaimer']}"
            )

        st.markdown("</div>", unsafe_allow_html=True)

        
        col_reset1, col_reset2 = st.columns(2)
        with col_reset1:
            if st.button("🔄 Clear Results", use_container_width=True):
                st.session_state.analysis_result = None
                st.rerun()
    
else:
    st.info("👤 Please login/register first to get AI analysis.")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; margin-top: 2rem;'>
    <p><strong>MediAssist AI</strong> | Your Personal Healthcare Assistant</p>
    <p style='font-size: 0.9rem;'>This application provides general wellness information only and is not a substitute for professional medical advice.</p>
</div>
""", unsafe_allow_html=True)