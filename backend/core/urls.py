from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from administracao.apis import router as administracaoRouter
from webScraping.views import iniciar_scraping, obter_dados

api = NinjaAPI(
    title="Api da Ludmila",
    version="1.0.0",
    description="Apis para serem usadas no frontend de escolas"
)
api.add_router("/administracao/", administracaoRouter)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
    path('scrape/', iniciar_scraping, name='iniciar_scraping'), 
    # path("scrape/", iniciar_scraping, name="scrape"),
    path("obter_dados/", obter_dados, name="obter_dados"), 
]
