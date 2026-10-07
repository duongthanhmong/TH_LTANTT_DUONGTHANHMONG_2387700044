# Hướng dẫn chụp ảnh Buổi 3 theo lab-03.pdf

Đối chiếu bản lab-03.pdf gồm 29 trang. Số trang dưới đây là số trang PDF, tính từ 1.
Đây là danh sách đề xuất để bám các bước minh họa; ưu tiên yêu cầu riêng của giảng viên nếu có.
LAB01 tương ứng secure-chat; LAB02 tương ứng netrecon trong giáo trình.

## 1. Cách chụp và lưu

- Chụp kết quả trên máy của bạn bằng Win+Shift+S, không dùng ảnh trong PDF làm bằng chứng chạy thật.
- Lưu LAB01/image/ và LAB02/image/; đặt tên có số thứ tự như các bảng dưới.
- Giữ được tên file hoặc lệnh vừa chạy và phần kết quả quan trọng, chữ đọc rõ.
- Không cần giống IP hay số phiên bản trong PDF; ghi đúng kết quả trên máy.
- Với .env/App Password, chỉ chụp tên biến hoặc trạng thái đã tạo; che toàn bộ mật khẩu.
- Không chụp nội dung private key, token hoặc mật khẩu. Các ảnh sẵn có đã kiểm tra không thấy các giá trị này.
- Hình giải thích SSL/PKI đầu chương là sơ đồ lý thuyết, không phải kết quả máy cần tái hiện.
- Các ảnh code ở giữa bài nên chụp nếu báo cáo yêu cầu trình bày mã; không thay thế ảnh chương trình chạy.

Đường dẫn làm việc hiện tại:
C:\Users\LOQ\OneDrive\Desktop\BUOI 3\BUOI3

## 2. LAB01 - ảnh kết quả thực hành

| Mã/tên gợi ý | Trang PDF | Chụp bước nào | Cần thấy rõ | Hiện trạng |
|---|---:|---|---|---|
| 01_openssl_download.png | 4 | Trang tải OpenSSL cho Windows | Bộ cài phù hợp Windows | Chưa có trong 5 ảnh đã cung cấp; chụp nếu cần mô tả cài đặt |
| 02_openssl_path.png | 4 | Cấu hình PATH | Đường dẫn thư mục bin của OpenSSL | Chưa có |
| 03_openssl_version.png | 4 | Kiểm tra OpenSSL trong terminal | Lệnh và số phiên bản, không có command not found | Chưa có |
| 04_tao_chung_chi.png | 7 | Kết quả chạy make-certs.bat | Tạo CA/server/client thành công | Chưa có; xem cách làm trong thư mục demo ở dưới |
| 05_cau_truc_certs.png | 7 | Mở cây certs trong VS Code | ca, server, client và tên .crt/.key; không mở nội dung .key | Chưa có |
| 06_verify_chung_chi.png | Bổ sung cho bước trang 7 | Xác minh chứng chỉ | server.crt: OK và client.crt: OK | Chưa có |
| 07_server_mtls.png | 13-14 | Chạy server và kết nối client | ssl.SSLContext, TLSv1.3 hoặc 1.2, Client certificate received | Đã có ảnh gốc số 2 và 4 |
| 08_client_echo.png | Bước kiểm tra bổ sung | Client nhận echo | Server received: Xin chao tu SecureChat Client | Đã có ảnh gốc số 1 |
| 09_alice.png | 14 | Alice gửi tin và nhận trả lời | Username alice, tin gửi, dòng [bob] nhận được | Đã có ảnh gốc số 3 |
| 10_bob.png | 14 | Bob nhận tin và trả lời | Username bob, dòng [alice], tin trả lời | Đã có ảnh gốc số 5 |
| 11_server_hai_client.png | 14 | Log server khi chat hai chiều | alice/bob vào general, hai dòng tin | Đã có ảnh gốc số 4 |
| 12_test_tu_dong.png | Bổ sung | Chạy test_secure_chat.py | Ran 16 tests và OK | Đã chạy kiểm tra; chưa có ảnh chụp terminal |
| 13_git_push.png | 14 | Kiểm tra commit sau khi push | git log -1, git status -sb, nhánh main theo dõi origin/main | Chụp sau khi push |
| 14_github.png | 14 | Mở repository trên GitHub | LAB01, LAB02, commit mới và thư mục ảnh | Chụp sau khi push |

