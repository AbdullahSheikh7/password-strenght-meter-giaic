import streamlit as st
import re, random, string

if "password" not in st.session_state or "password_status" not in st.session_state or "score" not in st.session_state:
    st.session_state.password = ""
    st.session_state.password_status = ""
    st.session_state.score = 0

suggestions_list = []
password_status = ""

def generate_strong_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.sample(characters, 8))
    return password

def password_score(password):
    global suggestions_list
    global password_status

    st.session_state.score = 0

    if len(password) >= 8:
        st.session_state.score += 1
    else:
        suggestions_list.append("❌ Password should be at least 8 characters long.")

    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        st.session_state.score += 1
    else:
        suggestions_list.append("❌ Include both uppercase and lowercase letters.")

    if re.search(r"\d", password):
        st.session_state.score += 1
    else:
        suggestions_list.append("❌ Add at least one number (0-9).")

    if re.search(r"[!@#$%^&*]", password):
        st.session_state.score += 1
    else:
        suggestions_list.append("❌ Include at least one special character (!@#$%^&*).")

    if st.session_state.score >= 4:
        password_status = "✅ Strong Password!"
    elif st.session_state.score == 3:
        password_status = "⚠️ Moderate Password - Consider adding more security features."
    else:
        password_status = "❌ Weak Password - Improve it using the suggestions above."

if "suggested_password" not in st.session_state:
    st.session_state.suggested_password = generate_strong_password()

def use_suggested():
    st.session_state.password = st.session_state.suggested_password

def regenerate_suggested():
    st.session_state.suggested_password = generate_strong_password()

# Title with GitHub link
st.markdown("# [Abdullah Salahuddin](https://github.com/AbdullahSheikh7/)")
st.markdown("## Password Strength Checker")

# Password Input
col1, col2 = st.columns(2, gap="large")

with col2:
    st.markdown(f"**Suggested Password:** `{st.session_state.suggested_password}`", unsafe_allow_html=True)

    col2_col1, col2_col2 = st.columns(2)

    with col2_col1:
        st.button("Use suggested", on_click=use_suggested)

    with col2_col2:
        st.button("Regenerate", on_click=regenerate_suggested)

suggestion_container = st.container()

def update_scores():
    password_score(st.session_state.password)

    suggestion_container.markdown(f"**Password Strength:** {password_status}", unsafe_allow_html=True)

    for suggestion in suggestions_list:
        suggestion_container.markdown(suggestion)

with col1:
    st.session_state.password = st.text_input("Enter your password", type="password", value=st.session_state.password, on_change=update_scores)

    st.button("Check Password Strength", on_click=update_scores)
