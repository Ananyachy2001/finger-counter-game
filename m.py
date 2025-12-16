import cv2
import mediapipe as mp
import numpy as np
import pygame
import random
import time

class KidsHandGame:
    def __init__(self):
        # Initialize MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Initialize Pygame for sound
        pygame.mixer.init()
        
        # Game variables
        self.current_challenge = 0
        self.score = 0
        self.game_mode = "menu"  # menu, counting, matching, freestyle
        self.target_number = 0
        self.challenge_start_time = 0
        self.success_time = 0
        self.feedback_message = ""
        
        # Colors (BGR format)
        self.colors = {
            'blue': (255, 200, 100),
            'green': (100, 255, 100),
            'yellow': (100, 255, 255),
            'pink': (200, 150, 255),
            'orange': (100, 165, 255),
            'purple': (255, 100, 200),
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'red': (100, 100, 255)
        }
        
    def play_sound(self, frequency, duration=0.2):
        """Generate a simple beep sound"""
        try:
            sample_rate = 22050
            frames = int(duration * sample_rate)
            arr = np.sin(2 * np.pi * frequency * np.linspace(0, duration, frames))
            arr = (arr * 32767).astype(np.int16)
            stereo = np.column_stack((arr, arr))
            sound = pygame.sndarray.make_sound(stereo)
            sound.play()
        except:
            pass  # Silent fail if sound doesn't work
    
    def play_success_sound(self):
        """Play a cheerful success melody"""
        notes = [523, 659, 784, 1047]  # C, E, G, high C
        for note in notes:
            self.play_sound(note, 0.15)
            time.sleep(0.1)
    
    def play_number_sound(self, number):
        """Play ascending notes for the number"""
        base_freq = 400
        for i in range(number):
            self.play_sound(base_freq + i * 100, 0.2)
            time.sleep(0.1)
    
    def count_fingers(self, hand_landmarks):
        """Count extended fingers"""
        if hand_landmarks is None:
            return 0
        
        fingers = []
        
        # Thumb (check if tip is to the right/left of IP joint)
        if hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x:
            fingers.append(1)
        else:
            fingers.append(0)
        
        # Other fingers (check if tip is above PIP joint)
        finger_tips = [8, 12, 16, 20]
        finger_pips = [6, 10, 14, 18]
        
        for tip, pip in zip(finger_tips, finger_pips):
            if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
                fingers.append(1)
            else:
                fingers.append(0)
        
        return sum(fingers)
    
    def draw_cute_stars(self, frame, x, y, color):
        """Draw decorative stars"""
        star_points = 5
        outer_radius = 20
        inner_radius = 10
        
        for _ in range(3):
            angle = random.uniform(0, 360)
            offset_x = random.randint(-50, 50)
            offset_y = random.randint(-50, 50)
            
            points = []
            for i in range(star_points * 2):
                r = outer_radius if i % 2 == 0 else inner_radius
                curr_angle = angle + (i * 180 / star_points)
                px = int(x + offset_x + r * np.cos(np.radians(curr_angle)))
                py = int(y + offset_y + r * np.sin(np.radians(curr_angle)))
                points.append([px, py])
            
            cv2.fillPoly(frame, [np.array(points)], color)
    
    def draw_menu(self, frame):
        """Draw main menu"""
        h, w = frame.shape[:2]
        
        # Title
        cv2.rectangle(frame, (0, 0), (w, 150), self.colors['blue'], -1)
        cv2.putText(frame, "HAND COUNTING GAME!", (w//2 - 350, 80),
                   cv2.FONT_HERSHEY_SIMPLEX, 2, self.colors['white'], 4)
        cv2.putText(frame, "For Little Learners!", (w//2 - 220, 130),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, self.colors['yellow'], 2)
        
        # Menu options
        options = [
            ("Press 1: Counting Game", 220, self.colors['green']),
            ("Press 2: Matching Game", 300, self.colors['pink']),
            ("Press 3: Free Play", 380, self.colors['orange']),
            ("Press Q: Quit", 460, self.colors['red'])
        ]
        
        for text, y, color in options:
            cv2.rectangle(frame, (w//2 - 250, y - 40), (w//2 + 250, y + 10), color, -1)
            cv2.putText(frame, text, (w//2 - 230, y),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.2, self.colors['white'], 3)
        
        # Score
        cv2.putText(frame, f"Score: {self.score}", (20, h - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, self.colors['purple'], 2)
    
    def draw_counting_game(self, frame, finger_count):
        """Counting game mode"""
        h, w = frame.shape[:2]
        
        # Header
        cv2.rectangle(frame, (0, 0), (w, 100), self.colors['green'], -1)
        cv2.putText(frame, "COUNTING GAME", (w//2 - 220, 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.8, self.colors['white'], 3)
        
        # Challenge
        if self.target_number == 0:
            self.target_number = random.randint(1, 5)
            self.challenge_start_time = time.time()
            self.play_number_sound(self.target_number)
        
        # Draw target number with fun graphics
        number_y = 200
        cv2.rectangle(frame, (w//2 - 200, number_y - 50), (w//2 + 200, number_y + 100),
                     self.colors['yellow'], -1)
        cv2.rectangle(frame, (w//2 - 200, number_y - 50), (w//2 + 200, number_y + 100),
                     self.colors['orange'], 5)
        cv2.putText(frame, f"Show me {self.target_number} fingers!",
                   (w//2 - 180, number_y + 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.3, self.colors['purple'], 3)
        
        # Draw emoji hands
        for i in range(self.target_number):
            emoji_x = w//2 - 100 + i * 50
            cv2.putText(frame, "✋", (emoji_x, number_y + 80),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, self.colors['pink'], 2)
        
        # Current count
        count_y = h - 200
        cv2.rectangle(frame, (50, count_y - 50), (300, count_y + 50),
                     self.colors['blue'], -1)
        cv2.putText(frame, f"Your fingers: {finger_count}",
                   (60, count_y + 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, self.colors['white'], 2)
        
        # Check success
        if finger_count == self.target_number and time.time() - self.challenge_start_time > 0.5:
            if self.success_time == 0:
                self.success_time = time.time()
                self.score += 10
                self.play_success_sound()
            
            # Show success message
            if time.time() - self.success_time < 2:
                cv2.rectangle(frame, (w//2 - 200, h//2 - 100), (w//2 + 200, h//2 + 100),
                             self.colors['green'], -1)
                cv2.putText(frame, "GREAT JOB!", (w//2 - 150, h//2),
                           cv2.FONT_HERSHEY_SIMPLEX, 2, self.colors['yellow'], 4)
                cv2.putText(frame, "+10 points!", (w//2 - 100, h//2 + 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.2, self.colors['white'], 3)
                
                # Draw celebration stars
                self.draw_cute_stars(frame, w//2, h//2 - 150, self.colors['yellow'])
            else:
                self.target_number = 0
                self.success_time = 0
        
        # Instructions
        cv2.putText(frame, "Press M for Menu", (w - 300, h - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.colors['white'], 2)
    
    def draw_matching_game(self, frame, finger_count):
        """Matching game with patterns"""
        h, w = frame.shape[:2]
        
        # Header
        cv2.rectangle(frame, (0, 0), (w, 100), self.colors['pink'], -1)
        cv2.putText(frame, "MATCHING GAME", (w//2 - 220, 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.8, self.colors['white'], 3)
        
        if self.target_number == 0:
            self.target_number = random.randint(1, 5)
            self.challenge_start_time = time.time()
        
        # Show pattern to match
        pattern_y = 200
        cv2.rectangle(frame, (w//2 - 250, pattern_y - 50), (w//2 + 250, pattern_y + 150),
                     self.colors['blue'], -1)
        cv2.putText(frame, "Match this pattern:", (w//2 - 180, pattern_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, self.colors['yellow'], 2)
        
        # Draw circles representing fingers
        for i in range(5):
            x = w//2 - 100 + i * 50
            color = self.colors['green'] if i < self.target_number else self.colors['white']
            cv2.circle(frame, (x, pattern_y + 80), 20, color, -1)
            cv2.circle(frame, (x, pattern_y + 80), 20, self.colors['black'], 2)
        
        # Your count
        cv2.putText(frame, f"Your count: {finger_count}", (w//2 - 100, h - 150),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, self.colors['purple'], 3)
        
        # Check match
        if finger_count == self.target_number and time.time() - self.challenge_start_time > 0.5:
            if self.success_time == 0:
                self.success_time = time.time()
                self.score += 15
                self.play_success_sound()
            
            if time.time() - self.success_time < 2:
                cv2.rectangle(frame, (w//2 - 200, h//2 - 80), (w//2 + 200, h//2 + 80),
                             self.colors['orange'], -1)
                cv2.putText(frame, "PERFECT!", (w//2 - 120, h//2 + 20),
                           cv2.FONT_HERSHEY_SIMPLEX, 2.5, self.colors['white'], 4)
                self.draw_cute_stars(frame, w//2, h//2 - 120, self.colors['pink'])
            else:
                self.target_number = 0
                self.success_time = 0
        
        cv2.putText(frame, "Press M for Menu", (w - 300, h - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.colors['white'], 2)
    
    def draw_freestyle(self, frame, finger_count):
        """Free play mode"""
        h, w = frame.shape[:2]
        
        # Header
        cv2.rectangle(frame, (0, 0), (w, 100), self.colors['purple'], -1)
        cv2.putText(frame, "FREE PLAY MODE", (w//2 - 220, 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.8, self.colors['yellow'], 3)
        
        # Large finger count display
        cv2.rectangle(frame, (w//2 - 150, h//2 - 100), (w//2 + 150, h//2 + 100),
                     self.colors['blue'], -1)
        cv2.rectangle(frame, (w//2 - 150, h//2 - 100), (w//2 + 150, h//2 + 100),
                     self.colors['yellow'], 8)
        cv2.putText(frame, str(finger_count), (w//2 - 50, h//2 + 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 6, self.colors['white'], 10)
        
        # Fun facts
        facts = [
            "Count with me!",
            "How many fingers?",
            "You're doing great!",
            "Keep practicing!",
            "Math is fun!"
        ]
        fact = facts[finger_count % len(facts)]
        cv2.putText(frame, fact, (w//2 - 150, h - 100),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.3, self.colors['green'], 3)
        
        cv2.putText(frame, "Press M for Menu", (w - 300, h - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.colors['white'], 2)
    
    def run(self):
        """Main game loop"""
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        print("🎮 Kids Hand Gesture Game Started!")
        print("📹 Camera opening...")
        
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                continue
            
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            
            # Process hand detection
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            
            finger_count = 0
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw hand landmarks with colorful style
                    self.mp_draw.draw_landmarks(
                        frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                        self.mp_draw.DrawingSpec(color=(255, 200, 100), thickness=3, circle_radius=5),
                        self.mp_draw.DrawingSpec(color=(100, 255, 100), thickness=3)
                    )
                    finger_count = self.count_fingers(hand_landmarks)
            
            # Draw based on game mode
            if self.game_mode == "menu":
                self.draw_menu(frame)
            elif self.game_mode == "counting":
                self.draw_counting_game(frame, finger_count)
            elif self.game_mode == "matching":
                self.draw_matching_game(frame, finger_count)
            elif self.game_mode == "freestyle":
                self.draw_freestyle(frame, finger_count)
            
            cv2.imshow('Kids Hand Gesture Learning Game', frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('1') and self.game_mode == "menu":
                self.game_mode = "counting"
                self.target_number = 0
            elif key == ord('2') and self.game_mode == "menu":
                self.game_mode = "matching"
                self.target_number = 0
            elif key == ord('3') and self.game_mode == "menu":
                self.game_mode = "freestyle"
            elif key == ord('m'):
                self.game_mode = "menu"
                self.target_number = 0
        
        cap.release()
        cv2.destroyAllWindows()
        print(f"🎯 Final Score: {self.score}")
        print("👋 Thanks for playing!")

if __name__ == "__main__":
    game = KidsHandGame()
    game.run()