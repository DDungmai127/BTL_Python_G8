import tkinter as tk
from tkinter import ttk, messagebox
import random
from playsound import playsound
import os
import dao
search_history = []  # Danh sách lưu lịch sử tìm kiếm
# Dữ liệu từ điển mẫu với loại từ và phiên âm
types_líst  = dao.getAllTypes()
themes_list = dao.getAllTheme()
dictionary_data = dao.getAllWords()
print(dictionary_data)
# Hàm tìm kiếm từ

def search_word(event=None):
    word = entry.get().lower()
    selected_type = type_combobox.get()
    searchList.delete(0, tk.END)  # Xóa danh sách từ tìm kiếm
    clear_labels()  # Xóa nội dung trong các label
    for key, data in dictionary_data.items():
        if word in key and (selected_type == "Tất cả" or data['type'] == selected_type):
            searchList.insert(tk.END, key) 
def show_recent_searches(event=None):
    searchList.delete(0, tk.END)  # Xóa danh sách từ tìm kiếm
    for word in search_history[-5:]:  # Hiển thị 5 từ tìm kiếm gần đây nhất
        searchList.insert(tk.END, word)

def save_to_history(selected_word):
    if selected_word not in search_history:
        search_history.append(selected_word)  # Lưu từ vào lịch sử tìm kiếm
# Hàm xóa nội dung trong các label
def clear_labels():
    meaning_label.config(text="")
    phonetic_display_label.config(text="")
    type_label.config(text="")
    usage_label.config(text="")
    synonyms_label.config(text="")
    antonyms_label.config(text="")
# Hàm hiển thị thông tin của từ được chọn
def show_search_result(event):
    if searchList.curselection():
        selected_word = searchList.get(searchList.curselection())
        data = dictionary_data.get(selected_word)
        if data:
            word_label.config(text=selected_word)
            meaning_label.config(text=f"Nghĩa: {data['meaning']}")
            phonetic_display_label.config(text=f"Phiên âm: {data['phonetic']}")
            type_label.config(text=f"Loại từ: {data['type']}")
            usage_label.config(text=f"Cách sử dụng: {data['usage']}")
            synonyms_label.config(text=f"Từ đồng nghĩa: {', '.join(data['synonyms']) if data['synonyms'] else 'Không có'}")
            antonyms_label.config(text=f"Từ trái nghĩa: {', '.join(data['antonyms']) if data['antonyms'] else 'Không có'}")
             # Lưu từ vào lịch sử khi chọn từ
            play_button.grid(row=2, column=4, padx=5, sticky='w')
            save_to_history(selected_word)

# Hàm lưu từ yêu thích
def save_word():
    selected_word_index = searchList.curselection()
    themes_list = dao.getAllTheme()
    if selected_word_index:
        selected_word = searchList.get(selected_word_index)
        # Tạo cửa sổ chọn chủ đề
        theme_save_window = tk.Toplevel(root)  # Cửa sổ mới
        theme_save_window.title("Chọn chủ đề")
        select_save_label = ttk.Label(theme_save_window, text="Chọn chủ đề:")
        select_save_label.pack(pady=10)
        theme_save_combox = ttk.Combobox(theme_save_window, values=themes_list, state="readonly")
        theme_save_combox.set(themes_list[0])  # Giá trị mặc định
        theme_save_combox.pack(pady=5)
        def confirm_selection():
            selected_theme = theme_save_combox.get()
            themeId = dao.getThemeByName(selected_theme)
            dao.addWordToTheme(selected_word, themeid=themeId)
            messagebox.showinfo("Thông báo", f"{selected_word} đã được lưu vào danh sách yêu thích với chủ đề {selected_theme}.")
            theme_save_window.destroy()  # Đóng cửa sổ chọn chủ đề
        confirm_button = ttk.Button(theme_save_window, text="Xác nhận", command=confirm_selection)
        confirm_button.pack(pady=10)
    else:
        messagebox.showwarning("Chưa chọn", "Hãy chọn từ để lưu.")
# Hàm hiển thị thông tin của từ yêu thích được chọn và chuyển trang
def show_word_selected_theme(event):
    if themes_listboxs.curselection():
        selected_word = themes_listboxs.get(themes_listboxs.curselection())  
        # Chuyển về trang 1
        notebook.select(page1)  # Chọn trang 1
        # Hiển thị thông tin từ
        entry.delete(0, tk.END)  # Xóa ô nhập
        entry.insert(0, selected_word)  # Nhập từ vào ô tìm kiếm
        search_word()  # Gọi hàm tìm kiếm để hiển thị danh sách từ
        # Tự động chọn từ và hiển thị thông tin chi tiết
        searchList.select_set(0)  # Chọn từ đầu tiên (hoặc bạn có thể sử dụng chỉ mục cụ thể)
        show_search_result(event)  # Hiển thị thông tin chi tiết
