import cv2

class ConsoleView:
    @staticmethod
    def show_menu():
        print("\n1. Thu ảnh training")
        print("2. Train model")
        print("3. Nhận diện realtime")
        print("4. Đánh giá accuracy")  # ← Thêm dòng này
        print("0. Thoát")
    
    @staticmethod
    def get_menu_choice():
        return input("Chọn: ")
    
    @staticmethod
    def get_person_name():
        return input("Tên người (không dấu): ")
    
    @staticmethod
    def show_message(message):
        print(message)
    
    @staticmethod
    def show_error(error_message):
        print(f"✗ Lỗi: {error_message}")
    
    @staticmethod
    def show_success(success_message):
        print(f"✓ {success_message}")
    
    @staticmethod
    def show_info(info_message):
        print(f"ℹ {info_message}")

class VideoView:
    @staticmethod
    def show_frame(window_name, frame):
        cv2.imshow(window_name, frame)
    
    @staticmethod
    def draw_face_rectangle(frame, face_rect, color=(0, 255, 0), thickness=2):
        x, y, w, h = face_rect
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, thickness)
    
    @staticmethod
    def draw_text(frame, text, position, color=(0, 255, 0)):
        cv2.putText(
            frame, 
            text, 
            position, 
            cv2.FONT_HERSHEY_SIMPLEX, 
            0.8, 
            color, 
            2
        )
    
    @staticmethod
    def wait_key(delay=1):
        return cv2.waitKey(delay) & 0xFF
    
    @staticmethod
    def close_all_windows():
        cv2.destroyAllWindows()
