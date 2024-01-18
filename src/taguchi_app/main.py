import tkinter as tk
from tkinter import messagebox
from make_img import make_img_fire, MakeImageInfo
import os 
import threading
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(CURRENT_DIR, "..", "..", "images", "outputs")


def add_task():
    task = task_entry.get()
  # 画像パスを取得
    if task != "":
        image_path = os.path.join(CURRENT_DIR, "..", "..", "images", "outputs", f"{task}.png")
        imageinfo = MakeImageInfo(prompt=task, width=512, height=512, output=image_path)
        threading.Thread(target=make_img_fire, args=(imageinfo,)).start()
        listbox.insert(tk.END, task)
        task_entry.delete(0, tk.END)
    else:
        messagebox.showinfo("警告", "タスクを入力してください")

def delete_task():
    try:
        task_index = listbox.curselection()[0]
        task = listbox.get(task_index)
        listbox.delete(task_index)
    except:
        messagebox.showinfo("警告", "削除するタスクを選択してください")

def complete_task():
    try:
        task_index = listbox.curselection()[0]
        task = listbox.get(task_index)
        listbox.itemconfig(task_index, fg="green")
        # ここで画像を変更する処理を追加する場合は、tasks_with_imagesを使用
    except:
        messagebox.showinfo("警告", "完了するタスクを選択してください")

root = tk.Tk()
root.title("TODOリスト")

frame = tk.Frame(root)
frame.pack()

listbox = tk.Listbox(frame, height=15, width=50, activestyle='dotbox', font=("Helvetica", 12))
listbox.pack(side=tk.LEFT, fill=tk.Y)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

task_entry = tk.Entry(root, font=("Helvetica", 24))
task_entry.pack()

add_button = tk.Button(root, text="タスク追加", command=add_task)
add_button.pack()

delete_button = tk.Button(root, text="タスク削除", command=delete_task)
delete_button.pack()

complete_button = tk.Button(root, text="タスク完了", command=complete_task)
complete_button.pack()

image_label = tk.Label(root)  # 画像を表示するためのラベルを作成
image_label.pack()

def update_image():
    try:
        task = listbox.get(listbox.curselection()[0])
        image_path = os.path.join(OUTPUT_PATH, f"{task}.png")
        if not os.path.exists(image_path):
            image_label.config(text="アイコン作成中")
            return
        image = tk.PhotoImage(file=image_path)
        image_label.config(image=image)
        image_label.image = image  # 画像を保持
    except:
        pass  # タスクが選択されていない場合は何もしない

listbox.bind('<<ListboxSelect>>', lambda _: update_image())  # タスクが選択されたときに画像を更新

# メインイベントループを開始
root.mainloop()