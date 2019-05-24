import sqlite3
import logging
class DiceDB:
   def __init__(self,respath):
      self.__respath=respath
      self.__conn=sqlite3.connect(self.__respath+'kostkadb.db')
      self.__cursor=self.__conn.cursor()
      logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
      self.__logger = logging.getLogger(__name__)
   def __del__(self):
        self.__conn.close()

   def addUser(self,userdata):
      sql="""
            INSERT INTO Users (id,fname,sname,uname)
            VALUES (?,?,?,?);"""
      try:
         self.__cursor.execute(sql, userdata)
         self.__conn.commit()
      except sqlite3.Error as e:
         self.__logger.error(e)
         return False
      return True

   def addGroup(self,grdata):
      sql="""
          INSERT INTO Groups (id,name)
          VALUES (?,?)
          """
      try:
          self.__cursor.execute(sql, grdata)
          self.__conn.commit()
      except sqlite3.Error as e:
          self.__logger.error(e)
          return False
      return True

   def listUsers(self,grp=None):
      sql="SELECT * FROM Users"
      bind=[]
      if (grp!=None):
          sql="""SELECT Users.id, Users.fname, Users.sname, Users.uname FROM
          Users_Groups INNER JOIN Users
          ON Users_Groups.uid=Users.id
          WHERE Users_Groups.gid=?"""
          bind=[grp]
      try:
          self.__cursor.execute(sql,bind)
          rows=self.__cursor.fetchall()
      except sqlite3.Error as e:
          self.__logger.error(e)
          return False
      return rows

   def UsrGrpAdd(self,pairGU):
      sql="INSERT INTO Users_Groups (gid,uid) values (?,?)"
      try:
          self.__cursor.execute(sql,pairGU)
          self.__conn.commit()
      except sqlite3.Error as e:
          self.__logger.error(e)
          return False
      return True
