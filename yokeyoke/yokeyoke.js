// game.js

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// ゲームの状態
let gameStarted = false;
let gameOver = false;
let score = 0;
let lastFrameTime = 0;

// プレイヤー
const player = {
    x: canvas.width / 2 - 25,
    y: canvas.height - 60,
    width: 15,
    height: 30,
    color: 'blue',
    speed: 5,
};

// 障害物
let obstacles = [];
const obstacleSpeed = 4.5;
const obstacleMinRadius = 10;
const obstacleMaxRadius = 25;
const obstacleSpawnInterval = 260; // ms
let lastObstacleSpawnTime = 0;

// スコア表示
function drawScore() {
    ctx.fillStyle = 'white';
    ctx.font = '20px Arial';
    ctx.fillText('Score: ' + Math.floor(score), 10, 30);
}

// プレイヤーを描画
function drawPlayer() {
    ctx.fillStyle = player.color;
    ctx.fillRect(player.x, player.y, player.width, player.height);
}

// 障害物を描画
function drawObstacles() {
    obstacles.forEach(obstacle => {
        ctx.fillStyle = obstacle.color;
        ctx.beginPath();
        ctx.arc(obstacle.x, obstacle.y, obstacle.radius, 0, Math.PI * 2);
        ctx.fill();
    });
}

// 障害物を生成
function spawnObstacle() {
    const radius = Math.random() * (obstacleMaxRadius - obstacleMinRadius) + obstacleMinRadius;
    const x = Math.random() * (canvas.width - radius * 2) + radius;
    obstacles.push({
        x: x,
        y: -radius,
        radius: radius,
        color: 'red',
    });
}

// プレイヤーの移動
canvas.addEventListener('mousemove', (e) => {
    if (!gameOver && gameStarted) {
        const mouseX = e.clientX - canvas.getBoundingClientRect().left;
        player.x = mouseX - player.width / 2;

        // 画面外に出ないように制限
        if (player.x < 0) {
            player.x = 0;
        }
        if (player.x + player.width > canvas.width) {
            player.x = canvas.width - player.width;
        }
    }
});

// 衝突判定 (四角形と円形)
function checkCollision() {
    for (let i = 0; i < obstacles.length; i++) {
        const obstacle = obstacles[i];

        // 矩形の中心と円の中心の距離
        const rectCenterX = player.x + player.width / 2;
        const rectCenterY = player.y + player.height / 2;

        // 円の中心から最も近い矩形上の点を見つける
        let testX = obstacle.x;
        let testY = obstacle.y;

        if (obstacle.x < player.x) {
            testX = player.x;
        } else if (obstacle.x > player.x + player.width) {
            testX = player.x + player.width;
        }

        if (obstacle.y < player.y) {
            testY = player.y;
        } else if (obstacle.y > player.y + player.height) {
            testY = player.y + player.height;
        }

        // 最も近い点と円の中心の距離を計算
        const distX = obstacle.x - testX;
        const distY = obstacle.y - testY;
        const distance = Math.sqrt((distX * distX) + (distY * distY));

        // 距離が円の半径より小さければ衝突
        if (distance < obstacle.radius) {
            gameOver = true;
            break;
        }
    }
}

// ゲームオーバー画面
function drawGameOver() {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = 'white';
    ctx.font = '34px Arial';
    ctx.fillText('GAME OVER', 40, canvas.height / 2 - 40);
    ctx.font = '21px Arial';
    ctx.fillText('Score: ' + Math.floor(score), 40, canvas.height / 2);
    ctx.font = '17px Arial';
    ctx.fillText('Click to Restart', 40, canvas.height / 2 + 40);
}

// ゲームのリセット
function resetGame() {
    player.x = canvas.width / 2 - 25;
    player.y = canvas.height - 60;
    obstacles.length = 0;
    score = 0;
    gameOver = false;
    gameStarted = true;
    lastObstacleSpawnTime = 0;
    lastFrameTime = 0;
    requestAnimationFrame(gameLoop);
}

// クリックでゲーム開始/リスタート
canvas.addEventListener('click', () => {
    if (!gameStarted || gameOver) {
        resetGame();
    }
});

// ゲームループ
function gameLoop(currentTime) {
    if (!gameStarted) {
        // ゲーム開始前の画面表示
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = 'white';
        ctx.font = '30px Arial';
        ctx.fillText('Click to Start', canvas.width / 2, canvas.height / 2);
        requestAnimationFrame(gameLoop);
        return;
    }

    if (gameOver) {
        drawGameOver();
        return;
    }

    if (lastFrameTime === 0) {
        lastFrameTime = currentTime;
    }
    const deltaTime = currentTime - lastFrameTime;
    lastFrameTime = currentTime;

    // 画面クリア
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 障害物の更新
    for (let i = 0; i < obstacles.length; i++) {
        obstacles[i].y += obstacleSpeed * (deltaTime / 16); // 60fps基準で調整
    }

    // 画面外に出た障害物を削除
    obstacles = obstacles.filter(obstacle => obstacle.y - obstacle.radius < canvas.height);

    // 障害物の生成
    if (currentTime - lastObstacleSpawnTime > obstacleSpawnInterval) {
        spawnObstacle();
        lastObstacleSpawnTime = currentTime;
    }

    // スコア更新
    score += deltaTime / 1000; // 1000msごとに1点

    // 描画
    drawPlayer();
    drawObstacles();
    drawScore();

    // 衝突判定
    checkCollision();

    requestAnimationFrame(gameLoop);
}

// ゲーム開始
requestAnimationFrame(gameLoop);
