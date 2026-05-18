from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.db.models import Exercise, Category, Program, ProgramDetail
from app.core.security import get_current_admin
from app.schemas import ProgramDetailResponse, ProgramResponse

router = APIRouter()

@router.get("/",response_model=list[ProgramResponse])
async def get_programs( db: AsyncSession = Depends(get_db), _=Depends(get_current_admin),program_id:int = None, name: str = None, creator: str = None ):
    query = select(Program)
    if name:
        query = query.where(Program.name.ilike(f"%{name}%"))
    if creator :
        query = query.where(Program.creator.ilike(f"%{creator}%"))
    result = await db.execute(query)
    programs = result.scalars().all()
    return programs

@router.post("/",status_code=201,response_model=ProgramResponse)
async def post_programs(db : AsyncSession = Depends(get_db),  
                         name: str = Form(...),
                         creator: str = Form(...),
                         _=Depends(get_current_admin)
                        ):
    program = Program(
        name =name,
        creator=creator,
    )

    db.add(program)
    await db.commit()   
    await db.refresh(program)
    return program
