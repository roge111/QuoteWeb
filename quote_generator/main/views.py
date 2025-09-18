from django.shortcuts import redirect, render
from managers.dataBase import DataBaseManager
from .inputData import InputQuote, InputUser
from datetime import datetime
import bcrypt

from random import random




def check_exist_login(login):
    result  = db.query_database(f"select 1 from users where login = '{login}';")
    if not(len(result)) or not(int(result[0][0])):
        return False
    return True

def check_like(user_id, quote_id):
    result = db.query_database(f"select 1 from likes where user_id = {user_id} and quote_id = {quote_id};")
    if not(len(result)) or not(int(result[0][0])):
        return False
    return True


def check_dislike(user_id, quote_id):
    result = db.query_database(f"select 1 from dislikes where user_id = {user_id} and quote_id = {quote_id};")
    if not(len(result)) or not(int(result[0][0])):
        return False
    return True

def check_exist_id_user(user_id):
    result  = db.query_database(f"select 1 from users where id = '{user_id}';")
    if not(len(result)) or not(int(result[0][0])):
        return False
    return True

def check_similar_quote_exists(quote_text):
    """Проверяет существование похожих цитат"""
    # Нормализуем текст: убираем лишние пробелы, приводим к нижнему регистру
    normalized_quote = ' '.join(quote_text.strip().lower().split())
    
    result = db.query_database(
        "SELECT 1 FROM quotes WHERE LOWER(TRIM(quote)) = %s;",
        (normalized_quote,)
    )
    return len(result) > 0

db = DataBaseManager()
# Create your views here.
def main_page(request):
    max_cumulative = db.query_database("SELECT max(cumulative) FROM quotes;")
    user_id = request.session.get('user_id')
    
    if len(max_cumulative) and max_cumulative[0][0]:
        cumulative_quote = round(random() * (max_cumulative[0][0]))
        print(cumulative_quote)
        quote_result = db.query_database(
            f"SELECT id, quote, count_watch FROM quotes WHERE cumulative >= {cumulative_quote} LIMIT 1;"
        )
        if quote_result:
            quote_id, quote_text, count_watch = quote_result[0]
            # ВАЖНО: определяем has_liked для КОНКРЕТНОЙ цитаты
            has_liked = check_like(user_id, quote_id) if user_id else False
            has_disliked = check_dislike(user_id, quote_id) if user_id else False
            db.query_database(f"UPDATE quotes SET count_watch = count_watch + 1 WHERE id = {quote_id};", reg=True)
            context = {
                'quote': quote_text,
                'quote_id': quote_id,
                'count_watch': count_watch + 1,
                'has_like': has_liked,  # ← Для этой конкретной цитаты!
                'has_dislike': has_disliked
            }
        else:
            context = {'quote': "Ошибка загрузки", 'quote_id': None, 'has_liked': False}
    else:
        context = {'quote': "Цитат еще нет(", 'quote_id': None, 'has_liked': False}
    
    return render(request, 'main/index.html', context)

def add_quote(request):
    if request.method == 'POST':
        try:
            form = InputQuote(request.POST)

            if form.is_valid():

                cleaned_data = form.cleaned_data

                quote = cleaned_data['quote_field']
                wieght = cleaned_data['wieght']
                source = cleaned_data['source']
                
                # Проверяем наличие такое цитаты в цитатнике
                if check_similar_quote_exists(quote):
                    context = {
                        'message': 'Такая цитата уже существует!',
                        'form': form
                    }
                    return render(request, 'main/addquote.html', context)

                count_source = db.query_database(f"select count(*) from quotes where source = '{source.lower().replace(' ', '')}';")
                if len(count_source) and int(count_source[0][0]) < 3:
                    
                    cumulative = db.query_database(f"SELECT cumulative FROM quotes ORDER BY cumulative DESC LIMIT 1;")
                    if len(cumulative):
                        cumulative = int(cumulative[0][0]) + int(wieght)
                    else:
                        cumulative = 1
                    db.query_database(f"insert into quotes (quote, weight, cumulative, source) values ('{quote}', {int(wieght)}, {cumulative}, '{source.lower().replace(' ', '')}');", reg=True)
                    return redirect('main_page')
                else:
                    print(count_source)
                    context = context = {
                            'message': f'Уже много цитат от данного источника: {source}',
                            'form': InputQuote()
                        }
                    return render(request, 'main/addquote.html', context)
            else:
                return render(request, 'main/addquote.html', {'form': form})
        except Exception as e:
            return render(request, 'main/addquote.html', {'form': form})
    else:
        form = InputQuote()
        return render(request, 'main/addquote.html', {'form': form})
    




            

def register(request):
    if request.method == 'POST':
        form = InputUser(request.POST)
        
        if form.is_valid():
            cleaned_data = form.cleaned_data
            login = cleaned_data['login']
            password = cleaned_data['password']
            
            # Проверяем существование логина
            if check_exist_login(login):
                context = {
                    'message': 'Такой логин уже существует.',
                    'form': InputUser()  # Новая форма для повторной попытки
                }
                return render(request, 'main/register.html', context)
            
            # Регистрируем пользователя
            try:
                # Хэшируем пароль
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                
                # Сохраняем в БД
                db.query_database(
                    "INSERT INTO users (login, password) VALUES (%s, %s);", 
                    (login, hashed_password), 
                    reg=True
                )
                request.session['user_id'] = db.query_database(f"select id from users where login = '{login}';")[0][0]
            
                
                context = {
                    'message': 'Успешная регистрация! Теперь можете войти.',
                    'form': InputUser()
                }
                return render(request, 'main/register.html', context)
                
            except Exception as e:
                print(f"Ошибка при регистрации: {e}")
                context = {
                    'message': 'Ошибка при регистрации. Попробуйте позже.',
                    'form': InputUser()
                }
                return render(request, 'main/register.html', context)
        else:
            # Форма не валидна - показываем форму с ошибками
            return render(request, 'main/register.html', {'form': form})
    
    # GET запрос
    form = InputUser()
    return render(request, 'main/register.html', {'form': form})


