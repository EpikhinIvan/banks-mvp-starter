1. Скопируйте `.env.example` → `.env` (можно оставить значения по умолчанию).
2. В корне проекта выполните:
   ```
   docker compose up --build
   ```
3. создайте суперпользователя (для админки Django):
   ```
   docker compose exec backend python app/manage.py createsuperuser
   ```
4. Откройте:
   - Фронтенд: http://localhost:3000
   - API:      http://localhost:8000/api
   - Админка:  http://localhost:8000/admin

```
docker compose down
```

