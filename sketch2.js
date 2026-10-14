createCanvas(altura.value, largura.value);
background(0); // Fundo branco

function draw() {
    // Desenha apenas quando o botão do mouse estiver pressionado
    if (mouseIsPressed) {
      stroke(cor.value); // Cor da linha (preto)
      strokeWeight(espessura.value); // Espessura da linha
      // Desenha uma linha da posição anterior do mouse até a posição atual
      line(pmouseX, pmouseY, mouseX, mouseY);
    }
  }

  function keyPressed() {
    if (key === 'c' || key === 'C' || keyCode === 32) {
      background(255);
    }
  }