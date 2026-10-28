**MSSV:** 2387700044
**Họ và tên:** Dương Thanh Mộng
**Lớp:** 23DATA1
**Bài:** Bài 6: Bảo mật với DevSecOps

---

# BUOI6 - Bảo mật với DevSecOps

BUOI6 được xây dựng theo `lab-06 (1).pdf`, gồm phần lý thuyết DevSecOps và hai cấu hình thực hành CI/CD với GitLab:

```text
BUOI6/
├── README.md
├── lab1/
│   └── basic-pipeline/
│   ├── .gitlab-ci.yml              # pipeline 4 job theo mục 6.2.1
│   ├── images/                     # ảnh thực hành pipeline cơ bản
│   └── README.md
└── lab2/
    └── docusaurus-pipeline/
    ├── .gitlab-ci.yml              # build artifact và GitLab Pages
    ├── images/                     # ảnh thực hành Docusaurus/Pages
    ├── package.json
    ├── docusaurus.config.js
    ├── sidebars.js
    ├── docs/
    ├── src/
    ├── static/
    └── README.md
```

## Đối chiếu với giáo trình

| Phần | Nội dung đã chuẩn bị | Trang PDF |
|---|---|---|
| DevSecOps | Security gates, secrets, runner, audit và IaC | 1-4 |
| Pipeline cơ bản | `build-job`, `test-job1`, `test-job2`, `deploy-prod` | 5-9 |
| Pipeline Docusaurus | `test-job`, `build-job`, artifacts và `pages` | 10-15 |
| Kết quả cần chụp | Pipeline graph, job log, artifact và GitLab Pages | 8-15 |

## Cách làm thực hành

1. Đọc [hướng dẫn pipeline cơ bản](lab1/basic-pipeline/README.md).
2. Tạo một project GitLab riêng cho pipeline cơ bản, upload `.gitlab-ci.yml`, commit và mở **Build → Pipelines**.
3. Chụp ảnh pipeline graph và log của từng job theo danh sách trong README; lưu ảnh vào thư mục `images/` của đúng phần thực hành.
4. Sau khi pipeline cơ bản chạy đạt, làm [pipeline Docusaurus](lab2/docusaurus-pipeline/README.md).
5. Chụp ảnh build artifact, job `pages`, **Deploy → Pages** và URL website.

## Trạng thái kiểm chứng hiện tại

| Hạng mục | Trạng thái |
|---|---|
| YAML pipeline cơ bản | Đã kiểm tra cấu trúc, gồm 3 stage và 4 job |
| Demo pipeline cơ bản cục bộ | Đã chạy, cả 4 job `passed`, đã lưu ảnh trong `lab1/basic-pipeline/images/` |
| `npm install` Docusaurus | Đã hoàn tất cục bộ |
| `npm run build` Docusaurus | Đã thành công, tạo thư mục `build/` |
| Website Docusaurus local | Đã mở tại `localhost:3000` |
| Trang tài liệu `/docs/intro` | Đã mở và chụp đủ phần `build-job`, `pages`, `build/`, `public/` |
| GitLab hosted pipeline | Chưa chạy được vì tài khoản yêu cầu xác minh; ảnh lỗi đã lưu để làm bằng chứng |

## Ranh giới kiểm chứng

Các file YAML và dự án Docusaurus ở đây đã được chuẩn bị cục bộ. Trạng thái runner, pipeline, artifact và Pages chỉ được coi là đã chạy khi có ảnh hoặc log thật từ GitLab của bạn. Không đưa token, mật khẩu, access key hoặc secret vào repository và ảnh chụp.

## Ảnh thực hành

Các ảnh GitLab có giá trị được lưu trong thư mục `images/` của đúng phần thực hành và đối chiếu trong README:

**Project đã commit `.gitlab-ci.yml`:**

![Project basic pipeline đã commit ](lab1/basic-pipeline/images/01-basic-project-commit.png)

**Pipeline bị GitLab chặn vì tài khoản chưa xác minh:** đây là bằng chứng trạng thái môi trường, không phải kết luận YAML sai.

![GitLab yêu cầu xác minh tài khoản trước khi chạy pipeline ](lab1/basic-pipeline/images/02-pipeline-account-verification.png)

Sau mỗi ảnh hợp lệ tiếp theo, chèn vào README tương ứng bằng đường dẫn tương đối, ví dụ:

```markdown
![Pipeline cơ bản ](lab1/basic-pipeline/images/01-basic-pipeline-graph.png)
```
