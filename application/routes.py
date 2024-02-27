from application import app,db,bcrypt
from flask import request,jsonify
from application.forms import SleepForm,LoginForm,SignUpForm
from application.models import Sleep,User

@app.before_request
def create_tables():
    db.create_all()


@app.route('/api/signup', methods=['POST'])
def signup():
    form = SignUpForm(request.form)
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user_data = {
        "username": form.username.data,
        "email": form.email.data,
        "password": hashed_password
    }
    user = User(**user_data)
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Account created successfully!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error in creating new account: {str(e)}'}), 400
    
 
@app.route('/api/login',methods=['POST'])
def login():
    form=LoginForm(request.form)
    if request.method=='POST':
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            return jsonify({'message':f"{user.username}, logged in successfully!"}),200
        else:
            return jsonify({"message":"Incorrect Username or Passsword"}),400
        
        
@app.route('/api/sleep', methods=['GET'])
def getAllSleepDetails():
    try:
        data=Sleep.query.order_by(Sleep.startTime).all()
        sleepdict=[{'id':sleep.id,
                            'startTime':sleep.startTime,
                            'endTime':sleep.endTime,
                            'sleepDuration':sleep.sleepDuration,
                            'sleepQuality':sleep.sleepQuality
                            }for sleep in data]
        return jsonify({'sleepdata':sleepdict})
    except Exception as e:
        return jsonify({'error':str(e)}),500
        
        
@app.route('/api/sleep/<int:owner_id>',methods=['POST','GET'])
def SleepDetails(owner_id):
    if request.method=='POST': 
            form=SleepForm(request.form)  
            data = {
                'startTime': form.startTime.data,
                'endTime': form.endTime.data,
                'sleep_owner':owner_id
            }
            sleep = Sleep(**data)
            sleep.sleepDuration=sleep.calculateSleepDuration
            sleep.sleepQuality=sleep.calculateSleepQuality
            db.session.add(sleep)
            try:
                db.session.commit()
                return jsonify({"message": "Data added successfully"})
            except Exception as e:
                return jsonify({"error": str(e)})
    elif request.method=='GET':
            try:
                data=User.query.filter_by(id=owner_id).first()
                sleepdict=[{'id':sleep.id,
                            'startTime':sleep.startTime,
                            'endTime':sleep.endTime,
                            'sleepDuration':sleep.sleepDuration,
                            'sleepQuality':sleep.sleepQuality
                            }for sleep in data.sleeplist]
                return jsonify({'sleepdata':sleepdict})
            except Exception as e:
                return jsonify({'error':str(e)}),500
            
        
        
        
