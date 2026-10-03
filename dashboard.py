import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Smart Exam Seating System",
    page_icon="🎓",
    layout="wide"
)

# -----------------------------
# Sample Data
# -----------------------------
total_students = 120
total_rooms = 4
total_seats = 160
total_subjects = 6

assigned_students = 0
conflicts = 0
arrangement_status = "Not Generated"

subjects = {
    "Data Structures": 20,
    "Database Management Systems": 20,
    "Operating Systems": 20,
    "Computer Networks": 20,
    "Machine Learning": 20,
    "Java Programming": 20
}

rooms = {
    "Block A - Room 101": 40,
    "Block A - Room 102": 40,
    "Block B - Room 201": 40,
    "Block B - Room 202": 40
}

# -----------------------------
# Header
# -----------------------------
st.title("🎓 Smart Exam Seating Arrangement System")
st.caption("AI-Based Exam Seating Management Dashboard")

st.divider()

# -----------------------------
# Main Statistics
# -----------------------------
st.subheader("📊 Examination Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👨‍🎓 Total Students", total_students)

with col2:
    st.metric("🏫 Total Rooms", total_rooms)

with col3:
    st.metric("💺 Total Seats", total_seats)

with col4:
    st.metric("📚 Total Subjects", total_subjects)

# -----------------------------
# Generate Seating Arrangement
# -----------------------------
st.subheader("🤖 Seating Arrangement")


st.divider()
occupied_per_room = total_students // total_rooms
# -----------------------------
# Student Data
# -----------------------------
students = []

subjects_list = [
    "Data Structures",
    "Database Management Systems",
    "Operating Systems",
    "Computer Networks",
    "Machine Learning",
    "Java Programming"
]

for i in range(1, 121):
    student = {
        "Register No": f"REG{i:03d}",
        "Name": f"Student {i}",
        "Subject": subjects_list[(i - 1) % len(subjects_list)]
    }
    students.append(student)

st.subheader("👨‍🎓 Student Information")

st.write(f"Total Students: **{len(students)}**")

st.dataframe(students, use_container_width=True)
# -----------------------------
# Room Seats
# -----------------------------
room_seats = {}

for room, capacity in rooms.items():
    seats = []

    for i in range(1, capacity + 1):
        seats.append(f"Seat-{i}")

    room_seats[room] = seats

st.subheader("🪑 Room Seats")

for room, seats in room_seats.items():
    st.write(f"**{room}** - {len(seats)} seats")
    # -----------------------------
# Constraint Checking
# -----------------------------
def is_valid_seat(allocation, student, room, seat):

    seat_number = int(seat.split("-")[1])

    for assigned in allocation:

        if assigned["Room"] == room:

            assigned_seat_number = int(
                assigned["Seat"].split("-")[1]
            )

            # Same subject cannot sit in adjacent seats
            if (
                assigned["Subject"] == student["Subject"]
                and abs(assigned_seat_number - seat_number) == 1
            ):
                return False

    return True
# -----------------------------
# Constraint Propagation
# -----------------------------
def get_valid_seats(allocation, student, room, room_seat_list):

    valid_seats = []

    for seat in room_seat_list:

        seat_used = any(
            a["Room"] == room and a["Seat"] == seat
            for a in allocation
        )

        if seat_used:
            continue

        if is_valid_seat(
            allocation,
            student,
            room,
            seat
        ):
            valid_seats.append(seat)

    return valid_seats

# -----------------------------
# Conflict Calculation
# -----------------------------
def calculate_conflicts(allocation):

    conflicts = 0

    for i in range(len(allocation)):

        for j in range(i + 1, len(allocation)):

            a = allocation[i]
            b = allocation[j]

            if a["Room"] == b["Room"]:

                seat_a = int(a["Seat"].split("-")[1])
                seat_b = int(b["Seat"].split("-")[1])

                if (
                    a["Subject"] == b["Subject"]
                    and abs(seat_a - seat_b) == 1
                ):
                    conflicts += 1

    return conflicts

