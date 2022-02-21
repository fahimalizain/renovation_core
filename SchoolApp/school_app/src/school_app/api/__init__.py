from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
async def ping():
    return "pong"


@router.get("/schools")
async def get_schools():
    from school_app.core.model import School
    return await School.get_all(None, ["name"])


@router.get("/schools-sync")
async def get_schools_sync():
    from school_app.core.model import School
    return School.get_all_sync(None, ["name"])


@router.post("/school")
async def insert_school(school: dict):
    from school_app.core.model import School
    return School.insert(doc=school)


@router.get("/multi-thread")
async def multi():
    # from asyncer import asyncify
    from renovation.utils.async_db import asyncify

    import frappe
    import asyncio

    schools = asyncio.create_task(asyncify(frappe.get_all, db_read_only=True)("School"))
    users = asyncio.create_task(asyncify(frappe.get_all, db_read_only=True)("User"))
    todo = asyncio.create_task(asyncify(frappe.get_all, db_read_only=True)("ToDo"))
    doctypes = asyncio.create_task(asyncify(frappe.get_all, db_read_only=True)("DocType"))

    return dict(
        schools=await schools,
        users=await users,
        todo=await todo,
        doctypes=await doctypes,
    )
