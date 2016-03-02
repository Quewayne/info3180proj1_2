from . import db

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(64))
    lname = db.Column(db.String(64))
    age = db.Column(db.String(4))
    sex= db.Column(db.String(2))
    img = db.Column(db.String(150))
    uname= db.Column(db.String(64))
    hscore=db.Column(db.Integer) 
    tdoll=db.Column(db.Integer)
    added=db.Column(db.DateTime)
    uid=db.Column(db.String(20))

    def __init__(self, fname, lname, age, sex,img,uname, added, uid):
       self.fname = fname
       self.lname = lname
       self.age = age
       self.sex = sex
       self.img=img
       self.uname = uname 
       self.hscore = 0 
       self.tdoll = 0
       self.added = added
       self.uid = uid
