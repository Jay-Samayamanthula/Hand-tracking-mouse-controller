import cv2
import mediapipe as mp
import pyautogui
import math
import time

# ---------------- BASIC CONFIG ----------------
pyautogui.FAILSAFE = False
screen_w, screen_h = pyautogui.size()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=2,
    model_complexity=0,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# ---------- TUNING / SENSITIVITY ----------
CLICK_MAX_TIME = 0.18
DRAG_HOLD_TIME = 0.22

SCROLL_DELTA_THRESHOLD = 15
SCROLL_AMOUNT = 40

VOLUME_DELTA_THRESHOLD = 25
MAX_VOLUME_STEPS_PER_FRAME = 4
VOLUME_MODE_Y_FRACTION = 0.3   # top 30% = volume zone
SCROLL_MODE_Y_FRACTION = 0.7   # bottom 30% = scroll zone (middle = media/zoom zone)

MIDDLE_PINCH_THRESH = 28
RIGHT_CLICK_COOLDOWN = 0.4

MIN_MOVE_DELTA = 8              # min cursor movement (pixels)
CURSOR_SMOOTH_ALPHA = 0.3       # 0–1. Higher = snappier, lower = smoother

SCROLL_LOCK_TIME = 0.4
VOLUME_LOCK_TIME = 0.4
SCROLL_REENTER_DELAY = 1.0

# Media gesture thresholds
THUMB_RING_THRESH = 32
THUMB_PINKY_THRESH = 40   # slightly easier than ring

# Zoom gesture thresholds
ZOOM_DELTA_THRESHOLD = 40
MAX_ZOOM_STEPS_PER_FRAME = 3

# ---------- STATE VARIABLES ----------
# Left-hand click/drag
left_pinch_prev = False         # for click/drag
left_pinch_start_time = 0.0
left_dragging = False

# Scroll
prev_left_wrist_y = None
scroll_accum = 0.0
is_scrolling = False
last_scroll_time = 0.0

# Volume (horizontal)
prev_left_wrist_x = None
volume_accum = 0.0
is_volume_adjusting = False
last_volume_time = 0.0

# Media gesture state
prev_ring_pinch = False
prev_pinky_pinch = False

# Right-click via middle pinch
right_middle_prev = False
last_right_click_time = 0.0

# Mouse move (right hand)
prev_mouse_x, prev_mouse_y = None, None
smooth_mouse_x, smooth_mouse_y = None, None

# Left hand visibility / re-entry
left_visible_prev = False
left_reenter_time = 0.0

# AIR MODE (master on/off) - toggled by keyboard 'e'
air_mode_enabled = True

# Zoom state (two hands)
prev_hand_dist = None
zoom_accum = 0.0
left_index_global = None
right_index_global = None
left_ok_for_zoom = False
right_ok_for_zoom = False