# -----------------------------
# Local Search Optimization
# -----------------------------
def calculate_conflicts(allocation):

    conflicts = 0

    for i in range(len(allocation)):

        for j in range(i + 1, len(allocation)):

            a = allocation[i]
            b = allocation[j]

            if a["Room"] == b["Room"]:

                seat_a = int(a["Seat"].split("-")[1])
                seat_b = int(b["Seat"].split("-")[1])

                # Adjacent seats with same subject
                if (
                    a["Subject"] == b["Subject"]
                    and abs(seat_a - seat_b) == 1
                ):
                    conflicts += 1

    return conflicts

# -----------------------------
# Local Search Optimization
# -----------------------------
def local_search_optimize(allocation):

    current_conflicts = calculate_conflicts(allocation)

    improved = True

    while improved:

        improved = False

        for i in range(len(allocation)):

            for j in range(i + 1, len(allocation)):

                if allocation[i]["Room"] != allocation[j]["Room"]:
                    continue

                allocation[i]["Seat"], allocation[j]["Seat"] = (
                    allocation[j]["Seat"],
                    allocation[i]["Seat"]
                )

                new_conflicts = calculate_conflicts(allocation)

                if new_conflicts < current_conflicts:
                    current_conflicts = new_conflicts
                    improved = True

                else:
                    allocation[i]["Seat"], allocation[j]["Seat"] = (
                        allocation[j]["Seat"],
                        allocation[i]["Seat"]
                    )

    return allocation

# -----------------------------
# CSP Backtracking Allocation
# -----------------------------
def backtrack_allocate(index, students, allocation, seats):

    # All students allocated
    if index == len(students):
        return True

    student = students[index]

    # Distribute students equally among rooms
    room_order = sorted(
        seats.items(),
        key=lambda item: sum(
            1 for a in allocation
            if a["Room"] == item[0]
        )
    )

    # Try each room
    for room, room_seat_list in room_order:

        # Constraint Propagation
        valid_seats = get_valid_seats(
            allocation,
            student,
            room,
            room_seat_list
        )

        # Try only valid seats
        for seat in valid_seats:

            # Assign student to seat
            allocation.append({
                "Register No": student["Register No"],
                "Name": student["Name"],
                "Subject": student["Subject"],
                "Room": room,
                "Seat": seat
            })

            # Recursively allocate next student
            if backtrack_allocate(
                index + 1,
                students,
                allocation,
                seats
            ):
                return True

            # Backtrack
            allocation.pop()

    # No valid seat found
    return False

