import logging

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from database.sqdb import SqDB
from models.address import AddressModel

address_router = APIRouter()


@address_router.post("/create")
async def create_new_address(request: Request, address: AddressModel):
    """
    creates a new address in database.
    :param request: currently not using in any operations.
    :param address: address of AddressModel pydantic class. This model ensures schema validation for incoming data.
    :return: 200 if success 500 in case of internal errors 422 in case of schema validation failed.
    """
    try:
        insert_sql = "INSERT INTO address(name, email, country, lat, lon) VALUES(?, ?, ?, ?, ?)"
        data = address.to_tuple()
        sq_db = SqDB("address_db.db")
        result = sq_db.insert_update_delete_data(insert_sql, data)
        if result:
            return JSONResponse({"status": "success"}, 200)
        else:
            return JSONResponse({"status": "failed"}, 500)
    except Exception as e:
        logging.error(f"Create new address failed: {str(e)}")
        return JSONResponse({"status": "failed"}, 500)


@address_router.get("/")
async def get_address_list(request: Request):
    """
    Returns list of all the addresses.
    :param request: currently not using.
    :return: [] if no data is available, [{data}] if data available, 500 on internal server errors
    """
    try:
        sql = "SELECT * FROM address"
        sq_db = SqDB("address_db.db")
        result = sq_db.query(sql)
        if result:
            return JSONResponse([dict(row) for row in result],
                                200)  # [dict(row) for row in result] to convert row object to dictionary
        elif result == []:
            return JSONResponse([], 200)
        else:
            JSONResponse({"status": "failed"}, 500)
    except Exception as e:
        logging.error(f"Get address list failed: {str(e)}")
        return JSONResponse({"status": "failed"}, 500)


@address_router.delete("/{id}/delete")
async def delete_address(request: Request, id: int):
    """
    deletes address by id
    :param request:
    :param id: id to delete. id can be identified using get api that returns all the addresses.
    :return: 200 if success, 500 in case of internal error
    """
    try:
        delete_sql = "DELETE FROM address where id = ?"
        data = [id]
        sq_db = SqDB("address_db.db")
        result = sq_db.insert_update_delete_data(delete_sql, data)
        if result:
            return JSONResponse({"status": "success"}, 200)
        else:
            return JSONResponse({"status": "failed"}, 500)
    except Exception as e:
        logging.error(f"Create new address failed: {str(e)}")
        return JSONResponse({"status": "failed"}, 500)


@address_router.patch("/{id}/update")
async def delete_address(request: Request, id: int, address: AddressModel):
    """
    update data with id. Currently, for simplicity API expects data in AddressModel. So all the data should be entered
    inorder to update.
    :param request:
    :param id: id to update.
    :param address: address of AddressModel object.
    :return: 200 if success, 500 if failed.
    """
    try:
        delete_sql = "UPDATE address SET name=?,email=?,country=?,lat=?,lon=? WHERE id = ?"
        data = address.to_tuple()
        data_with_id = data + (id,)
        sq_db = SqDB("address_db.db")
        result = sq_db.insert_update_delete_data(delete_sql, data_with_id)
        if result:
            return JSONResponse({"status": "success"}, 200)
        else:
            return JSONResponse({"status": "failed"}, 500)
    except Exception as e:
        logging.error(f"Create new address failed: {str(e)}")
        return JSONResponse({"status": "failed"}, 500)
