"i" - insert - создание новой записи - (автор; название; год) Пример: "i; Пушкин А.С.; Евгений Онегин; 1833"

"if" - import file - импортировать данные JSON-формата - (путь до JSON-файла) Пример: "if /home/user/python/database.json"

"s" - search - поиск по [автору/названию/году/id] - Пример: "s; author; Pushkin A.S.;"

"e" - edit - изменить
1. изменить параметр "In stock" - (id) - Пример: "e; 0x34f0" 
2. изменить запись полностью - (id; author; title; year; status). Пример: "e; 0x34f0; NewAuthor; Newtitle; 1234; true"

"d" - delete - удалить запись - (id) Пример: "d 0x34f0"

">" - next page - следующая страница

"<" - previous page - предыдущая страница

"c" - change table's showing items - изменить количество отображаемых в консоли записей - Пример: "c 20"

"exit" - закрыть программу
