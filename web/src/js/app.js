class InputCanvas {
  constructor(onMouseUp) {
    this.canvas = document.getElementById('input-canvas');
    this.lineWidth = 16;
    this.canvas.height = this.lineWidth * 28;
    this.canvas.width = this.lineWidth * 28;
    this.context = this.canvas.getContext('2d');
    this.drawing = false;
    this.onMouseUp = onMouseUp;

    this._setEventListeners();
  }

  clear() {
    this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
  }

  _setEventListeners() {
    this.canvas.addEventListener('mousedown', (e) => {
      e.preventDefault();

      this._startDrawing(e.pageX, e.pageY);
    });

    this.canvas.addEventListener('mousemove', (e) => {
      e.preventDefault();

      this._continueDrawing(e.pageX, e.pageY);
    });

    this.canvas.addEventListener('mouseup', (e) => {
      e.preventDefault();

      this._endDrawing(e.pageX, e.pageY);
    });

    this.canvas.addEventListener('touchstart', (e) => {
      e.preventDefault();

      let touch = e.changedTouches[0];
      this._startDrawing(touch.pageX, touch.pageY);
    });

    this.canvas.addEventListener('touchmove', (e) => {
      e.preventDefault();

      let touch = e.changedTouches[0];
      this._continueDrawing(touch.pageX, touch.pageY);
    });

    this.canvas.addEventListener('touchend', (e) => {
      e.preventDefault();

      let touch = e.changedTouches[0];
      this._endDrawing(touch.pageX, touch.pageY);
    });
  }

  _startDrawing(pageX, pageY) {
    let position = this._normalizedPosition(pageX, pageY);
    this.context.lineWidth = this.lineWidth;
    this.context.beginPath();
    this.context.moveTo(position.x, position.y);
    this.drawing = true;
  }

  _continueDrawing(pageX, pageY) {
    if (!this.drawing) { return; }

    let position = this._normalizedPosition(pageX, pageY);
    this.context.lineTo(position.x, position.y);
    this.context.stroke();
  }

  _endDrawing(pageX, pageY) {
    let position = this._normalizedPosition(pageX, pageY);
    this.context.lineTo(position.x, position.y);
    this.context.stroke();
    this.context.closePath();
    this.drawing = false;

    this.onMouseUp(this.canvas.toDataURL());
  }

  _normalizedPosition(x, y) {
    let rect = this.canvas.getBoundingClientRect();
    return { x: x - rect.left, y: y - rect.top };
  }
}

class App {
  constructor() {
    this.inputCanvas = new InputCanvas(this.onMouseUp.bind(this));
    this.hiddenCanvas = document.createElement('canvas');
    this.$guess = $('#guess');
    this.$clearButton = $('#button-clear')

    this.$clearButton.on('click', () => {
      this.inputCanvas.clear();
      this.$guess.text('');
    });
  }

  onMouseUp(dataUrl) {
    let image = new Image();
    image.src = dataUrl;
    image.onload = () => {
      let context = this.hiddenCanvas.getContext('2d');
      context.clearRect(0, 0, this.hiddenCanvas.width, this.hiddenCanvas.height);
      context.drawImage(image, 0, 0, image.width, image.height, 0, 0, 28, 28);
      let data = context.getImageData(0, 0, 28, 28).data;
      let input = [];
      for (let i = 0; i < 28 * 28; i ++) {
        input[i] = data[4 * i + 3];
      }
/*
      for (let r = 0; r < 28; r++) {
        let str = '';
        for (let c = 0; c < 28; c++) {
          let i = r * 28 + c;
          if (input[i] >= 100) { str += input[i] + ' '; }
          else if (input[i] >= 10) { str += ' ' + input[i] + ' '; }
          else { str += '  ' + input[i] + ' '; }
        }
        console.log(str);
      }
*/

      $.ajax({
        url: '/guess',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
          image: input,
        }),
        success: (e) => {
          this.$guess.text(e);
        },
        error: (e) => {
          console.debug(e);
        }
      });
    }
  }
}

$(() => {
  let app = new App();
})
