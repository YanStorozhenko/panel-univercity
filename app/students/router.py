from fastapi import APIRouter, Depends
from sqlalchemy import select
from app.database import async_session_maker
from app.students.models import Student
from app.students.dao_base import StudentDAO
from app.students.scheme import SchemStudent
from app.students.rb import RBStudent

router = APIRouter(prefix="/students", tags=['Работа со студентами'])



@router.get("/", summary="Получить всех студентов")
async def get_all_students(request_body: RBStudent = Depends()) -> list[SchemStudent]:
    return await StudentDAO.find_all(**request_body.to_dict())

@router.get("/{id}", summary="Получить одного студента по id")
async def get_student_by_id(student_id: int) -> SchemStudent | dict:
    rez = await StudentDAO.find_full_data(student_id)
    if rez is None:
        return {'message': f'Студент с ID {student_id} не найден!'}
    return rez

@router.get("/by_filter", summary="Получить одного студента по фильтру")
async def get_student_by_filter(request_body: RBStudent = Depends()) -> SchemStudent | dict:
    rez = await StudentDAO.find_one_or_none(**request_body.to_dict())
    if rez is None:
        return {'message': f'Студент с указанными вами параметрами не найден!'}
    return rez
