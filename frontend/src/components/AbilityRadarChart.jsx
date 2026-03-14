/**
 * 用户能力雷达图组件
 * 使用 SVG 绘制五维能力雷达图
 */

import React, { useEffect, useRef } from 'react';

const AbilityRadarChart = ({
  abilities,
  width = 300,
  height = 300,
  className = ''
}) => {
  const svgRef = useRef(null);

  // 五维能力数据
  const dimensions = [
    { key: 'stability', label: '稳定性', color: '#5796B3' },  // cyan-glaze
    { key: 'accuracy', label: '准确度', color: '#C04851' },   // vermilion
    { key: 'speed', label: '速度', color: '#CCD4BF' },        // tea-green
    { key: 'creativity', label: '创意', color: '#5796B3' },   // cyan-glaze
    { key: 'knowledge', label: '知识', color: '#2B2B2B' },    // ink-black
  ];

  // 计算雷达图顶点坐标
  const center = { x: width / 2, y: height / 2 };
  const radius = Math.min(width, height) / 2 - 40;
  const angleStep = (Math.PI * 2) / dimensions.length - Math.PI / 2;

  const getPoint = (index, value) => {
    const angle = angleStep * index;
    const r = (value / 100) * radius;
    return {
      x: center.x + r * Math.cos(angle),
      y: center.y + r * Math.sin(angle)
    };
  };

  // 生成雷达图路径
  const generatePath = (dataScale = 1) => {
    const points = dimensions.map((dim, i) => {
      const value = (abilities?.[dim.key] || 0) * dataScale;
      return getPoint(i, value);
    });

    if (points.length === 0) return '';

    const pathData = points.map((point, i) => {
      return i === 0 ? `M ${point.x} ${point.y}` : `L ${point.x} ${point.y}`;
    }).join(' ');

    return `${pathData} Z`;
  };

  // 生成网格线（五边形）
  const gridLevels = [20, 40, 60, 80, 100];

  return (
    <div className={`relative ${className}`}>
      <svg
        ref={svgRef}
        width={width}
        height={height}
        className="mx-auto"
      >
        {/* 背景网格 */}
        {gridLevels.map((level) => {
          const points = dimensions.map((_, i) => {
            const point = getPoint(i, level);
            return `${point.x},${point.y}`;
          }).join(' ');

          return (
            <polygon
              key={level}
              points={points}
              fill="none"
              stroke="#E5E5E5"
              strokeWidth="1"
              opacity={level === 100 ? 0.5 : 0.3}
            />
          );
        })}

        {/* 维度轴线 */}
        {dimensions.map((dim, i) => {
          const point = getPoint(i, 100);
          return (
            <line
              key={dim.key}
              x1={center.x}
              y1={center.y}
              x2={point.x}
              y2={point.y}
              stroke="#E5E5E5"
              strokeWidth="1"
            />
          );
        })}

        {/* 雷达图填充区域 */}
        <path
          d={generatePath()}
          fill="url(#abilityGradient)"
          stroke="#C04851"
          strokeWidth="2"
          className="transition-all duration-500 ease-in-out"
        />

        {/* 渐变定义 */}
        <defs>
          <linearGradient id="abilityGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#C04851" stopOpacity="0.4" />
            <stop offset="100%" stopColor="#5796B3" stopOpacity="0.2" />
          </linearGradient>
        </defs>

        {/* 顶点标记 */}
        {dimensions.map((dim, i) => {
          const point = getPoint(i, abilities?.[dim.key] || 0);
          return (
            <g key={`label-${dim.key}`}>
              <circle
                cx={point.x}
                cy={point.y}
                r="4"
                fill={dim.color}
                stroke="#fff"
                strokeWidth="2"
              />
              {/* 维度标签 */}
              <text
                x={point.x}
                y={point.y}
                dy={i === 0 ? -15 : i === 1 ? 15 : i === 2 ? 15 : i === 3 ? 15 : -15}
                textAnchor="middle"
                className="text-xs font-serif fill-ink-black"
                style={{ fontSize: '11px', fontWeight: '500' }}
              >
                {dim.label}
              </text>
            </g>
          );
        })}

        {/* 中心文字 */}
        <text
          x={center.x}
          y={center.y}
          textAnchor="middle"
          className="font-calligraphy"
          style={{ fontSize: '16px', fill: '#2B2B2B' }}
        >
          能力值
        </text>
      </svg>

      {/* 图例 */}
      <div className="flex flex-wrap justify-center gap-4 mt-4 text-xs font-serif">
        {dimensions.map((dim) => (
          <div key={dim.key} className="flex items-center gap-2">
            <div
              className="w-3 h-3 rounded-full"
              style={{ backgroundColor: dim.color }}
            ></div>
            <span className="text-charcoal/70">{dim.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AbilityRadarChart;
