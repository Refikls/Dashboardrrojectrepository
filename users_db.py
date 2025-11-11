import pandas as pd
import os
import re

DB_FILE = 'users.csv'

def load_users():
    if not os.path.exists(DB_FILE):
        df = pd.DataFrame(columns=['email', 'password', 'role'])
        df.to_csv(DB_FILE, index=False)
    return pd.read_csv(DB_FILE)

def save_users(df):
    df.to_csv(DB_FILE, index=False)

def check_user(email, password):
    df = load_users()
    user = df[df['email'].str.lower() == email.lower()]
    
    if user.empty:
        return None
    
    if user.iloc[0]['password'] == password:
        return user.iloc[0]['role']
    
    return None

def user_exists(email):
    df = load_users()
    return not df[df['email'].str.lower() == email.lower()].empty

def get_role_from_email(email):
    email_lower = email.lower()
    
    student_pattern = r"^[a-z\.]+\.\d{2}@uni-dubna\.ru$"
    staff_pattern = r"^[a-z\.]+@uni-dubna\.ru$"
    
    if re.match(student_pattern, email_lower):
        return 'student'
    elif re.match(staff_pattern, email_lower):
        return 'staff'
    
    return None

def add_user(email, password):
    if user_exists(email):
        return False, "Пользователь с такой почтой уже существует."
    
    role = get_role_from_email(email)
    
    if not role:
        return False, "Неверный формат почты. Нужна почта @uni-dubna.ru"
        
    df = load_users()
    new_user = pd.DataFrame([{'email': email.lower(), 'password': password, 'role': role}])
    df = pd.concat([df, new_user], ignore_index=True)
    save_users(df)
    
    return True, f"Вы успешно зарегистрированы как {role}"