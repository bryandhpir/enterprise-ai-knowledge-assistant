---
title: Quy trình đặt lại mật khẩu tài khoản công ty
category: Account & Identity
id: IT-KB-001
audience: Nhân viên, IT Helpdesk
tags: [password, mat-khau, reset, sso, mfa, tai-khoan]
version: '1.0'
status: Tài liệu mẫu cho dự án AI Knowledge Assistant
---

# Quy trình đặt lại mật khẩu

## 1. Mục đích và phạm vi
Hướng dẫn nhân viên đặt lại mật khẩu khi quên mật khẩu, tài khoản bị khóa hoặc nghi ngờ thông tin đăng nhập đã bị lộ. Áp dụng cho tài khoản doanh nghiệp do bộ phận IT quản lý (ví dụ: tài khoản đăng nhập máy tính, email hoặc SSO). Tên cổng, phương thức xác thực và quyền truy cập thực tế tùy thuộc doanh nghiệp.

## 2. Trước khi bắt đầu
- Có mã nhân viên hoặc tên đăng nhập doanh nghiệp.
- Có quyền truy cập phương thức xác thực đã đăng ký (ứng dụng MFA, khóa bảo mật hoặc phương thức khác được doanh nghiệp cho phép).
- Sử dụng **cổng đặt lại mật khẩu chính thức** do IT công bố; không sử dụng đường dẫn nhận từ nguồn không xác minh.
- Không cung cấp mật khẩu, mã OTP, mã khôi phục hoặc mã MFA cho bất kỳ ai, kể cả người tự xưng là IT.

## 3. Quy trình tự đặt lại mật khẩu
1. Truy cập **[Cổng đặt lại mật khẩu chính thức của doanh nghiệp]** bằng đường dẫn đã được công bố trong hệ thống nội bộ.
2. Chọn **Quên mật khẩu / Forgot password**.
3. Nhập tài khoản hoặc địa chỉ email công ty theo hướng dẫn trên màn hình.
4. Hoàn tất xác minh danh tính bằng phương thức đã đăng ký. **Không chia sẻ mã xác minh với người khác.**
5. Thiết lập mật khẩu mới theo chính sách hiện hành. Ưu tiên mật khẩu dài, duy nhất và được lưu trong trình quản lý mật khẩu đã được phê duyệt.
6. Đăng nhập lại vào dịch vụ cần sử dụng. Nếu doanh nghiệp có SSO, kiểm tra thêm email, VPN hoặc ứng dụng liên quan.
7. Nếu hệ thống yêu cầu, cập nhật thông tin đăng nhập đã lưu trên thiết bị và hoàn tất bước xác thực lại.

**Kết quả thành công:** Nhân viên đăng nhập được bằng mật khẩu mới; tài khoản không còn bị khóa và các dịch vụ cần thiết hoạt động bình thường.

## 4. Không tự đặt lại được thì làm gì?
1. Tạo yêu cầu qua **[Cổng IT Helpdesk nội bộ]** hoặc liên hệ kênh hỗ trợ đã được doanh nghiệp công bố.
2. Cung cấp mã nhân viên, bộ phận, thông báo lỗi, thời điểm gặp lỗi và tên dịch vụ bị ảnh hưởng. **Không gửi mật khẩu hay mã xác thực.**
3. IT kiểm tra danh tính theo quy trình chính thức của doanh nghiệp trước khi thay đổi hoặc khôi phục thông tin tài khoản.
4. IT hỗ trợ khôi phục qua công cụ quản trị được cấp quyền, ghi nhận mã ticket và thông báo cách đăng nhập lại.
5. Người dùng xác nhận truy cập thành công; IT đóng ticket sau khi kiểm tra.

## 5. Trường hợp đặc biệt
- **Không nhận được yêu cầu xác minh:** Kiểm tra thư rác, kết nối mạng và phương thức xác thực đã đăng ký; nếu vẫn lỗi, liên hệ IT.
- **Mất điện thoại hoặc thiết bị MFA:** Không tìm cách bỏ qua MFA. Liên hệ IT để xác minh danh tính và cấp lại phương thức MFA theo quy trình.
- **Tài khoản bị khóa:** Chờ theo thông báo hệ thống hoặc tạo ticket; không thử đăng nhập liên tục.
- **Nghi ngờ bị lộ mật khẩu / đăng nhập lạ:** Báo ngay IT/Security qua kênh chính thức. IT đánh giá việc khóa tài khoản, thu hồi phiên đăng nhập và kiểm tra dấu hiệu truy cập bất thường. Người dùng chỉ đổi mật khẩu tại thiết bị và trang đăng nhập đáng tin cậy.

## 6. Khi nào cần chuyển cấp xử lý?
Chuyển cho nhóm quản trị danh tính hoặc Security nếu: không xác minh được chủ tài khoản; nghi ngờ bị chiếm quyền; MFA mất và không có phương thức dự phòng hợp lệ; tài khoản quản trị bị ảnh hưởng; lỗi xảy ra hàng loạt.

## 7. Câu hỏi thường gặp
**Hỏi: IT có cần biết mật khẩu cũ của tôi không?**  
Đáp: Không. Không cung cấp mật khẩu cũ hoặc mới cho IT.

**Hỏi: Tôi vừa đổi mật khẩu nhưng email vẫn hỏi mật khẩu cũ?**  
Đáp: Đóng/mở lại ứng dụng và đăng nhập lại qua luồng chính thức. Nếu vẫn lỗi, tạo ticket kèm tên ứng dụng và thông báo lỗi.

**Hỏi: Có được dùng cùng một mật khẩu cho tài khoản cá nhân và công ty không?**  
Đáp: Không. Mật khẩu tài khoản công ty phải là duy nhất.

## 8. Tài liệu liên quan
- [Hướng dẫn kết nối VPN](vpn_access.md)
- [Xử lý lỗi email công ty](email_support.md)
- [Quy định bảo mật thông tin](security_policy.md)