# Hàm để hiển thị từ theo chủ đề đã chọn
def update_themes():
    selected_theme = theme_combobox.get()
    themes_listboxs.delete(0, tk.END)  # Xóa danh sách hiện tại
    themeid = dao.getThemeByName(selected_theme)
    words = dao.getWordByThemeId(theme_id=themeid)
    # Lọc và thêm từ vào ListBox theo chủ đề đã chọn
    for word in words:
        themes_listboxs.insert(tk.END, word)  # Thêm từ vào danh sách
def add_theme():
    theme_window = tk.Toplevel(root, height=20, width=50)  # Cửa sổ mới
    theme_window.title("Thêm chủ đề")
    theme_label = ttk.Label(theme_window, text="Nhập tên chủ đề:")
    theme_label.pack(pady=10)
    theme_entry = ttk.Entry(theme_window)
    theme_entry.pack(pady=5)
    def confirm_add():
        themes_list = dao.getAllTheme()
        new_theme = theme_entry.get().strip()
        print(themes_list)
        if new_theme and new_theme not in themes_list:
            print(themes_list)
            dao.addTheme(new_theme)
            themes_list = dao.getAllTheme()
            theme_combobox['values'] = themes_list  # Cập nhật giá trị của combobox
            theme_combobox.set(new_theme)  # Đặt giá trị mặc định là chủ đề vừa thêm
            messagebox.showinfo("Thông báo", f"Đã thêm chủ đề: {new_theme}")
            theme_window.destroy()
        else:
            messagebox.showwarning("Cảnh báo", "Chủ đề đã tồn tại hoặc rỗng.")
    confirm_button = ttk.Button(theme_window, text="Xác nhận", command=confirm_add)
    confirm_button.pack(pady=10)

# Hàm xóa chủ đề
def delete_theme():
    selected_theme = theme_combobox.get()  # Lấy chủ đề được chọn
    themes_list = dao.getAllTheme()

    if selected_theme in themes_list:
        dao.deleteTheme(selected_theme)
        themes_list.remove(selected_theme) # Xóa chủ đề khỏi danh sách
        themes_list = dao.getAllTheme()
        theme_combobox['values'] = themes_list  # Cập nhật giá trị của combobox
        theme_combobox.set(themes_list[0] if themes_list else "")  # Đặt giá trị mặc định
        messagebox.showinfo("Thông báo", "Chủ đề đã được xóa.")
    else:
        messagebox.showwarning("Chưa chọn", "Hãy chọn chủ đề để xóa.")
# Hàm xóa từ yêu thích
def delete_word_in_theme():
    selected_index = themes_listboxs.curselection()  # Lấy chỉ số của từ được chọn
    selected_theme = theme_combobox.get()
    theme_id = dao.getThemeByName(selected_theme)
    if selected_index:
        selected_word = themes_listboxs.get(selected_index)
        themes_listboxs.delete(selected_index)  # Xóa từ được chọn
        dao.removeWordOutTheme(selected_word, theme_id)
        messagebox.showinfo("Thông báo", "Từ đã được xóa khỏi danh sách.")
    else:
        messagebox.showwarning("Chưa chọn", "Hãy chọn từ để xóa.")

# Biến toàn cục để lưu từ hiện tại đang ôn tập
current_word = ""
is_reviewing = False  # Trạng thái ôn tập
# Hàm bắt đầu ôn tập từ vựng
# Hàm chọn từ ngẫu nhiên và cập nhật giao diện
def start_vocabulary_review():
    global current_word
    global is_reviewing 
    review_type = review_type_combobox.get()
    if not is_reviewing: 
        is_reviewing = True
        start_button.config(text="Kết thúc ôn tập")
        answer_entry.pack(pady=5)
        answer_label.pack(pady=10)
        check_button.pack(pady=10)
        continue_button.pack(pady=10)
        choose_random_word(review_type)
    else:
        # Nếu đang ôn tập, kết thúc ôn tập
        end_vocabulary_review()

# Hàm chọn từ ngẫu nhiên và cập nhật giao diện
def choose_random_word(review_type):
    global current_word
    current_word = random.choice(list(dictionary_data.keys()))  # Chọn ngẫu nhiên một từ
    if review_type == "Theo nghĩa":
        meaning_label.config(text=dictionary_data[current_word]['meaning'])  # Hiển thị nghĩa
        phonetic_check_label.config(text=f"Phiên âm: {dictionary_data[current_word]['phonetic']}")
        answer_label.config(text="Nhập từ tiếng Anh:")
    elif review_type == "Theo phát âm":
        phonetic_check_label.config(text=f"Phiên âm: {dictionary_data[current_word]['phonetic']}")
        meaning_label.config(text="Nhập từ tiếng Anh tương ứng:")
