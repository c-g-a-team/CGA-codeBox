import traceback

import pymysql


class MyDBHelper:
    # 添加交警信息
    def add(self, args):
        # 1.建立连接
        conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            db="police",
            user="root",
            password="123456!Wt",
            charset="utf8"
        )
        # 2.创建游标
        cs = conn.cursor()
        # 3.执行sql语句
        print(args)
        try:
            cs.execute("insert into policeregister values(null,%s,%s)", args)
            # 4.提交
            conn.commit()
            # print(conn)
        except:
            traceback.print_exc()
            conn.rollback()
            return '注册失败'

    # 添加车辆识别信息
    def add1(self, args):
        # 1.建立连接
        conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            db="police",
            user="root",
            password="redhat",
            charset="utf8"
        )
        # 2.创建游标
        cs = conn.cursor()
        # 3.执行sql语句
        row = cs.execute("insert into carcheckinfo values(null,%s,%s,%s,'学院路',%s,0,0,0)", args)
        # print("影响的行数",row)
        # 4.提交
        conn.commit()
        # print(conn)
        return row

    # 交警登录查询
    def login(self, args):
        # 1.建立连接
        conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            db="police",
            user="root",
            password="redhat",
            charset="utf8"
        )
        # 2.创建游标
        cs = conn.cursor()
        sql = "select * from policeregister where policeName=%s and policePassword=%s"
        try:
            # 执行sql语句
            cs.execute(sql, args)
            result = cs.fetchone()
            print(result)
            print(len(result))
            if len(result) == 3:
                return '登录成功'
            else:
                return '用户名或密码不正确'
            # 提交到数据库执行
            conn.commit()
        except:
            # 如果发生错误则回滚
            traceback.print_exc()
            conn.rollback()
        # 关闭数据库连接
        conn.close()

    # 车主登录查询
    def login01(self, args):
        # 1.建立连接
        conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            db="car_user",
            user="root",
            password="redhat",
            charset="utf8"
        )
        # 2.创建游标
        cs = conn.cursor()
        sql = "select * from caruserregister where carNum=%s and engineNum=%s"
        try:
            # 执行sql语句
            cs.execute(sql, args)
            result = cs.fetchone()
            print(len(result))
            if len(result) == 3:
                return '登录成功'
            else:
                return '登陆失败'
            # 提交到数据库执行
            conn.commit()
        except:
            # 如果发生错误则回滚
            traceback.print_exc()
            conn.rollback()
        # 关闭数据库连接
        conn.close()

    # 多条查询
    def showAllUser(self, place):
        try:
            conn = pymysql.connect(
                host="127.0.0.1",
                port=3306,
                db="police",
                user="root",
                password="redhat",
                charset="utf8"
            )
            cs = conn.cursor()
            cs.execute("select * from carcheckinfo where carPlace=%s", [place])
            result = cs.fetchall()
            print(result)
            return result
        except Exception as e:
            print(e)
        finally:
            if conn != None:
                conn.close()

    # 车主违章记录查询
    def searchUser(self, carnumber):
        try:
            conn = pymysql.connect(
                host="127.0.0.1",
                port=3306,
                db="police",
                user="root",
                password="redhat",
                charset="utf8"
            )
            cs = conn.cursor()
            cs.execute("select * from carcheckinfo where carNumber=%s", [carnumber])
            result = cs.fetchone()
            print(result, "已执行此行")
            return result
        except Exception as e:
            print(e)
        finally:
            if conn != None:
                conn.close()

    # 待审核查询
    def searchPending(self):
        try:
            conn = pymysql.connect(
                host="127.0.0.1",
                port=3306,
                db="police",
                user="root",
                password="redhat",
                charset="utf8"
            )
            cs = conn.cursor()
            cs.execute("select * from carcheckinfo where applyIf=1 and checkIf=0")
            result = cs.fetchone()
            print(result, "已执行此行")
            return result
        except Exception as e:
            print(e)
        finally:
            if conn != None:
                conn.close()

    # 已审核查询
    def searchSolved(self):
        try:
            conn = pymysql.connect(
                host="127.0.0.1",
                port=3306,
                db="police",
                user="root",
                password="redhat",
                charset="utf8"
            )
            cs = conn.cursor()
            cs.execute("select * from carcheckinfo where applyIf=1 and checkIf=1")
            result = cs.fetchone()
            print(result, "已执行此行")
            return result
        except Exception as e:
            print(e)
        finally:
            if conn != None:
                conn.close()

    # 多条查询
    def searchMoreUser(self):
        try:
            conn = pymysql.connect(
                host="127.0.0.1",
                port=3306,
                db="police",
                user="root",
                password="redhat",
                charset="utf8"
            )
            cs = conn.cursor()
            cs.execute("select * from carcheckinfo where applyIf=1 and checkIf=0 ")
            result = cs.fetchall()
            print(result)
            return result
        except Exception as e:
            print(e)
        finally:
            if conn != None:
                conn.close()

    # 修改carnumber数据
    def updatecarnumber(self, carnumber):
        # 1.建立连接
        conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            db="police",
            user="root",
            password="redhat",
            charset="utf8"
        )
        # 2.创建游标
        cs = conn.cursor()
        # 3.执行sql语句
        row = cs.execute("update carcheckinfo set applyIf=1 where carNumber=%s", [carnumber])
        # print("影响的行数",row)
        # 4.提交
        conn.commit()
        # print(conn)
        return row

    # 修改checkIf数据
    def updatecheckIf(self):
        # 1.建立连接
        conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            db="police",
            user="root",
            password="redhat",
            charset="utf8"
        )
        # 2.创建游标
        cs = conn.cursor()
        # 3.执行sql语句
        row = cs.execute("update carcheckinfo set checkIf=1 where carNumber='京FL0278'")
        # print("影响的行数",row)
        # 4.提交
        conn.commit()
        # print(conn)
        return row

    # 排序
    def arrange(self):
        try:
            conn = pymysql.connect(
                host="127.0.0.1",
                port=3306,
                db="police",
                user="root",
                password="redhat",
                charset="utf8"
            )
            cs = conn.cursor()
            cs.execute("SELECT * from roadstatistics ORDER BY unum DESC")
            result = cs.fetchall()
            return result
        except Exception as e:
            print(e)
        finally:
            if conn != None:
                conn.close()

    # 查询指定路段违章次数
    def checkplace(self, place):
        try:
            conn = pymysql.connect(
                host="127.0.0.1",
                port=3306,
                db="police",
                user="root",
                password="redhat",
                charset="utf8"
            )
            cs = conn.cursor()
            row = cs.execute("select * from carcheckinfo where carPlace=%s", [place])
            print(row, "已执行此行")
            return row
        except Exception as e:
            print(e)
        finally:
            if conn != None:
                conn.close()

    # 插入数据到路段次数统计表
    def placeaddsta(self, place, num):
        # 1.建立连接
        conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            db="police",
            user="root",
            password="redhat",
            charset="utf8"
        )
        # 2.创建游标
        cs = conn.cursor()
        # 3.执行sql语句
        cs.execute("update roadstatistics set unum=%s where uplace=%s", [num, place])
        print("影响的行数")
        # 4.提交
        conn.commit()
        # print(conn)
