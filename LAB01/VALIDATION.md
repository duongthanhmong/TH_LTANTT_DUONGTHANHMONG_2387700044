# Kiểm tra LAB01 sau khi sắp xếp thư mục

Ngày kiểm tra: 07/10/2026.
Vị trí: Desktop/BUOI 3/LAB01.
Lệnh: python -X utf8 test_secure_chat.py.
Kết quả thực tế: Ran 16 tests in 3.188s - OK.
Server kiểm tra dùng cổng riêng 53070 và đã dừng sau khi kiểm tra.

Đã xác nhận hai tiến trình client.py thật chat Alice -> Bob và Bob -> Alice,
sau đó cả hai thoát với mã 0. Bộ kiểm tra cũng xác nhận tin Unicode dài,
gửi đồng thời, phân tách khung, tách phòng, tên trùng, cleanup, TLS 1.2,
và từ chối thiếu cert/CA không tin cậy/hostname sai.

Thư mục image có 5 ảnh do sinh viên cung cấp, được xem trực tiếp:
echo client, chứng chỉ phía server, Alice, server hai client và Bob.
Tên file và mô tả được liệt kê trong image/README.md.

Trước các cập nhật tài liệu, toàn bộ 47 file sao chép từ secure-chat sang LAB01
đã được đối chiếu SHA-256 và đều khớp, bao gồm chứng chỉ và ảnh.
Khóa/chứng chỉ, cache và bản sao trong work chỉ giữ cục bộ, không đưa vào commit.

Phạm vi: bằng chứng chạy localhost trên Windows. Không tuyên bố E2EE
trước server không đáng tin, danh tính PKI riêng cho từng username,
hoặc hoàn tất NetRecon (LAB02 mới là cấu trúc chuẩn bị).
