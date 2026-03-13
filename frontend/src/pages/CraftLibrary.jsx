import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import Card from '../components/Card';
import SuEmbroidery from '../assets/Suzhou-embroidery.png';
import PurpleClay from '../assets/Purple-Clay.png';
import PaperCutting from '../assets/Paper-Cutting.png';
import Batik from '../assets/Batik.png';
import ShadowPuppetImg from '../assets/Shadow-Puppet.png';

const CraftLibrary = () => {
  const [activeTab, setActiveTab] = useState('all');

  const crafts = [
    {
      id: 1,
      name: "苏绣 · 平针绣",
      category: "embroidery",
      image: SuEmbroidery,
      desc: "苏绣基础针法，线条流畅，平整光亮。适合初学者入门，通过视觉 Agent 实时纠正下针角度。",
      features: ["视觉纠偏支持"],
      learners: "1.2k"
    },
    {
      id: 2,
      name: "紫砂 · 拍泥片",
      category: "clay",
      image: PurpleClay,
      desc: "宜兴紫砂壶成型的关键工序。通过 ST-GCN 分析手臂发力与拍打节奏，还原大师手感。",
      features: ["动作捕捉支持"],
      learners: "856"
    },
    {
      id: 3,
      name: "剪纸 · 团花纹",
      category: "paper",
      image: PaperCutting,
      desc: "利用对称美学创作团花。创意艺匠 Agent 可辅助生成纹样草图，并指导折叠技巧。",
      features: ["AIGC 生成支持"],
      learners: "2.3k"
    },
    {
      id: 4,
      name: "蜡染 · 冰裂纹",
      category: "batik",
      image: Batik,
      desc: "苗族传统印染技艺。模拟蜡刀绘画路径，掌握冰裂纹的自然形成规律。",
      features: ["AIGC 生成支持"],
      learners: "530"
    },
    {
      id: 5,
      name: "皮影 · 操纵技法",
      category: "shadow",
      image: ShadowPuppetImg,
      desc: "皮影戏核心表演技艺，用三根竹签操纵影人。视觉导师 Agent 实时捕捉手势动作，纠正操纵姿势。",
      features: ["视觉纠偏支持", "手势追踪"],
      learners: "1.8k"
    }
  ];

  return (
    <div className="min-h-screen bg-rice-paper">
      <Navbar />
      
      <main className="pt-32 pb-20 px-4 md:px-12 max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-12 text-center">
          <h1 className="font-calligraphy text-5xl mb-4 text-ink-black">非遗技艺库</h1>
          <p className="text-charcoal/60 font-serif text-lg tracking-widest">探寻千年匠心，重拾指尖传承</p>
        </div>

        {/* Filter Tabs */}
        <div className="flex justify-center gap-8 mb-16 border-b border-ink-black/10 pb-4">
          {['all', 'embroidery', 'clay', 'paper', 'batik', 'shadow'].map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`font-xiaowei text-lg pb-2 transition-colors ${
                activeTab === tab
                  ? 'text-vermilion font-bold border-b-2 border-vermilion'
                  : 'text-charcoal/60 hover:text-ink-black'
              }`}
            >
              {tab === 'all' ? '全部' : tab === 'embroidery' ? '苏绣' : tab === 'clay' ? '紫砂' : tab === 'paper' ? '剪纸' : tab === 'batik' ? '蜡染' : '皮影戏'}
            </button>
          ))}
        </div>

        {/* Grid Layout */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {crafts.filter(craft => activeTab === 'all' || craft.category === activeTab).map(craft => (
            <Card key={craft.id} className="cursor-pointer group" onClick={() => window.location.href = craft.category === 'shadow' ? '/shadow-puppet' : '#'}>
              <div className="absolute top-4 right-4 z-10 bg-black/60 text-white text-xs px-2 py-1 rounded-sm font-sans backdrop-blur-sm">热门</div>
              <div className="h-64 overflow-hidden relative">
                <div className="absolute inset-0 bg-ink-black/10 group-hover:bg-transparent transition-colors z-10"></div>
                <img
                  src={craft.image}
                  alt={craft.name}
                  className="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-700"
                />
              </div>
              <div className="p-6 relative">
                <div className="absolute -top-10 left-6 bg-rice-paper border border-ink-black/10 p-2 shadow-sm">
                  <span className="font-calligraphy text-2xl text-vermilion">
                    {craft.name[0]}
                  </span>
                </div>
                <h3 className="font-xiaowei text-2xl mb-2 mt-2 group-hover:text-vermilion transition-colors">
                  {craft.name}
                </h3>
                <p className="text-charcoal/70 text-sm mb-4 line-clamp-2">
                  {craft.desc}
                </p>
                <div className="flex justify-between items-center border-t border-ink-black/5 pt-4">
                  <span className="text-xs text-cyan-glaze font-bold bg-cyan-glaze/10 px-2 py-1 rounded">
                    {craft.features[0]}
                  </span>
                  <span className="text-charcoal/40 text-sm font-serif">{craft.learners} 人修习中</span>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </main>
    </div>
  );
};

export default CraftLibrary;
