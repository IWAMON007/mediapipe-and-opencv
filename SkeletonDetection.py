import mediapipe as mp
import cv2
# モデルの読み込み
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_holistic = mp.solutions.holistic
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# カメラの設定
cap = cv2.VideoCapture(0)  # 0は内蔵カメラを指定する

# モデルを初期化する
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:

    while True:
        # フレームを読み込む
        ret, frame = cap.read()
        
        # 画像の左右を反転する
        img_flipped = cv2.flip(frame, 1)
        
        # 画像をRGBに変換する
        image = cv2.cvtColor(img_flipped, cv2.COLOR_BGR2RGB)
        
        # 骨格検出を実行
        results = pose.process(image)

        # 検出結果を表示する
        mp_drawing.draw_landmarks(
            img_flipped, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        #鼻のx,y座標の表示
        results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].x
        results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].y
        print("X: " + str(round(results.pose_landmarks.landmark[0].x,3)) + "  Y: " +
             str(round(results.pose_landmarks.landmark[0].y,3)))
        
        # 結果を表示する
        cv2.imshow('MediaPipe Pose', img_flipped)
        
        
        # ESCキーで終了する
        if cv2.waitKey(1) == 27:
            break
    
    
    cap.release()
    cv2.destroyAllWindows()
