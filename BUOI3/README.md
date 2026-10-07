# TH_LTANTT_DUONGTHANHMONG_2387700044

Bài thực hành Lập trình an toàn thông tin - Buổi 3
Sinh viên: DUONGTHANHMONG - MSSV: 2387700044

| Thư mục | Nội dung | Trạng thái |
|---|---|---|
| [LAB01](LAB01/README.md) | SecureChat: TLS/mTLS, AES-CBC, chat nhiều client và phòng chat | Đã thực hành; 5 ảnh thật và bộ 16 kiểm tra |
| [LAB02](LAB02/README.md) | NetRecon: quét cổng, dịch vụ, banner, CLI/web/email | Đã thực hành CLI, web và nhận email; có 10 ảnh gốc, 8 ảnh nhúng trong gallery |

- [Hướng dẫn chạy và kết quả LAB02](LAB02/README.md)
- [Ảnh thực hành LAB01](LAB01/image/README.md)
- [Thư mục ảnh LAB02](LAB02/image/README.md)

## Chạy LAB02

Mã nguồn thực tế nằm trong LAB02/netrecon:

~~~powershell
cd "C:\Users\LOQ\OneDrive\Desktop\BUOI 3\BUOI3\LAB02\netrecon"
python -m pip install -r requirements.txt
python cli.py --help
python app.py
~~~

Mở http://localhost:5000/ để dùng giao diện web.
Xem [README LAB02](LAB02/README.md) để cấu hình email, chạy các chế độ CLI và đối chiếu kết quả.
Gallery không nhúng hai ảnh tài khoản/cấu hình chưa che thông tin nhạy cảm.
Mật khẩu ứng dụng đã hiển thị trong ảnh cần được thu hồi và thay mới.

## Chạy LAB01

Trong terminal tại LAB01, cài thư viện nếu máy chưa có:

~~~powershell
python -m pip install -r requirements.txt
~~~

Máy clone mới cần tự tạo bộ chứng chỉ bằng make-certs.bat sau khi cài OpenSSL.
Không chạy lại tạo chứng chỉ trên máy đã có bộ chứng chỉ đang sử dụng.

Mở ba terminal riêng tại LAB01:

~~~powershell
python server.py
~~~

~~~powershell
python client.py --username alice
~~~

~~~powershell
python client.py --username bob
~~~

Kiểm tra tự động:

~~~powershell
python -X utf8 test_secure_chat.py
~~~

## Lưu ý dữ liệu cục bộ

Repository chứa mã nguồn, hướng dẫn và ảnh thực hành.
certs/, khóa riêng, .env, cache và work/ được giữ tại máy và loại khỏi Git.
Mô hình SecureChat theo bài mẫu cho server giải mã rồi mã hóa lại tin nhắn;
không mô tả mô hình này là E2EE trước một server không đáng tin.
