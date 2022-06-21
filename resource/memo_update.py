from http import HTTPStatus
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql.connector.errors import Error
from mysql_connection import get_connection
import mysql.connector

class MemoUpdateResource(Resource) :
    # 데이터를 업데이트하는 API들은 PUT 함수를 사용한다.
    @jwt_required()
    def put(self, memo_id) :

        # body에서 전달된 데이터를 처리
        data = request.get_json()

        user_id = get_jwt_identity()

        # DB 업데이트 실행 코드        
        try :
            # 데이터 insert
            #1. DB에 연결
            connection = get_connection()

            # 먼저 memo_id에 들어있는 user_id가
            # 이사람인지 먼저 확인한다.

            query = '''select user_id
                        from memo
                        where id = %s'''

            record = (memo_id, )

            cursor = connection.cursor(dictionary = True)

            cursor.execute(query, record)

            result_list = cursor.fetchall()

            memo = result_list[0]

            if memo['user_id'] != user_id :
                cursor.close()
                connection.close()

                return {'error' : '남의 레시피를 수정할 수 없습니다.'}, 401

            #2. 쿼리문 만들기
            query = '''update memo
                    set title = %s, todo_date = %s, content = %s
                    where id = %s ;'''

            record = ( data['title'], data['todo_date'], data['content'], memo_id )

            #3. 커서를 가져온다.
            cursor = connection.cursor()
            #4. 쿼리문을 커서를 이용해서 실행한다.
            cursor.execute(query, record)
            #5. 커넥션을 커밋해줘야 한다. => 디비에 영구적으로 반영하라는 뜻
            connection.commit()
            #6. 자원 해제
            cursor.close()
            connection.close()

        # 정상적이지 않을때
        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {'error' : str(e)}, 503


        return {'result' : 'success'}, 200




    # 삭제하는 delete 함수
    @jwt_required()
    def delete(self, memo_id) :

        user_id = get_jwt_identity()
        try :
            # 데이터 삭제
            #1. DB에 연결
            connection = get_connection()

            # 먼저 memo_id에 들어있는 user_id가
            # 이사람인지 먼저 확인한다.

            query = '''select user_id
                        from memo
                        where id = %s'''

            record = (memo_id, )

            cursor = connection.cursor(dictionary = True)

            cursor.execute(query, record)

            result_list = cursor.fetchall()

            memo = result_list[0]

            if memo['user_id'] != user_id :
                cursor.close()
                connection.close()

                return {'error' : '남의 레시피를 삭제할 수 없습니다.'}, 401

            #2. 쿼리문 만들기
            query = '''delete from memo
                    where id = %s ;'''

            record = (memo_id, )

            #3. 커서를 가져온다.
            cursor = connection.cursor()
            #4. 쿼리문을 커서를 이용해서 실행한다.
            cursor.execute(query, record)
            #5. 커넥션을 커밋해줘야 한다. => 디비에 영구적으로 반영하라는 뜻
            connection.commit()
            #6. 자원 해제
            cursor.close()
            connection.close()

        # 정상적이지 않을때
        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {'error' : str(e)}, 503
        
        return {'result' : 'success'}, 200