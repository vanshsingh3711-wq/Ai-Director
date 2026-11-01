import React, { useRef, useLayoutEffect } from 'react';
import { AbsoluteFill, useVideoConfig, useCurrentFrame, interpolate, spring } from 'remotion';
import * as THREE from 'three';
import { FONT, useExitFade } from '../shared';

export interface PhoneMessage {
  id?: string;
  sender?: 'bot' | 'user';
  text: string;
  badge?: string;
  badgeColor?: string;
  time?: string;
}

export interface DeviceMockupPhoneProps {
  appTitle?: string;
  botName?: string;
  avatarText?: string;
  screenshotUrl?: string;
  messages?: PhoneMessage[];
  tiltAngleY?: number;
  tiltAngleX?: number;
  accentColor?: string;
  personality?: string;
}

function createRoundedRectShape(w: number, h: number, r: number): THREE.Shape {
  const shape = new THREE.Shape();
  const x = -w / 2;
  const y = -h / 2;
  shape.moveTo(x + r, y);
  shape.lineTo(x + w - r, y);
  shape.quadraticCurveTo(x + w, y, x + w, y + r);
  shape.lineTo(x + w, y + h - r);
  shape.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  shape.lineTo(x + r, y + h);
  shape.quadraticCurveTo(x, y + h, x, y + h - r);
  shape.lineTo(x, y + r);
  shape.quadraticCurveTo(x, y, x + r, y);
  return shape;
}

function wrapText(
  context: CanvasRenderingContext2D,
  text: string,
  x: number,
  y: number,
  maxWidth: number,
  lineHeight: number
) {
  const words = text.split(' ');
  let line = '';
  let curY = y;
  for (let n = 0; n < words.length; n++) {
    const testLine = line + words[n] + ' ';
    const metrics = context.measureText(testLine);
    if (metrics.width > maxWidth && n > 0) {
      context.fillText(line, x, curY);
      line = words[n] + ' ';
      curY += lineHeight;
    } else {
      line = testLine;
    }
  }
  context.fillText(line, x, curY);
  return curY + lineHeight;
}

function drawBadge(
  context: CanvasRenderingContext2D,
  label: string,
  color: string,
  x: number,
  y: number
) {
  context.save();
  context.fillStyle = color + '22';
  context.beginPath();
  context.roundRect(x, y - 30, 280, 48, 14);
  context.fill();
  context.strokeStyle = color + 'aa';
  context.lineWidth = 1.5;
  context.stroke();
  context.fillStyle = color;
  context.font = 'bold 20px monospace';
  context.fillText('● ' + label, x + 16, y);
  context.restore();
}

