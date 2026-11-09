---
title: Quy trình cài đặt thiết bị cho nhân viên mới
category: Endpoint & Onboarding
id: IT-KB-004
audience: HR, Quản lý, IT Helpdesk, Nhân viên mới
tags: [onboarding, laptop, device, setup, mdm, endpoint]
version: '1.0'
status: Tài liệu mẫu cho dự án AI Knowledge Assistant
---

# Cài đặt thiết bị cho nhân viên mới

## 1. Mục tiêu
Bảo đảm nhân viên mới nhận được thiết bị hoạt động ổn định, có đúng quyền truy cập theo vị trí công việc và đáp ứng yêu cầu bảo mật trước ngày bắt đầu làm việc.

## 2. Thông tin cần có từ HR / quản lý
- Họ tên, mã nhân viên (nếu đã có), bộ phận và người quản lý trực tiếp.
- Ngày bắt đầu làm việc, địa điểm làm việc và hình thức làm việc (tại văn phòng/từ xa).
- Loại thiết bị, phụ kiện và ứng dụng cần sử dụng theo vai trò.
- Các quyền hệ thống được người có thẩm quyền phê duyệt.

**Không cấp quyền chỉ dựa trên yêu cầu miệng hoặc vì người khác trong nhóm đang có quyền đó.**

## 3. Quy trình dành cho IT
### Bước 1 — Tiếp nhận và phê duyệt
1. Nhận yêu cầu onboarding qua **[Cổng IT Helpdesk nội bộ]**.
2. Xác nhận thông tin với HR và người quản lý, kiểm tra phê duyệt thiết bị và quyền truy cập.
3. Lập danh sách đầu việc và người chịu trách nhiệm; ghi mã ticket.

### Bước 2 — Chuẩn bị phần cứng
1. Chọn thiết bị đã được doanh nghiệp phê duyệt, kiểm tra tình trạng vật lý và phụ kiện.
2. Ghi mã tài sản, số serial và người nhận vào hệ thống quản lý tài sản.
3. Kiểm tra kết nối mạng, camera, micro, bàn phím và nguồn/sạc.

### Bước 3 — Cài đặt hệ điều hành và bảo mật
1. Cài hoặc khôi phục ảnh hệ điều hành chuẩn của doanh nghiệp.
2. Cài bản cập nhật và trình điều khiển từ nguồn chính thức.
3. Đăng ký thiết bị vào giải pháp quản lý thiết bị (MDM/endpoint management) nếu doanh nghiệp sử dụng.
4. Bật mã hóa ổ đĩa, khóa màn hình, chống mã độc và firewall theo chính sách.
5. Cấu hình tài khoản người dùng với quyền tối thiểu cần thiết; không tự cấp quyền quản trị cục bộ.

### Bước 4 — Thiết lập tài khoản và phần mềm
1. Kích hoạt tài khoản doanh nghiệp/SSO theo quy trình quản lý danh tính.
2. Hướng dẫn nhân viên tự thiết lập mật khẩu và MFA qua kênh chính thức; IT **không cần biết mật khẩu**.
3. Cài các ứng dụng được duyệt: trình duyệt, bộ công cụ văn phòng, email, chat, ứng dụng chuyên môn.
4. Cài và kiểm tra VPN nếu vai trò công việc được cấp quyền truy cập từ xa.
5. Gán quyền ứng dụng và thư mục dùng chung theo phê duyệt của quản lý.

### Bước 5 — Kiểm thử trước khi bàn giao
- Đăng nhập được bằng tài khoản của nhân viên trên thiết bị được giao.
- Truy cập được email và các ứng dụng bắt buộc.
- MFA hoạt động; VPN hoạt động nếu có cấp quyền.
- Thiết bị mã hóa, cập nhật và hiển thị tuân thủ trong hệ thống quản lý (nếu có).
- Phần mềm bảo vệ đang hoạt động; không có cảnh báo chưa xử lý.

### Bước 6 — Bàn giao và hướng dẫn
1. Bàn giao thiết bị, phụ kiện, biên bản bàn giao và hướng dẫn liên hệ Helpdesk.
2. Giới thiệu quy định bảo mật, khóa màn hình, cách báo cáo phishing và sự cố thiết bị.
3. Nhân viên xác nhận nhận đúng tài sản và sử dụng được các công cụ bắt buộc.
4. IT cập nhật người sở hữu tài sản, trạng thái thiết bị, kết quả kiểm thử và đóng ticket.

## 4. Quy trình dành cho nhân viên mới (ngày đầu)
1. Kiểm tra tình trạng thiết bị và phụ kiện theo biên bản.
2. Đăng nhập bằng tài khoản được cấp qua kênh chính thức.
3. Thiết lập MFA và phương thức khôi phục theo hướng dẫn IT.
4. Thử mở email, ứng dụng làm việc và VPN nếu được cấp.
5. Đọc [quy định bảo mật thông tin](security_policy.md); báo ngay các lỗi hoặc quyền truy cập thiếu.

## 5. Trường hợp cần chuyển cấp
- Không có phê duyệt cấp quyền hoặc yêu cầu quyền cao bất thường: chuyển quản lý hệ thống/chủ dữ liệu.
- Không đạt kiểm tra mã hóa, bảo vệ thiết bị hoặc MDM: chuyển nhóm Endpoint/Security.
- Không có thiết bị đúng tiêu chuẩn: chuyển nhóm quản lý tài sản/mua sắm.
- Thiết bị có dấu hiệu bị can thiệp hoặc chứa dữ liệu của người dùng cũ: tạm dừng bàn giao, báo IT/Security.

## 6. Câu hỏi thường gặp
**Hỏi: Nhân viên mới có cần quyền admin trên máy không?**  
Đáp: Không mặc định. Chỉ cấp khi có nhu cầu công việc và được phê duyệt theo quy trình.

**Hỏi: Có thể cài phần mềm ngoài danh sách công ty không?**  
Đáp: Gửi yêu cầu IT đánh giá và phê duyệt trước khi cài.

## 7. Tài liệu liên quan
- [Hướng dẫn kết nối VPN](vpn_access.md)
- [Quy trình đặt lại mật khẩu](password_reset.md)
- [Quy định bảo mật thông tin](security_policy.md)
