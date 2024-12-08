const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Screens
const welcomeScreen = document.getElementById('welcome-screen');
const overScreen = document.getElementById('over-screen');
const finalScoreEl = document.getElementById('final-score');
const startButton = document.getElementById('start-button');
const playAgainButton = document.getElementById('play-again-button');

// Controls
const upArrow = document.querySelector('.arrow.up');
const downArrow = document.querySelector('.arrow.down');
const leftArrow = document.querySelector('.arrow.left');
const rightArrow = document.querySelector('.arrow.right');

// Game Variables
const SCREEN_WIDTH = 1200;
const SCREEN_HEIGHT = 720;

let gameState = 'welcome';
let snake = [];
let snakeLength = 1;
let snakeSize = 17;
let snakeX = SCREEN_WIDTH / 2;
let snakeY = SCREEN_HEIGHT / 2;
let velocityX = 0;
let velocityY = 0;
let topV = 1;
let score = 0;
let highscore = localStorage.getItem("highscore") ? parseInt(localStorage.getItem("highscore"),10) : 0;
let foodX, foodY;

// Assets
const bgImg = new Image();
bgImg.src = 'assets/bg.png';

const eatSound = new Audio('assets/eat.mp3');
const startSound = new Audio('assets/start.mp3');
const goverSound = new Audio('assets/gover.mp3');
const resetSound = new Audio('assets/reset.mp3');
const bgMusic = new Audio('assets/bg.mp3');
bgMusic.loop = true;

// Events
document.addEventListener('keydown', handleKeydown);
startButton.addEventListener('click', startGame);
playAgainButton.addEventListener('click', resetGame);

// Touch & Mouse Controls
upArrow.addEventListener('touchstart', () => setDirection(0, -topV), false);
downArrow.addEventListener('touchstart', () => setDirection(0, topV), false);
leftArrow.addEventListener('touchstart', () => setDirection(-topV, 0), false);
rightArrow.addEventListener('touchstart', () => setDirection(topV, 0), false);

upArrow.addEventListener('mousedown', () => setDirection(0, -topV));
downArrow.addEventListener('mousedown', () => setDirection(0, topV));
leftArrow.addEventListener('mousedown', () => setDirection(-topV, 0));
rightArrow.addEventListener('mousedown', () => setDirection(topV, 0));

function setDirection(vx, vy) {
  // Prevent immediate reversal
  if ((vx !== 0 && vx !== -velocityX) || (vy !== 0 && vy !== -velocityY)) {
    velocityX = vx; velocityY = vy;
  }
}

function handleKeydown(e) {
  if (gameState === 'welcome' && (e.code === 'Space' || e.code === 'Enter')) {
    startGame();
  } else if (gameState === 'game') {
    if (e.code === 'ArrowRight' && velocityX !== -topV) { velocityX = topV; velocityY = 0; }
    else if (e.code === 'ArrowLeft' && velocityX !== topV) { velocityX = -topV; velocityY = 0; }
    else if (e.code === 'ArrowUp' && velocityY !== topV) { velocityX = 0; velocityY = -topV; }
    else if (e.code === 'ArrowDown' && velocityY !== -topV) { velocityX = 0; velocityY = topV; }
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
  snakeX += velocityX;
  snakeY += velocityY;

  // Boundary
  if (snakeX < 0 || snakeX > SCREEN_WIDTH || snakeY < 0 || snakeY > SCREEN_HEIGHT) {
    gameOver();
    return;
  }

  // Eat
  if (Math.abs(snakeX - foodX) < 15 && Math.abs(snakeY - foodY) < 15) {
    score += 10;
    placeFood();
    snakeLength += 7.5;
    topV += 0.1;
    eatSound.play();
  }

  let head = {x: snakeX, y: snakeY};
  snake.push(head);
  if (snake.length > snakeLength) {
    snake.shift();
  }

  // Self-collision
  for (let i = 0; i < snake.length - 1; i++) {
    if (snake[i].x === head.x && snake[i].y === head.y) {
      gameOver();
      return;
    }
  }
}

function drawGame() {
  if (gameState === 'game') {
    ctx.drawImage(bgImg, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);

    // Food
    ctx.beginPath();
    ctx.fillStyle = 'red';
    ctx.arc(foodX, foodY, snakeSize - 5, 0, Math.PI * 2);
    ctx.fill();

    // Snake
    ctx.fillStyle = 'black';
    for (let i = 0; i < snake.length; i++) {
      ctx.beginPath();
      ctx.arc(snake[i].x, snake[i].y, snakeSize - 5, 0, Math.PI * 2);
      ctx.fill();
    }

    // Score
    ctx.fillStyle = 'red';
    ctx.font = '60px Hyperwave, sans-serif';
    ctx.fillText(`Score: ${score}   High Score: ${highscore}`, 5, 60);
  }
}

function gameLoop() {
  if (gameState === 'game') {
    updateGame();
  }
  ctx.clearRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
  drawGame();
  requestAnimationFrame(gameLoop);
}

// Initialize screens
welcomeScreen.style.display = 'block';
overScreen.style.display = 'none';

gameLoop();
