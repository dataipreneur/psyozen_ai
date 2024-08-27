import React, { useEffect, useRef } from 'react';

class SiriWave9Curve {
  constructor(opt) {
    opt = opt || {};
    this.controller = opt.controller;
    this.color = opt.color;
    this.tick = 0;
    this.respawn();
  }

  respawn() {
    this.amplitude = 0.3 + Math.random() * 0.7;
    this.seed = Math.random();
    this.open_class = 2 + (Math.random() * 3) | 0;
  }

  equation(i) {
    const p = this.tick;
    const y = -1 * Math.abs(Math.sin(p)) * this.controller.amplitude * this.amplitude * this.controller.MAX * Math.pow(1 / (1 + Math.pow(this.open_class * i, 2)), 2);
    if (Math.abs(y) < 0.001) {
      this.respawn();
    }
    return y;
  }

  _draw(m) {
    this.tick += this.controller.speed * (1 - 0.5 * Math.sin(this.seed * Math.PI));

    const ctx = this.controller.ctx;
    ctx.beginPath();

    const x_base = this.controller.width / 2 + (-this.controller.width / 4 + this.seed * (this.controller.width / 2));
    const y_base = this.controller.height / 2;

    let x_init;
    let i = -3;
    while (i <= 3) {
      const x = x_base + i * this.controller.width / 4;
      const y = y_base + (m * this.equation(i));
      x_init = x_init || x;
      ctx.lineTo(x, y);
      i += 0.01;
    }

    const h = Math.abs(this.equation(0));
    const gradient = ctx.createRadialGradient(x_base, y_base, h * 1.15, x_base, y_base, h * 0.3);
    gradient.addColorStop(0, `rgba(${this.color.join(',')},0.4)`);
    gradient.addColorStop(1, `rgba(${this.color.join(',')},0.2)`);

    ctx.fillStyle = gradient;

    ctx.lineTo(x_init, y_base);
    ctx.closePath();

    ctx.fill();
  }

  draw() {
    this._draw(-1);
    this._draw(1);
  }
}

class SiriWave9 {
  static COLORS = [
    [32, 133, 252],
    [94, 252, 169],
    [253, 71, 103]
  ];

  constructor(opt) {
    opt = opt || {};

    this.tick = 0;
    this.run = false;

    // UI vars
    this.ratio = opt.ratio || window.devicePixelRatio || 1;
    this.width = this.ratio * (opt.width || 320);
    this.height = this.ratio * (opt.height || 100);
    this.MAX = this.height / 2;

    this.speed = 0.1;
    this.amplitude = opt.amplitude || 1;

    // Canvas
    this.canvas = document.createElement('canvas');
    this.canvas.width = this.width;
    this.canvas.height = this.height;
    this.canvas.style.width = `${this.width / this.ratio}px`;
    this.canvas.style.height = `${this.height / this.ratio}px`;

    this.container = opt.container || document.body;
    this.container.appendChild(this.canvas);

    this.ctx = this.canvas.getContext('2d');

    // Create curves
    this.curves = [];
    for (let i = 0; i < SiriWave9.COLORS.length; i++) {
      const color = SiriWave9.COLORS[i];
      for (let j = 0; j < (3 * Math.random()) | 0; j++) {
        this.curves.push(new SiriWave9Curve({
          controller: this,
          color: color
        }));
      }
    }

    if (opt.autostart) {
      this.start();
    }
  }

  _clear() {
    this.ctx.globalCompositeOperation = 'destination-out';
    this.ctx.fillRect(0, 0, this.width, this.height);
    this.ctx.globalCompositeOperation = 'lighter';
  }

  _draw() {
    if (this.run === false) return;

    this._clear();
    for (let i = 0, len = this.curves.length; i < len; i++) {
      this.curves[i].draw();
    }

    requestAnimationFrame(this._draw.bind(this));
  }

  start() {
    this.tick = 0;
    this.run = true;
    this._draw();
  }

  stop() {
    this.tick = 0;
    this.run = false;
  }
}
const SiriWaveComponent = ({ width, height, amplitude, speed }) => {
    const canvasRef = useRef(null);
    const siriWaveRef = useRef(null);
  
    useEffect(() => {
      if (canvasRef.current) {
        siriWaveRef.current = new SiriWave9({
          width: width || 259,
          height: height || 50,
          speed: speed || 0.12,
          amplitude: amplitude || 1,
          container: canvasRef.current,
          autostart: true,
        });
  
        return () => {
          if (siriWaveRef.current) {
            siriWaveRef.current.stop();
          }
        };
      }
    }, [width, height, amplitude, speed]);
  
    return (
      <div
        style={{
          position: 'relative',
          width: width || 259,
          height: height || 50
        }}
        ref={canvasRef}
      />
    );
  };
  
  export default SiriWaveComponent;