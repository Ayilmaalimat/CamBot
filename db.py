from config import DB, connect


def return_statistics():
    query = """
        SELECT SWIPE_ID, ATTENDANCE_DATE, SWIPE_NAME, DEPT_NAME, SIGNIN_TIME, SIGNOUT_TIME 
        FROM dss.adm_attendance_record_info_202101 
        join dss.adm_card_department 
        on dss.adm_attendance_record_info_202101.DEPT_CODE = dss.adm_card_department.DEPT_CODE 
        WHERE ATTENDANCE_DATE = CURRENT_DATE()
    """
    DB.execute(query)
    result = DB.fetchall()

    for i, data in enumerate(result):
        result[i][3] = data[3].decode()
        result[i][4] = data[4].decode()
        result[i][5] = data[5].decode()

    return result


def crete_user(userID, username):
    query = """INSERT INTO usersBot (userID,username) VALUES (%s, %s);"""
    val = (userID, username)

    try:
        DB.execute(query, val)
        connect.commit()
        return f'Ваш айди успешно идентифицирован!'
    except Exception as e:
        return f'--> Ошибка в обработке запроса: ```{e}```'


def check_user(userID):
    query = """SELECT * FROM usersBot WHERE userID = (%s)"""

    DB.execute(query, (userID,))
    return DB.fetchall()


def all_users():
    query = """SELECT * FROM usersBot"""

    DB.execute(query)
    return DB.fetchall()