# -----------------------------
# Generate CSP Seating Arrangement
# -----------------------------
if st.button("🧠 Generate CSP Seating Arrangement", type="primary"):

    csp_allocation = []
    st.session_state["csp_allocation"] = csp_allocation

    success = backtrack_allocate(
        0,
        students,
        csp_allocation,
        room_seats
    )

    if success:
        st.success("✅ CSP seating arrangement generated successfully!")

        # Actual Dashboard Metrics
        assigned_students = len(csp_allocation)
        conflicts = calculate_conflicts(csp_allocation)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Assigned Students", assigned_students)

        with col2:
            st.metric("Conflicts", conflicts)

        with col3:
            st.metric("Status", "Generated")

        before_conflicts = calculate_conflicts(csp_allocation)

        csp_allocation = local_search_optimize(csp_allocation)

        after_conflicts = calculate_conflicts(csp_allocation)

        if after_conflicts == 0:
            st.success("✅ No seating conflicts found!")
        else:
            st.warning(
            f"⚠️ {after_conflicts} seating conflicts found."
        )

        # -----------------------------
        # Dynamic Room Occupancy
        # -----------------------------
        st.subheader("🏫 Actual Room Occupancy")

        for room, capacity in rooms.items():

            occupied = sum(
                1 for student in csp_allocation
                if student["Room"] == room
            )

            available = capacity - occupied
            percentage = occupied / capacity

            st.write(f"**{room}**")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Capacity", capacity)

            with col2:
                st.metric("Occupied", occupied)

            with col3:
                st.metric("Available", available)

            st.progress(percentage)
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Before Local Search", before_conflicts)

        with col2:
            st.metric("After Local Search", after_conflicts)

        st.subheader("🧠 AI Seating Allocation")

        st.dataframe(
            csp_allocation,
            use_container_width=True
        )
        allocation_df = pd.DataFrame(csp_allocation)

        csv_data = allocation_df.to_csv(index=False)

        st.download_button(
            label="📥 Download Seating Arrangement",
            data=csv_data,
            file_name="CSP_Seating_Arrangement.csv",
                mime="text/csv"
        )
        
        st.write(
            f"Students Allocated: **{len(csp_allocation)}**"
        )
        # -----------------------------
        # Room 101 Seating Layout
        # -----------------------------
        st.subheader("🪑 Room 101 - Seating Layout")

        room_101_students = [
            student for student in csp_allocation
            if student["Room"] == "Block A - Room 101"
        ]

        for row in range(5):
            cols = st.columns(8)

            for col in range(8):
                index = row * 8 + col

                with cols[col]:
                    if index < len(room_101_students):
                       student = room_101_students[index]

                       st.write(
                          f"**{student['Seat']}**  \n"
                          f"{student['Register No']}"
                    )
                    else:
                        st.write("Empty")
        # -----------------------------
        # Room 102 Seating Layout
        # -----------------------------
        st.subheader("🪑 Room 102 - Seating Layout")

        room_102_students = [
            student for student in csp_allocation
            if student["Room"] == "Block A - Room 102"
        ]

        for row in range(5):
            cols = st.columns(8)

            for col in range(8):
                index = row * 8 + col

                with cols[col]:
                    if index < len(room_102_students):
                        student = room_102_students[index]

                        st.write(
                            f"**{student['Seat']}**  \n"
                            f"{student['Register No']}"
                    )
                    else:
                        st.write("Empty")   
        # -----------------------------
        # Room 201 Seating Layout
        # -----------------------------
        st.subheader("🪑 Room 201 - Seating Layout")

        room_201_students = [
            student for student in csp_allocation
            if student["Room"] == "Block B - Room 201"
        ]

        for row in range(5):
            cols = st.columns(8)

            for col in range(8):
                index = row * 8 + col

                with cols[col]:
                    if index < len(room_201_students):
                        student = room_201_students[index]

                        st.write(
                            f"**{student['Seat']}**  \n"
                            f"{student['Register No']}"
                    )
                    else:
                        st.write("Empty")                             

        # -----------------------------
        # Room 202 Seating Layout
        # -----------------------------
        st.subheader("🪑 Room 202 - Seating Layout")

        room_202_students = [
            student for student in csp_allocation
            if student["Room"] == "Block B - Room 202"
        ]

        for row in range(5):
            cols = st.columns(8)

            for col in range(8):
                index = row * 8 + col

                with cols[col]:
                    if index < len(room_202_students):
                        student = room_202_students[index]

                        st.write(
                            f"**{student['Seat']}**  \n"
                            f"{student['Register No']}"
                        )
                    else:
                        st.write("Empty")            
    else:
        st.error("❌ No valid seating arrangement found.")

# -----------------------------
# Basic Seat Allocation
# -----------------------------
allocation = []

student_index = 0

for room, seats in room_seats.items():
    for seat in seats:

        if student_index < len(students):

            student = students[student_index]

            allocation.append({
                "Register No": student["Register No"],
                "Name": student["Name"],
                "Subject": student["Subject"],
                "Room": room,
                "Seat": seat
            })

            student_index += 1

st.subheader("📋 Seating Allocation")

st.dataframe(allocation, use_container_width=True)

st.write(f"Students Allocated: **{len(allocation)}**")

# -----------------------------
# Subject Distribution
# -----------------------------
st.subheader("📚 Subject-wise Student Distribution")

for subject, count in subjects.items():
    st.write(f"**{subject}** — {count} students")
    st.progress(count / total_students)

st.divider()

# -----------------------------
# Exam Information
# -----------------------------
st.subheader("📝 Exam Information")

col1, col2 = st.columns(2)

with col1:
    st.write("**Exam:** Semester Examination")
    st.write("**Date:** 26 September 2026")

with col2:
    st.write("**Session:** FN")
    st.write(f"**Students:** {total_students}")

st.divider()

st.info(
    "💡 Seating arrangement has not been generated yet. "
    "Generate the arrangement to assign students to available seats."
)
