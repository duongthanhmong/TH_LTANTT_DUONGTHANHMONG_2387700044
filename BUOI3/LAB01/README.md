# SecureChat - tiếp tục Lab 03 sau bước kiểm tra TLS

## Bước tiếp theo trong giáo trình

Trang PDF 14 của lab-03.pdf yêu cầu chạy thêm một client để kiểm tra chat.
Sau bước này giáo trình mới chuyển sang commit/push GitHub và phần NetRecon.
Project đã được chuyển từ echo một lần sang chat tương tác nhiều client.

## Chạy demo bằng ba terminal PowerShell

Nếu server cũ còn chạy, nhấn Ctrl+C trong terminal đó trước.
Nạp lại các file đã thay đổi trên đĩa trong VS Code nếu tab đang giữ bản chưa lưu;
đừng ghi đè bản mới bằng nội dung cũ trong tab.

Trong mỗi terminal, vào thư mục:

~~~powershell
cd "C:\Users\LOQ\OneDrive\Desktop\BUOI 3\BUOI3\LAB01"
~~~

Terminal 1:

~~~powershell
python server.py
~~~

Chờ dòng [+] Listening on 127.0.0.1:8443.

Terminal 2:

~~~powershell
python client.py
~~~

Nhập alice khi được hỏi Username:. Giữ terminal mở.

Terminal 3:

~~~powershell
python client.py
~~~

Nhập bob khi được hỏi Username:. Giữ terminal mở.

Sau khi cả hai đã kết nối, trong terminal Alice nhập:

~~~text
Xin chao Bob
~~~

Terminal Bob phải hiện:

~~~text
[alice]: Xin chao Bob
~~~

Trong terminal Bob nhập:

~~~text
Chao Alice, minh da nhan duoc
~~~

Terminal Alice phải hiện:

~~~text
[bob]: Chao Alice, minh da nhan duoc
~~~

Server in ra tên phòng, người gửi và nội dung tương ứng.
Client không echo lại tin của chính mình; tin xuất hiện ở client còn lại.
Nếu phòng chỉ có một người, server sẽ thông báo cần mở client thứ hai.
Nhập exit hoặc /quit ở từng client để thoát. Nhấn Ctrl+C để dừng server.

Có thể bỏ qua câu hỏi Username bằng:

~~~powershell
python client.py --username alice
python client.py --username bob
~~~

Hai lệnh này chạy ở hai terminal riêng.

## Phòng chat

Mỗi client mặc định vào phòng general và chỉ ở một phòng tại một thời điểm.

- /users: liệt kê người trong phòng hiện tại.
- /rooms: liệt kê phòng cùng số người.
- /join hocnhom: tạo/vào phòng hocnhom, đồng thời rời phòng cũ.
- /help: xem lệnh.
- exit hoặc /quit: thoát.

Thử /join hocnhom chỉ ở Bob: tin nhắn từ Alice trong general không đến Bob.
Cho Alice cũng nhập /join hocnhom: hai người lại chat được.
Tên người dùng và phòng dùng 1-32 ký tự chữ không dấu, số, dấu chấm, gạch dưới hoặc gạch ngang.
Tin nhắn hỗ trợ Unicode và tối đa 16000 byte UTF-8.

## Kiểm tra lại echo và kiểm tra tự động

Với server bản mới đang chạy:

~~~powershell
python client.py --echo
~~~

Kết quả phải chứa:

~~~text
[<] Server: Server received: Xin chao tu SecureChat Client
~~~

Chạy bộ kiểm tra:

~~~powershell
python -X utf8 test_secure_chat.py
~~~

Bộ kiểm tra tự mở server trên cổng trống do Windows cấp, rồi dừng nó khi kết thúc.
Nó không dừng server demo trên cổng 8443.

Kết quả đã quan sát ngày 07/10/2026: 16 tests, OK; server kiểm tra dùng cổng 58096.
Các lần chạy sau thường dùng cổng khác.

