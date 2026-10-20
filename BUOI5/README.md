- **MSSV:** 2387700044
- **Họ và tên:** Dương Thanh Mộng
- **Lớp:** 23DATA1
- **Bài:** Bài 5: Phân tích và kiểm thử bảo mật

---

# BUOI5 - Phân tích và kiểm thử bảo mật

Nguồn: `lab-05 (1).pdf`, 24 trang, Bài 5. Đã đọc toàn bộ phần chữ và đối chiếu trực quan các trang có ảnh mã nguồn. Cấu trúc theo các thư mục sẵn có trên repository: `lab1/<tên dự án>` và `lab2/<tên dự án>`.

```text
BUOI5/
├── .gitignore
├── README.md
├── lab1/
│   └── sast-tool/
│       ├── README.md
│       ├── images/
│       ├── examples/
│       ├── rules/
│       ├── sast_tool/
│       ├── tests/
│       ├── requirements.txt
│       ├── report.sarif
│       ├── report_01.sarif
│       ├── report_02.sarif
│       └── verification.txt
└── lab2/
    └── dast-tool/
        ├── README.md
        ├── images/
        ├── tests/
        ├── __init__.py
        ├── app.py
        ├── main.py
        ├── memory_analyzer.py
        ├── network_traffic_analyzer.py
        ├── runtime_monitor.py
        ├── security_behavior_checker.py
        ├── virtual_sandbox.py
        ├── requirements.txt
        └── verification.txt
```

## Bắt đầu trong VS Code

1. Nếu dùng ZIP, giải nén trước. Chọn **File → Open Folder... → BUOI5**.
2. Mở [hướng dẫn LAB01](lab1/sast-tool/README.md), nhấn Ctrl+Shift+V để xem.
3. Mở Terminal → New Terminal, chọn PowerShell; làm tuần tự bước tạo `.venv`, cài thư viện, chạy test, chạy chương trình trong README của từng LAB.
4. Làm xong LAB01 thì mở terminal mới từ BUOI5 và chuyển sang [hướng dẫn LAB02](lab2/dast-tool/README.md). Mỗi LAB dùng môi trường riêng `.venv`.
5. Ảnh thực hành người dùng đã được lưu và chèn vào README từng LAB. LAB01 đủ ảnh unit test, chạy hai ví dụ và xem hai báo cáo SARIF. LAB02 đủ ảnh cài thư viện, 5 unit test đạt, hai phần kết quả main.py, Flask chạy trực tiếp app.py theo PDF và phản hồi của cả 5 API. Sau khi kết thúc thực hành, chọn terminal chạy Flask và nhấn Ctrl+C để dừng server.

## Đối chiếu file với PDF

| Trang | File/nội dung đã chép |
|---|---|
| 1-3 | Lý thuyết AST, pattern matching, chất lượng mã; làm bối cảnh, không phải LAB riêng |
| 4 | Yêu cầu SAST, cấu trúc và requirements LAB01 |
| 5 | examples/vulnerable_01.py |
| 6 | examples/vulnerable_02.py, rules/default_rules.json, sast_tool/__init__.py, ast_analyzer.py |
| 7-8 | code_quality_checker.py, sarif_reporter.py, security_rule_engine.py, phần đầu vuln_pattern_matcher.py |
| 9 | phần còn lại vuln_pattern_matcher.py, sast_tool/main.py, tests/__init__.py |
| 10-12 | 5 file unit test SAST (6 test case) và hướng dẫn chạy/xem báo cáo |
| 13 | Kết quả minh họa và thao tác Git trong tài liệu; không tự commit/push |
| 14-16 | Lý thuyết DAST và yêu cầu bài thực hành |
| 17 | requirements LAB02, memory_analyzer.py, network_traffic_analyzer.py |
| 18 | runtime_monitor.py, security_behavior_checker.py |
| 19 | virtual_sandbox.py, main.py |
| 20-21 | app.py, test_memory_analyzer.py, test_network_traffic_analyzer.py, đầu test_runtime_monitor.py |
| 22 | phần còn lại test_runtime_monitor.py, test_security_behavior_checker.py, test_virtual_sandbox.py |
| 23 | Lệnh chạy main, Flask và hướng dẫn Git trong PDF |
| 24 | Trang trống |

## Đối chiếu ảnh thực hành với giáo trình

Đã xem lại ảnh thực hành đã lưu và các trang tương ứng trong giáo trình ngày 20/10/2026. Kết luận: **ảnh chạy của cả hai LAB khớp kết quả mẫu và hành vi của mã thực hành trong giáo trình**.