Năm ảnh gốc giữ nguyên tên. Xem LAB01/image/README.md để xem từng ảnh kèm mô tả.
Trong ảnh cũ, editor đang hiển thị nội dung server chưa lưu của bản echo, nhưng terminal chạy bản chat mới.
Nếu chụp ảnh code, hãy mở lại file trên đĩa tại LAB01 để hình khớp với code đã nộp.

### Lệnh chụp nhanh LAB01

Trong terminal:

~~~powershell
cd "C:\Users\LOQ\OneDrive\Desktop\BUOI 3\BUOI3\LAB01"
& "C:\Program Files\OpenSSL-Win64\bin\openssl.exe" version
& "C:\Program Files\OpenSSL-Win64\bin\openssl.exe" verify -CAfile certs\ca\ca.crt -purpose sslserver certs\server\server.crt
& "C:\Program Files\OpenSSL-Win64\bin\openssl.exe" verify -CAfile certs\ca\ca.crt -purpose sslclient certs\client\client.crt
python -X utf8 test_secure_chat.py
~~~

Chụp từng nhóm kết quả, không cần gom tất cả vào một ảnh quá dài.

Nếu cần ảnh quá trình tạo chứng chỉ ở trang 7 mà chưa lưu kết quả cũ, tạo bộ demo riêng.
Không ghi đè bộ certs đang dùng của LAB01:

~~~powershell
cd "C:\Users\LOQ\OneDrive\Desktop\BUOI 3\BUOI3\LAB01"
New-Item -ItemType Directory -Path .\work\cert-demo -Force
Copy-Item .\openssl.cnf, .\make-certs.bat .\work\cert-demo\
$env:Path += ";C:\Program Files\OpenSSL-Win64\bin"
Push-Location .\work\cert-demo
.\make-certs.bat
Pop-Location
~~~

Ảnh ghi rõ đây là bộ chứng chỉ demo. Thư mục work bị loại khỏi Git.

### Ảnh mã nguồn LAB01 nếu giảng viên yêu cầu

| Trang PDF | File/đoạn cần chụp |
|---|---|
| 5 | openssl.cnf: req, v3_ca và các extension serverAuth/clientAuth đã sửa |
| 5-7 | make-certs.bat: tạo CA, ký cert server/client, verify |
| 8 | message_encryption.py: encrypt/decrypt |
| 8-9 | connection_manager.py: thêm/xóa client và gửi tin |
| 9-10 | room_manager.py: tạo/vào/rời phòng |
| 10-12 | server.py: cấu hình TLS, nhận chứng chỉ, đăng ký và chuyển tiếp tin |
| 12-13 | client.py: CA/hostname, load_cert_chain, nhập tên, gửi/nhận |

Nếu file dài, chụp 2-3 ảnh liên tiếp có số dòng; không thu nhỏ đến mức không đọc được.
Có thể thêm ảnh tls_runtime.py để giải thích bản sửa môi trường Windows.

## 3. LAB02 - chuẩn bị và kết quả cần chụp sau khi triển khai

LAB02 hiện chỉ có cấu trúc chuẩn bị, chưa có chương trình CLI/web chạy được.
Những lệnh cli.py/app.py dưới đây là mốc sẽ dùng sau khi viết xong các file tương ứng.

