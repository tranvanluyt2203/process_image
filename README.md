<h1>Các file</h1>
<br>
Repair_trainmodel.ipynb : để lấy kết quả tạm có gì sửa sau
<br>
train_model.ipynb : Xây dựng mô hình, chọn các tham số
<br>
Repair_trainmodel_test_update.ipynb : đang chạy có gì chạy xong update lên, chỉ lần phần Data augmentation
<hr>
<h1>Hướng dẫn chạy Source</h1>
<hr>
<h2>Tải file data</h2>
<b>Link data : </b><a href="https://drive.google.com/drive/folders/1B6L0nlIfTmzdR5Xw529FqAAphzjWdJ0x?usp=sharing">https://drive.google.com/drive/folders/1B6L0nlIfTmzdR5Xw529FqAAphzjWdJ0x?usp=sharing<a>
<br>
Giải nén file và lưu vào thư mục Data (đường dẫn là : Data/A_Z Handwritten Data.csv)
<h2>Tạo file model</h2>
Chạy file trainmodel.ipynb để tạo fille model
<br>
<h2>Chạy web dự đoán</h2>
<b>Chạy : </b>  py manage.py runserver 1234 (chạy ở thư mục PredictImage)
<br>
<b>Link local để chạy dự án: </b> <a href="http://127.0.0.1:1234/">http://127.0.0.1:1234/<a>
<p>Upload ảnh (chọn ảnh có trong thư mục Data/image_test) và click vào nút predict để hiển thị kết quả dự đoán chữ cái</p>
<hr>
