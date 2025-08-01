# 🛡️ Auth Service

Универсальный сервис аутентификации и авторизации для микросервисных приложений. Поддерживает регистрацию, логин, обновление токена, выход из системы и управление данными пользователя.

## 📦 Основной функционал

- `POST /register` — регистрация нового пользователя  
- `POST /login` — вход в систему, выдача access и refresh токенов  
- `POST /refresh` — обновление access токена по refresh токену  
- `POST /logout` — выход из системы (аннулирование refresh токена)  
- `POST /verify` — проверка токена / email / подтверждение действий  
- `POST /change_password` — смена пароля  
- `POST /change_data` — изменение пользовательских данных (имя, email и т.д.)

## 🛠️ Технологии

- Python 3.x  
- FastAPI  
- JWT (access / refresh)  
- OAuth2 / Password flow  
- PostgreSQL / Redis (опционально для blacklist refresh-токенов)
- SQLAlchemy

## 🚀 Быстрый старт

```bash
git clone https://github.com/yourusername/auth-service.git
cd auth-service
cp .env.example .env
# Отредактируйте .env при необходимости, заполнив нужные значения
docker-compose up --build


