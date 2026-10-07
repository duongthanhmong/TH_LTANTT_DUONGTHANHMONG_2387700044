# Ảnh thực hành LAB01

Năm ảnh gốc do sinh viên cung cấp, đã xem trực tiếp; giữ nguyên tên và nội dung.
Ảnh có đường dẫn secure-chat vì được chụp trước khi chuyển bản làm việc sang LAB01.

## 1. Client kiểm tra echo qua TLS 1.3

Phần cuối ảnh có ssl.SSLContext chuẩn và chuỗi Server received. Phần đầu còn lịch sử lỗi cũ.

![Client kiểm tra echo qua TLS 1.3](1791337481055_2278494996850434872_151818230746414013_d8e66219a1b93109f4c5c3d2d0730424.jpg)

## 2. Server nhận chứng chỉ client

Có Client certificate received và thông tin CN=client, CA=MyRootCA.

![Server nhận chứng chỉ client](1791337498186_2278494996850434872_151818230746414013_95aa07eec0483ff6a2259b2eccb055b6.jpg)

## 3. Alice nhận tin từ Bob

Alice gửi Xin chao Bob và nhận [bob]: Chao Alice, minh da nhan duoc.

![Alice nhận tin từ Bob](1791338818975_2278494996850434872_151818230746414013_8ce6687f8f15659c9692aaead5c41924.jpg)

## 4. Server ghi nhận hai client chat

Alice và Bob cùng vào general; server ghi nhận hai chiều nhắn tin.

![Server ghi nhận hai client chat](1791338856631_2278494996850434872_151818230746414013_706fa90cb53aae835e56512de17e189b.jpg)

## 5. Bob nhận tin từ Alice

Bob nhận [alice]: Xin chao Bob rồi gửi câu trả lời.

![Bob nhận tin từ Alice](1791338870886_2278494996850434872_151818230746414013_58b7048a1ebf1d5fb55f68c7dabfb2ec.jpg)
