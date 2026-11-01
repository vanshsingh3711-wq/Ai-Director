import React from 'react';
import { AbsoluteFill, useVideoConfig, useCurrentFrame, interpolate, spring } from 'remotion';
import { FONT, useExitFade } from '../shared';

export interface OrbitalNode {
  label?: string;
  icon?: string;
  isComplete?: boolean;
}

export interface OrbitalAgentBadgeProps {
  centerTitle?: string;
  centerSubtitle?: string;
  badgeLabel?: string;
  nodesCount?: number;
  accentColor?: string;
  orbitRadius?: number;
  personality?: string;
}

export const OrbitalAgentBadge: React.FC<OrbitalAgentBadgeProps> = ({
  centerTitle = 'AI Agent',
  centerSubtitle = 'AUTONOMOUS REASONING CORE',
  badgeLabel = 'SYNCHRONIZED SWARM',
  nodesCount = 8,
  accentColor = '#00e5ff',
  orbitRadius,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames, width, height } = useVideoConfig();
  const exit = useExitFade(durationInFrames, 14);

  const isLandscape = width > height;
  const radius = orbitRadius || (isLandscape ? 280 : 250);

  // Entrance spring for central badge
  const centerSpring = spring({
    frame,
    fps,
    config: { damping: 12, mass: 0.6, stiffness: 180 },
  });
  const centerScale = interpolate(centerSpring, [0, 1], [0.4, 1]);
  const centerOpacity = interpolate(centerSpring, [0, 0.4], [0, 1], { extrapolateRight: 'clamp' });

  // Dashed orbit rotation over time
  const orbitRotation = (frame / fps) * 25; // 25 degrees per second

  // Breathing electric glow pulse
  const pulseScale = 1 + Math.sin((frame / fps) * 3.5) * 0.04;
  const glowIntensity = Math.sin((frame / fps) * 3) * 15 + 35;

  return (
    <AbsoluteFill
      style={{
        background: 'transparent',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        ...exit,
      }}
    >
      {/* Top Category Badge */}
      <div
        style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: 8,
          padding: '6px 16px',
          borderRadius: 20,
          background: 'rgba(0, 229, 255, 0.12)',
          border: '1px solid rgba(0, 229, 255, 0.35)',
          fontFamily: FONT.mono,
          fontSize: 12,
          fontWeight: 800,
          color: accentColor,
          letterSpacing: 1.5,
          marginBottom: 36,
          boxShadow: `0 0 25px ${accentColor}40`,
          opacity: centerOpacity,
        }}
      >
        <span style={{ width: 8, height: 8, borderRadius: '50%', background: accentColor, boxShadow: `0 0 8px ${accentColor}` }} />
        {badgeLabel}
      </div>

      {/* Main Orbit Stage */}
      <div
        style={{
          width: radius * 2 + 160,
          height: radius * 2 + 160,
          position: 'relative',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        {/* Soft Radial Core Ambient Glow */}
        <div
          style={{
            position: 'absolute',
            width: radius * 2,
            height: radius * 2,
            borderRadius: '50%',
            background: `radial-gradient(circle, ${accentColor}26 0%, rgba(14, 165, 233, 0.08) 50%, transparent 75%)`,
            filter: 'blur(35px)',
            pointerEvents: 'none',
          }}
        />

        {/* SVG Dashed Orbit Track */}
        <svg
          width={radius * 2 + 80}
          height={radius * 2 + 80}
          viewBox={`0 0 ${radius * 2 + 80} ${radius * 2 + 80}`}
          style={{
            position: 'absolute',
            transform: `rotate(${orbitRotation}deg)`,
          }}
        >
          <circle
            cx={radius + 40}
            cy={radius + 40}
            r={radius}
            fill="none"
            stroke="rgba(255, 255, 255, 0.40)"
            strokeWidth="2.5"
            strokeDasharray="8 8"
          />
          {/* Subtle Outer Thin Guide Ring */}
          <circle
            cx={radius + 40}
            cy={radius + 40}
            r={radius + 18}
            fill="none"
            stroke={`${accentColor}33`}
            strokeWidth="1"
          />
        </svg>

        {/* Orbiting Satellite Checkmark Badges */}
        {Array.from({ length: nodesCount }).map((_, idx) => {
          const angleStep = (2 * Math.PI) / nodesCount;
          // Position nodes around the perimeter
          const baseAngle = idx * angleStep;
          const currentAngle = baseAngle + (orbitRotation * Math.PI) / 180;

          const cx = Math.cos(currentAngle) * radius;
          const cy = Math.sin(currentAngle) * radius;

          // Staggered popping entrance for each node
          const nodeSpring = spring({
            frame: frame - 10 - idx * 4,
            fps,
            config: { damping: 11, mass: 0.5, stiffness: 220 },
          });
          const nodeScale = interpolate(nodeSpring, [0, 1], [0, 1]);
          const nodeOpacity = interpolate(nodeSpring, [0, 0.3], [0, 1], { extrapolateRight: 'clamp' });

          return (
            <div
              key={idx}
              style={{
                position: 'absolute',
                transform: `translate(${cx}px, ${cy}px) scale(${nodeScale})`,
                opacity: nodeOpacity,
                width: 44,
                height: 44,
                borderRadius: '50%',
                background: '#FFFFFF',
                boxShadow: `0 0 ${glowIntensity}px rgba(255, 255, 255, 0.95), 0 0 30px ${accentColor}80`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                zIndex: 10,
              }}
            >
              {/* Checkmark Icon inside circular badge */}
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#08101a" strokeWidth="3.5" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="20 6 9 17 4 12" />
              </svg>
            </div>
          );
        })}

        {/* Center Glowing Robot Icon Badge */}
        <div
          style={{
            position: 'relative',
            width: 170,
            height: 170,
            borderRadius: 36,
            background: 'linear-gradient(145deg, #0d1722 0%, #060b11 100%)',
            border: `2px solid ${accentColor}`,
            boxShadow: `
              0 20px 60px rgba(0, 0, 0, 0.9),
              0 0 50px ${accentColor}55,
              inset 0 0 30px ${accentColor}26
            `,
            transform: `scale(${centerScale * pulseScale})`,
            opacity: centerOpacity,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 20,
            padding: 16,
          }}
        >
          {/* Robot Head Vector SVG */}
          <svg width="68" height="68" viewBox="0 0 68 68" fill="none">
            {/* Robot Antenna */}
            <line x1="34" y1="8" x2="34" y2="16" stroke="#FFFFFF" strokeWidth="3.5" strokeLinecap="round" />
            <circle cx="34" cy="6" r="3.5" fill="#FFFFFF" />

            {/* Left & Right Ears */}
            <rect x="6" y="27" width="6" height="18" rx="3" fill="#FFFFFF" />
            <rect x="56" y="27" width="6" height="18" rx="3" fill="#FFFFFF" />

            {/* Robot Head Body */}
            <rect x="15" y="16" width="38" height="38" rx="12" fill="#FFFFFF" />

            {/* Glowing Eyes */}
            <circle cx="27" cy="33" r="4.5" fill="#0b1723" />
            <circle cx="41" cy="33" r="4.5" fill="#0b1723" />
            <circle cx="28.5" cy="31.5" r="1.5" fill="#00e5ff" />
            <circle cx="42.5" cy="31.5" r="1.5" fill="#00e5ff" />

            {/* Friendly Smile Arc */}
            <path d="M28 43 Q34 47 40 43" stroke="#0b1723" strokeWidth="2.5" strokeLinecap="round" fill="none" />
          </svg>

          {/* Badge Label */}
          <div
            style={{
              fontFamily: FONT.display,
              fontSize: 16,
              fontWeight: 800,
              color: '#FFFFFF',
              marginTop: 8,
              letterSpacing: -0.3,
              textShadow: `0 0 10px ${accentColor}80`,
            }}
          >
            {centerTitle}
          </div>
        </div>
      </div>

      {/* Subtitle / Explainer Label at Bottom */}
      <div
        style={{
          marginTop: 36,
          textAlign: 'center',
          opacity: centerOpacity,
        }}
      >
        <div
          style={{
            fontFamily: FONT.mono,
            fontSize: 13,
            fontWeight: 700,
            color: 'rgba(255, 255, 255, 0.7)',
            letterSpacing: 1.2,
          }}
        >
          {centerSubtitle}
        </div>
      </div>
    </AbsoluteFill>
  );
};

