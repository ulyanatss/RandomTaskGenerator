import random
import json
import os
from tkinter import *
from tkinter import ttk, messagebox

# Файл для сохранения истории
HISTORY_FILE = "task_history.json"

# Предопределённые задачи с категориями
DEFAULT_TASKS = [
    {"text": "Прочитать статью", "category": "учёба"},
    {"text": "Сделать зарядку", "category": "спорт"},
    {"text": "Написать отчёт", "category": "работа"},
    {"text": "Выучить 10 новых слов", "category": "учёба"},
    {"text": "Пробежка 2 км", "category": "спорт"},
    {"text": "Созвониться с клиентом", "category": "работа"},
    {"text": "Решить задачу по математике", "category": "учёба"},
    {"text": "Планка 3 минуты", "category": "спорт"},
    {"text": "Подготовить презентацию", "category": "работа"}
]

class TaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("600x500")

        # Список задач (будет загружен из истории или по умолчанию)
        self.tasks = []
        self.history = []  # Список сгенерированных задач (с категориями)

        # Загружаем историю и задачи из файла
        self.load_history()

        # Переменные для фильтра
        self.filter_category = StringVar(value="все")

        # Создание интерфейса
        self.create_widgets()

    def create_widgets(self):
        # --- Верхняя панель: генерация задачи и фильтр ---
        frame_top = ttk.Frame(self.root)
        frame_top.pack(pady=10, padx=10, fill=X)

        ttk.Button(frame_top, text="Сгенерировать задачу", command=self.generate_task).pack(side=LEFT, padx=5)

        ttk.Label(frame_top, text="Фильтр по категории:").pack(side=LEFT, padx=(20,5))
        categories = ["все", "учёба", "спорт", "работа"]
        category_combo = ttk.Combobox(frame_top, textvariable=self.filter_category, values=categories, state="readonly")
        category_combo.pack(side=LEFT, padx=5)
        ttk.Button(frame_top, text="Применить фильтр", command=self.update_history_display).pack(side=LEFT, padx=5)

        # --- Панель добавления новой задачи ---
        frame_add = ttk.LabelFrame(self.root, text="Добавить новую задачу")
        frame_add.pack(pady=10, padx=10, fill=X)

        ttk.Label(frame_add, text="Название:").grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.new_task_entry = ttk.Entry(frame_add, width=40)
        self.new_task_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_add, text="Категория:").grid(row=0, column=2, padx=5, pady=5, sticky=W)
        self.new_category_var = StringVar(value="учёба")
        cat_menu = ttk.Combobox(frame_add, textvariable=self.new_category_var, values=["учёба", "спорт", "работа"], state="readonly")
        cat_menu.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(frame_add, text="Добавить задачу", command=self.add_task).grid(row=0, column=4, padx=10, pady=5)

        # --- Список истории ---
        frame_history = ttk.LabelFrame(self.root, text="История сгенерированных задач")
        frame_history.pack(pady=10, padx=10, fill=BOTH, expand=True)

        # Treeview для отображения истории с колонками
        columns = ("№", "Задача", "Категория")
        self.tree = ttk.Treeview(frame_history, columns=columns, show="headings")
        self.tree.heading("№", text="№")
        self.tree.heading("Задача", text="Задача")
        self.tree.heading("Категория", text="Категория")
        self.tree.column("№", width=40)
        self.tree.column("Задача", width=400)
        self.tree.column("Категория", width=100)

        scrollbar = ttk.Scrollbar(frame_history, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        # --- Кнопка очистки истории ---
        ttk.Button(self.root, text="Очистить историю", command=self.clear_history).pack(pady=5)

        # Отображаем начальную историю
        self.update_history_displ
    def load_history(self):
        """Загружает историю и список задач из JSON-файла."""
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.history = data.get("history", [])
                    # Восстанавливаем список задач: сохраняем предопределённые + добавленные пользователем
                    # Для простоты будем хранить отдельный файл задач, но можно извлекать из истории уникальные.
                    # В данном примере при запуске берём DEFAULT_TASKS и добавляем задачи, которых нет в history.
                    # Но правильнее хранить отдельно базу задач. Реализуем отдельный файл tasks.json.
                    self.load_tasks()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить историю:\n{e}")
                self.history = []
                self.load_tasks()
        else:
            self.history = []
            self.load_tasks()

    def load_tasks(self):
        """Загружает список доступных задач из tasks.json или создаёт по умолчанию."""
        tasks_file = "tasks.json"
        if os.path.exists(tasks_file):
            try:
                with open(tasks_file, "r", encoding="utf-8") as f:
                    self.tasks = json.load(f)
            except:
                self.tasks = DEFAULT_TASKS.copy()
        else:
            self.tasks = DEFAULT_TASKS.copy()
            self.save_tasks()

    def save_tasks(self):
        """Сохраняет текущий список задач в tasks.json."""
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=4)

    def save_history(self):
        """Сохраняет историю в HISTORY_FILE."""
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump({"history": self.history}, f, ensure_ascii=False, indent=4)

    def generate_task(self):
        """Генерирует случайную задачу с учётом текущего фильтра отображения (но генерирует из всех задач)."""
        if not self.tasks:
            messagebox.showwarning("Нет задач", "Список задач пуст. Добавьте задачи вручную.")
            return
        # Случайный выбор из всех доступных задач
        chosen = random.choice(self.tasks)
        # Добавляем в историю
        self.history.append({"text": chosen["text"], "category": chosen["category"]})
        self.save_history()
        self.update_history_display()
        messagebox.showinfo("Новая задача", f"Ваша задача:\n{chosen['text']}\n(Категория: {chosen['category']})")

    def add_task(self):
        """Добавляет новую задачу, если введена не пустая строка."""
        new_text = self.new_task_entry.get().strip()
        new_cat = self.new_category_var.get()
        if not new_text:
            messagebox.showwarning("Ошибка ввода", "Название задачи не может быть пустым.")
            return
        # Проверяем, нет ли уже такой задачи
        for task in self.tasks:
            if task["text"].lower() == new_text.lower() and task["category"] == new_cat:
                messagebox.showinfo("Информация", "Такая задача уже существует в данной категории.")
                return
        self.tasks.append({"text": new_text, "category": new_cat})
        self.save_tasks()
        self.new_task_entry.delete(0, END)
        messagebox.showinfo("Успех", f"Задача '{new_text}' добавлена в категорию '{new_cat}'.")

    def update_history_display(self):
        """Обновляет отображение истории в Treeview с учётом фильтра."""
        # Очищаем текущие строки
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Фильтруем историю
        filter_cat = self.filter_category.get()
        filtered_history = self.history
        if filter_cat != "все":
            filtered_history = [item for item in self.history if item["category"] == filter_cat]
          # Отображаем с нумерацией
        for idx, item in enumerate(filtered_history, 1):
            self.tree.insert("", END, values=(idx, item["text"], item["category"]))

    def clear_history(self):
        """Очищает историю после подтверждения."""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            self.history = []
            self.save_history()
            self.update_history_display()
            messagebox.showinfo("История очищена", "История успешно очищена.")

if __name__ == "__main__":
    root = Tk()
    app = TaskGeneratorApp(root)
    root.mainloop()
```