export const DeviceMockupPhone: React.FC<DeviceMockupPhoneProps> = ({
  appTitle = 'AI ORCHESTRATOR',
  botName = 'Nexus-Agent-Core',
  avatarText = '⚡',
  messages = [
    {
      sender: 'bot',
      text: 'Multi-agent consensus achieved in 142ms. Orchestrator assigned parallel micro-tasks across Hermes-Agent and Docker sandbox with zero deadlock.',
      badge: 'REASONING // 128 tok/s',
      badgeColor: '#38bdf8',
      time: '07:00',
    },
    {
      sender: 'bot',
      text: '$ hermes spawn --cluster=swarm_04\n✓ DeepSeek-R1-671B quantized engine mounted\n→ Refactoring database indices: 0 deadlocks\n✓ Test suite pass: 42/42 deterministic gates',
      badge: 'TERMINAL PASS',
      badgeColor: '#10b981',
      time: '07:01',
    },
    {
      sender: 'bot',
      text: 'Continuous automated audit: egress bandwidth validated, API keys encrypted with hardware KMS, zero data leakage across all 8 nodes.',
      badge: '100% AUDIT PASS',
      badgeColor: '#00e5ff',
      time: '07:02',
    },
  ],
  tiltAngleY = -18,
  tiltAngleX = 9,
  accentColor = '#00e5ff',
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames, width, height } = useVideoConfig();
  const exit = useExitFade(durationInFrames, 14);

  const canvasRef = useRef<HTMLCanvasElement>(null);
  const threeRef = useRef<{
    renderer: THREE.WebGLRenderer;
    scene: THREE.Scene;
    camera: THREE.PerspectiveCamera;
    phoneGroup: THREE.Group;
    screenTexture: THREE.CanvasTexture;
    screenCanvas: HTMLCanvasElement;
    screenCtx: CanvasRenderingContext2D;
  } | null>(null);

  // Entrance spring
  const entrance = spring({
    frame,
    fps,
    config: { damping: 14, mass: 0.8, stiffness: 140 },
  });

  // Oscillations
  const floatY = Math.sin((frame / fps) * 2.2) * 0.35;
  const floatRotateY = Math.sin((frame / fps) * 1.8) * 0.02;
  const floatRotateX = Math.cos((frame / fps) * 2.0) * 0.015;

  // Entrance interpolation
  const enterZ = interpolate(entrance, [0, 1], [-8, 0]);
  const enterY = interpolate(entrance, [0, 1], [-4, 0]);
  const enterRotY = interpolate(entrance, [0, 1], [0.35, 0]);

  useLayoutEffect(() => {
    if (!canvasRef.current) return;

    if (!threeRef.current) {
      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(32, width / height, 0.1, 100);
      camera.position.set(0, 0, 31);
      camera.lookAt(0, 0, 0);

      const renderer = new THREE.WebGLRenderer({
        canvas: canvasRef.current,
        alpha: true,
        antialias: true,
        preserveDrawingBuffer: true,
      });
      renderer.setSize(width, height);
      renderer.setPixelRatio(1);
      renderer.toneMapping = THREE.ACESFilmicToneMapping;
      renderer.toneMappingExposure = 1.15;

      // --- Geometry ---
      const phoneW = 7.4;
      const phoneH = 15.2;
      const phoneR = 1.35;
      const phoneD = 0.65;

      const chassisShape = createRoundedRectShape(phoneW, phoneH, phoneR);
      const extrudeSettings = {
        depth: phoneD,
        bevelEnabled: true,
        bevelSegments: 10,
        steps: 1,
        bevelSize: 0.14,
        bevelThickness: 0.14,
      };
      const chassisGeom = new THREE.ExtrudeGeometry(chassisShape, extrudeSettings);
      chassisGeom.center();

      const chassisMat = new THREE.MeshPhysicalMaterial({
        color: 0x161e29,
        metalness: 0.95,
        roughness: 0.18,
        clearcoat: 0.6,
        clearcoatRoughness: 0.1,
        reflectivity: 0.95,
      });
      const chassisMesh = new THREE.Mesh(chassisGeom, chassisMat);

      // Screen plane
      const screenW = phoneW - 0.28;
      const screenH = phoneH - 0.28;
      const screenR = phoneR - 0.14;
      const screenShape = createRoundedRectShape(screenW, screenH, screenR);
      const screenGeom = new THREE.ShapeGeometry(screenShape, 32);

      // UV mapping
      const pos = screenGeom.attributes.position;
      const uvs: number[] = [];
      for (let i = 0; i < pos.count; i++) {
        const x = pos.getX(i);
        const y = pos.getY(i);
        uvs.push((x + screenW / 2) / screenW, (y + screenH / 2) / screenH);
      }
      screenGeom.setAttribute('uv', new THREE.Float32BufferAttribute(uvs, 2));

      // Screen 2D Canvas
      const screenCanvas = document.createElement('canvas');
      screenCanvas.width = 1080;
      screenCanvas.height = 2220;
      const screenCtx = screenCanvas.getContext('2d')!;

      const screenTexture = new THREE.CanvasTexture(screenCanvas);
      screenTexture.generateMipmaps = true;
      screenTexture.minFilter = THREE.LinearMipmapLinearFilter;

      const screenMat = new THREE.MeshBasicMaterial({
        map: screenTexture,
        toneMapped: false,
      });
      const screenMesh = new THREE.Mesh(screenGeom, screenMat);
      screenMesh.position.z = phoneD / 2 + 0.141;

      const phoneGroup = new THREE.Group();
      phoneGroup.add(chassisMesh);
      phoneGroup.add(screenMesh);
      scene.add(phoneGroup);

      // Studio Lighting
      const ambLight = new THREE.AmbientLight(0x283a4d, 1.4);
      scene.add(ambLight);

      const keyLight = new THREE.DirectionalLight(0x50d4ff, 4.5);
      keyLight.position.set(-10, 16, 16);
      scene.add(keyLight);

      const fillLight = new THREE.DirectionalLight(0x9955ff, 2.8);
      fillLight.position.set(14, -8, 10);
      scene.add(fillLight);

      const glintLight = new THREE.PointLight(0xffffff, 4.0, 35);
      glintLight.position.set(-7, 9, 10);
      scene.add(glintLight);

      // Soft contact shadow
      const shadowCanvas = document.createElement('canvas');
      shadowCanvas.width = 512;
      shadowCanvas.height = 512;
      const sdc = shadowCanvas.getContext('2d')!;
      const sGrad = sdc.createRadialGradient(256, 256, 20, 256, 256, 240);
      sGrad.addColorStop(0, 'rgba(0, 0, 0, 0.85)');
      sGrad.addColorStop(0.5, 'rgba(0, 0, 0, 0.45)');
      sGrad.addColorStop(1, 'rgba(0, 0, 0, 0)');
      sdc.fillStyle = sGrad;
      sdc.fillRect(0, 0, 512, 512);

      const shadowTexture = new THREE.CanvasTexture(shadowCanvas);
      const shadowGeom = new THREE.PlaneGeometry(12, 18);
      const shadowMat = new THREE.MeshBasicMaterial({
        map: shadowTexture,
        transparent: true,
        opacity: 0.65,
        depthWrite: false,
      });
      const shadowMesh = new THREE.Mesh(shadowGeom, shadowMat);
      shadowMesh.rotation.x = -Math.PI / 2 + 0.1;
      shadowMesh.position.set(0.5, -8.2, -1.0);
      scene.add(shadowMesh);

      threeRef.current = {
        renderer,
        scene,
        camera,
        phoneGroup,
        screenTexture,
        screenCanvas,
        screenCtx,
      };
    }

    const { renderer, scene, camera, phoneGroup, screenTexture, screenCanvas, screenCtx } =
      threeRef.current;

    // --- Redraw Screen UI with Current Props & Animations ---
    screenCtx.fillStyle = '#070c14';
    screenCtx.fillRect(0, 0, 1080, 2220);

    // Subtle wallpaper grid
    screenCtx.fillStyle = 'rgba(0, 229, 255, 0.025)';
    for (let gx = 30; gx < 1080; gx += 36) {
      for (let gy = 30; gy < 2220; gy += 36) {
        screenCtx.beginPath();
        screenCtx.arc(gx, gy, 1.2, 0, Math.PI * 2);
        screenCtx.fill();
      }
    }

    // Top Status Bar
    screenCtx.fillStyle = '#f8fafc';
    screenCtx.font = 'bold 40px -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto';
    screenCtx.fillText('9:41', 110, 115);

    // Dynamic Island
    screenCtx.fillStyle = '#000000';
    screenCtx.beginPath();
    screenCtx.roundRect(540 - 150, 75, 300, 75, 37.5);
    screenCtx.fill();
    screenCtx.strokeStyle = '#1e293b';
    screenCtx.lineWidth = 2.5;
    screenCtx.stroke();

    // Camera sensor & indicator
    screenCtx.fillStyle = '#0f172a';
    screenCtx.beginPath();
    screenCtx.arc(645, 112, 15, 0, Math.PI * 2);
    screenCtx.fill();
    screenCtx.fillStyle = '#10b981';
    screenCtx.beginPath();
    screenCtx.arc(445, 112, 7, 0, Math.PI * 2);
    screenCtx.fill();

    screenCtx.fillStyle = '#f8fafc';
    screenCtx.font = 'bold 34px sans-serif';
    screenCtx.fillText('5G  100%', 840, 115);

    // App Bar Header
    screenCtx.fillStyle = '#0b1320';
    screenCtx.beginPath();
    screenCtx.roundRect(60, 200, 960, 130, 28);
    screenCtx.fill();
    screenCtx.strokeStyle = `${accentColor}40`;
    screenCtx.lineWidth = 2;
    screenCtx.stroke();

    // Avatar Icon
    screenCtx.fillStyle = accentColor;
    screenCtx.beginPath();
    screenCtx.arc(125, 265, 36, 0, Math.PI * 2);
    screenCtx.fill();
    screenCtx.fillStyle = '#020617';
    screenCtx.font = 'bold 36px sans-serif';
    screenCtx.textAlign = 'center';
    screenCtx.fillText(avatarText, 125, 277);
    screenCtx.textAlign = 'left';

    screenCtx.fillStyle = '#ffffff';
    screenCtx.font = '900 38px -apple-system, BlinkMacSystemFont, "Segoe UI"';
    screenCtx.fillText(botName, 185, 255);

    screenCtx.fillStyle = '#10b981';
    screenCtx.font = 'bold 22px monospace';
    screenCtx.fillText(`● STATUS: ONLINE // ${appTitle}`, 185, 290);

    // Render Message Cards
    let startY = 370;
    messages.slice(0, 3).forEach((msg, idx) => {
      // Stagger entrance per card
      const cardSpring = spring({
        frame: frame - 6 - idx * 8,
        fps,
        config: { damping: 14, mass: 0.7, stiffness: 150 },
      });
      const cardAlpha = interpolate(cardSpring, [0, 0.4], [0, 1], {
        extrapolateRight: 'clamp',
      });

      if (cardAlpha > 0.05) {
        screenCtx.save();
        screenCtx.globalAlpha = cardAlpha;

        const cardH = idx === 1 ? 480 : 380;
        screenCtx.fillStyle = 'rgba(15, 23, 42, 0.95)';
        screenCtx.beginPath();
        screenCtx.roundRect(60, startY, 960, cardH, 32);
        screenCtx.fill();
        screenCtx.strokeStyle = `${msg.badgeColor || accentColor}55`;
        screenCtx.lineWidth = 2;
        screenCtx.stroke();

        // Card Title
        screenCtx.fillStyle = msg.badgeColor || accentColor;
        screenCtx.font = 'bold 32px -apple-system, BlinkMacSystemFont';
        screenCtx.fillText(
          `${idx + 1}. ${idx === 0 ? '🧠 Consensus Stream' : idx === 1 ? '⚡ Terminal Output' : '🛡️ Security Sentinel'}`,
          105,
          startY + 65
        );

        // Card Body Text
        screenCtx.fillStyle = '#e2e8f0';
        screenCtx.font = idx === 1 ? '26px monospace' : '29px -apple-system, BlinkMacSystemFont';
        const lines = msg.text.split('\n');
        let textY = startY + 125;
        lines.forEach((line) => {
          if (idx === 1 && line.startsWith('✓')) {
            screenCtx.fillStyle = '#10b981';
          } else if (idx === 1 && line.startsWith('$')) {
            screenCtx.fillStyle = '#94a3b8';
          } else if (idx === 1 && line.startsWith('→')) {
            screenCtx.fillStyle = '#f59e0b';
          } else {
            screenCtx.fillStyle = '#e2e8f0';
          }
          textY = wrapText(screenCtx, line, 105, textY, 870, 42);
        });

        // Badge
        if (msg.badge) {
          drawBadge(
            screenCtx,
            msg.badge,
            msg.badgeColor || accentColor,
            105,
            startY + cardH - 30
          );
        }

        screenCtx.restore();
        startY += cardH + 30;
      }
    });

    // Bottom home bar
    screenCtx.fillStyle = 'rgba(255, 255, 255, 0.7)';
    screenCtx.beginPath();
    screenCtx.roundRect(540 - 180, 2170, 360, 10, 5);
    screenCtx.fill();

    screenTexture.needsUpdate = true;

    // --- Update 3D Phone Pose ---
    const baseYRad = (tiltAngleY * Math.PI) / 180;
    const baseXRad = (tiltAngleX * Math.PI) / 180;

    phoneGroup.rotation.y = baseYRad + floatRotateY + enterRotY;
    phoneGroup.rotation.x = baseXRad + floatRotateX;
    phoneGroup.rotation.z = -0.05;
    phoneGroup.position.set(0, floatY + enterY + 0.2, enterZ);

    renderer.render(scene, camera);
  }, [frame, fps, width, height, tiltAngleY, tiltAngleX, accentColor, appTitle, botName, avatarText, messages, entrance, floatY, floatRotateY, floatRotateX, enterZ, enterY, enterRotY]);

  return (
    <AbsoluteFill
      style={{
        background: 'transparent',
        ...exit,
      }}
    >
      <canvas
        ref={canvasRef}
        width={width}
        height={height}
        style={{
          width: '100%',
          height: '100%',
        }}
      />
    </AbsoluteFill>
  );
};
