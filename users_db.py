import pandas as pd
import os
import re

DB_FILE = 'users.csv'

def load_users():
    if not os.path.exists(DB_FILE):
        df = pd.DataFrame(columns=['email', 'password', 'base_role', 'permissions'])
        df.to_csv(DB_FILE, index=False)
    return pd.read_csv(DB_FILE)

def save_users(df):
    df.to_csv(DB_FILE, index=False)

def check_user(email, password):
    df = load_users()
    user = df[df['email'].str.lower() == email.lower()]
    
    if user.empty:
        return None, None
    
    if user.iloc[0]['password'] == password:
        base_role = user.iloc[0]['base_role']
        permissions = user.iloc[0]['permissions']
        return base_role, permissions
    
    return None, None

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
    
    base_role = get_role_from_email(email)
    
    if not base_role:
        return False, "Неверный формат почты. Нужна почта @uni-dubna.ru"
        
    df = load_users()
    
    new_user_data = {
        'email': email.lower(), 
        'password': password, 
        'base_role': base_role, 
        'permissions': "" 
    }
    
    new_user = pd.DataFrame([new_user_data])
    df = pd.concat([df, new_user], ignore_index=True)
    save_users(df)
    
    return True, f"Вы успешно зарегистрированы как {base_role}"