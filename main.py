from fastapi import FastAPI
from contextlib import asynccontextmanager

from core.config.database import engine, BaseModel
from apps.User.controllers.user_controller import user_router
from apps.Role.controllers.role_controller import role_router
from apps.Student.controllers.student_controller import router as student_router   
from apps.Parent.controllers.parent_controller import router as parent_controller
from apps.Teacher.controllers.teacher_controller import router as teacher_controller
from apps.Payment.controllers.payment_controller import router as payment_controller
from apps.Group.controllers.group_controller import router as group_controller
from apps.Enrollment.controllers.enrollment_controller import router as enrollment_controller
from apps.Course.controllers.course_controller import router as course_controller
from apps.Lesson.controllers.lesson_controller import router as lesson_controller
from apps.Homework.controllers.homework_controller import router as homework_controller
from apps.HomeworkResult.controllers.homework_result_controller import router as homework_result_controller
from apps.Attendance.controllers.attendance_controller import router as attendance_controller

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(
    title="FastAPI JWT Authentication",
    description="Мини приложение с JWT аутентификацией, ролями и студентами",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(user_router)
app.include_router(role_router)
app.include_router(student_router)  
app.include_router(parent_controller)
app.include_router(teacher_controller)
app.include_router(payment_controller)
app.include_router(group_controller)
app.include_router(enrollment_controller)
app.include_router(course_controller)
app.include_router(lesson_controller)
app.include_router(homework_controller)
app.include_router(homework_result_controller)
app.include_router(attendance_controller)




@app.get("/")
async def root():
    return {
        "message": "Welcome to FastAPI JWT Authentication API",
        "docs": "/docs",
        "endpoints": {
            "register": "POST /auth/register",
            "login": "POST /auth/login",
            "me": "GET /auth/me",
            "roles": "GET /roles/",
            "students": "GET /students/"   
        }
    }