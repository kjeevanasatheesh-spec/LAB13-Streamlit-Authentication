import streamlit as st

from db import create_users_table
from auth import signup_user, login_user


st.set_page_config(
    page_title="Login and Signup",
    page_icon="🔐",
    layout="centered"
)

st.title("Lab 13: Login and Signup Application")

# Create the users table
try:
    create_users_table()
except Exception as error:
    st.error("Could not connect to PostgreSQL.")
    st.error(str(error))
    st.stop()


# Initialize session state
if "user" not in st.session_state:
    st.session_state.user = None


# If the user is logged in
if st.session_state.user is not None:

    st.success(
        f"Welcome, {st.session_state.user['name']}!"
    )

    st.write("You are successfully logged in.")

    st.write(
        "Email:",
        st.session_state.user["email"]
    )

    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()


# If the user is not logged in
else:

    page = st.radio(
        "Choose an option",
        ["Sign Up", "Login"],
        horizontal=True
    )

    # Signup page
    if page == "Sign Up":

        st.subheader("Create a New Account")

        with st.form("signup_form"):

            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
            password = st.text_input(
                "Password",
                type="password"
            )
            confirm_password = st.text_input(
                "Confirm Password",
                type="password"
            )

            submitted = st.form_submit_button("Sign Up")

            if submitted:

                name = name.strip()
                email = email.strip().lower()

                if not name or not email or not password:
                    st.error("Please fill in all required fields.")

                elif password != confirm_password:
                    st.error("Passwords do not match.")

                elif len(password) < 8:
                    st.error(
                        "Password must contain at least 8 characters."
                    )

                else:
                    try:
                        success = signup_user(
                            name,
                            email,
                            password
                        )

                        if success:
                            st.success(
                                "Account created successfully! "
                                "Select Login to sign in."
                            )
                        else:
                            st.error(
                                "This email is already registered."
                            )

                    except Exception as error:
                        st.error("Signup failed.")
                        st.error(str(error))

    # Login page
    elif page == "Login":

        st.subheader("Login to Your Account")

        with st.form("login_form"):

            email = st.text_input("Email Address")
            password = st.text_input(
                "Password",
                type="password"
            )

            submitted = st.form_submit_button("Login")

            if submitted:

                email = email.strip().lower()

                if not email or not password:
                    st.error(
                        "Please enter your email and password."
                    )

                else:
                    try:
                        user = login_user(email, password)

                        if user:
                            st.session_state.user = user
                            st.rerun()
                        else:
                            st.error(
                                "Invalid email or password."
                            )

                    except Exception as error:
                        st.error("Login failed.")
                        st.error(str(error))