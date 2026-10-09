let cor;
let espessura;

function setup() {
    // Cria uma tela de 800x600 pixels
    createCanvas(800, 600);
    background(255); // Fundo branco
    cor = document.getElementById('escolher-cor');
    espessura = document.getElementById('escolher-espessura')
  }
  
  function draw() {
    // Desenha apenas quando o botão do mouse estiver pressionado
    if (mouseIsPressed) {
      stroke(cor.value); // Cor da linha (preto)
      strokeWeight(espessura.value); // Espessura da linha
      // Desenha uma linha da posição anterior do mouse até a posição atual
      line(pmouseX, pmouseY, mouseX, mouseY);
    }
  }
  
  // Limpa a tela ao pressionar a tecla 'C' ou ESPAÇO
  function keyPressed() {
    if (key === 'c' || key === 'C' || keyCode === 32) {
      background(255);
    }
  }
