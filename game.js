// Canvas and Context
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Screens
const welcomeScreen = document.getElementById('welcome-screen');
const overScreen = document.getElementById('over-screen');
const finalScoreEl = document.getElementById('final-score');
const startButton = document.getElementById('start-button');
const playAgainButton = document.getElementById('play-again-button');

// Game Variables
const SCREEN_WIDTH = canvas.width;
const SCREEN_HEIGHT = canvas.height;

let gameState = 'welcome'; // 'welcome', 'game', 'over'
let snake = [];
let snakeLength = 1;
let snakeSize = 17;
let snakeX = SCREEN_WIDTH / 2;
let snakeY = SCREEN_HEIGHT / 2;
let velocityX = 0;
let velocityY = 0;
let topV = 1;

let score = 0;
let highscore = 0;
if (localStorage.getItem("highscore")) {
  highscore = parseInt(localStorage.getItem("highscore"), 10);
} else {
  highscore = 0;
}

let foodX, foodY;

// Assets
const bgImg = new Image();
bgImg.src = 'assets/bg.png';

const wlcImg = new Image();
wlcImg.src = 'assets/wlc.png';

const overImg = new Image();
overImg.src = 'assets/over.png';

// Sounds
const eatSound = new Audio('assets/eat.mp3');
const startSound = new Audio('assets/start.mp3');
const hoverSound = new Audio('assets/hover.mp3');
const goverSound = new Audio('assets/gover.mp3');
const resetSound = new Audio('assets/reset.mp3');
const bgMusic = new Audio('assets/bg.mp3');
bgMusic.loop = true;

// Event Listeners
document.addEventListener('keydown', handleKeydown);
startButton.addEventListener('click', startGame);
playAgainButton.addEventListener('click', resetGame);

function handleKeydown(e) {
  if (gameState === 'welcome' && (e.code === 'Space' || e.code === 'Enter')) {
    startGame();
  } else if (gameState === 'game') {
    switch (e.code) {
      case 'ArrowRight':
        if (velocityX !== -topV) { velocityX = topV; velocityY = 0; }
        break;
      case 'ArrowLeft':
        if (velocityX !== topV) { velocityX = -topV; velocityY = 0; }
        break;
      case 'ArrowUp':
        if (velocityY !== topV) { velocityX = 0; velocityY = -topV; }
        break;
      case 'ArrowDown':
        if (velocityY !== -topV) { velocityX = 0; velocityY = topV; }
        break;
      case 'Escape':
        velocityX = 0; velocityY = 0;
        break;
    }
  } else if (gameState === 'over' && (e.code === 'Enter' || e.code === 'Space')) {
    resetGame();
  }
}

function initGame() {
  snakeX = SCREEN_WIDTH / 2;
  snakeY = SCREEN_HEIGHT / 2;
  velocityX = 0;
  velocityY = 0;
  topV = 1;
  score = 0;
  snakeLength = 1;
  snake = [];
  placeFood();
}

function placeFood() {
  foodX = randomInt(SCREEN_WIDTH / 10, (3 * SCREEN_WIDTH) / 4);
  foodY = randomInt(SCREEN_HEIGHT / 10, (3 * SCREEN_HEIGHT) / 4);
}

function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min) + min);
}

function startGame() {
  startSound.play();
  setTimeout(() => {
    bgMusic.play();
  }, 950);
  initGame();
  gameState = 'game';
  welcomeScreen.style.display = 'none';
  overScreen.style.display = 'none';
}

function resetGame() {
  resetSound.play();
  setTimeout(() => {
    gameState = 'welcome';
    welcomeScreen.style.display = 'block';
    overScreen.style.display = 'none';
    bgMusic.pause();
    bgMusic.currentTime = 0;
  }, 500);
}

function gameOver() {
  goverSound.play();
  bgMusic.pause();
  bgMusic.currentTime = 0;
  if (score > highscore) {
    highscore = score;
    localStorage.setItem("highscore", highscore.toString());
  }
  gameState = 'over';
  finalScoreEl.textContent = score.toString();
  overScreen.style.display = 'block';
}

function updateGame() {
  // Update snake position
  snakeX += velocityX;
  snakeY += velocityY;

  // Boundary check
  if (snakeX < 0 || snakeX > SCREEN_WIDTH || snakeY < 0 || snakeY > SCREEN_HEIGHT) {
    gameOver();
    return;
  }

  // Eat food
  if (Math.abs(snakeX - foodX) < 15 && Math.abs(snakeY - foodY) < 15) {
    score += 10;
    placeFood();
    snakeLength += 7.5;
    topV += 0.1;
    eatSound.play();
  }

  // Update snake body
  let head = {x: snakeX, y: snakeY};
  snake.push(head);
  if (snake.length > snakeLength) {
    snake.shift();
  }

  // Check self collision
  for (let i = 0; i < snake.length - 1; i++) {
    if (snake[i].x === head.x && snake[i].y === head.y) {
      gameOver();
      return;
    }
  }
}

function drawGame() {
  ctx.clearRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);

  if (gameState === 'welcome') {
    // The welcome screen overlay is handling display
  } else if (gameState === 'game') {
    ctx.drawImage(bgImg, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);

    // Draw food
    ctx.beginPath();
    ctx.fillStyle = 'red';
    ctx.arc(foodX, foodY, snakeSize - 5, 0, Math.PI * 2);
    ctx.fill();

    // Draw snake
    ctx.fillStyle = 'black';
    for (let i = 0; i < snake.length; i++) {
      ctx.beginPath();
      ctx.arc(snake[i].x, snake[i].y, snakeSize - 5, 0, Math.PI * 2);
      ctx.fill();
    }

    // Display Score
    ctx.fillStyle = 'red';
    ctx.font = '60px Hyperwave, sans-serif';
    ctx.fillText(`Score: ${score}   High Score: ${highscore}`, 5, 60);

  } else if (gameState === 'over') {
    // The over screen overlay is handling display
  }
}

function gameLoop() {
  if (gameState === 'game') {
    updateGame();
  }
  drawGame();
  requestAnimationFrame(gameLoop);
}

// Initially show welcome screen
welcomeScreen.style.display = 'block';
overScreen.style.display = 'none';

gameLoop();