# Hàm kết thúc ôn tập
def end_vocabulary_review():
    global is_reviewing
    meaning_label.config(text="")
    phonetic_check_label.config(text="")
    answer_entry.delete(0, tk.END)
    result_check_label.config(text="")
    start_button.config(text="Bắt đầu ôn tập")  # Đổi tên nút
    is_reviewing = False  # Cập nhật trạng thái ôn tập
    answer_entry.pack_forget()  # Ẩn ô nhập
    answer_label.pack_forget()  # Ẩn label nhập
    check_button.pack_forget()  # Ẩn nút kiểm tra
    continue_button.pack_forget()  # Ẩn nút tiếp tục


# Hàm tiếp tục ôn tập
def continue_review():
    review_type = review_type_combobox.get()
    choose_random_word(review_type)  # Gọi hàm chọn từ ngẫu nhiên

# Hàm lấy câu trả lời đúng
def get_correct_answer():
    return current_word

# Hàm kiểm tra câu trả lời
def check_answer():
    user_answer = answer_entry.get().strip().lower()
    if not user_answer:
        result_check_label.config(text="Vui lòng nhập câu trả lời trước khi kiểm tra.", foreground="red")
        return  # Thoát khỏi hàm nếu ô nhập rỗng
    correct_answer = get_correct_answer()  # Giả sử bạn có hàm để lấy câu trả lời đúng

    if user_answer == correct_answer:
        result_check_label.config(text="Chính xác! Bạn đã trả lời đúng.", foreground="green")
    else:
        result_check_label.config(text=f"Sai rồi! Đáp án đúng là: {correct_answer}.", foreground="red")

# Hàm đọc từ
def play_audio():
    selected_word_index = searchList.curselection()
    # selected_word = phonetic_display_label.cget().split(":")
    if selected_word_index:
        selected_word = searchList.get(selected_word_index)
        # audio_file = os.path.join("audio", f"{selected_word}.mp3")  # Đường dẫn đến tệp âm thanh
        link = dictionary_data[selected_word]["path"]
        print(link)
        # audio_file = os.path.join(link)  # Đường dẫn đến tệp âm thanh
        # print(audio_file)
        # if os.path.exists("audio/python.mp3"):
        #     playsound("audio/python.mp3")
        if os.path.exists(link):
            playsound(link)  # Phát âm thanh
        else:
            messagebox.showwarning("Cảnh báo", "Tệp âm thanh không tồn tại.")
    else:
        messagebox.showinfo("Chưa chọn", "Hãy chọn từ để phát âm.")



# Tạo cửa sổ chính
root = tk.Tk()
root.title("Ứng Dụng Từ Điển Mở Rộng")
root.geometry("600x500")
# Tạo Notebook
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)
# Tạo các trang
page1 = ttk.Frame(notebook)
page2 = ttk.Frame(notebook)
page3 = ttk.Frame(notebook)
# Thêm các trang vào Notebook
notebook.add(page1, text='Tra cứu từ')
notebook.add(page2, text='Chủ đề')
notebook.add(page3, text='Học từ vựng')
# Nội dug cho Trang Tra cứu từ
label = ttk.Label(page1, text="Nhập từ cần tra cứu:")
label.grid(row=0, column=0, pady=10, sticky='w')
entry = ttk.Entry(page1, width=25)
entry.grid(row=0, column=1, pady=5, sticky='ew')
entry.bind('<KeyRelease>', search_word)  # Lắng nghe sự kiện nhấn phím
entry.bind('<FocusIn>', show_recent_searches)  # Hiển thị lịch sử khi nhấn vào ô tìm kiếm
entry.bind('<Return>', search_word)  # Gán phím Enter cho hàm tìm kiếm
# Combobox để chọn loại từ
type_label = ttk.Label(page1, text="Chọn loại từ:")
type_label.grid(row=0, column=2, pady=10, sticky='w')
type_combobox = ttk.Combobox(page1, values=types_líst, state="readonly")
type_combobox.set("Tất cả")  # Giá trị mặc định
type_combobox.grid(row=0, column=3, pady=5, sticky='ew')
type_combobox.bind('<<ComboboxSelected>>', search_word)
save_button = ttk.Button(page1, text="Lưu", command=save_word)
save_button.grid(row=0, column=4, padx=5)
searchList = tk.Listbox(page1, height=10, width=50)  # Hiển thị từ tìm kiếm
searchList.grid(row=1, column=0, columnspan=5, pady=10)
# Kết nối sự kiện chọn từ trong Listbox
searchList.bind('<<ListboxSelect>>', show_search_result)
# Các label để hiển thị thông tin từ

