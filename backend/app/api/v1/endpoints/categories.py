from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.db.models import Category
from app.core.security import get_current_admin
from app.schemas import CategoryResponse
from app.services.storage import save_file,delete_file

router = APIRouter()

@router.get("/",response_model=list[CategoryResponse])
async def get_categories( db: AsyncSession = Depends(get_db), _=Depends(get_current_admin)):
    result = await db.execute(select(Category))
    categories = result.scalars().all()
    return categories

@router.post("/",status_code=201,response_model=CategoryResponse)
async def post_categories(db : AsyncSession = Depends(get_db),     
                            name: str = Form(...),
                            icon: UploadFile = File(...),
                            icon_female: UploadFile = File(...),
                            _=Depends(get_current_admin)
                        ):
    allowed_extensions =  {"png", "jpg", "jpeg", "gif"}
    folder =  "thumbnails"
    icon_path = save_file(icon,folder,allowed_extensions)
    icone_path_female = save_file(icon_female, folder, allowed_extensions)
    category = Category(
        name =name,
        number_of_instances=0,
        icone_path=  icon_path,
        icone_path_female= icone_path_female
    )
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category

@router.patch("/{id}", response_model=CategoryResponse)
async def patch_category(id:int,
                         name: str = Form(None),
                         icon: UploadFile = File(None),
                         icon_female: UploadFile = File(None),
                         db : AsyncSession = Depends(get_db),
                         _=Depends(get_current_admin)
                        ):
    result = await db.execute(select(Category).where(Category.id==id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found.")
    allowed_extensions =  {"png", "jpg", "jpeg", "gif"}
    folder =  "thumbnails"
    if name:
        category.name = name
    if icon:
        icon_path = save_file(icon,folder,allowed_extensions)
        delete_file(category.icone_path, folder)
        category.icone_path = icon_path
    if icon_female:
        icone_path_female = save_file(icon_female, folder, allowed_extensions)
        delete_file(category.icone_path_female, folder)
        category.icone_path_female = icone_path_female
    await db.commit()
    await db.refresh(category)
    return category

@router.delete("/{id}", status_code=204)
async def delete_category(id:int,
                          db:AsyncSession=Depends(get_db),
                          _=Depends(get_current_admin)):
    folder =  "thumbnails"
    result = await db.execute(select(Category).where(Category.id==id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category doesn't exist")
    delete_file(category.icone_path,folder)
    delete_file(category.icone_path_female,folder)
    await db.delete(category)
    await db.commit()
    
