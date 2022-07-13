from fastapi import APIRouter

dashboard = APIRouter(
    prefix="/api"
)


@dashboard.get('/dashboard')
def home_view():
    return {'Hello': "dashboard"}