from PyQt5.QtWidgets import (
 QWidget, QApplication, QTextEdit, QHBoxLayout, QVBoxLayout,
 QListWidget, QPushButton, QLineEdit, QLabel, QInputDialog
)
import json

style = """
QlistWidget, QTextEdit, QlineEdit {
    border: 1px solid black;
    border-radius: 5px;
    padding: 5px;
}

QPushButton {
    background-color: green;
    color: black;
    border-radius: 5px;
    padding: 10px;
}

QPushButton:hover {
    background-color: gray;
}

Qlabel {
    font-weight: bold;
}
"""

#интерфейс
app = QApplication([]) 
window = QWidget()
window.setWindowTitle('Мега заметки Аниме') 
window.resize(1200, 600) #размер окна
window.setStyleSheet(style)

#текст для виджетов
text_list = QLabel('Список заметок')
text_tag = QLabel('Список тегов')

#нужные интерфейсы
field_text = QTextEdit() #окно для текста
notes_list = QListWidget()#окно для заметок
notes_list_tag = QListWidget()#окно для тегов
search_filed = QLineEdit()#для поиска тегов

#кнопки для списка
btn_create_note = QPushButton('Создать заметку')
btn_save_note = QPushButton('Сохранить заметку')
btn_delete_note = QPushButton('Удалить заметку')

#кнопки для тега
btn_create_tag = QPushButton('Добавить тег')
btn_find = QPushButton('Поиск')
btn_delete_tag = QPushButton('Удалить тег')

#размещение интерфейса
main_line = QHBoxLayout()
v_line = QVBoxLayout()
h1_line = QHBoxLayout()
h2_line = QHBoxLayout()

main_line.addWidget(field_text)
main_line.addLayout(v_line)

#список заметок
v_line.addWidget(text_list) #доавить текст
v_line.addWidget(notes_list) #добавить список заметок

v_line.addLayout(h1_line) #добваить первую линию

h1_line.addWidget(btn_create_note) 
h1_line.addWidget(btn_save_note)
v_line.addWidget(btn_delete_note)

#список тегов
v_line.addWidget(text_tag) #добавить текст
v_line.addWidget(notes_list_tag)
v_line.addWidget(search_filed) #добавить поисковик

v_line.addLayout(h2_line) #добваить вторую линию

h2_line.addWidget(btn_create_tag) #добавить список тегов
h2_line.addWidget(btn_find) #прикрепить поисковик
v_line.addWidget(btn_delete_tag)

#функционал
def show_note(): #показать заметки
    key = notes_list.selectedItems()[0].text()
    field_text.setText(notes[key]['текст'])

    notes_list_tag.clear()
    notes_list_tag.addItems(notes[key]['теги'])

def create_note(): #добавть заметки
    note_name, ok = QInputDialog().getText(window, 'Добавить замеку', 'Назвать заметку')
    if note_name != '':
        notes[note_name] = {"текст": "","теги": []}
        with open('data.json','w',encoding="UTF-8") as file:
            json.dump(notes,file,ensure_ascii=False)
        notes_list.addItem(note_name)
    
def save_note(): #сохранить заметку
    key = notes_list.selectedItems()[0].text()
    text = field_text.toPlainText()
    notes[key]['текст'] = text
    with open('data.json','w',encoding="UTF-8") as file:
        json.dump(notes,file,ensure_ascii=False)

def remove_note(): #удалить заметку
    if notes_list.selectedItems():
        key = notes_list.selectedItems()[0].text()
        del notes[key]
        with open('data.json','w',encoding="UTF-8") as file:
            json.dump(notes,file,ensure_ascii=False)
        notes_list.clear()
        field_text.clear()
        notes_list_tag.clear()
        notes_list.addItems(notes)

def create_tag(): #создать теги
    if notes_list.selectedItems():
        key = notes_list.selectedItems()[0].text()
        tag = search_filed.text()
        if not tag in notes[key]['теги'] and tag != '':
            notes[key]['теги'].append(tag)
            notes_list_tag.clear()
            search_filed.clear()
            notes_list_tag.addItems(notes[key]['теги'])

        with open('data.json','w',encoding="UTF-8") as file:
            json.dump(notes,file,ensure_ascii=False)

def remove_tag():
    if notes_list_tag.selectedItems():
        key = notes_list.selectedItems()[0].text()
        tag = notes_list_tag.selectedItems()[0].text()
        notes[key]['теги'].remove(tag)
        notes_list_tag.clear()
        notes_list_tag.addItems(notes[key]['теги'])
        with open('data.json','w',encoding="UTF-8") as file:
            json.dump(notes,file,ensure_ascii=False)

def search():
    tag = search_filed.text()
    if btn_find.text() == 'Поиск' and tag != '':
        notes_filtred = {}
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filtred[note] = notes[note]
        search_filed.clear()
        notes_list_tag.clear()
        notes_list.clear()
        
        notes_list.addItems(notes_filtred)
        btn_find.setText('Сбросить')
    elif btn_find.text() == 'Сбросить':
        search_filed.clear()
        notes_list_tag.clear()
        notes_list.clear()

        notes_list.addItems(notes)
        btn_find.setText('Поиск')
                

#подписки на событие
notes_list.itemClicked.connect(show_note)
btn_create_note.clicked.connect(create_note)
btn_save_note.clicked.connect(save_note)
btn_delete_note.clicked.connect(remove_note)

btn_create_tag.clicked.connect(create_tag)
btn_delete_tag.clicked.connect(remove_tag)
btn_find.clicked.connect(search)

#запуск приложение
with open('data.json','r',encoding="UTF-8") as file:
    notes = json.load(file)

notes_list.addItems(notes) #выводение заметок

window.setLayout(main_line)
window.show()
app.exec()
