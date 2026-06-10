import streamlit as st
from datetime import date
import database

def is_valid_aadhaar(value: str) -> bool:
    return value.isdigit() and len(value) == 12

def is_valid_pin(value: str) -> bool:
    return value.isdigit() and len(value) == 6

def load_student_selection():
    students = database.get_all_students()
    options = [f"{student['id']}: {student['name']} ({student['student_id']})" for student in students]
    return students, options

def parse_selection(selection: str) -> int:
    return int(selection.split(":")[0]) if selection else None

def show_registration_form():
    st.subheader("Register New Student")
    with st.form("register_form"):
        name = st.text_input("Name", max_chars=26)
        student_id = st.text_input("Student ID", max_chars=20)
        relation_name = st.text_input("Relation Name", max_chars=26)
        date_of_birth = st.date_input("Date of Birth", value=date(2005, 1, 1))
        aadhaar_number = st.text_input("Aadhaar Number", max_chars=12)
        city = st.text_input("City", max_chars=100)
        pin_code = st.text_input("PIN Code", max_chars=6)
        is_active = st.checkbox("Active Status", value=True)
        submitted = st.form_submit_button("Add Student")

        if submitted:
            if not name:
                st.error("Name is required.")
                return
            if not student_id:
                st.error("Student ID is required.")
                return
            if not aadhaar_number or not is_valid_aadhaar(aadhaar_number):
                st.error("Aadhaar Number must be 12 digits.")
                return
            if not pin_code or not is_valid_pin(pin_code):
                st.error("PIN Code must be 6 digits.")
                return

            try:
                database.add_student(
                    name=name.strip(),
                    student_id=student_id.strip(),
                    relation_name=relation_name.strip() or None,
                    date_of_birth=date_of_birth,
                    aadhaar_number=aadhaar_number.strip(),
                    city=city.strip() or None,
                    pin_code=pin_code.strip(),
                    is_active=is_active,
                )
                st.success("Student profile added successfully.")
            except Exception as exc:
                st.error(f"Error adding student: {exc}")


def show_all_records():
    st.subheader("All Student Records")
    students = database.get_all_students()
    if not students:
        st.info("No records found. Add a student first.")
        return
    st.dataframe(students)


def show_search_panel():
    st.subheader("Search Students")
    search_by = st.radio("Search by", ["Name", "Student ID"], horizontal=True)
    query = st.text_input("Search term")
    if st.button("Search"):
        if not query.strip():
            st.error("Enter a search term.")
            return
        results = database.search_students(query, search_by=search_by.lower())
        if results:
            st.success(f"Found {len(results)} record(s).")
            st.dataframe(results)
        else:
            st.warning("No matching students found.")


def show_update_delete_panel():
    st.subheader("Update or Delete Student")
    students, options = load_student_selection()
    if not options:
        st.info("No students available for update/delete.")
        return

    selected_option = st.selectbox("Select student record", options)
    student_pk = parse_selection(selected_option)
    student = database.get_student_by_id(student_pk)

    if not student:
        st.error("Selected student could not be loaded.")
        return

    with st.form("edit_form"):
        name = st.text_input("Name", value=student["name"], max_chars=26)
        student_id = st.text_input("Student ID", value=student["student_id"], max_chars=20)
        relation_name = st.text_input("Relation Name", value=student.get("relation_name") or "", max_chars=26)
        date_of_birth = st.date_input("Date of Birth", value=student["date_of_birth"] or date(2005, 1, 1))
        aadhaar_number = st.text_input("Aadhaar Number", value=student.get("aadhaar_number") or "", max_chars=12)
        city = st.text_input("City", value=student.get("city") or "", max_chars=100)
        pin_code = st.text_input("PIN Code", value=student.get("pin_code") or "", max_chars=6)
        is_active = st.checkbox("Active Status", value=student.get("is_active", True))
        updated = st.form_submit_button("Update Student")

        if updated:
            if not name:
                st.error("Name is required.")
                return
            if not student_id:
                st.error("Student ID is required.")
                return
            if not aadhaar_number or not is_valid_aadhaar(aadhaar_number):
                st.error("Aadhaar Number must be 12 digits.")
                return
            if not pin_code or not is_valid_pin(pin_code):
                st.error("PIN Code must be 6 digits.")
                return

            try:
                database.update_student(
                    student_pk=student_pk,
                    name=name.strip(),
                    student_id=student_id.strip(),
                    relation_name=relation_name.strip() or None,
                    date_of_birth=date_of_birth,
                    aadhaar_number=aadhaar_number.strip(),
                    city=city.strip() or None,
                    pin_code=pin_code.strip(),
                    is_active=is_active,
                )
                st.success("Student information updated successfully.")
            except Exception as exc:
                st.error(f"Error updating student: {exc}")

    if st.button("Delete Student"):
        try:
            database.delete_student(student_pk)
            st.success("Student record deleted successfully.")
        except Exception as exc:
            st.error(f"Error deleting student: {exc}")


def main():
    st.set_page_config(page_title="Student Profile Management", layout="wide")
    st.title("Student Profile Management System")

    try:
        database.create_database_if_not_exists()
        database.create_table()
        database.insert_sample_data()
    except Exception as exc:
        st.error(f"Database initialization failed: {exc}")
        return

    section = st.sidebar.radio(
        "Navigation",
        ["Register Student", "View Records", "Search Students", "Update/Delete Student"],
    )

    if section == "Register Student":
        show_registration_form()
    elif section == "View Records":
        show_all_records()
    elif section == "Search Students":
        show_search_panel()
    elif section == "Update/Delete Student":
        show_update_delete_panel()


if __name__ == "__main__":
    main()
