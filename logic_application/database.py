from WTH.wsgi import application
from wth_base.models import User, Location


def push_database(data: dict):
    try:
        User.objects.create(user_telegram_id=data['chat']['id'])
    except Exception as _er:
        pass


def gen_answer(use, *args, **kwargs):
    func = _use[use]
    return func(*args, **kwargs)


def add(msg, user_id):
    msg = msg if msg != '/add' else None
    success = 'успешно добавлено'
    error = 'ошибка'
    if not msg:
        return error
    Location.objects.create(user=User.objects.get(user_telegram_id=user_id), stop_name=msg)
    return success


def view(msg, *args, **kwargs):
    msg = msg if msg != '/view' else None
    success = ['Есть', 'Нет']
    error = 'ошибка'
    if not msg:
        return error
    loc = Location.objects.filter(stop_name=msg, visible=True)
    if loc:
        return success[0]
    else:
        return success[1]


def report(msg, *args, **kwargs):
    msg = msg if msg != '/report' else None
    success = 'Соощение добавлено'
    error = ['Что-то пошло не так:( Проверьте сообщение, которое вы ввели', 'Такой отметке пока нет']
    if not msg:
        return error[0]
    locs = Location.objects.filter(stop_name=msg)
    for loc in locs:
        loc.user.fake_count += 1
        loc.user.save()
    if not locs:
        return error[1]
    else:
        return success


_use = {
    'add': add,
    'view': view,
    'report': report,
}