while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    now = time.time()

    h, w, _ = frame.shape
    left_visible_this_frame = False
    left_index_global = None
    right_index_global = None
    left_ok_for_zoom = False
    right_ok_for_zoom = False

    # -------- DRAW HANDS ----------
    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, info in zip(results.multi_hand_landmarks,
                                        results.multi_handedness):
            label = info.classification[0].label
            wrist = hand_landmarks.landmark[0]
            wx, wy = int(wrist.x * w), int(wrist.y * h)

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            cv2.putText(frame, label, (wx - 20, wy - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            if label == "Left":
                left_visible_this_frame = True

    # -------- AIR MODE STATUS ONLY (no MODE/IDLE) ----------
    status_text = "AIR MODE: ON" if air_mode_enabled else "AIR MODE: OFF"
    status_color = (0, 255, 100) if air_mode_enabled else (0, 0, 255)
    cv2.putText(frame, status_text, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, status_color, 2)

    # If air mode OFF, just show video + status and skip gesture controls
    if not air_mode_enabled:
        cv2.imshow("Air Control", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('e'):
            air_mode_enabled = not air_mode_enabled
        # optional brightness keys
        if key == ord('k'):
            pyautogui.press("brightnessdown")
        elif key == ord('l'):
            pyautogui.press("brightnessup")
        continue

    # -------- MAIN GESTURE LOGIC WHEN AIR MODE ON ----------
    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, info in zip(results.multi_hand_landmarks,
                                        results.multi_handedness):
            label = info.classification[0].label
            wrist = hand_landmarks.landmark[0]
            wx, wy = int(wrist.x * w), int(wrist.y * h)

            index_tip = hand_landmarks.landmark[8]
            thumb_tip = hand_landmarks.landmark[4]
            ix, iy = int(index_tip.x * w), int(index_tip.y * h)
            tx, ty = int(thumb_tip.x * w), int(thumb_tip.y * h)

            # ---------- RIGHT HAND: CURSOR (with smoothing) ----------
            if label == "Right":
                right_index_global = (ix, iy)
                right_ok_for_zoom = True

                lock_cursor = (
                    is_scrolling and (now - last_scroll_time) < SCROLL_LOCK_TIME
                ) or (
                    is_volume_adjusting and (now - last_volume_time) < VOLUME_LOCK_TIME
                )

                if not lock_cursor:
                    raw_x = int((ix / w) * screen_w)
                    raw_y = int((iy / h) * screen_h)

                    if smooth_mouse_x is None:
                        smooth_mouse_x, smooth_mouse_y = raw_x, raw_y
                        prev_mouse_x, prev_mouse_y = raw_x, raw_y

                    # exponential smoothing
                    smooth_mouse_x = int(
                        CURSOR_SMOOTH_ALPHA * raw_x + (1 - CURSOR_SMOOTH_ALPHA) * smooth_mouse_x
                    )
                    smooth_mouse_y = int(
                        CURSOR_SMOOTH_ALPHA * raw_y + (1 - CURSOR_SMOOTH_ALPHA) * smooth_mouse_y
                    )

                    if math.hypot(smooth_mouse_x - prev_mouse_x,
                                  smooth_mouse_y - prev_mouse_y) > MIN_MOVE_DELTA:
                        pyautogui.moveTo(smooth_mouse_x, smooth_mouse_y)
                        prev_mouse_x, prev_mouse_y = smooth_mouse_x, smooth_mouse_y

            # ---------- LEFT HAND: CLICK / DRAG / RIGHT CLICK / SCROLL / VOLUME / MEDIA ----------
            if label == "Left":
                left_visible_this_frame = True
                left_index_global = (ix, iy)

                # Re-entry handling
                if not left_visible_prev:
                    left_reenter_time = now
                    prev_left_wrist_y = wy
                    prev_left_wrist_x = wx
                    scroll_accum = 0.0
                    volume_accum = 0.0
                    is_scrolling = False
                    is_volume_adjusting = False

                # Distances for gestures
                dist_index = math.hypot(ix - tx, iy - ty)
                index_pinch = dist_index < 32

                middle_tip = hand_landmarks.landmark[12]
                mx, my = int(middle_tip.x * w), int(middle_tip.y * h)
                dist_middle = math.hypot(mx - tx, my - ty)
                middle_pinch = dist_middle < MIDDLE_PINCH_THRESH

                # ring & pinky for media gestures
                ring_tip = hand_landmarks.landmark[16]
                pinky_tip = hand_landmarks.landmark[20]
                rx, ry = int(ring_tip.x * w), int(ring_tip.y * h)
                px, py_ = int(pinky_tip.x * w), int(pinky_tip.y * h)
                dist_ring = math.hypot(rx - tx, ry - ty)
                dist_pinky = math.hypot(px - tx, py_ - ty)
                ring_pinch = dist_ring < THUMB_RING_THRESH
                pinky_pinch = dist_pinky < THUMB_PINKY_THRESH

                neutral = not index_pinch and not middle_pinch and not left_dragging
                can_interact_now = (now - left_reenter_time) > SCROLL_REENTER_DELAY

                norm_y = wy / h
                in_volume_zone = norm_y < VOLUME_MODE_Y_FRACTION
                in_scroll_zone = norm_y > SCROLL_MODE_Y_FRACTION
                in_media_zone = not in_volume_zone and not in_scroll_zone

                # For zoom: require left neutral and in media zone
                left_ok_for_zoom = neutral and in_media_zone and can_interact_now

                # ----- MEDIA MODE (middle band): play/pause, next -----
                if can_interact_now and in_media_zone and neutral:
                    # Thumb + pinky pinch => Play/Pause (space)
                    if pinky_pinch and not prev_pinky_pinch:
                        pyautogui.press("space")

                    # Thumb + ring pinch => Next track
                    if ring_pinch and not prev_ring_pinch:
                        pyautogui.press("nexttrack")

                    prev_pinky_pinch = pinky_pinch
                    prev_ring_pinch = ring_pinch
                else:
                    prev_pinky_pinch = pinky_pinch
                    prev_ring_pinch = ring_pinch

                # ----- CLICK / DRAG (WORKS IN ALL ZONES) -----
                if can_interact_now:
                    if index_pinch and not left_pinch_prev:
                        left_pinch_start_time = now

                    if index_pinch and not left_dragging:
                        if (now - left_pinch_start_time) > DRAG_HOLD_TIME:
                            pyautogui.mouseDown()
                            left_dragging = True

                    if not index_pinch and left_pinch_prev:
                        hold_time = now - left_pinch_start_time
                        if left_dragging:
                            pyautogui.mouseUp()
                            left_dragging = False
                        else:
                            if hold_time <= CLICK_MAX_TIME:
                                pyautogui.click()

                left_pinch_prev = index_pinch

                # ----- RIGHT CLICK (everywhere) -----
                if (can_interact_now and neutral and middle_pinch
                        and not right_middle_prev
                        and (now - last_right_click_time) > RIGHT_CLICK_COOLDOWN):
                    pyautogui.rightClick()
                    last_right_click_time = now

                right_middle_prev = middle_pinch

                # ----- VOLUME / SCROLL -----
                if can_interact_now and neutral:
                    # VOLUME MODE (upper)
                    if in_volume_zone:
                        if prev_left_wrist_x is not None:
                            dx = wx - prev_left_wrist_x
                            volume_accum += dx

                            steps = 0
                            while volume_accum > VOLUME_DELTA_THRESHOLD and steps < MAX_VOLUME_STEPS_PER_FRAME:
                                pyautogui.press("volumeup")
                                volume_accum -= VOLUME_DELTA_THRESHOLD
                                steps += 1
                                is_volume_adjusting = True
                                last_volume_time = now

                            while volume_accum < -VOLUME_DELTA_THRESHOLD and steps < MAX_VOLUME_STEPS_PER_FRAME:
                                pyautogui.press("volumedown")
                                volume_accum += VOLUME_DELTA_THRESHOLD
                                steps += 1
                                is_volume_adjusting = True
                                last_volume_time = now

                        prev_left_wrist_x = wx
                        prev_left_wrist_y = wy
                        scroll_accum = 0.0
                        is_scrolling = False

                    # SCROLL MODE (lower)
                    elif in_scroll_zone:
                        if prev_left_wrist_y is not None:
                            dy = wy - prev_left_wrist_y
                            scroll_accum += dy

                            while scroll_accum > SCROLL_DELTA_THRESHOLD:
                                pyautogui.scroll(-SCROLL_AMOUNT)
                                scroll_accum -= SCROLL_DELTA_THRESHOLD
                                is_scrolling = True
                                last_scroll_time = now

                            while scroll_accum < -SCROLL_DELTA_THRESHOLD:
                                pyautogui.scroll(SCROLL_AMOUNT)
                                scroll_accum += SCROLL_DELTA_THRESHOLD
                                is_scrolling = True
                                last_scroll_time = now

                        prev_left_wrist_y = wy
                        prev_left_wrist_x = wx
                        volume_accum = 0.0
                        is_volume_adjusting = False

    # ----- TWO-HAND ZOOM GESTURE (in MEDIA zone, neutral) -----
    if air_mode_enabled and left_index_global and right_index_global and left_ok_for_zoom and right_ok_for_zoom:
        lx, ly = left_index_global
        rx, ry = right_index_global
        dist = math.hypot(rx - lx, ry - ly)
        if prev_hand_dist is None:
            prev_hand_dist = dist
        else:
            delta = dist - prev_hand_dist
            prev_hand_dist = dist
            zoom_accum += delta

            steps = 0
            while zoom_accum > ZOOM_DELTA_THRESHOLD and steps < MAX_ZOOM_STEPS_PER_FRAME:
                pyautogui.hotkey('ctrl', '+')
                zoom_accum -= ZOOM_DELTA_THRESHOLD
                steps += 1

            while zoom_accum < -ZOOM_DELTA_THRESHOLD and steps < MAX_ZOOM_STEPS_PER_FRAME:
                pyautogui.hotkey('ctrl', '-')
                zoom_accum += ZOOM_DELTA_THRESHOLD
                steps += 1
    else:
        prev_hand_dist = None
        zoom_accum = 0.0

    # Reset left-related state if hand disappears
    if not left_visible_this_frame and left_visible_prev:
        prev_left_wrist_y = None
        prev_left_wrist_x = None
        scroll_accum = 0.0
        volume_accum = 0.0
        is_scrolling = False
        is_volume_adjusting = False

    left_visible_prev = left_visible_this_frame

    # -------- DISPLAY FRAME & HANDLE KEYBOARD HOTKEYS ----------
    cv2.imshow("Air Control", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    elif key == ord('e'):
        air_mode_enabled = not air_mode_enabled
        # reset movement state whenever we toggle
        left_dragging = False
        scroll_accum = 0.0
        volume_accum = 0.0
        is_scrolling = False
        is_volume_adjusting = False
        prev_mouse_x, prev_mouse_y = None, None
        smooth_mouse_x, smooth_mouse_y = None, None
        prev_hand_dist = None
        zoom_accum = 0.0
    # brightness hotkeys (optional)
    elif key == ord('k'):
        pyautogui.press("brightnessdown")
    elif key == ord('l'):
        pyautogui.press("brightnessup")

cap.release()
cv2.destroyAllWindows()
