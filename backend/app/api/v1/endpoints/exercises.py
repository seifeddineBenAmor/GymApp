from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.db.models import Exercise, Category
from app.core.security import get_current_admin
from app.schemas import ExerciseResponse
from app.services.storage import save_file,delete_file

router = APIRouter()

@router.get("/",response_model=list[ExerciseResponse])
async def get_exercises( db: AsyncSession = Depends(get_db), _=Depends(get_current_admin),category_id:int = None, search: str = None ):
    query = select(Exercise)
    if category_id:
        query = query.where(Exercise.category_id == category_id)
    if search :
        query = query.where(Exercise.name.ilike(f"%{search}%"))
    result = await db.execute(query)
    exercises = result.scalars().all()
    return exercises

@router.post("/",status_code=201,response_model=ExerciseResponse)
async def post_exercises(db : AsyncSession = Depends(get_db),     
                            category_id: int = Form(...),
                            name: str = Form(...),
                            description: str = Form(...),
                            video_male: UploadFile = File(...),
                            video_female: UploadFile = File(...),
                            _=Depends(get_current_admin)
                        ):
    query = select(Category).where(Category.id == category_id)
    result = await db.execute(query)
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found.")
    code =  f"{category.name[:2].upper()}_{name[:1].upper()}_{category.number_of_instances + 1}"
    category.number_of_instances += 1

    allowed_extensions =  {"mp4", "mov", "avi", "mkv", "webm"}
    folder =  "videos"
    video_path_male = save_file(video_male,folder,allowed_extensions)
    video_path_female = save_file(video_female, folder, allowed_extensions)
    exercise = Exercise(
        name =name,
        code=code,
        description=description,
        video_path=  video_path_male,
        video_path_female= video_path_female,
        category = category
    )
    db.add(exercise)
    await db.commit()   
    await db.refresh(exercise)
    return exercise

@router.patch("/{code}", response_model=ExerciseResponse)
async def patch_exercise(code:str,
                            category_id: int = Form(None),
                            name: str = Form(None),
                            description: str = Form(None),
                            video_male: UploadFile = File(None),
                            video_female: UploadFile = File(None),
                         db : AsyncSession = Depends(get_db),
                         _=Depends(get_current_admin)
                        ):
    result = await db.execute(select(Exercise).where(Exercise.code==code))
    exercise = result.scalar_one_or_none()
    if not exercise :
        raise HTTPException(status_code=404, detail="exercise not found.")
    allowed_extensions =  {"mp4", "mov", "avi", "mkv", "webm"}
    folder =  "videos"
    if name:
        exercise .name = name
    if video_male:
        video_male_path = save_file(video_male,folder,allowed_extensions)
        delete_file(exercise .video_path, folder)
        exercise .video_path = video_male_path
    if video_female:
        video_female_path = save_file(video_female, folder, allowed_extensions)
        delete_file(exercise .video_path_female, folder)
        exercise .video_path_female = video_female_path
    if description:
        exercise .description = description
    if category_id:
        exercise .category_id = category_id
    await db.commit()
    await db.refresh(exercise )
    return exercise 

@router.delete("/{code}", status_code=204)
async def delete_exercise(code:str,
                          db:AsyncSession=Depends(get_db),
                          _=Depends(get_current_admin)):
    folder =  "videos"
    result = await db.execute(select(Exercise).where(Exercise.code==code))
    exercise = result.scalar_one_or_none()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise doesn't exist")
    delete_file(exercise.video_path,folder)
    delete_file(exercise.video_path_female,folder)
    await db.delete(exercise)
    await db.commit()
    