Đã kiểm tra:
- Hai tiến trình client.py thật chat Alice -> Bob và Bob -> Alice, rồi exit bình thường.
- Chat hai chiều qua mTLS; TLS 1.2 vẫn hoạt động.
- Tin tiếng Việt dài hơn 4096 byte; 30 tin gửi liên tiếp.
- Hai người gửi đồng thời đến một người nhận, không trộn khung tin.
- Cách ly phòng, chuyển phòng và liệt kê thành viên.
- Từ chối tên người dùng trùng; xóa thành viên khi thoát.
- Echo trả đúng chuỗi cũ.
- Server từ chối thiếu chứng chỉ client.
- Client từ chối hostname sai và CA không tin cậy.
- Một kết nối chưa hoàn thành TLS không chặn các client khác.
- Đọc đúng khung bị chia nhỏ/gộp; từ chối khung quá lớn hoặc bị cắt dở.

Log server của lần kiểm tra gần nhất nằm trong work/chat-integration-server.log.

## Các file và sự tương ứng với giáo trình

- server.py: server đa luồng, xác minh chứng chỉ client, đăng ký tên và khóa phiên,
  giải mã rồi mã hóa lại tin cho từng người nhận.
- client.py: xác minh CA/hostname, nhập tên, gửi/nhận liên tục, exit.
- message_encryption.py: giữ thuật toán AES-256-CBC + PKCS7 của bài mẫu.
- connection_manager.py: quản lý phiên, tên duy nhất, khóa ghi riêng cho từng client.
- room_manager.py: thành viên phòng và gửi tin đúng phòng.
- chat_protocol.py: thêm độ dài trước từng thông điệp, dùng sendall và đọc đủ dữ liệu.
- tls_runtime.py: giữ bản sửa monkey-patch pip/truststore.
- test_secure_chat.py: bộ kiểm tra bằng socket TLS và tiến trình thật.

Bản nguồn trước khi tích hợp được sao lưu tại:
work/before-textbook-chat-20261007-085913.

## Giới hạn cần trình bày đúng

- CA và hostname vẫn được xác minh; server vẫn dùng CERT_REQUIRED.
  Không dùng dòng check_hostname = False trong ảnh mã mẫu.
- TLS tối thiểu 1.2; không ép hạ từ TLS 1.3.
- Theo kiến trúc mã mẫu, client gửi khóa AES cho server bên trong kênh mTLS.
  Server đọc được tin để mã hóa lại cho từng người nhận. Đây KHÔNG phải E2EE
  giữa Alice và Bob trước một server không đáng tin.
- AES-CBC trong module mẫu không tự xác thực nội dung. Tính toàn vẹn trên đường
  truyền do TLS cung cấp; không dùng module này riêng cho dữ liệu ngoài kênh TLS.
- Hai client demo dùng cùng bộ chứng chỉ client hiện có. Username là tên hiển thị;
  alice và bob chưa phải hai danh tính PKI được cấp chứng chỉ riêng.
- Bản mới dùng khung thông điệp nên phải khởi động lại cả server và client.
  Server echo cũ đang chạy trong bộ nhớ sẽ không hiểu giao thức mới.

## Repository bài tập

Repository: https://github.com/duongthanhmong/TH_LTANTT_DUONGTHANHMONG_2387700044
LAB01 chứa SecureChat; LAB02 dành cho NetRecon.
Ảnh thực hành nằm trong image/. Xem image/README.md để đối chiếu nội dung từng ảnh.
Các chứng chỉ, private keys và work/ vẫn có ở máy nhưng không đưa lên GitHub.
Các ảnh cũ hiển thị đường dẫn secure-chat là ảnh gốc chụp trước khi sắp xếp thư mục.

## Chạy khi clone về máy mới

Cài Python, OpenSSL và thư viện bằng python -m pip install -r requirements.txt.
Chỉ khi máy mới chưa có bộ certs, chạy make-certs.bat từ LAB01 để tạo chứng chỉ cục bộ.
Không cần tạo lại chứng chỉ trên máy hiện tại; toàn bộ certs đã được sao chép nguyên vẹn.
Xem ../HUONG_DAN_CHUP_ANH.md để chụp đủ các bước của giáo trình.
