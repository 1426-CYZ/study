
import React, { useEffect, useRef } from 'react';

const ParticleBackground: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let particles: Bubble[] = [];
    const mouse = { x: -1000, y: -1000, radius: 300 };

    class Bubble {
      x: number;
      y: number;
      size: number;
      baseX: number;
      baseY: number;
      density: number;
      color: string;
      glowColor: string;
      opacity: number;
      isHighlighted: boolean;
      glowStrength: number;

      constructor(x: number, y: number) {
        this.x = x;
        this.y = y;
        this.size = Math.random() * 7 + 4; // 稍微调大粒径
        this.baseX = this.x;
        this.baseY = this.y;
        this.density = (Math.random() * 60) + 20; // 增加推开的灵敏度
        this.opacity = Math.random() * 0.7 + 0.4; // 显著提高基础透明度
        this.glowStrength = 0;
        
        // 极显眼的浅紫色调调色板
        const palette = [
          { base: 'rgba(216, 180, 254,', glow: 'rgba(232, 121, 249, 1)' }, // 浅紫
          { base: 'rgba(192, 132, 252,', glow: 'rgba(255, 255, 255, 1)' }, // 亮紫
          { base: 'rgba(167, 139, 250,', glow: 'rgba(255, 190, 255, 1)' }  // 霓虹紫
        ];
        const selected = palette[Math.floor(Math.random() * palette.length)];
        this.color = selected.base;
        this.glowColor = selected.glow;
        this.isHighlighted = false;
      }

      draw() {
        if (!ctx) return;
        ctx.save();
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        
        if (this.isHighlighted) {
          // 显著强化自发光效果
          ctx.shadowBlur = 40 * this.glowStrength;
          ctx.shadowColor = this.glowColor;
          ctx.fillStyle = this.glowColor;
          ctx.globalAlpha = 0.9;
          
          // 增加外圈描边让它更有质感
          ctx.strokeStyle = `rgba(255, 255, 255, ${0.9 * this.glowStrength})`;
          ctx.lineWidth = 2;
          ctx.stroke();
        } else {
          ctx.shadowBlur = 0;
          ctx.fillStyle = `${this.color} ${this.opacity})`;
          ctx.globalAlpha = this.opacity;
          ctx.strokeStyle = `rgba(255, 255, 255, ${this.opacity * 0.5})`;
          ctx.lineWidth = 1;
          ctx.stroke();
        }
        
        ctx.fill();
        ctx.restore();
      }

      update() {
        const dx = mouse.x - this.x;
        const dy = mouse.y - this.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        this.isHighlighted = distance < mouse.radius;

        if (distance < mouse.radius) {
          // 强化发光强度函数
          this.glowStrength = Math.pow((mouse.radius - distance) / mouse.radius, 1.2);
          
          const forceDirectionX = dx / distance;
          const forceDirectionY = dy / distance;
          const force = (mouse.radius - distance) / mouse.radius;
          const directionX = forceDirectionX * force * this.density;
          const directionY = forceDirectionY * force * this.density;
          
          // 推开逻辑：距离越近推力越大
          this.x -= directionX;
          this.y -= directionY;
        } else {
          this.glowStrength = 0;
          // 回位逻辑：更加平滑地回到基准位置
          if (this.x !== this.baseX) {
            this.x -= (this.x - this.baseX) / 20;
          }
          if (this.y !== this.baseY) {
            this.y -= (this.y - this.baseY) / 20;
          }
          // 基础漂浮动画
          this.baseY += Math.sin(Date.now() * 0.002 + this.baseX) * 0.12;
        }
      }
    }

    const init = () => {
      particles = [];
      // 增加粒子密度：降低分母
      const count = (canvas.width * canvas.height) / 600; 
      for (let i = 0; i < count; i++) {
        particles.push(new Bubble(Math.random() * canvas.width, Math.random() * canvas.height));
      }
    };

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      particles.forEach(p => {
        p.update();
        p.draw();
      });
      requestAnimationFrame(animate);
    };

    const handleResize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      init();
    };

    const handleMouseMove = (e: MouseEvent) => {
      mouse.x = e.clientX;
      mouse.y = e.clientY;
    };

    window.addEventListener('resize', handleResize);
    window.addEventListener('mousemove', handleMouseMove);
    handleResize();
    animate();

    return () => {
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('mousemove', handleMouseMove);
    };
  }, []);

  return (
    <canvas 
      ref={canvasRef} 
      className="fixed inset-0 z-[1] pointer-events-none" // 稍微提高z-index到1，但保持在内容0之下
      style={{ mixBlendMode: 'screen' }} 
    />
  );
};

export default ParticleBackground;
