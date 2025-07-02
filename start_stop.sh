#!/bin/bash

# アプリケーションの開始
start_app() {
    echo "Starting the application..."
    # main.py をバックグラウンドで実行
    python main.py &
    # プロセスIDをファイルに保存
    echo $! > app.pid
    echo "Application started."
}

# アプリケーションの停止
stop_app() {
    echo "Stopping the application..."
    if [ -f app.pid ]; then
        PID=$(cat app.pid)
        # プロセスを終了
        kill $PID
        # PIDファイルを削除
        rm app.pid
        echo "Application stopped."
    else
        echo "Application is not running or PID file not found."
    fi
}

# メイン処理
case "$1" in
    start)
        start_app
        ;;
    stop)
        stop_app
        ;;
    restart)
        stop_app
        start_app
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac

exit 0