word_label = ttk.Label(page1, 
                       text="", 
                       wraplength=500, 
                       justify="left", 
                       font=("Arial", 20, "bold"),  # Sử dụng font Arial, kích thước 24, kiểu bold
                       padding=(10, 0, 0, 0))  # Padding bên trái (10px)

word_label.grid(row=2, column=0, columnspan=5, pady=5, sticky='w')
meaning_label = ttk.Label(page1, text="", wraplength=500, justify="left")
meaning_label.grid(row=3, column=0, columnspan=5, pady=5, sticky='w')
phonetic_display_label = ttk.Label(page1, text="", wraplength=500, justify="left")
phonetic_display_label.grid(row=4, column=0, columnspan=5, pady=5, sticky='w')
# Thêm nút "Đọc từ" vào trang Tra cứu từ, gần chỗ phiên âm
play_button = ttk.Button(page1, text="Đọc từ", command=play_audio)
# play_button.grid(row=3, column=4, padx=5, sticky='w')
play_button.pack_forget() # Đặt nút ở cột 4, cùng hàng với label phiên âm
type_label = ttk.Label(page1, text="", wraplength=500, justify="left")
type_label.grid(row=5, column=0, columnspan=5, pady=5, sticky='w')
usage_label = ttk.Label(page1, text="", wraplength=500, justify="left")
usage_label.grid(row=6, column=0, columnspan=5, pady=5, sticky='w')
synonyms_label = ttk.Label(page1, text="", wraplength=500, justify="left")
synonyms_label.grid(row=7, column=0, columnspan=5, pady=5, sticky='w')
antonyms_label = ttk.Label(page1, text="", wraplength=500, justify="left")
antonyms_label.grid(row=8, column=0, columnspan=5, pady=5, sticky='w')

# Định dạng label cho đẹp hơn
meaning_label.config(font=('Arial', 10, 'bold'))
phonetic_display_label.config(font=('Arial', 10))
type_label.config(font=('Arial', 10))
usage_label.config(font=('Arial', 10))
synonyms_label.config(font=('Arial', 10))
antonyms_label.config(font=('Arial', 10))
# PAGE 2
# Thêm label và combobox để chọn chủ đề
theme_label = ttk.Label(page2, text="Chọn chủ đề:")
theme_label.pack(pady=5)
theme_combobox = ttk.Combobox(page2, values=themes_list, state="readonly")
theme_combobox.pack(pady=5)
# Kết nối sự kiện thay đổi chủ đề
theme_combobox.bind('<<ComboboxSelected>>', lambda e: update_themes())
# Giao diện cho nút thêm và xóa chủ đề
add_theme_button = ttk.Button(page2, text="Thêm chủ đề", command=add_theme)
add_theme_button.pack(pady=5)

delete_theme_button = ttk.Button(page2, text="Xóa chủ đề", command=delete_theme)
delete_theme_button.pack(pady=5)
themes_listboxs = tk.Listbox(page2, height=15, width=50)  # Danh sách từ yêu thích
themes_listboxs.pack(pady=10)
# Nút để xóa từ yêu thích
delete_button = ttk.Button(page2, text="Xóa từ khỏi chủ đề", command=delete_word_in_theme)
delete_button.pack(pady=10)

# Kết nối sự kiện chọn từ trong danh sách yêu thích
themes_listboxs.bind('<Double-Button-1>', show_word_selected_theme)
# Thêm label để hiển thị kết quả kiểm tra
result_check_label = ttk.Label(page3, text="", wraplength=500, justify="left")
result_check_label.pack(pady=10)

vocab_label = ttk.Label(page3, text="Chọn phương thức ôn tập:")
vocab_label.pack(pady=10)
review_type_combobox = ttk.Combobox(page3, values=["Theo nghĩa", "Theo phát âm"], state="readonly")
review_type_combobox.set("Theo nghĩ`a")  # Giá trị mặc định
review_type_combobox.pack(pady=5)
start_button = ttk.Button(page3, text="Bắt đầu ôn tập", command=start_vocabulary_review)
start_button.pack(pady=10)
meaning_label = ttk.Label(page3, text="", wraplength=500, justify="left")
meaning_label.pack(pady=5)
phonetic_check_label = ttk.Label(page3, text="", wraplength=500, justify="left")
phonetic_check_label.pack(pady=5)
answer_label =ttk.Label(page3, text="Nhập từ tiếng Anh:")
answer_label.pack_forget() 
answer_entry = ttk.Entry(page3, width=25)
answer_entry.pack_forget() 
check_button = ttk.Button(page3, text="Kiểm tra", command=check_answer)
check_button.pack_forget()
# Thêm nút Tiếp tục
continue_button = ttk.Button(page3, text="Tiếp tục",command=continue_review)
continue_button.pack_forget()  # Ẩn nút ban đầu

# Bắt đầu vòng lặp chính của ứng dụng
root.mainloop()