| Mã/tên gợi ý | Trang PDF | Chụp bước nào | Cần thấy rõ |
|---|---:|---|---|
| 01_nmap_download.png | 16 | Trang tải Nmap Windows hoặc cửa sổ cài đặt | Bộ cài Windows |
| 02_nmap_version.png | 16 | nmap --version | Phiên bản; không có lỗi không tìm thấy lệnh |
| 03_app_password_da_che.png | 16-17 | Trạng thái tạo App Password | Tên ứng dụng và trạng thái đã tạo; KHÔNG chụp mật khẩu |
| 04_cau_truc.png | 17 | Explorer của LAB02 | modules, static, templates, cli.py, app.py, requirements.txt sau khi viết |
| 05_cai_goi.png | 17 | python -m pip install -r requirements.txt | Hoàn tất cài đặt hoặc already satisfied |
| 06_env_da_che.png | 17 | Cấu hình môi trường | SMTP_USER/SMTP_PASS có tên biến; giá trị bí mật che kín, có thể chụp .env.example |
| 07_cli.png | 25-26 | Chạy CLI với mục tiêu lab | Lệnh, địa chỉ mục tiêu, cổng/trạng thái và kết quả thật |
| 08_cli_scan.png | 26 | CLI ở mode scan | Các cổng được quét và trạng thái |
| 09_cli_all.png | 26 | CLI ở mode all | Kết quả scan/service/banner/map/vuln theo chức năng đã triển khai |
| 10_flask.png | 26 | Chạy app.py | Flask lắng nghe cổng 5000; chụp terminal |
| 11_web_form.png | 26-27 | Mở localhost:5000 và điền form | Target, Ports, Mode, Email, nút Scan |
| 12_web_result.png | 27 | Trang kết quả sau Scan | Service Detection, Banner Grabbing, Network Map, các phần còn lại nếu có |
| 13_email.png | 27-28 | Email báo kết quả thực tế | Tiêu đề, thời gian và nội dung phù hợp lần quét; có thể che địa chỉ email cá nhân |
| 14_git_push.png | 29 | Commit/push LAB02 sau khi làm xong | Commit mới, đồng bộ với origin/main |
| 15_github_lab02.png | 29 | Repository sau push LAB02 | Mã nguồn và ảnh của bài, không có .env |

Lưu kết quả thật, kể cả closed/filtered/timeout. Không ghi cổng open hoặc gửi email thành công nếu chưa quan sát được.
Dùng 127.0.0.1 hoặc IP máy lab đã được cho phép. Không lấy IP ví dụ trong sách làm mục tiêu mặc định.
Để có ảnh cổng mở dễ đối chiếu, có thể chạy dịch vụ HTTP thử nghiệm trên máy của mình:

~~~powershell
python -m http.server 8000 --bind 127.0.0.1
~~~

Sau khi CLI NetRecon đã triển khai, các mốc kiểm tra dự kiến:

~~~powershell
cd "C:\Users\LOQ\OneDrive\Desktop\BUOI 3\BUOI3\LAB02"
python cli.py --target 127.0.0.1 --ports 8000 --mode scan
python cli.py --target 127.0.0.1 --ports 8000 --mode all
python app.py
~~~

Đây là hướng dẫn cho bước tiếp theo, không phải kết quả đã chạy trong lần chuẩn bị này.
Bước email cần cấu hình tài khoản của bạn tại máy và gửi đến địa chỉ thử nghiệm bạn chọn.
Không sao chép tài khoản hoặc mật khẩu xuất hiện trong hình minh họa của giáo trình.

### Ảnh mã nguồn LAB02 nếu cần bám đủ các hình code

| Trang PDF | File/đoạn cần chụp sau khi viết |
|---|---|
| 17 | requirements.txt và cấu hình môi trường đã che |
| 17-18 | modules/banner_grabber.py |
| 18 | modules/email_sender.py |
| 19 | modules/filter_utils.py và modules/network_mapper.py |
| 19-20 | modules/port_scanner.py |
| 21 | modules/service_detector.py và modules/vuln_checker.py |
| 22 | templates/index.html và templates/layout.html |
| 22-23 | templates/result.html |
| 23 | static/style.css |
| 23-24 | cli.py |
| 24-25 | app.py |
| 25 | .gitignore có loại trừ .env và certs |

## 4. Chụp trạng thái Git sau khi push

~~~powershell
cd "C:\Users\LOQ\OneDrive\Desktop\BUOI 3\BUOI3"
git log -1 --oneline
git status -sb
git remote -v
~~~

Kết quả cần có commit vừa nộp, nhánh main đồng bộ origin/main và đúng repository:
https://github.com/duongthanhmong/TH_LTANTT_DUONGTHANHMONG_2387700044

Nếu muốn nộp cả ảnh chụp xác nhận push: chụp ảnh sau lần push đầu, lưu vào thư mục image,
sau đó commit/push thêm ảnh đó ở một commit tiếp theo.
