import os

# Транслитерация кириллицы в латиницу
TRANSLIT = {
    "а":"a","б":"b","в":"v","г":"g","д":"d","е":"e","ё":"e","ж":"zh","з":"z","и":"i",
    "й":"i","к":"k","л":"l","м":"m","н":"n","о":"o","п":"p","р":"r","с":"s","т":"t",
    "у":"u","ф":"f","х":"h","ц":"ts","ч":"ch","ш":"sh","щ":"shch","ъ":"","ы":"y",
    "ь":"","э":"e","ю":"yu","я":"ya","А":"A","Б":"B","В":"V","Г":"G","Д":"D","Е":"E",
    "Ё":"E","Ж":"Zh","З":"Z","И":"I","Й":"I","К":"K","Л":"L","М":"M","Н":"N","О":"O",
    "П":"P","Р":"R","С":"S","Т":"T","У":"U","Ф":"F","Х":"H","Ц":"Ts","Ч":"Ch","Ш":"Sh",
    "Щ":"Shch","Ъ":"","Ы":"Y","Ь":"","Э":"E","Ю":"Yu","Я":"Ya"
}

def slugify(name):
    # Транслитерация и замена пробелов на дефис
    translit = ''.join(TRANSLIT.get(c, c) for c in name)
    return translit.lower().replace(' ', '-')

# Получаем все папки в текущей директории
current_dir = os.getcwd()
folders = [f for f in os.listdir(current_dir) if os.path.isdir(f)]

for folder in folders:
    new_name = slugify(folder)
    if folder != new_name:
        print(f'Renaming "{folder}" → "{new_name}"')
        os.rename(os.path.join(current_dir, folder), os.path.join(current_dir, new_name))