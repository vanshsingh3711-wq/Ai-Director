import React from 'react';
import { AbsoluteFill, useVideoConfig, useCurrentFrame, interpolate, spring } from 'remotion';
import { FONT, useExitFade } from '../shared';

export interface CardItem {
  id?: string;
  title: string;
  badge?: string;
  badgeColor?: string;
  type?: 'docker' | 'terminal' | 'analytics';
  accentColor?: string;
}

export interface IsometricCardDeckProps {
  headline?: string;
  subheadline?: string;
  cards?: CardItem[];
  rotationY?: number;
  rotationX?: number;
  accentColor?: string;
  personality?: string;
}

export const IsometricCardDeck: React.FC<IsometricCardDeckProps> = ({
  headline = 'AUTONOMOUS SWARM INFRASTRUCTURE',
  subheadline = 'DOCKER CLUSTERS RUNNING CONCURRENTLY WITH PERSISTENT AGENTS',
  cards = [
    {
      title: 'Docker Manager — Swarm Cluster #04',
      badge: 'ACTIVE 8/8 NODES',
      badgeColor: '#10b981',
      type: 'docker',
      accentColor: '#00e5ff',
    },
    {
      title: 'Hermes-Agent-Core // Recursive Loop',
      badge: 'REASONING // 128 tok/s',
      badgeColor: '#a855f7',
      type: 'terminal',
      accentColor: '#a855f7',
    },
    {
      title: 'Telemetry & Anomaly Verification',
      badge: '100% BUILD PASS',
      badgeColor: '#38bdf8',
      type: 'analytics',
      accentColor: '#38bdf8',
    },
  ],
  rotationY = -18,
  rotationX = 10,
  accentColor = '#00e5ff',
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames, width, height } = useVideoConfig();
  const exit = useExitFade(durationInFrames, 14);

  const isLandscape = width > height;

  // Header entrance spring
  const headerSpring = spring({
    frame,
    fps,
    config: { damping: 14, mass: 0.7, stiffness: 150 },
  });
  const headerOpacity = interpolate(headerSpring, [0, 0.4], [0, 1], { extrapolateRight: 'clamp' });
  const headerTranslateY = interpolate(headerSpring, [0, 1], [-20, 0]);

  // Floating bobbing effect
  const floatY = Math.sin((frame / fps) * 2.0) * 8;
  const floatTilt = Math.sin((frame / fps) * 1.5) * 1.2;

  return (
    <AbsoluteFill
      style={{
        background: 'transparent',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        perspective: 1600,
        padding: isLandscape ? '40px 60px' : '60px 30px',
        ...exit,
      }}
    >
      {/* Top Section Header */}
      <div
        style={{
          textAlign: 'center',
          marginBottom: isLandscape ? 30 : 40,
          opacity: headerOpacity,
          transform: `translateY(${headerTranslateY}px)`,
          zIndex: 10,
        }}
      >
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
            marginBottom: 12,
            boxShadow: '0 0 20px rgba(0, 229, 255, 0.25)',
          }}
        >
          <span style={{ width: 8, height: 8, borderRadius: '50%', background: accentColor, boxShadow: `0 0 8px ${accentColor}` }} />
          MULTI-AGENT ENVIRONMENT
        </div>
        <h2
          style={{
            fontFamily: FONT.display,
            fontSize: isLandscape ? 36 : 38,
            fontWeight: 900,
            color: '#FFFFFF',
            margin: '0 0 6px 0',
            letterSpacing: -0.8,
            textShadow: '0 4px 20px rgba(0,0,0,0.8)',
          }}
        >
          {headline}
        </h2>
        <p
          style={{
            fontFamily: FONT.mono,
            fontSize: 13,
            color: 'rgba(255, 255, 255, 0.6)',
            margin: 0,
            letterSpacing: 0.5,
          }}
        >
          {subheadline}
        </p>
      </div>

      {/* 3D Staggered Isometric Cascade */}
      <div
        style={{
          width: '100%',
          maxWidth: isLandscape ? 1200 : 880,
          display: 'flex',
          flexDirection: isLandscape ? 'row' : 'column',
          alignItems: 'center',
          justifyContent: 'center',
          gap: isLandscape ? 24 : -40, // overlap cards slightly in portrait
          transformStyle: 'preserve-3d',
          transform: `rotateY(${rotationY + floatTilt}deg) rotateX(${rotationX}deg) translateY(${floatY}px)`,
          position: 'relative',
        }}
      >
        {cards.map((card, idx) => {
          // Stagger card entrance with individual springs
          const cardSpring = spring({
            frame: frame - 8 - idx * 10,
            fps,
            config: { damping: 13, mass: 0.7, stiffness: 160 },
          });

          const cardOpacity = interpolate(cardSpring, [0, 0.4], [0, 1], { extrapolateRight: 'clamp' });
          const cardTranslateZ = interpolate(cardSpring, [0, 1], [-200, idx * 50]);
          const cardTranslateX = interpolate(cardSpring, [0, 1], [idx % 2 === 0 ? -60 : 60, 0]);
          const cardTranslateY = interpolate(cardSpring, [0, 1], [60, 0]);

          const cardAccent = card.accentColor || accentColor;

          return (
            <div
              key={idx}
              style={{
                width: isLandscape ? 360 : '100%',
                maxWidth: 780,
                borderRadius: 24,
                background: 'linear-gradient(145deg, rgba(16, 25, 38, 0.94) 0%, rgba(8, 13, 21, 0.96) 100%)',
                backdropFilter: 'blur(24px)',
                border: `1.5px solid ${cardAccent}4d`,
                boxShadow: `
                  0 30px 80px rgba(0, 0, 0, 0.85),
                  0 0 40px ${cardAccent}26,
                  inset 0 1px 1px rgba(255, 255, 255, 0.2)
                `,
                padding: '20px 24px',
                transformStyle: 'preserve-3d',
                transform: `translate3d(${cardTranslateX}px, ${cardTranslateY}px, ${cardTranslateZ}px)`,
                opacity: cardOpacity,
                zIndex: cards.length - idx,
                position: 'relative',
                marginBottom: isLandscape ? 0 : 16,
              }}
            >
              {/* Window Header Bar */}
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  paddingBottom: 14,
                  borderBottom: '1px solid rgba(255, 255, 255, 0.08)',
                  marginBottom: 14,
                }}
              >
                {/* Traffic Light Dots */}
                <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                  <div style={{ width: 10, height: 10, borderRadius: '50%', background: '#ef4444' }} />
                  <div style={{ width: 10, height: 10, borderRadius: '50%', background: '#f59e0b' }} />
                  <div style={{ width: 10, height: 10, borderRadius: '50%', background: '#10b981' }} />
                  <span
                    style={{
                      marginLeft: 8,
                      fontFamily: FONT.display,
                      fontSize: 13,
                      fontWeight: 700,
                      color: '#E5E7EB',
                    }}
                  >
                    {card.title}
                  </span>
                </div>

                {/* Status Badge */}
                {card.badge && (
                  <div
                    style={{
                      padding: '4px 10px',
                      borderRadius: 12,
                      background: `${card.badgeColor || '#10b981'}1f`,
                      border: `1px solid ${card.badgeColor || '#10b981'}66`,
                      fontFamily: FONT.mono,
                      fontSize: 10,
                      fontWeight: 800,
                      color: card.badgeColor || '#10b981',
                      letterSpacing: 0.5,
                      display: 'flex',
                      alignItems: 'center',
                      gap: 5,
                    }}
                  >
                    <span
                      style={{
                        width: 6,
                        height: 6,
                        borderRadius: '50%',
                        background: card.badgeColor || '#10b981',
                        boxShadow: `0 0 6px ${card.badgeColor || '#10b981'}`,
                      }}
                    />
                    {card.badge}
                  </div>
                )}
              </div>

              {/* Card Body Renderings based on Type */}
              {card.type === 'docker' ? (
                /* Docker Manager Table Mockup */
                <div style={{ display: 'flex', flexDirection: 'column', gap: 8, fontFamily: FONT.mono, fontSize: 12 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', color: 'rgba(255, 255, 255, 0.4)', fontSize: 10, borderBottom: '1px solid rgba(255, 255, 255, 0.05)', paddingBottom: 4 }}>
                    <span>CONTAINER / AGENT</span>
                    <span>STATUS</span>
                    <span>ACCESS</span>
                  </div>
                  {[
                    { name: 'hermes-agent-viral', port: ':8001', cpu: '14.2%', status: 'Running', color: '#10b981' },
                    { name: 'openclaw-audit-v2', port: ':9090', cpu: '32.1%', status: 'Running', color: '#10b981' },
                    { name: 'traefik-proxy-gateway', port: ':443', cpu: '4.8%', status: 'Running', color: '#10b981' },
                  ].map((row, rIdx) => (
                    <div
                      key={rIdx}
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        padding: '6px 8px',
                        borderRadius: 8,
                        background: rIdx === 0 ? 'rgba(0, 229, 255, 0.06)' : 'rgba(255, 255, 255, 0.02)',
                        border: rIdx === 0 ? '1px solid rgba(0, 229, 255, 0.2)' : 'none',
                      }}
                    >
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        <span style={{ color: cardAccent }}>▶</span>
                        <span style={{ color: '#F3F4F6', fontWeight: 600 }}>{row.name}</span>
                        <span style={{ color: 'rgba(255, 255, 255, 0.4)', fontSize: 10 }}>{row.port}</span>
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 6, color: row.color, fontWeight: 700, fontSize: 11 }}>
                        <span style={{ width: 6, height: 6, borderRadius: '50%', background: row.color }} />
                        {row.status}
                      </div>
                      <div style={{ padding: '2px 8px', borderRadius: 6, background: 'rgba(255, 255, 255, 0.08)', color: '#38bdf8', fontSize: 10 }}>
                        Terminal ↗
                      </div>
                    </div>
                  ))}
                </div>
              ) : card.type === 'terminal' ? (
                /* Terminal / Code Stream Mockup */
                <div
                  style={{
                    borderRadius: 12,
                    background: '#04070d',
                    padding: '12px 14px',
                    fontFamily: FONT.mono,
                    fontSize: 11,
                    lineHeight: 1.6,
                    color: '#94a3b8',
                    border: '1px solid rgba(255, 255, 255, 0.06)',
                  }}
                >
                  <div style={{ color: cardAccent }}>$ hermes agent --spawn-swarm --threads=8</div>
                  <div style={{ color: 'rgba(255, 255, 255, 0.6)' }}>[INFO] Allocating isolated sandbox memory namespaces...</div>
                  <div style={{ color: '#10b981' }}>✔ Loaded model weights: DeepSeek-R1-671B quantized (vLLM engine)</div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                    <span style={{ color: '#f59e0b' }}>[THINK]</span>
                    <span style={{ color: '#E2E8F0' }}>Refactoring database indices: zero deadlock detected.</span>
                    <span style={{ width: 6, height: 12, background: cardAccent, display: 'inline-block' }} />
                  </div>
                </div>
              ) : (
                /* Telemetry & Analytics Progress */
                <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontFamily: FONT.mono, fontSize: 12 }}>
                    <span style={{ color: 'rgba(255, 255, 255, 0.6)' }}>Test Suite Pass Rate</span>
                    <span style={{ color: '#10b981', fontWeight: 800 }}>100.0% (42/42)</span>
                  </div>
                  {/* Progress Bar */}
                  <div style={{ width: '100%', height: 8, borderRadius: 4, background: 'rgba(255, 255, 255, 0.08)', overflow: 'hidden' }}>
                    <div style={{ width: '100%', height: '100%', background: 'linear-gradient(90deg, #00e5ff 0%, #10b981 100%)', boxShadow: '0 0 12px #10b981' }} />
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 11, color: 'rgba(255, 255, 255, 0.5)', fontFamily: FONT.mono }}>
                    <span>Latency: 41ms</span>
                    <span>Deterministic Gate: ENFORCED</span>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

