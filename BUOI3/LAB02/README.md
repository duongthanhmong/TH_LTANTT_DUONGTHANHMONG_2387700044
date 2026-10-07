# LAB02 - NetRecon

Trạng thái: đã chuẩn bị thư mục, chưa triển khai hoặc chạy bài NetRecon.

Đối chiếu mục 3.4 của lab-03.pdf, trang PDF 15-29.
LAB02 là tên thư mục theo yêu cầu bài nộp; tương ứng thư mục netrecon trong giáo trình.

## Cấu trúc đã tạo

- modules/: các module Python, có __init__.py.
- static/: CSS và tài nguyên giao diện.
- templates/: giao diện Flask.
- image/: lưu ảnh thực hành.
- requirements.txt: Flask, Click, python-dotenv.
- .env.example: tên biến cấu hình email, chưa có thông tin tài khoản.

## Các file sẽ làm ở bước tiếp theo

- modules/banner_grabber.py
- modules/email_sender.py
- modules/filter_utils.py
- modules/network_mapper.py
- modules/port_scanner.py
- modules/service_detector.py
- modules/vuln_checker.py
- cli.py
- app.py
- templates/index.html, layout.html, result.html
- static/style.css

Chưa tạo cli.py hoặc app.py rỗng để tránh hiểu nhầm là chương trình đã chạy được.
Chưa cài Nmap, chưa cài các thư viện, chưa cấu hình SMTP và chưa gửi email trong bước chuẩn bị này.
Lệnh kiểm tra hiện tại không tìm thấy nmap trong PATH; điều này chưa đủ kết luận máy chưa cài Nmap.

## Bước bắt đầu

1. Kiểm tra Nmap bằng nmap --version; nếu không có, kiểm tra đường dẫn cài đặt.
2. Chuẩn bị môi trường Python và cài requirements.txt khi bắt đầu triển khai.
3. Viết và kiểm tra từng module trước khi chạy CLI/web.
4. Dùng 127.0.0.1 hoặc máy lab được cấp phép làm mục tiêu thử nghiệm.
5. Điền .env tại máy khi đến bước email; không đưa giá trị SMTP_PASS vào ảnh/Git.
6. Chụp bằng chứng theo ../HUONG_DAN_CHUP_ANH.md.

Ảnh kết quả sẽ được lưu tại image/.
