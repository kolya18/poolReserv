import psycopg2
from fastapi import FastAPI, HTTPException

app = FastAPI()

DATABASE_URL = "postgresql://mos_hack:hackme12345@db:5432/mos_hack"

def get_connection():
    return psycopg2.connect(DATABASE_URL)

@app.on_event("startup")
def startup():
    # Здесь можно выполнить любые начальные действия, например, проверку подключения к БД
    pass


##Создает новый бассейн.
@app.post("/pools/")
def create_pool(name: str, address: str, capacity: int, schedule_id: int, is_open: bool):
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cursor:
                query = """
                INSERT INTO "Pools" (name, address, capacity, schedule_id, is_open)
                VALUES (%s, %s, %s, %s, %s) RETURNING id;
                """
                cursor.execute(query, (name, address, capacity, schedule_id, is_open))
                pool_id = cursor.fetchone()[0]
                return {"id": pool_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

##Получает список всех бассейнов.
@app.get("/pools/")
def read_pools():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            query = 'SELECT * FROM "Pools";'
            cursor.execute(query)
            pools = cursor.fetchall()
            return [{"id": pool[0], "name": pool[1], "address": pool[2], "capacity": pool[3], "schedule_id": pool[4], "is_open": pool[5]} for pool in pools]
    finally:
        conn.close()

##Обновляет данные о бассейне по его ID. Если бассейн не найден, возвращает ошибку 404.
@app.put("/pools/{pool_id}")
def update_pool(pool_id: int, name: str = None, address: str = None,
                capacity: int = None, schedule_id: int = None,
                is_open: bool = None):
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cursor:
                query = """
                UPDATE "Pools"
                SET name = COALESCE(%s, name),
                    address = COALESCE(%s, address),
                    capacity = COALESCE(%s, capacity),
                    schedule_id = COALESCE(%s, schedule_id),
                    is_open = COALESCE(%s, is_open)
                WHERE id = %s;
                """
                cursor.execute(query, (name, address, capacity, schedule_id, is_open, pool_id))
                if cursor.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Pool not found")
                return {"message": "Pool updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()
##Удаляет бассейн по его ID. Если бассейн не найден, возвращает ошибку 404.
@app.delete("/pools/{pool_id}")
def delete_pool(pool_id: int):
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cursor:
                query = 'DELETE FROM "Pools" WHERE id = %s;'
                cursor.execute(query, (pool_id,))
                if cursor.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Pool not found")
                return {"message": "Pool deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