| Nội dung đối chiếu | Giáo trình | Ảnh thực hành | Kết luận |
|---|---|---|---|
| LAB01 unit test | Trang 12: 6 test, OK | 6 test, OK | Khớp |
| LAB01 vulnerable_01.py | Trang 12: 8 issues | 8 issues | Khớp |
| LAB01 vulnerable_02.py | Trang 13: 4 issues | 4 issues | Khớp |
| LAB01 SARIF Viewer | Trang 13: 8 kết quả, nhóm No Location | Báo cáo 01 có 8 kết quả, cùng nhóm No Location; báo cáo 02 có 4 kết quả tương ứng lần chạy thứ hai | Khớp |
| LAB02 unit test | Trang 22: 5 test, OK | 5 test, OK | Khớp |
| LAB02 main.py | Trang 19, 23: các nhóm thông tin tiến trình, bộ nhớ, mạng, chuỗi lời gọi và sandbox | Đủ các nhóm; Memory Leaks rỗng, Overflow Test True, đủ ba chuỗi, stdout Hello Sandbox và stderr rỗng | Khớp |
| LAB02 Flask | Trang 21, 23: chạy app.py, host 0.0.0.0, cổng 5000 | Chạy trực tiếp app.py, có all addresses, loopback và địa chỉ LAN | Khớp |
| LAB02 bốn API GET | Trang 20: monitor, memory, network, security | Có phản hồi JSON và các trường tương ứng cho cả bốn API | Khớp |
| LAB02 API sandbox | Trang 21: POST nhận command, trả stdout và stderr | POST echo Hello Sandbox, stdout đúng và stderr rỗng | Khớp |

PID, thời gian chạy test, CPU, RAM, file đang mở, địa chỉ IP, tên card và bộ đếm mạng phụ thuộc máy/thời điểm nên không cần bằng từng con số trong ảnh mẫu. Cảnh báo development server của Flask cũng có trong giáo trình; DeprecationWarning của jsonpickle trong ảnh LAB01 không làm test thất bại. Phần Git được thực hiện khi bàn giao BUOI5 lên repository; bảng đối chiếu này tập trung vào ảnh chạy chương trình.

## Nguyên tắc giữ mã nguồn

Giữ tên file, module, class, hàm, test, endpoint, chuỗi mẫu và logic trong ảnh code của PDF. Chỉ đổi thư mục bao ngoài `sast-tool` thành `LAB01`, `dast-tool` thành `LAB02` để khớp cấu trúc yêu cầu. Phục hồi thụt dòng/xuống dòng từ ảnh và thêm newline cuối file; không thêm chức năng hoặc sửa các hạn chế logic của bài. Mã Python là mã thông dịch: đã kiểm tra cú pháp/biên dịch bytecode và chạy thực tế, không tạo file exe.

Các file bổ sung phục vụ bàn giao: README, thư mục image với `.gitkeep`, `.gitignore`, log verification và hai báo cáo SAST sinh khi chạy thử. Kịch bản kiểm chứng và môi trường agent nằm ngoài BUOI5, không đưa vào ZIP.

## Kết quả đã chạy thật ngày 20/10/2026

| Hạng mục | Kết quả |
|---|---|
| Cú pháp toàn bộ file Python | Đạt |
| LAB01 unit test nguyên bản | 6/6 đạt |
| SAST vulnerable_01.py | Thành công, 8 issues |
| SAST vulnerable_02.py | Thành công, 4 issues |
| Báo cáo SAST | Đã sinh và đọc lại JSON của cả hai báo cáo |
| LAB02 unit test nguyên bản | 5/5 đạt |
| LAB02 main.py | Chạy thành công, stdout sandbox đúng |
| GET /api/monitor | HTTP 200 |
| GET /api/memory | HTTP 200, overflow_test=true |
| GET /api/network | HTTP 200 |
| GET /api/security | HTTP 200 |
| POST /api/sandbox | HTTP 200, echo Hello Sandbox đúng, stderr rỗng |
| Ảnh chụp VS Code | Cả hai LAB đã đủ ảnh thực hành người dùng. LAB02 có đủ phản hồi monitor, memory, network, security và sandbox; ảnh đã chèn trong README từng LAB |
| SARIF Viewer trong VS Code | Ảnh người dùng xác nhận báo cáo 01 có 8 kết quả, báo cáo 02 có 4 kết quả; cùng hiển thị trong nhóm No Location |
| Git commit/push | Xem lịch sử commit của thư mục BUOI5 trên repository để kiểm tra bản bàn giao |

Xem log gốc: [lab1/sast-tool/verification.txt](lab1/sast-tool/verification.txt), [lab2/dast-tool/verification.txt](lab2/dast-tool/verification.txt). Không coi test đạt là bằng chứng mọi khả năng lý thuyết đều có trong mã mẫu. Các giới hạn cụ thể đã ghi trong README từng LAB.

## Môi trường kiểm chứng

Windows, Python 3.11; flake8 7.4.1, sarif-om 1.0.4, jsonpickle 4.1.4, psutil 7.2.2, Flask 3.1.3. Requirements giữ theo PDF, không khóa phiên bản. Có DeprecationWarning của jsonpickle về thay đổi mặc định trong tương lai, không có test thất bại.

API sandbox thực thi shell và không có cơ chế cách ly thật; README hướng dẫn chạy trực tiếp app.py theo giáo trình và có lựa chọn Flask CLI trên loopback. File app.py vẫn giữ `0.0.0.0:5000` đúng bản gốc. Dịch vụ kiểm chứng của agent đã được dừng sau khi thử.
