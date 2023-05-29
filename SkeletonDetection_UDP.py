import mediapipe as mp
import cv2

#ソケット通信（UDP/TCP）をするためのライブラリをインポート
import socket

#ポートとホスト
HOST = "127.0.0.1"
PORT = 60000

#通信クライアントの作成
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# モデルの読み込み
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_holistic = mp.solutions.holistic

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
        
        #鼻のx,y座標を変数に格納
        nose_x = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x
        nose_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y

        #座標を文字列に変換
        sendstr = ",".join([str(nose_x),str(nose_y)])
        
        #鼻の座標を送信
        client.sendto(sendstr.encode('utf-8'),(HOST,PORT))

        # 結果を表示する
        cv2.imshow('MediaPipe Pose', img_flipped)
        
        
        # ESCキーで終了する
        if cv2.waitKey(1) == 27:
            break
    
    
    cap.release()
    cv2.destroyAllWindows()