def logIn(request):
    
    if request.method == 'POST':
        form = InputUser(request.POST)
        try:
            if form.is_valid():
                cleaned_data = form.cleaned_data

                login = cleaned_data['login']
                password = cleaned_data['password']

                if check_exist_login(login):
                    hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

                    hash_pwd_db = db.query_database(f"select password from users where login = '{login}';")[0][0]
                    print(db.query_database(f"select id from users where login = '{login}';"))
                    if bcrypt.checkpw(password.encode('utf-8'), hash_pwd_db.encode('utf-8')):
                        request.session['is_authenticated'] = True
                        request.session['login'] = login
                        request.session['user_id'] = db.query_database(f"select id from users where login = '{login}';")[0][0]
                        request.session.save()

                        return redirect('main_page')
                    else:
                        context = {
                            'message': 'Неверный пароль. Попробуйте снова',
                            'form': InputUser()
                        }
                        return render(request, 'main/logIn.html', context)
                else:
                    return render(request, 'main/register.html')
        except Exception as e:
            print(f"Ошибка при автризации: {e}")
            context = {
                'message': 'Ошибка при авторизации. Попробуйте позже.',
                'form': InputUser()
            }
            return render(request, 'main/logIn.html', context)
    #GET запрос
    form = InputUser()
    return render(request, 'main/logIn.html', {'form': form})

def like_quote(request):
    quote_id = request.POST.get('quote_id')
    user_id = request.session.get('user_id')
    
    # ПРОВЕРКА: существует ли цитата?
    quote_result = db.query_database(f"SELECT quote FROM quotes WHERE id = {quote_id};")
    if not quote_result:
        return redirect('main_page')  # Цитата не существует
    
    quote = quote_result[0][0]
    
    if not check_exist_id_user(user_id):
        return redirect('logIn')
    
    if not check_like(user_id, quote_id):
        if check_dislike(user_id, quote_id):
            db.query_database(
                f"DELETE FROM dislikes WHERE user_id = {user_id} AND quote_id = {quote_id};", 
                reg=True
            )

        date_now = datetime.now()
        db.query_database(
            f"INSERT INTO likes (user_id, quote_id, created_at) VALUES ({user_id}, {quote_id}, '{date_now}');", 
            reg=True
        )
    else:
        # УДАЛЕНИЕ лайка - это нормально при нажатии кнопки
        db.query_database(
            f"DELETE FROM likes WHERE user_id = {user_id} AND quote_id = {quote_id};", 
            reg=True
        )
    
    return redirect('main_page')
        

def logout(request):
    request.session.flush()  # Полностью очищает сессию
    return redirect('main_page')

     
def popluar(request):
    query = """
        SELECT 
            q.id,
            q.quote,
            COUNT(l.user_id) as likes_count
        FROM quotes q
        LEFT JOIN likes l ON q.id = l.quote_id
        GROUP BY q.id, q.quote
        ORDER BY likes_count DESC
        LIMIT (
            SELECT 
                CASE 
                    WHEN COUNT(*) < 10 THEN COUNT(*)
                    ELSE 10
                END
            FROM quotes
        )
        """
        
    raw_quotes = db.query_database(query)
            
    # Преобразуем в список словарей для удобства
    quotes = [
        {
            'id': quote[0],
            'quote': quote[1],
            'likes_count': quote[2]
        }
        for quote in raw_quotes
    ]

    return render(request, 'main/top_quotes.html', {'quotes': quotes})

def dislike_quote(request):
    quote_id = request.POST.get('quote_id')
    user_id = request.session.get('user_id')
    
    # ПРОВЕРКА: существует ли цитата?
    quote_result = db.query_database(f"SELECT quote FROM quotes WHERE id = {quote_id};")
    if not quote_result:
        return redirect('main_page')  # Цитата не существует
    
    quote = quote_result[0][0]
    like = check_like(user_id, quote_id)
    dislike = check_dislike(user_id, quote_id)
    if not check_exist_id_user(user_id):
        return redirect('logIn')
    
    if not like and not dislike:
        date_now = datetime.now()
        db.query_database(
            f"INSERT INTO dislikes (user_id, quote_id, created_at) VALUES ({user_id}, {quote_id}, '{date_now}');", 
            reg=True
        )
    elif like  and not dislike:
        db.query_database(
            f"DELETE FROM likes WHERE user_id = {user_id} AND quote_id = {quote_id};", 
            reg=True
        )

        date_now = datetime.now()
        db.query_database(
            f"INSERT INTO dislikes (user_id, quote_id, created_at) VALUES ({user_id}, {quote_id}, '{date_now}');", 
            reg=True
        )

    elif dislike:
        # УДАЛЕНИЕ дизлайка - это нормально при нажатии кнопки
        db.query_database(
            f"DELETE FROM dislikes WHERE user_id = {user_id} AND quote_id = {quote_id};", 
            reg=True
        )
    
    return redirect('main_page')



        