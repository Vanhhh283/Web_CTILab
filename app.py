import streamlit as st
import pandas as pd
from models import session, Student, StudentSchedule
from datetime import datetime
import calendar


st.set_page_config(layout="wide")
st.title("Trang web quản lý sinh viên CTILab4EVs")

menu = st.sidebar.radio("Chọn chức năng", ["Thêm sinh viên", "Xem danh sách", "Cập nhật", "Lên lịch"])

# ----- THÊM SINH VIÊN -----
if menu == "Thêm sinh viên":
    name = st.text_input("Họ tên")
    mssv = st.text_input("MSSV")
    email = st.text_input("Email sinh viên (sis.hust.edu.vn)")
    phone = st.text_input("Số điện thoại")
    
    supervisor_options = [" -- Giảng viên hướng dẫn ", "GS. TSKH. Trần Hoài Linh", "PGS. Võ Duy Thành", "TS. Nguyễn Bảo Huy"]
    supervisor = st.selectbox("Giảng viên hướng dẫn", supervisor_options)
    
    program_options = [" -- Chương trình đào tạo", "EE2", "EE-E8", "EE-EP", "EETN", "MSc", "PHD"]
    program = st.selectbox("Chương trình đào tạo", program_options)
    
    k = st.text_input("Khóa")
    research_topic = st.text_input("Đề tài nghiên cứu")

    if st.button("Thêm thông tin sinh viên"):
        if all([name, mssv, email, phone, k, research_topic]) \
            and supervisor != supervisor_options[0] \
            and program != program_options[0]:
            
            student = Student(
                name=name, student_id=mssv, email=email, phone=phone,
                supervisor=supervisor, program=program, k=k, research_topic=research_topic
            )
            session.add(student)
            session.commit()
            st.success("Đã thêm thành công!")
        else:
            st.warning("Vui lòng điền đầy đủ thông tin")

# ----- XEM DANH SÁCH SINH VIÊN -----
elif menu == "Xem danh sách":
    students = session.query(Student).all()
    data = [{
        "Họ và tên": s.name,
        "Mã sinh viên": s.student_id,
        "Email": s.email,
        "Số điện thoại": s.phone,
        "Giảng viên hướng dẫn": s.supervisor,
        "Chương trình đào tạo": s.program,
        "Khóa": s.k,
        "Đề tài nghiên cứu": s.research_topic
    } for s in students]

    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

# ----- LÊN LỊCH CHO SINH VIÊN -----
elif menu == "Lên lịch":
    all_schedules = session.query(StudentSchedule).all()
    # Tạo DataFrame 
    schedule_data = []
    for s in all_schedules:
        schedule_data.append({
            "student": s.student.name,
            "date": s.start_time.date(),
            "job": s.title
        })

    df = pd.DataFrame(schedule_data)
    df['date'] = pd.to_datetime(df['date'])

    # Hiển thị lịch
    st.subheader("Lịch làm việc của sinh viên")
    today = datetime.now()
    year = st.selectbox("Năm", list(range(today.year - 1, today.year + 2)), index=1)
    month = st.selectbox("Tháng", list(range(1, 13)), index=today.month - 1)

    # Tạo lịch 
    cal = calendar.Calendar(firstweekday=0)
    month_days = list(cal.itermonthdates(year, month))

    cols = st.columns(7)
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i in range(7):
        cols[i].markdown(f"**{weekdays[i]}**")

    week = []
    for day in month_days:
        if day.month != month:
            week.append("")
        else:
            sv_list = df[df['date'].dt.date == day]['student'].tolist()
            job_list = df[df['date'].dt.date == day]['job'].tolist()
            content = f"**{day.day}**"
            for s, j in zip(sv_list, job_list):
                content += f"\n- {s}: {j}"
            week.append(content)

        if len(week) == 7:
            cols = st.columns(7)
            for i in range(7):
                with cols[i]:
                    st.markdown(week[i] if week[i] else " ")
            week = []

# ----- CẬP NHẬP THÔNG TIN SINH VIÊN -----
# elif menu == "Cập nhật":
#     students = session.query(Student).all()
#     selected = st.selectbox("Chọn sinh viên", students, format_func=lambda s: f"{s.name} ({s.student_id})")

#     new_name = st.text_input("Tên", selected.name)
#     new_mssv = st.text_input("MSSV", selected.student_id)
#     new_email = st.text_input("Email", selected.email)
#     new_phone = st.text_input("Số điện thoại", selected.phone)
#     new_supervisor = st.selectbox("Giảng viên hướng dẫn", ["GS. TSKH. Trần Hoài Linh", "PGS. Võ Duy Thành", "TS. Nguyễn Bảo Huy"], index=["GS. TSKH. Trần Hoài Linh", "PGS. Võ Duy Thành", "TS. Nguyễn Bảo Huy"].index(selected.supervisor))
#     new_program = st.selectbox("Chương trình đào tạo", ["EE2", "EE-E8", "EE-EP", "EETN", "MSc", "PHD"], index=["EE2", "EE-E8", "EE-EP", "EETN", "MSc", "PHD"].index(selected.program))
#     new_k = st.text_input("Khóa", selected.k)
#     new_research_topic = st.text_input("Đề tài nghiên cứu", selected.research_topic)

#     if st.button("Cập nhật"):
#         selected.name = new_name
#         selected.student_id = new_mssv
#         selected.email = new_email
#         selected.phone = new_phone
#         selected.supervisor = new_supervisor
#         selected.program = new_program
#         selected.k = new_k
#         selected.research_topic = new_research_topic
#         session.commit()
#         st.success("Đã cập nhật!")
