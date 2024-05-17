import streamlit as st
import json

def update_json(data):
    with open("auth.json", "w") as f:
        json.dump(data, f, indent=2)

def add_user(data, new_user, new_password, new_userid, new_state):
    data[new_user] = {
        "password": new_password,
        "userid": new_userid,
        "selection_docs_state": new_state
    }
    update_json(data)
    st.success(f"User '{new_user}' added successfully!")

def update_user(data, user, new_password, new_userid, new_state):
    if user in data:
        data[user]["password"] = new_password
        data[user]["userid"] = new_userid
        data[user]["selection_docs_state"] = new_state
        update_json(data)
        st.success(f"User '{user}' updated successfully!")
    else:
        st.warning("No user found with the selected ID.")

def delete_user(data, user):
    if user in data:
        del data[user]
        update_json(data)
        st.success(f"User '{user}' deleted successfully!")
    else:
        st.warning("No user found with the selected ID.")

def main():
    st.set_page_config(page_title="Admin Dashboard", layout="wide")
    st.title("Admin Dashboard")

    try:
        with open("auth.json", "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    except FileNotFoundError:
        data = {}

    action = st.sidebar.radio("Admin Options", ["Add User", "Update User", "Delete User"])

    if action == "Add User":
        st.subheader("Add User")
        new_user = st.text_input("User ID")
        new_password = st.text_input("Password", type="password")
        modes = st.text_input("Langchain Modes (comma-separated)")
        path = st.text_input("Path")
        user_type = st.selectbox("Type", ["shared", "personal"])

        new_state = {
            "langchain_modes": modes.split(","),
            "langchain_mode_paths": {mode: path for mode in modes.split(",")},
            "langchain_mode_types": {mode: user_type for mode in modes.split(",")}
        }

        if st.button("Add"):
            add_user(data, new_user, new_password, new_user, new_state)

    elif action == "Update User":
        st.subheader("Update User")
        selected_user = st.selectbox("Select User", [""] + list(data.keys()))
        if selected_user:
            user_data = data[selected_user]
            new_password = st.text_input("Enter new password", type="password", value=user_data["password"])
            new_userid = st.text_input("Enter new user ID", value=user_data["userid"])

            new_state = user_data["selection_docs_state"]

            modes = st.multiselect("Select langchain modes", ["UserData", "MyData", "LLM", "Disabled", "trial", "dummy", "research_articles", "db_dir_Infosys", "db_dir_Lodha", "db_dir_New_Laws", "db_dir_emp", "db_dir_Research_Articles"], default=new_state["langchain_modes"])
            new_state["langchain_modes"] = modes

            for mode in modes:
                path = st.text_input(f"Enter path for '{mode}' mode", value=new_state["langchain_mode_paths"].get(mode, ""))
                new_state["langchain_mode_paths"][mode] = path

                mode_type = st.selectbox(f"Select type for '{mode}' mode", ["shared", "personal"], index=["shared", "personal"].index(new_state["langchain_mode_types"].get(mode, "shared")))
                new_state["langchain_mode_types"][mode] = mode_type

            if st.button("Update User"):
                update_user(data, selected_user, new_password, new_userid, new_state)
        else:
            st.warning("Please select a user.")

    elif action == "Delete User":
        st.subheader("Delete User")
        selected_user = st.selectbox("Select User", [""] + list(data.keys()))
        if selected_user:
            if st.button("Delete User"):
                delete_user(data, selected_user)
        else:
            st.warning("Please select a user.")
            
    st.sidebar.title("Current Users")
    if len(data) == 0:
        st.sidebar.write("No users found.")
    else:
        for i, user in enumerate(data.keys()):
            st.sidebar.write(f"{i+1}. {user}")

if __name__ == "__main__":
    main()
